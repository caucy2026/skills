---
name: bot云机编译，kemi box真机验证
description: 在 Grok Bot 云电脑（box）按 KEMI 真机（默认 Linux 101）探测环境搭镜像构建客机、编译 aarch64 产物，再经控制机或云机本机 Vibekits 仿真推真机冷启/投递时使用。含摸底、ABCD/半残注册自愈、consent、identity_mismatch、transport_timeout 静默 peer、tool-bridge 云机直连 101 及同类设备投递口令；冒烟≠正式 deb。
---
# bot云机编译，kemi box真机验证

**跨机文件传递**：引用其它技能脚本时用 GitHub raw（`https://raw.githubusercontent.com/caucy2026/skills/main/...` 或本仓 `.../grok.skills.vibekits/main/...`），禁止写死 `/Users`、`/Volumes/ORICO` 技能路径。

标准口径：**云机（Grok Bot box）编译 →（可选）控制机仿真通道 → KEMI 真机验证**。默认真机为 Linux **101**（`mp730-156` / routingId `7634801763`）。**同类型设备**（同代 Vibekits、可仿真的 Linux/Mac 客机）换 `routingId` 后按同一套路；先摸底再推包。

合主线注明「gork.bot协助开发」。**验证 ≠ 编译**。禁止 `SendToAgent` 甩锅；禁止为推包停真机上的 **vibekits**。

**仿真通道优先序**

1. 有控制机 `invoke.rb` 且只需投递/冷启 → 优先控制机发仿真（§5）。
2. 必须从 **bot 云机本机** 当控制器（Docker Ubuntu20 amd64 冒烟/运行时）连 101 或同类设备 → **§6 + §6.8–§6.12**（ABCD / 半残注册自愈 / consent / 错误字典 / tool-bridge 投递）。
3. 冒烟运行时 ≠ 正式商场 amd64 `.deb` 上架包。

同事**不必读聊天记录**：按 §0 最短口令 + §6 清单即可仿针/投递。

---

## 0. 最短口令（云机直接仿 101 / 同类设备）

目标：在 bot 云机容器里当控制器，对目标 `RID` 做 `connect` → `upload_file` / `ssh_exec` → `disconnect`。

| 步骤 | 做什么 | 停条件 |
|---|---|---|
| 0 | 确认容器在跑（例：`vk-u20-amd64-772-run`）；`sudo docker` | 无容器则先按冒烟搭法起 runtime，勿把 smoke 当上架 deb |
| 1 | §6.2 钉 **宿主机 + 容器** ABCD（禁止解析成 `198.18.0.1`） | `getent hosts kemi-chat1…` 须真 IP |
| 2 | §6.8 **实活注册**（不只看 CLI `registered`）：须有到 ABCD 的 ESTAB/`request_pk`；半残则只重启容器内 vibekits+relay | routingId/digest 变了 → 目标要**重新同意**，STOP 告知用户 |
| 3 | `openssh-client`；`simulatorAccessEnabled=true`；记下控制器 `routingId` 与 `protocol_vN`（目标同类宜 `protocol_v4`） | |
| 4 | 首次对该目标：`connect` → 目标 UI **同意**（§6.5）；同控制器+同公钥可复用 ledger allow | 禁止旁路 consent；禁止杀目标 vibekits |
| 5 | **恰好 1 次**真实 `connect`（tool-bridge 字段名是 **`toolId`**，不是 `name`） | 失败按 §6.9 字典；**禁止盲连第二遍** |
| 6 | 通则：`ssh_exec 'hostname; uname -m'`；投递：`upload_file`（`localPath`=**控制器本机/容器内**绝对路径） | 验收 §6.6 |
| 7 | `disconnect`；回执写控制器/目标 ID、transport、hostname、是否经 consent | |

默认真机：`RID=7634801763`（101）。其它设备：用户给的 `routingId`，先 §2 摸底。

---

## 1. 三角色

| 角色 | 身份 | 职责 |
|---|---|---|
| **云机 / box** | Grok Bot 云电脑 | 搭与真机对齐的编译客机、编译、打包、探针；也可本机跑 vibekits 作**控制端**（§6） |
| **控制机 newlink** | `machineId=92c2f165-4f49-452d-b60c-ae24cb8eb990` | VibeKits bridge + `invoke.rb`（首选仿真入口）；大包中转；lima 备用客机 |
| **KEMI 真机 / box（设备）** | 默认 101=`mp730-156`，`7634801763` | 只部署、冷启、取证；**同意仿真请求**；其上 vibekits **禁止误杀** |

说明：口语「kemi box」= 真机；「bot 云机」= 本助手云电脑。

**routingId（示意，一律以当次 harness status 实读为准）**

| 角色 | 常见示例 | 备注 |
|---|---|---|
| 默认真机 101 | `7634801763` | `mp730-156` / aarch64 |
| 控制机 newlink | `1554650784` | Mac 侧 vibekits |
| bot 云机控制器 | 如 `9245390203` | 容器内新起 Harness 会换 ID；**勿写死进脚本当永久常量**；冒烟例容器名 `vk-u20-amd64-772-run` |

---

## 2. 怎么知道真机的系统与编译相关环境（摸底）

不要猜发行版/glibc。一律经仿真连上后 **只读采集**，写成当次 `TARGET_PROFILE`。

### 2.1 连接

**首选（控制机）**：

```bash
INV_URL=https://raw.githubusercontent.com/caucy2026/skills/main/vibekits-remote-simulator/scripts/invoke.rb
curl -fsSL "$INV_URL" -o /tmp/vibekits-invoke.rb
INV=/tmp/vibekits-invoke.rb
RID=7634801763   # 或用户给的 ID
ruby "$INV" vibekits.simulator.connect "{\"routingId\":\"$RID\"}"
```

验收：`ok`、`connected:true`、`routingId` 匹配、`hostname`、`targetPlatform`、`transport`、`sshReady:true`、`sshHostKeyFingerprint`。

**bot 云机本机**：先 §6（含 §6.8 实活），再用 §6.11 tool-bridge；`consent_pending` 时在**目标设备 UI** 点同意，禁止旁路。

### 2.2 必采清单（ssh_exec）

**身份 / OS**：`hostname`；`uname -a`；`uname -m`；`/etc/os-release`；`/proc/version`；`/proc/cmdline`。

**CPU / 内存 / 负载**：`lscpu`；`free -h`；MemTotal/SwapTotal（101：**无 swap**）；`loadavg`。

**libc / 编译器基线**：`ldd --version` → max-glibc（101：**2.31**）；`ld-linux-aarch64.so.1`；GLIBCXX 上限（101 常到 **3.4.28**）；有则记 gcc/g++。

**磁盘**：`df -hT` 关键路径；部署前可用字节 > 包体×2。

**显示 / GPU（GUI）**：DISPLAY/XAUTH（101 常见 `:0` + `/run/user/0/gdm/Xauthority`）；`/dev/dri`；Mesa/EGL。

**网络与已有部署**：`ip -br a`；`/opt`；**vibekits 是否在跑**（PID 记回执，禁止误杀）。

### 2.3 产出物

`hw/<target>-profile.env` + 短证据 md。101 冻结基线（2026-11，改机重采）：aarch64 · Ubuntu 20.04.5 · glibc **2.31** · 8×A73 · RAM≈5.5G · swap=0 · gdm3+Xorg:0 · Mesa/EGL≈21.2 · 根盘偏满。

采完 `disconnect`。

---

## 3. 怎么在云端搭建「对应」的编译环境

原则：**运行 ABI 对齐真机**；工具链可新，产物不得要求比真机更新的 glibc（除非自带 loader+libs）。

### 3.1 先看云机自身

`uname -m`（常 x86_64）；`ldd --version`（常远高于真机）；docker/qemu/binfmt。box **不能**把原生 x86 ELF 直接当 101 产物。

### 3.2 选型矩阵

| 真机约束 | 云端编译客机 | 产物形态 |
|---|---|---|
| Ubuntu 20.04 + glibc≤2.31 | **Ubuntu 20.04 arm64** 客机 | 普通动态链接；可捆绑更高 libstdc++ |
| 需 Qt≥6.6 等，真机仍 2.31 | 较新 arm64 客机 + **自包含 runtime** | `--library-path` 启 |
| 仅 Rust 等 | `cargo-zigbuild` 钉 `…gnu.2.31` 一类 | 探针过即推 |

### 3.3 bot 云机搭客机

arm64 容器/rootfs，用户态 glibc≤真机（101 → Ubuntu focal）。启用 qemu-user-static；自检 `uname -m`/`ldd`；并发按真机内存保守（101 参考 `KOFFICE_ENGINE_JOBS=3`）。

### 3.4 控制机 lima 备用

`LIMA_HOME=/Volumes/ORICO/lh`：`ko-u20`（focal/aarch64）、`ko-r26`（新 Qt，须自包含 runtime）。回执写「实际编译宿主=…」。

### 3.5 开编前勾选

- [ ] arch 对齐；glibc≤真机或自包含
- [ ] GLIBCXX；GUI env（101：`QT_QPA_PLATFORM=xcb`、`QT_OPENGL=egl`）
- [ ] 输出目录与 SHA 路径已定

---

## 4. 编译 → 探针 → 打包

1. 冻结 commit / 脏文件。
2. 对齐客机内编译。
3. 推真机前 `probe_elf.py --target-arch arm64 --max-glibc 2.31`（失败禁止上传）。
4. `tar` + `zstd` + `.sha256`。

---

## 5. 产物送达 → 仿真推真机

### 5.1 经控制机（首选大包/同事 Mac 隧道）

`upload_file.localPath` 在 **newlink** 解析。

```bash
RID=7634801763
ruby "$INV" vibekits.simulator.connect "{\"routingId\":\"$RID\"}"
ruby "$INV" vibekits.simulator.upload_file "{\"routingId\":\"$RID\",\"localPath\":\"/abs/on/newlink/pkg.tar.zst\"}"
ruby "$INV" vibekits.simulator.ssh_exec "{\"routingId\":\"$RID\",\"command\":\"...\"}"
ruby "$INV" vibekits.simulator.disconnect "{\"routingId\":\"$RID\"}"
```

≤100MiB：`CopyFromBox` → newlink；更大则在 newlink 卷终包。通道是 **VibeKits 仿真**，不是公网手写 SSH。

### 5.2 经 bot 云机控制器（已打通 §6）

`localPath` = **云机容器内**（或 tool-bridge 所见）绝对路径；先把包 `docker cp` / 挂进容器，再 `upload_file`。口令见 **§6.11–§6.12**。验收标准与 §5.1 相同。

---

## 6. 云机本机跑 vibekits（ABCD · 注册 · consent · 投递）

适用：在 Grok Bot box 上起 vibekits / harness-relay（常见 Docker Ubuntu 20.04 **amd64** 冒烟）再连 KEMI 真机或同类设备。

### 6.1 根因速记（DNS 假 IP）

`SAND_EGRESS` 下容器 DNS 常把集群名解析成 **`198.18.0.1`** → ESTAB「假通」→ `offline` / `HARNESS_REGISTRATION_PENDING`。**容器有独立 `/etc/hosts`**，须宿主机 + 容器各钉一份；重建用 `--add-host` 或启动脚本重写。

### 6.2 清单 A — 钉 ABCD

| 节点 | 主机名 | 真 IP | HBBS（常见） |
|---|---|---|---|
| **A** | `kemi-chat1.newlinksz.com`（兼 `kemi-chat.newlinksz.com`） | `119.96.24.110` | `:21116`（relay `:21117`） |
| **B** | `kemi.newlinksz.com` | `171.43.138.47` | `:23116` |
| **C** | `kemi-sh1.newlinksz.com` | `159.27.117.207` | `:24116` |
| **D** | `kemi-sg1.newlinksz.com` | `172.188.240.186` | `:21116` |

```
# vibekits-kemi-abcd
119.96.24.110 kemi-chat1.newlinksz.com kemi-chat.newlinksz.com
171.43.138.47 kemi.newlinksz.com
159.27.117.207 kemi-sh1.newlinksz.com
172.188.240.186 kemi-sg1.newlinksz.com
```

勾选：宿主机+容器 hosts；`getent` 非 198.18；至少 A:21116 可达；`kemi-cluster-node` 与 `custom-rendezvous-server` 一致（国内常用 **a** + `kemi-chat1:21116`）。

### 6.3 清单 B — 重启 bot 侧并验收注册

只重启 **bot 侧** vibekits + vibekits-harness-relay；**不要**杀目标 vibekits。

验收：`state=registered`；`rendezvousOnline`/`callable`/`registrationKeyConfirmed`；记下 `routingId`；出站 ESTAB **真 IP**；`simulatorAccessEnabled=true`；`protocol_vN`（与目标对齐，已验证路径为 **v4**）。冒烟 relay 可能需 `LD_LIBRARY_PATH=<runtime>/lib`。

**且必须满足 §6.8（防虚报 registered）。**

### 6.4 清单 C — `openssh-client`

缺则 `missing_ssh_keygen`。容器内：`apt-get install -y openssh-client`。

### 6.5 清单 D — 首次仿真与 `consent_pending`

新控制器第一次连目标：`code=consent_pending`。动作：

1. **目标设备 UI** 点同意（ConsentHost 需当前路由；应用中心等模态会挡住）。
2. 禁止旁路 / 改授权库 / 杀目标 vibekits。
3. `consent_pending` ≠ 弹窗已出现：核对 `pendingConsentRequests` / ledger。
4. 同意后再 connect；ledger `decision=allow`。同控制器 routingId+公钥可复用 allow（digest 变了要重同意）。

### 6.5.1 同意后仍 `identity_mismatch`（停盲目重试）

- 校验看 **HarnessIdentityProof**，**不看** appBuild（壳 2772 连目标 2832 可以通，前提 relay/控制面同代）。
- 缺证明 / unsupported proof → 常 `protocol_upgrade_required`；其它 verify Err → `identity_mismatch`。
- 对齐两侧 `protocol_vN`（升 bot 侧 relay 到 v4）；目标 registered；ESTAB 真 IP。
- **同 ID 双端**：目标上 KEMI 与 Vibekits 同抢一 `routingId` → 打孔落 KEMI、无 SourceBinding → 字面 `identity_mismatch`。处置：只留 Vibekits 占该 ID，再恰好 1 次 connect。
- 次要：`my_id` 写成 `id@server` → `consent_controller_id_mismatch`；出证明前用裸 ID。
- 诊断：login JSON `detail`；Dart 透传；合主线「gork.bot协助开发」。勿加 appBuild 比对当身份条件。

### 6.6 验收（云机控制器路径）

```text
connect → ok / connected=true / sshReady=true / hostname 与目标一致
ssh_exec → hostname; uname -m
（投递）upload_file → 目标路径存在且 SHA/大小对账
disconnect
```

### 6.7 与正式包的边界

Docker 冒烟/拼装 runtime 只用于通路与编译验证；**正式市场 amd64 `.deb` 另线**。

### 6.8 半残注册（虚报 `registered`）— 连前必做

**现象（已多次实测）**：CLI/`--vibekits-harness-status` 仍报 `state=registered` · `callable=true`，但对 ABCD **TCP/UDP 套接字计数=0**；server 日志早期 `ipc … Address already in use`；`ipc_person_consent` 等僵尸；`request_pk` 停更。此时 connect 易失败或误判。

**处置（只动 bot 云机）**

1. 保留 Xvfb（如 `:99`）。
2. **只**停容器内 `vibekits` + `vibekits-harness-relay`；清理陈旧 `/tmp/VibekitsHarness-*` IPC 套接字/pid（勿广清用户数据）。
3. 按既有 boot/`restart-abcd` 拉起；`--vibekits-harness-simulator-access true`。
4. 验收：**同一** `routingId` + 公钥 digest；`protocol_vN`；ESTAB → 真 IP（如 A `119.96.24.110:21116`）；有新的 `request_pk`/注册成功日志。
5. 若 ID/digest **变了**：STOP，请用户在目标 UI 重新同意；禁止假装仍有旧 allow。

**不要**为自愈去重启目标机或 Mac 上正给同事开隧道的 Vibekits。

### 6.9 错误字典（云机 ↔ 目标）

| 表象 | 高置信含义 | 先做什么 | 禁止 |
|---|---|---|---|
| DNS/`198.18` ESTAB | 假 IP | §6.2 双钉 hosts | 只钉宿主机 |
| `HARNESS_REGISTRATION_PENDING` / offline | 未挂上会合 | §6.2–6.3 + §6.8 | 盲连目标 |
| 虚报 registered + socks=0 | 半残 mediator/IPC | §6.8 只重启 bot 侧 | 杀目标 vibekits |
| `consent_pending` | 等目标同意 | 目标 UI 同意；查挡板模态 | 旁路 ledger |
| `identity_mismatch` | 证明失败 **或** 同 ID 抢打孔无 SourceBinding | 停重试；对 protocol_vN；查 KEMI/Vibekits 双端 | 清 consent 掩盖 |
| `protocol_upgrade_required` | 证明协议/字段不入流 | 升 bot relay 至与目标同代（v4） | 拿 appBuild 当身份 |
| `transport_timeout`（打孔+`Harness identity proof created` 后 ~18s 无 `peer info`） | **目标静默 peer**（进程假死/半注册/过载）；Dart 映射 Timeout | 用户确认目标 UI 可点、registered、非 TOO_FREQUENT；必要时**用户授权**后才重启**目标** Vibekits；同时排除控制器半残（§6.8） | 无新修复时盲连；把单边 ABCD 当唯一根因 |
| `http_404` 且阶段含 `notifications/initialized` | MCP 隧打错口或抖动：控制面 `32148` vs MCP `32147`；桌面三步各开会合 | 核隧道 argv 目标口；对齐同代后再 **1 次**连 | 当成同意失败 |
| `missing_ssh_keygen` | 缺 openssh-client | §6.4 | |
| 集群 `TOO_FREQUENT` / `SERVER_ERROR` | 加重因素（双侧注册风暴） | 冷却；对齐 node/rendezvous；不杀同事隧道 | 当作唯一根因掩盖静默 peer |

**成功时间线对照**：proof 后 **~0.4–0.6s** 应出现 `peer info supported_encoding` → port-forward；若 proof 后十几秒只有 `Connection closed: Timeout` → 按静默 peer，不要当成 identity。

### 6.10 来龙去脉（给维护者，执行可跳过）

2026-11 云机路径踩坑顺序（合主线 gork.bot协助开发）：

1. ABCD/`198.18` → 注册不上。
2. 目标同意链路通（可先连控制机 Mac UI 验）。
3. `identity_mismatch`：升云机 relay → **protocol_v4**（不看 appBuild）；另案同 ID 上 KEMI 抢打孔。
4. 同意后偶发 `http_404`（MCP/控制口）：对齐隧道口后可通。
5. `transport_timeout`：双侧打孔+proof 成功但目标不回 peer → 用户重启目标 Vibekits 后恢复。
6. 连前反复出现云机 **虚报 registered**：§6.8 只重启容器 vibekits+relay，保持同一控制器 ID，即可再 `connect`+`ssh_exec`（101 验过 `mp730-156`/`aarch64`）。

证据目录习惯：`work-notes/DEBUG-T*-*.md`（勿把密钥写进技能）。

### 6.11 tool-bridge 调用约定（云机）

1. 读容器内 `VibekitsData/Mcp/tool-bridge.json`：`endpoint`（如 `http://127.0.0.1:<port>`）、`token`、`processId`。**token 勿写入技能/聊天/证据明文扩散**；用后即弃。
2. `POST {endpoint}/invoke`，JSON 形如：

```json
{
  "toolId": "vibekits.simulator.connect",
  "arguments": { "routingId": "<RID>" }
}
```

关键 toolId（以当次 list 为准）：`vibekits.simulator.connect` / `upload_file` / `ssh_exec` / `disconnect`；可能还有 `peer_presence`。

3. **字段名必须是 `toolId`**。误用 `name` 会立刻「未知 Vibekits 工具」，**不进打孔**——勿计入「已 connect 一次」。
4. Header：按实现带 Bearer/`token`（与 json 内 token 一致）。
5. 在 **容器网络命名空间**内 curl（`docker exec …`）；宿主机直访问 127.0.0.1 容器口通常不通。
6. 每次真实 `connect` 记隧道日志（hole punch / proof / peer info），便于套用 §6.9。

### 6.12 云机投递文件（upload）

```text
预检 §6.8 → connect(RID) → upload_file → ssh_exec 校验 → disconnect
```

- `upload_file` 参数：`routingId` + `localPath`（**控制器可见**的绝对路径）。云机路径：先把文件放进容器（`docker cp` 或 bind），再传该容器路径。
- 大包：优先控制机 §5.1；云机路径适合中小包与通路验证。
- 校验：`ssh_exec` 对目标路径 `ls -l` / `sha256sum`；回执写字节数与 SHA。
- 未授权不上传商场；不覆盖目标 vibekits 树。

示例（结构示意，口令随环境改）：

```bash
CTR=vk-u20-amd64-772-run
RID=7634801763
# 1) 包进容器
sudo docker cp ./pkg.tar.zst "$CTR":/tmp/pkg.tar.zst
# 2) 容器内读 bridge 并 invoke connect / upload_file / ssh_exec / disconnect
#    toolId=vibekits.simulator.upload_file
#    arguments: {"routingId":"$RID","localPath":"/tmp/pkg.tar.zst"}
```

---

## 7. 真机部署与冷启验证

1. 解压到 `/opt/<app>-<YYYYMMDD>/...`，勿动 vibekits 树。
2. GUI：`DISPLAY=:0` + 真实 `XAUTHORITY`；硬件 env 见 §8。
3. ABI 对齐直接跑；自包含用 bundled `ld-linux` + `--library-path`。
4. 最低验收：进程存活（如 ≥20s）+（GUI）窗口；记 PID/RSS/标题/SHA256。
5. 证据入 `work-notes/`；`disconnect`。区分 cold pass vs 未测项。

---

## 8. 硬件优化默认（101）

```bash
export KOFFICE_TARGET_HOSTNAME=mp730-156
export KOFFICE_TARGET_ROUTING_ID=7634801763
export KOFFICE_TARGET_ARCH=aarch64
export KOFFICE_ENGINE_JOBS=3
export KOFFICE_ONLINE_JOBS=2
export KOFFICE_RENDER_WORKERS=2
export KOFFICE_CACHE_BUDGET_MB=256
export KOFFICE_DISABLE_SWAP_ASSUMPTION=1
export KOFFICE_PREFER_EGL=1
export QT_OPENGL=egl
export QT_QPA_PLATFORM=xcb
export KOFFICE_LO_DISTRO=CPLinux-LOKit
```

其它设备：按 §2 profile 改 hostname/RID/arch/jobs。

---

## 9. 清理与总口令

谁产生构建树谁收尾：`kemi-storage-cleanup` / `cloud-build-cleanup`。

1. 摸底（控制机 invoke **或** 云机 §0/§6）→ 冻 profile。
2. bot 云机搭对齐客机（或声明 lima）→ 编译 → probe → 打包。
3. 控制机 §5.1 **或** 云机 §6.12 推目标 → 冷启取证 → disconnect。
4. 不停目标 vibekits；不旁路 consent；`identity_mismatch`/`transport_timeout` 按 §6.9；冒烟 ≠ 正式 deb；合主线「gork.bot协助开发」。

