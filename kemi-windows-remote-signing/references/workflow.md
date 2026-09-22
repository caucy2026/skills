# VibeKits 远程仿真 Windows Authenticode 签名

本流程用于通过 VibeKits 远程仿真接口，在已授权 Windows 设备的登录桌面会话中调用硬件令牌完成 Authenticode 签名，并由控制端持续跟踪到最终验签结论。它适用于 iTrus、SafeNet、eToken 等把私钥保存在硬件令牌中的代码签名证书。

本文是执行手册。开始前必须同时遵循 `vibekits-remote-simulator` 和 `kemi-windows-device-lab`，并读取同目录的 `authenticode-signing.md`。项目自己的签名清单、包装顺序和发布规则优先。

## 完成标准

只有以下条件全部成立，才能报告签名成功：

1. 本次运行新生成最终 `summary.json`，状态为 `PASS`，退出码为 0。
2. 固定清单中的每个 PE 文件均重新验签；文件数与预期完全相等。
3. 每个应由产品证书签名的文件，其嵌入签名证书指纹与本次发现并锁定的证书一致。
4. 每个文件都有可信时间戳，`signtool verify /pa /all /v /tw` 退出码为 0。
5. 主程序另外执行一次独立验签并通过。
6. 最终文件的大小和 SHA-256 在签名后重新计算并写入报告。
7. 若存在最终安装包或自解压外壳，必须先签内部 PE、再打包、最后单独签外壳；内部签名不能替代外壳签名。

“SignTool 进程退出”“PIN 已输入”“某一批签名完成”“Get-AuthenticodeSignature 显示 Valid”都不是单独的完成证据。

## 安全边界

- 只使用用户明确授权的 VibeKits 设备 ID。连接后核对 `connected: true`、原设备 ID、`transport: p2p_or_relay`、主机名、用户名和已记录的 SSH 主机密钥指纹。
- 不询问设备 IP、SSH 密码、私钥、RustDesk 密码或令牌 PIN。
- PIN 只允许用户在 Windows 硬件令牌对话框中输入。不得读取、保存、猜测、粘贴、脚本化或写入日志。
- 不使用远程桌面 UI。控制端使用 VibeKits 仿真工具；登录会话内的启动由 `vibekits.device.app_control` 完成。
- SSH 命令运行在 Session 0，只能用于只读检查、上传、哈希、准备固定脚本和读取报告。硬件令牌签名必须运行在已登录的 Session 1 或当前交互会话。
- 所有可控文件、日志、脚本、候选和结果都放在 `D:\KEMI-Test`。不要在 `C:` 或用户配置目录创建项目载荷。
- 不覆盖已验证入口、历史报告或已签候选。新版本使用新的版本化名称和结果目录。
- 重试前先确定旧进程是否仍在运行，绝不并行启动两个签名进程写同一候选。

## 1. 连接与身份核验

在 VibeKits Harness 内优先直接调用已注册工具。外部 macOS 控制端没有注册工具时，使用技能自带的本机回环桥：

```bash
ruby /Users/<user>/.codex/skills/vibekits-remote-simulator/scripts/invoke.rb \
  vibekits.simulator.connect '{"routingId":"<DEVICE_ID>"}'
```

结构化结果至少应包含：

```json
{
  "connected": true,
  "routingId": "<DEVICE_ID>",
  "transport": "p2p_or_relay",
  "sshReady": true,
  "mcpReady": true,
  "hostname": "<EXPECTED_HOST>",
  "sshUsername": "<EXPECTED_USER>",
  "sshHostKeyFingerprint": "<EXPECTED_FINGERPRINT>"
}
```

任何身份或主机密钥不匹配都必须停止。不要删除 known-host 记录或绕过主机密钥验证。

期望主机名、用户和 SSH 指纹必须来自项目受信节点登记文档或用户本次明确提供的记录，不能把本次 `connect` 返回值自身当作信任根。首次接入的新节点缺少可信记录时，先完成节点登记，不能在签名流程中现场接受未知指纹。

短 PowerShell 检查必须编码为 UTF-16LE Base64，再作为一个精确命令传给 `vibekits.simulator.ssh_exec`：

```text
powershell.exe -NoLogo -NoProfile -NonInteractive -EncodedCommand <BASE64>
```

每次检查同时验证外层和内层的 `ok`、`exitCode`、`stdout`、`stderr`；HTTP 或工具传输成功不等于远端脚本成功。

## 2. 只读盘点当前状态

任何启动或重试之前，先检查：

- `D:` 是否存在且可写，候选、工作目录、结果目录是否都在 `D:\KEMI-Test`。
- Windows 主机名、当前登录用户、活动桌面会话及锁屏状态。
- 交互用户、会话用户名和目标 Session ID 必须绑定到同一次运行；“Session ID 非 0”不足以证明会话正确。拒绝 Disconnected、残留 RDP 和快速用户切换留下的非活动会话。
- 是否已有同一版本的 `pwsh`、`powershell`、`signtool` 或固定签名脚本进程。
- 候选目录是否自包含；主程序和必须的运行库是否齐全。
- 固定清单的文件数、路径、大小和签名前 SHA-256。
- 本次版本化的入口脚本、实现脚本、报告目录和日志是否已存在。
- 当前登录会话的 `Cert:\CurrentUser\My` 中是否有唯一、未过期、带私钥且含代码签名 EKU `1.3.6.1.5.5.7.3.3` 的证书。
- x64 SignTool 的绝对路径和版本。

若签名已在运行，先读取进程、日志、批次报告和最终报告。不要因为某个 `signtool.exe` 暂时消失就立即判定失败；签名脚本可能正在逐文件验签。也不要因为父 `pwsh` 仍在就判定仍等待 PIN。

## 3. 冻结候选与固定清单

签名前复制出独立的版本化候选目录，后续只在此目录签名。不要直接修改正在运行的安装目录或上一版候选。

固定清单必须：

1. 递归枚举项目要求签名的 `.exe`、`.dll`、`.msi`、`.msix`。
2. 使用绝对路径并稳定排序。
3. 记录路径、字节数和签名前 SHA-256。
4. 写入版本化 `pre-sign-manifest.json`。
5. 在执行前断言实际文件数与 `ExpectedFileCount` 完全相等。

命令行长度可能使大量文件无法一次传给 SignTool。按路径字符串总长度确定批次，例如把每批控制在约 18,000 字符以内。批次边界必须由脚本确定并写入日志，不能临时手工拼接。

## 4. 使用固定签名实现

优先复用全局 `Invoke-KemiAuthenticode.ps1` 或项目内已验证的等价实现。禁止临时拼接 `signtool` 命令，禁止使用 `/a` 自动选择证书。

每批调用形态：

```powershell
& 'D:\KEMI-Test\work\Invoke-KemiAuthenticode.ps1' `
  -Mode Sign `
  -Path ([string[]]$batch) `
  -ExpectedFileCount $batch.Count `
  -ExpectedThumbprint $currentThumbprint `
  -Description '<PRODUCT_NAME>' `
  -ReportPath "D:\KEMI-Test\results\signing\<RUN_ID>\batch-01-sign.json"
```

签名实现必须固定使用：

```text
signtool sign /v /s My /sha1 <THUMBPRINT> /fd SHA256 \
  /tr http://timestamp.digicert.com /td SHA256 /d <DESCRIPTION> <FILES...>
```

签名后立即对本批每个文件执行：

```text
signtool verify /pa /all /v /tw <FILE>
```

报告至少保存路径、字节数、签名后 SHA-256、状态、签名者主题、签名者指纹、时间戳证书、SignTool 验签退出码和最终布尔值。

## 5. 在登录会话启动固定入口

固定入口由三层组成：

1. 版本化 PowerShell 实现，例如 `Sign-Product-1.2.3-20260918.ps1`。
2. 版本化 CMD 包装器，把 stdout/stderr 写到版本化日志并返回真实退出码。
3. 极小的 GUI 启动器 EXE，使用 `UseShellExecute=true` 从登录桌面启动 CMD。

CMD 示例：

```bat
@echo off
"C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -NonInteractive ^
  -File "D:\KEMI-Test\work\Sign-Product-1.2.3-20260918.ps1" ^
  > "D:\KEMI-Test\results\signing\Product-1.2.3-20260918.log" 2>&1
exit /b %ERRORLEVEL%
```

GUI 启动器只启动这个固定 CMD，不接受任意命令参数。通过仿真接口调用：

```json
{
  "routingId": "<DEVICE_ID>",
  "toolId": "vibekits.device.app_control",
  "arguments": {
    "action": "launch",
    "target": "D:\\KEMI-Test\\work\\Launch-Sign-Product-1.2.3-20260918.exe"
  }
}
```

若项目尚无固定 GUI 启动器，可使用下列最小实现为本次版本生成一个只指向固定 CMD 的 EXE，并记录 C# 源码和 EXE 的 SHA-256。生成后不得改变目标路径：

```csharp
using System.Diagnostics;
internal static class Program {
  [System.STAThread]
  private static void Main() {
    Process.Start(new ProcessStartInfo {
      FileName = @"D:\KEMI-Test\work\Run-Sign-Product-1.2.3-20260918.cmd",
      WorkingDirectory = @"D:\KEMI-Test\work",
      UseShellExecute = true,
      WindowStyle = ProcessWindowStyle.Minimized
    });
  }
}
```

在 Windows 上用系统 .NET Framework 编译器生成：

```text
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /nologo /target:winexe \
  /out:D:\KEMI-Test\work\Launch-Sign-Product-1.2.3-20260918.exe \
  D:\KEMI-Test\work\Launch-Sign-Product-1.2.3-20260918.cs
```

这段启动器只解决 Session 1 启动，不证明会话 Active 或解锁。调用前必须通过当前节点的 WTS/桌面代理确认目标用户的会话状态为 Active，调用后再核对父 PowerShell、SignTool 和 PIN 窗口全部位于同一 Session ID。

启动后 10 秒内必须观察到以下至少一个信号：

- Session 1 中出现固定脚本的父 PowerShell 进程；
- Session 1 中出现 `signtool.exe`；
- 出现硬件令牌 PIN 对话框；
- 本次版本化日志或状态文件刷新。

若均未出现，结果是 `INTERACTIVE_WRAPPER_NOT_STARTED`。不要从 Session 0 重试 SignTool。

## 6. 确认 PIN 对话框真实可见

“进程的 `MainWindowTitle` 曾显示设备登录”不足以证明用户当前能看到窗口。**签名人员实际看到 PIN 对话框截图，是进入等待输入状态的强制门槛。** 不能只报告窗口标题或 `Visible=true`，也不能让用户盲输 PIN。

### 6.1 强制截图与展示

窗口恢复并置前后，控制端必须立即调用 `vibekits.simulator.screenshot`。截图必须满足以下全部条件：

1. 截图来自本次连接的同一设备，并在 PIN 窗口置前后生成。
2. 画面清楚显示“设备登录”或等价的硬件令牌 PIN 对话框；输入框必须为空，不能在用户开始输入后再取证。
3. 控制端实际打开图片检查，不能只看 `captured: true`、文件大小或下载成功。
4. 图片必须直接展示给签名人员，随后明确提示“PIN 窗口已显示，请在目标机输入 PIN”。仅给远端路径不算完成。
5. 在本次结果目录记录截图时间、设备 ID、Session ID、PID、HWND、像素尺寸、捕获方式和 PNG 的 SHA-256。远端建议路径为 `D:\KEMI-Test\results\signing\<RUN_ID>\pin-before-input.png`。

截图中不得出现 PIN 明文。用户开始输入后不得重复截取输入框；签名完成后的证据使用状态文件、报告和验签结果，不使用含认证输入状态的截图。

### 6.2 仿真截图黑屏时的固定补救

仿真接口返回全黑、纯色、旧画面、零尺寸或看不到 PIN 对话框时，不能把黑屏解释为“没有窗口”，也不能跳过截图。按以下顺序补救：

1. 用下方只读窗口探测器确认 PIN 窗口的 PID、HWND、可见性和矩形。
2. 只对已核实属于本次 `signtool` 或令牌中间件的 HWND 执行恢复和置前。
3. 在同一 Session 1 中，通过固定、版本化的截图辅助程序捕获虚拟桌面，保存到本次结果目录。禁止从 SSH 所在的 Session 0 直接截图。
4. 用 `vibekits.simulator.download_file` 下载 PNG，在控制端打开检查并展示给签名人员。
5. 若 Session 1 截图仍因安全桌面或中间件保护而不可见，状态写为 `PIN_SCREENSHOT_UNAVAILABLE`，报告具体原因并要求签名人员直接查看目标机屏幕。此时不得声称“PIN 对话框已可见”，也不得进入无人值守等待。

Session 1 截图辅助程序可固定使用以下 PowerShell 实现；它只截屏，不读取控件、不发送输入。脚本必须由 `vibekits.device.app_control` 启动到活动会话：

```powershell
param([Parameter(Mandatory=$true)][string]$OutFile)
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
  $graphics.CopyFromScreen($bounds.Left, $bounds.Top, 0, 0, $bounds.Size)
  $bitmap.Save($OutFile, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
  $graphics.Dispose()
  $bitmap.Dispose()
}
```

截图辅助程序、启动器和输出路径必须固定到本次 `RUN_ID`；保存源码和 SHA-256，禁止接收任意命令。图片检查至少确认像素尺寸正常、画面不是单色，并由控制端视觉确认 PIN 对话框确实在画面中。

### 6.3 窗口探测与置前

Windows 仿真控件树在某些节点可能不可用，因此应在 Session 1 中运行只读窗口探测器，枚举顶层窗口并记录：

- HWND；
- PID；
- 标题；
- `Visible`；
- `Enabled`；
- `Minimized`；
- 窗口矩形。

合格信号是 `signtool` 或令牌中间件拥有标题类似“设备登录”的窗口，且 `Visible=true`、`Enabled=true`。

窗口探测器必须是固定的、受限的版本化辅助程序，只允许枚举窗口元数据，以及对调用者明确传入且再次核实属于当前 `signtool` PID 的 HWND 执行恢复/置前。它的源码、EXE SHA-256、目标 PID、输出 JSON 和运行时间必须保存在本次结果目录。禁止使用可发送任意键盘输入或读取密码控件内容的通用自动化器。

如果窗口存在但最小化或被其他窗口遮挡，可通过受限的 Session 1 辅助程序仅对该已核实 HWND 调用：

```text
ShowWindow(hwnd, SW_RESTORE)
BringWindowToTop(hwnd)
SetForegroundWindow(hwnd)
```

辅助程序不得发送按键、读取控件值或输入 PIN。置前后重新枚举窗口，确认仍属于本次 `signtool` PID。

若 `signtool` 在运行但没有任何顶层或子窗口，先进入至少 30 秒的观察宽限期。期间每 2–3 秒检查 CPU、候选文件签名/哈希变化、日志、状态心跳和批次报告：有进展通常表示 PIN 已成功输入并正在签名；完全无进展且状态仍为 `WAITING_FOR_PIN` 才按“PIN 窗口消失”处理。禁止仅凭窗口消失终止进程。若此前尚未把合格的 PIN 截图展示给签名人员，则必须先恢复窗口并完成第 6.1 或 6.2 节，不能直接进入等待输入状态。

## 7. 实时跟踪 PIN 输入后的状态

当用户输入 PIN 后，控制端必须继续同一轮工作，不能把后台定时任务当作实时响应，也不能要求用户再次通知。

展示 PIN 截图和输入提示后，控制端必须马上进入本节轮询；不要结束当前任务、不要创建新的定时任务、不要停在一次长时间阻塞调用中。窗口消失、CPU/文件开始变化或报告生成时应在下一次 2–3 秒轮询中响应，并继续追踪到 `PASS` 或 `FAIL`。

建议每 2–3 秒检查以下条件，单次等待不超过 45–60 秒，然后立即继续下一轮：

1. 当前 `signtool` PID 是否仍存在。
2. 父 PowerShell PID 是否仍存在。
3. 当前批次报告是否新生成。
4. `resume-state.json` 或同类状态文件是否从 `SIGNING` 变为 `VERIFYING_ALL`、`PASS` 或 `FAIL`。
5. `resume-exit.json`、`summary.json` 是否新生成。

状态解释：

| 观察 | 含义 | 动作 |
|---|---|---|
| `signtool` 存在，PIN 窗口可见 | 等待用户输入 | 保持实时轮询，不重复催促 |
| `signtool` 退出，父 PowerShell 存在，无批次报告 | 签名实现可能正在验本批文件 | 继续跟踪父进程和报告 |
| 批次报告出现，父 PowerShell 存在 | 本批完成，正在做全量验签 | 继续跟踪，不能提前宣布成功 |
| 父进程退出，最终报告和退出文件存在 | 已得到可判定结果 | 按最终门槛核验 |
| 父进程退出，无最终报告 | 异常中止 | 读取日志尾部和已有批次报告 |
| 进程存在但无窗口、无报告、状态不更新 | PIN 窗口消失或中间件挂起 | 保存证据，精确终止本次进程，最多重试一次 |

状态文件必须包含阶段、已处理数量、更新时间、PID 和 Session ID。最终报告必须先写临时文件再原子替换。固定包装器若不能产生状态、心跳和最终退出文件，就不满足“实时跟踪”前置条件；应先制作版本化包装器，不能仅靠进程标题猜测阶段。

推荐的可观测阶段为 `STAGED` → `WAITING_FOR_PIN` → `SIGNING_BATCH_1`/`SIGNING_BATCH_2` → `VERIFYING_ALL` → `PASS`，错误终态为 `FAIL` 或 `CANCELLED`。现有脚本阶段名不同时，应在运行手册中给出一一对应关系。

包装器必须为每次运行生成唯一 `runId` 和 `attemptId`，并在状态、批次报告和最终报告中写入：启动时间、脚本 SHA-256、签前清单 SHA-256、父子进程 PID、Session ID、证书指纹和最近心跳。读取结果时必须核对这些字段，不能把上一轮遗留的同名报告当成本轮结果。

推荐每 2–3 秒轮询，单次控制端等待不超过 45–60 秒；单批签名/验签的总超时由项目文件规模决定，但连续 120 秒没有状态心跳、日志增长、CPU 活动、文件变化或报告更新时必须进入诊断，而不是无限等待。

## 8. Microsoft Catalog 签名误判

Windows 对少数微软组件可能优先返回 Catalog 签名。此时：

- `Get-AuthenticodeSignature` 可能显示 Microsoft 签名者和 `SignatureType=Catalog`；
- 同一文件内部仍可能已经包含本次产品证书的有效 Authenticode 签名；
- `signtool verify /pa /all /v /tw` 会展示实际嵌入签名链。

不要因为 Windows API 返回微软 Catalog 签名就重新签文件或把它标为失败。对这类文件同时收集：

1. Windows 返回的状态、类型和签名者；
2. 从文件嵌入签名提取的证书指纹；
3. SignTool `/all` 的完整验签结果；
4. 时间戳证书。

合格条件仍是：状态有效、嵌入签名指纹匹配本次产品证书、时间戳存在、SignTool 退出码 0。最终报告另外记录 `CatalogSignatureCount`，保留可审计性。

提取嵌入签名证书时使用文件自身的 PKCS#7，而不是 `Get-AuthenticodeSignature.SignerCertificate`：

```powershell
$embedded = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new(
  [System.Security.Cryptography.X509Certificates.X509Certificate]::CreateFromSignedFile($path)
)
$embeddedThumbprint = $embedded.Thumbprint.ToUpperInvariant()
```

然后仍以 `signtool verify /pa /all /v /tw` 验证完整签名链和时间戳。固定最终验签器必须实际使用这两个信号；仅在文档中解释 Catalog 差异、而实现仍只比较 `Get-AuthenticodeSignature.SignerCertificate`，会继续误报。

这里的“Catalog 优先”专指 Windows 对普通 PE 查询时优先返回系统目录签名，并不表示本流程正在生成或签署 `.cat` 文件。驱动、WHQL、attestation 或自有 `.cat` 包需要单独的 catalog 生成、成员摘要和 `/kp` 或项目指定策略验证；不能套用本节，也不能用本地 EV Authenticode 批签替代 Microsoft Hardware/Partner Center 签名。

## 9. 安全续签与一次性重试

批次中断后不要重新签整个候选。续签脚本应：

1. 重新读取签前清单，确认总数和路径未变。
2. 验证已生成批次报告中的每个文件，其当前 SHA-256 与报告中的签名后 SHA-256 一致。
3. 对被 Catalog 签名遮盖的文件独立验证嵌入签名。
4. 从固定清单减去已完成文件，得到唯一的剩余集合。
5. 对剩余文件重新核对签前 SHA-256，防止中途被修改。
6. 只签剩余集合，然后对全部文件重新验签。

若中断发生在单个大批次内部且尚未生成批次报告，不能只用签前 SHA-256 判断剩余集合，因为已签文件的哈希已经改变。优先方案是从只读冻结副本恢复这个未完成批次，再按固定清单完整重签该批；冻结副本也必须在 `D:` 且有清单哈希。没有冻结副本时，逐文件使用嵌入证书、时间戳和 SignTool 验证重新分类：完全满足目标签名门槛的文件进入已完成集合，仍保持签前哈希且未签的文件进入待签集合，其他任何混合或多重签名状态立即停止人工审查。不得盲目重跑造成意外附加签名。

若 PIN 窗口消失且本批没有报告：

1. 确认本次 `signtool` PID、父 PowerShell PID、Session ID 和无窗口事实。
2. 保存状态、日志、窗口清单和时间戳为 `attempt-01-*` 证据。
3. 精确结束这两个已核实 PID；禁止按名称广泛终止进程。
4. 确认没有批次报告、没有并行签名进程，候选清单和哈希仍符合续签前置条件。
5. 在同一登录会话用同一固定入口重试一次。
6. 10 秒内确认新的 PIN 对话框真实可见并置前。

第二次仍无可见 PIN 对话框或认证失败时停止，不做第三次盲目重试。报告令牌中间件或桌面会话阻塞。

不同失败必须分流：PIN 取消或窗口消失只允许在同一活动会话重试一次，并避免触发令牌锁定；时间戳服务网络故障可按项目策略有限退避；证书不匹配、证书过期、会话身份变化、清单变化或输入哈希变化必须立即停止。每次重试使用新 `attemptId`，但引用同一冻结清单并保留上一尝试的证据。

终止挂起尝试时，先把状态标记为 `CANCELLING`，停止精确的 `signtool` 子 PID，等待父 PowerShell写出失败/取消报告；只有父进程在宽限期后仍未退出，才停止该精确父 PID。随后确认没有同 runId 的进程仍持有候选文件，再开始重试。禁止按进程名称批量结束。

## 10. 最终全量验签

所有批次完成后，重新从固定清单逐个验证，而不是简单汇总批次计数。每个文件执行：

```powershell
$signature = Get-AuthenticodeSignature -LiteralPath $path
$verifyOutput = & $signTool verify /pa /all /v /tw $path 2>&1
$verifyExit = $LASTEXITCODE
```

同时读取嵌入签名证书，避免 Catalog 优先导致签名者误判。最终 `all-pe-verify.json` 每一项至少包含：

```json
{
  "Path": "D:\\KEMI-Test\\app\\product-signed\\app.exe",
  "Status": "Valid",
  "WindowsSignatureType": "Authenticode",
  "WindowsSignerThumbprint": "...",
  "EmbeddedSignerThumbprint": "...",
  "TimestampPresent": true,
  "SignToolVerifyExitCode": 0,
  "Sha256": "...",
  "Valid": true
}
```

主程序再独立执行一次同样的验证并写入 `main-independent-verify.json`。

最终 `summary.json` 建议包含：

```json
{
  "Status": "PASS",
  "Bundle": "D:\\KEMI-Test\\app\\product-signed",
  "ExpectedThumbprint": "<CURRENT_THUMBPRINT>",
  "FileCount": 336,
  "ValidCount": 336,
  "EmbeddedSignerMatchCount": 336,
  "CatalogSignatureCount": 5,
  "BatchCount": 2,
  "MainIndependentVerify": true,
  "StartedAt": "...",
  "CompletedAt": "...",
  "SessionId": 1
}
```

这些字段是最低 schema，而不是可选建议。`Status=PASS` 对应进程退出码 0；`FAIL`、`CANCELLED`、报告缺失或 JSON 无法解析都对应非零退出和未完成。控制端还必须核对 `runId`、`attemptId`、脚本哈希和清单哈希属于本次运行。

数字只是示例，实际必须与本次固定清单一致。

内部 PE 与最终外壳使用两个独立运行记录：`innerRunId` 的清单和 summary 全部通过后才允许打包；打包完成后为唯一外壳创建 `outerRunId`、单文件 manifest、独立签名报告和 summary。外壳 summary 必须引用 `innerRunId` 和打包后外壳 SHA-256。

## 11. 结果报告

对用户或发布负责人报告：

- 仿真设备 ID、主机名、登录用户、已核实的主机密钥指纹和传输类型；
- 候选绝对路径、版本、文件总数和批次数；
- 本次证书指纹、签名算法和时间戳服务；
- 各批文件数与结果；
- 全量有效数、嵌入签名匹配数、Catalog 签名数；
- 主程序独立验签结果；
- 最终退出码、完成时间、报告目录；
- 发生过的重试及保存的证据；
- 尚未完成的安装、启动或发布验收。

Authenticode 全量通过只证明签名完整性，不自动证明程序可启动、安装包生命周期或应用功能验收通过。

## 12. 结束连接

得到最终成功或明确阻塞结果后，调用：

```bash
ruby /Users/<user>/.codex/skills/vibekits-remote-simulator/scripts/invoke.rb \
  vibekits.simulator.disconnect '{"routingId":"<DEVICE_ID>"}'
```

断开仿真连接不会终止已独立运行的 Windows 进程。若签名仍在运行且任务只是暂时结束连接，必须先记录当前 PID、Session ID、状态文件和下一次读取点。

## 已验证实例（仅作证据）

2026-09-18，VibeKits `1.9.0-dev.221+2221` 在 Windows 10 节点通过上述路线完成签名：336 个 PE 分两批，最终 336/336 有效，336 个嵌入签名均匹配 GlobalSign EV 证书，5 个微软 DLL 出现 Catalog 优先但嵌入签名和 SignTool `/all` 验证正常，主程序独立验签通过。

该实例中的设备 ID、路径、指纹、文件数和版本都是历史证据，不是下一次签名的默认配置。每次执行都必须重新核实当前设备身份、证书、候选和固定清单。
