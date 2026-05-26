---
title: "存储哈希分流"
date: 2026-05-26T11:28:57+08:00
draft: false
series: ["工程实践"]
tags: ["Go", "对象存储", "Cloudflare R2", "阿里云 OSS", "S3", "灰度路由", "FNV-1a"]
summary: "线上 R2 网络问题暴露了单对象存储风险。改造方案引入阿里云 OSS，通过 storage.Client 抽象、FNV-1a id 哈希路由和 STORAGE_GRAY_THRESHOLD 控制新上传流量，支持灰度与切回。"
---

这篇记录一次存储单点改造。R2 网络问题暴露了单对象存储风险，后续通过 OSS 做双存储，并用 id 哈希控制新上传流量。重点是新上传请求的灰度、切回，以及同一任务文件不裂脑。

## 问题复盘

线上 R2 出现过短时网络问题，上传、转存、文件访问都受影响。由于所有生成产物都写同一个对象存储，且缺乏备用链路，服务全链路短时不可用。后续通过引入阿里云 OSS 做双存储，用配置控制新上传流量；分流粒度按 id 做 FNV-1a 哈希，保证同一任务的音频、视频、封面图、中间图片稳定落到同一个存储服务，避免按单次上传随机分流造成裂脑。

## Client 抽象

上传入口不能直接依赖 R2Client。先抽出统一的 `storage.Client`。

```go
type Client interface {
    UploadFile(ctx context.Context, content io.Reader, key, contentType string, size int64) (*UploadResult, error)
    UploadFileFromURL(ctx context.Context, fileURL, key string) (*UploadResult, error)
    GeneratePublicURL(key string) (string, error)
    GeneratePresignedURL(ctx context.Context, key string, expires time.Duration) (string, error)
    GenerateWorkflowPath(workflowType, executionID, fileType, extension string) string
    Provider() string
}
```

`R2Client` 和 `OSSClient` 都实现这个接口。业务代码只拿 `Client` 上传文件并生成 URL。

## 存储分流策略

### 方案取舍

存储切流有几种方案。

- **全量切 OSS**：操作简单，但风险集中。OSS 兼容、权限、公开 URL、上传链路都需要线上验证，一次性切换不适合做故障后的稳态方案。
- **按单次上传随机**：可以控制比例，但同一任务的多个文件可能落到不同存储服务，形成裂脑。
- **R2 和 OSS 双写**：回退空间最大，但上传耗时、存储成本、失败语义都会变复杂。一个存储写成功、另一个存储写失败时，业务要处理新的中间状态。
- **按 id 哈希路由**：同一任务稳定落到同一存储服务，整体流量仍然可以按阈值灰度。

最终选 id 哈希。它解决的是当前最需要的能力：新上传请求可灰度，同一任务内部不漂，出问题时可以通过配置切回。

### 实现

Router 持有两个存储 Client 和一个阈值。

```go
type RouterConfig struct {
    R2        Client
    OSS       Client
    Threshold int // 0-100
}
```

阈值语义：

- `100`：全部走 R2
- `95`：95% 走 R2，5% 走 OSS
- `0`：全部走 OSS

路由逻辑：

```go
func (r *Router) Route(id string) Client {
    if r.oss == nil {
        return r.r2
    }
    if r.r2 == nil {
        return r.oss
    }
    if r.threshold >= 100 {
        return r.r2
    }
    if r.threshold <= 0 {
        return r.oss
    }

    h := fnv32(id) % 100
    if h < uint32(r.threshold) {
        return r.r2
    }
    return r.oss
}

func fnv32(s string) uint32 {
    h := fnv.New32a()
    h.Write([]byte(s))
    return h.Sum32()
}
```

### 为什么是 FNV-1a

这个场景只需要把 id 稳定映射到 `0-99`。FNV-1a 够用。

- Go 标准库自带
- 计算快
- 对同一个 id 输出稳定
- `% 100` 后可以直接和灰度阈值比较

## 上传入口

上传入口只做三件事。

1. 取当前任务 id。
2. 调 `storageRouter.Route(executionID)` 取具体 Client。
3. 用 Client 上传并返回 URL。

```go
workflowType := getWorkflowType(ctx)
executionID := getExecutionID(ctx)

client := storageRouter.Route(executionID)

key := client.GenerateWorkflowPath(
    workflowType,
    executionID,
    input.FileType,
    getFileExtension(input.FileName),
)

uploadResult, err := client.UploadFileFromURL(ctx, input.FileURL, key)
```

数据库仍然存最终 URL。下游仍然按 URL 消费。历史文件不需要迁移。

## 接入改造

主要工作量在清理单存储依赖。

旧代码里很多地方默认只有 R2。公共处理步骤、业务流程、存储辅助入口都可能直接上传。只改新入口不够，旧入口会绕过 Router。

改造后，上传代码统一走 `storage.Client`。代码命名也从具体存储名收敛到 `storage`。

## OSS 兼容细节

阿里云 OSS 支持 S3 兼容协议。实际接入时仍然要看 SDK 路径。

`manager.Uploader` 这类高级封装可能带上传输编码或校验头。OSS 不一定完全支持。这里退回到更直接的 `PutObject`。

```go
input := PutObjectInput{
    Bucket:      bucket,
    Key:         key,
    Body:        content,
    ContentType: contentType,
    ACL:         "public-read",
}

_, err := client.PutObject(ctx, input)
```

协议兼容不等于所有客户端封装都兼容。

## 回退

回退只改灰度阈值。

`STORAGE_GRAY_THRESHOLD=100`，新请求全部走 R2。  
`STORAGE_GRAY_THRESHOLD=0`，新请求全部走 OSS。

OSS 灰度异常时，把阈值调回 100。新请求回到 R2。已写入数据库的 URL 不动。

## 结论

这次改造的核心是路由粒度。一次业务任务内部会产生多类文件，分流策略要把这些文件作为一个整体处理。

按单次上传随机分流，比例正确，但同一任务会漂。按 id 哈希分流，比例可控，同一任务稳定。这个选择把问题从“每个文件落到哪里”收敛成“这个任务落到哪里”。

`storage.Client` 解决调用边界。业务代码不再直接依赖 R2 或 OSS。

`StorageRouter` 解决路由边界。同一个 id 只会稳定命中一个存储服务。

`STORAGE_GRAY_THRESHOLD` 解决操作边界。灰度、全量切换、回退都通过同一个配置完成。

最后的方案不复杂，但它补上了单存储架构缺的能力：R2 异常时，新上传请求有路可切；OSS 灰度时，同一任务不会裂脑；线上回退时，不需要改历史 URL。
