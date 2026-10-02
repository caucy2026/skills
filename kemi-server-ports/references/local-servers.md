# 本地服务器端口文档索引

本机索引更新：2026-09-24。用于跨项目找到唯一权威台账；其他设备复用时按实际路径调整。本索引不保存凭据，也不复制端口表以免分叉。

## KEMI 云端服务器

| 项目 | 当前本机记录 |
|---|---|
| 服务器标识 | kemi-cloud-production |
| 主机 / 服务域名 | 119.96.24.110 / kemi-chat.newlinksz.com |
| 权威端口文档 | [PORT_ALLOCATION.md](/Users/newlink/kemi/RustDesk/server/deployment/PORT_ALLOCATION.md) |
| 部署说明 | [README-部署说明.md](/Users/newlink/kemi/RustDesk/server/deployment/README-部署说明.md) |
| 服务端仓库 | /Users/newlink/kemi/RustDesk/server |
| 新集群项目 | /Volumes/ORICO/newlink-new/hbbv |
| hbbv 项目参考快照 | /Volumes/ORICO/newlink-new/hbbv/docs/PORT_ALLOCATION.md；不能替代权威表 |
| SSH 运维入口 | root@119.96.24.110:39281；只用已有授权身份或会话，账号不是凭据 |
| 只读远程核验约定 | [hbbc 生产操作参考](/Users/newlink/.codex/skills/kemi-hbbc-release/references/production-deployment.md) |

权威表逐项列有 hbbs、hbbr、hbbc、系统 SSH 与 hbbv。hbbv 的 21122/TCP 已登记为设计预留，尚未部署。2026-09-24 的只读 SSH 尝试到达认证阶段，返回 `Permission denied (publickey,password)`；没有取得远端 listener 列表，不能宣称端口空闲。后续核验成功应更新权威表和本段历史状态，不删除历史失败事实。

hbbc 源码监听配置及账号路由在 `hbbc/src/main.rs`、`hbbc/src/account.rs`，配置模板在 `deployment/hbbc.example.json`。正式 hbbs/hbbr 端口依据是其部署 unit 与 `build-rustdesk-server-oss.sh` 固定上游源码；仓库 `src/main.rs` 是简化 demo，不能据此漏掉 NAT/WebSocket 端口。

新增服务器时，在本索引登记它自己的主机/环境和权威文档路径，不把另一台服务器的端口直接加入本机已有服务器的表中。

## hbbv 本机开发环境（2026-09-25）

环境标识 hbbv-local-development：当前 ORICO 开发 Mac，计划回环 127.0.0.1:21122/TCP HTTP，设计预留、未部署。权威台账：[LOCAL_PORT_ALLOCATION.md](/Volumes/ORICO/newlink-new/hbbv/docs/LOCAL_PORT_ALLOCATION.md)。仅用于本机仿真；不代替云端 HTTPS 21122 的独立记录。现场有限检查及警告见该表，不能宣称完整验证空闲。其他电脑联调按各自主机另行登记。

2026-09-25：hbbv 源码与设计归档位置 [caucy2026/priv/hbbv](https://github.com/caucy2026/priv/tree/main/hbbv)。已完成本机能力展示链路；云端端口仍为设计预留。每个云端端口的具体服务类型已补在权威表第 8 节。
