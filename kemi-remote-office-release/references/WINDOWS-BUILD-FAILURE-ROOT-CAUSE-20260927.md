# Windows 编译机时好时坏：根因及处置（2026-09-27）

对象：仿真6192992780，xzl，既有C:/kemi/build工具链。仅记录真实事件，不把所有失败归结为同一个原因。

## 已证实的三类问题

| 阶段 | 证据 | 原因 | 处理 |
|---|---|---|---|
| 编译过程中执行生成程序 | CodeIntegrity 3077指向310的softbuffer build-script、315的syn/thiserror build-script及futures_macro/async_recursion DLL、360的libc/typenum build-script | Windows应用控制拒绝执行/加载这些编译期产物；不是Rust语法错误 | 记录精确文件、哈希、时间、策略ID和编译错误；交管理员按组织认可流程处置，或使用已批准的编译环境。禁止关闭保护、改路径规避、循环盲试 |
| 源码不完整 | cargo-build-367-first-missing-module.log：E0583，office_identity模块不存在，EXIT=101 | 源码同步漏文件，与签名无关 | 编译前核验主仓库、子模块及本地新增文件清单。补齐对应源码，不能签名解决，也不能从旧二进制凑包 |
| 编译成功后运行 | +369 Cargo Finished/EXIT=0，Flutter完整产物版本1.4.127+369；启动后3077指向window_size_plugin.dll、desktop_multi_window_plugin.dll；两DLL未签名 | 产品运行时插件被系统应用控制拦截 | 完整内层PE签名并验签后再启动；只签主EXE不能覆盖DLL。外层包在打包后另签 |

这些事件中策略ID相同：0283ac0f-fff1-49ae-ada1-8a933130cad6。当前只读查询VerifiedAndReputablePolicyState=1；事件直接证明应用控制在执行，不需要猜测是哪位同事阻拦。没有证据证明有人临时修改过系统策略。

## 为什么有时能编译

Cargo构建不仅编译业务源码，还需要运行依赖的build-script和加载proc-macro DLL。增量构建和重新构建所执行的文件集合并不相同。+367及+369成功时复用了既有工作目录/缓存；+369核心耗时3分35秒，明确EXIT=0。

因此“这次业务核心编译成功”不代表所有未来新生成的编译工具都能通过策略，也不代表生成的产品DLL能运行。**具体某个相同文件为什么后来被允许，现有证据不足**：没有保存每次拦截与成功时同文件哈希及判定变化，不能编造云信誉变化、自动放行或固定等待时间。缓存复用是成功路径的重要差异，但不是系统策略永久修复的证明。

## 后续固定检查顺序

1. 复用已有工具链和缓存；先确认没有同目录构建正在运行，保存源码/子模块/新增文件清单与哈希。
2. 遇到失败先分层：E0583/缺文件查源清单；4551/拒绝执行查同时间CodeIntegrity 3033/3077及精确路径；启动无窗口查运行时DLL事件。
3. 策略失败保留编译日志、事件、被阻文件哈希/签名、父进程路径；不得仅重试或重装环境。管理员处置后核验原文件确实可执行，再做一次有界原路线重试。
4. 成功须同时有构建日志EXIT=0、当前版本和新产物哈希；计划任务Ready或进程退出不足以证明成功。
5. 包内librustdesk.dll必须与本轮target/release一致，完整Flutter AOT及插件来自本轮完整构建。
6. 本机已实证会阻止未签名产品插件，进入它的运行验收前先完成内层签名；需要用户在58硬件令牌输入PIN时再通知，绝不要求把PIN发到聊天。
7. 真机启动、扩展、键盘、切换和性能测试独立执行，签名通过不能替代功能通过。

## 原始证据

- evidence/windows-build-policy-history.txt
- evidence/windows-build-policy-correlation.txt
- evidence/windows369-build-artifacts.json
- evidence/windows369-xzl-codeintegrity.json

当前结论：+369核心与Flutter构建通过，但虚拟屏组件构建未通过，完整Windows包尚未完成；五机100轮未通过，未发布。

## +369 当场复现：同机核心成功，虚拟屏组件失败

在同一工作目录、同一Rust1.75/VS/vcpkg环境，核心刚完成EXIT=0。随后构建dylib_virtual_display时，libsodium-sys新生成的build-script-build未执行即报4551；thiserror_impl-7333b05bede38997.dll加载失败并引发E0463。同期CodeIntegrity3077明确指向该宏DLL，仍是上述相同策略ID。完整证据：evidence/windows369-virtual-build-policy-failure.txt。

这直接证明不同构建目标/依赖组合触发不同编译期可执行文件检查，不能把“核心通过”当作整个工具链已永久放行。当前虚拟屏组件构建未通过，不能启动完整产品签名。需要管理员按照既有安全策略对开发用途作正式处置，或提供组织批准的构建环境；不得以换路径、改策略、旧DLL替代或不停重试规避本次明确拦截。最终产品代码签名与开发期依赖程序的运行许可不是同一个步骤。

## +353成功路线与+369的逐项比对

- +353与+369虚拟屏构建均使用 `cargo build --locked -p dylib_virtual_display --release`，不能归因于本次换了构建命令。
- Cargo.lock、虚拟屏Cargo.toml及hbb_common Cargo.toml归一化CRLF/LF后内容相同，现有对比不支持依赖升级这一解释。
- 两轮的thiserror_impl宏DLL和libsodium构建辅助EXE均为NotSigned；对应文件名后缀相同，但SHA-256不同。不能声称旧版编译期依赖签过名。
- 已证实的是新文件被执行/加载策略拒绝，尚未证实为何旧文件当时获准；不把编译源码、编译期间执行辅助程序、运行最终APP混为一谈。
- 比对证据：evidence/kemi369-vs353-build-executable-signatures.json、evidence/kemi369-vs353-normalized-diff.txt、evidence/kemi-virtual-build-command-comparison.json。

## 驱动包差异核验及候选补齐

原厂x64 usbmmIdd.dll为71616字节、微软签名；旧353为62464字节、企业签名。两者SignTool verify /kp /v /c usbmmidd.cat均EXIT=0，目录校验内容SHA1同为70B4B29B4C45CA5E83A2E7C55C1675A5DDBDDAB4。因此文件大小/SHA256差异不能直接认定为驱动代码版本变化，也不能声称旧包目录签名失效。此次保留原厂已验证签名，五个驱动资源已补入369独立候选目录并逐文件校验；未安装驱动、未覆盖运行程序。证据见evidence/kemi369-driver-*。自研dylib_virtual_display.dll仍未构建成功，候选包尚不完整，不能签名发布。

## 拦截策略已由事件XML定位

3077事件1417/1412明确给出PolicyName=VerifiedAndReputableDesktop，PolicyGUID={0283ac0f-fff1-49ae-ada1-8a933130cad6}，Requested Signing Level=2，Validated Signing Level=1，Status=0xc0e90002；被拦文件Flat SHA256与本轮宏DLL实际哈希一致。不是Codex审批拒绝，也不是源码语法失败。CiTool -lp -json只读查询返回0x80070005（访问拒绝），未修改策略。事件证据见evidence/windows369-active-ci-policy.txt；仍未证明旧353为何获准执行。

## 2026-09-27：编译期辅助文件被拦截与签名处理

### 已验证事实

- +369 Rust主库、Flutter Release已成功；单独虚拟屏组件失败。不能把局部失败报告成“Windows不允许编译”。
- `rustc.exe`加载`thiserror_impl-7333b05bede38997.dll`触发CodeIntegrity 3077；XML策略名称为`VerifiedAndReputableDesktop`，GUID为`{0283ac0f-fff1-49ae-ada1-8a933130cad6}`，要求签名级别2、实际1，状态`0xc0e90002`。`libsodium-sys`构建辅助EXE执行前报4551。
- 成功+353与本次使用相同`cargo build --locked -p dylib_virtual_display --release`；相关Cargo配置归一化换行后相同。旧新辅助文件均NotSigned，但SHA256不同。尚无证据解释旧文件为何被允许，不能编造“旧包签过名”或“等几分钟必然恢复”。
- 运行最终APP时插件DLL被拦截是另一阶段；源码同步漏`office_identity.rs`引起E0583又是另一问题，分别处理。

### 用户已授权签署编译辅助文件时的处理路线（2026-09-27 16:31已实测闭环）

1. 保存首个Cargo失败日志及同时间3077事件XML。列出精确的被拦DLL/EXE、来源依赖、大小、SHA256、签名状态及原目录。不得扩大为签整个未知target目录。
2. 确认原构建已终止，冻结这批文件并保留原件。使用独立版本化签名副本和显式清单；不能签正在被编译器重写的文件。
3. 复用本技能A→B受限挂载与`kemi-windows-remote-signing`交互流程：仿真app_control→固定GUI启动器→固定CMD→固定PowerShell→既有Invoke-KemiAuthenticode。重新核验当前证书、活动用户会话，PIN只由用户在令牌窗口输入。不要从SSH直接启动签名。
4. 签后逐文件验证指定证书、时间戳、SignTool结果并记录新SHA256；A端回读一致。回填原构建路径前确认原文件仍为冻结哈希，保留备份。只改变签名，不调整系统保护策略、工具链或业务源码。
5. 沿原命令执行一次有界重试，保存Cargo退出码、新事件与新产物哈希。签名成功不保证系统策略允许；仍被拒绝则按精确新证据处理，不无限重复签名/重试。Cargo若重生成该文件，旧签名结果不再适用。
6. 只有“签名验签通过→原路径原命令构建成功→新虚拟屏DLL身份核验”完整证据齐全，才能把此路线升级为已验证解决方法。编译辅助文件签名报告不能冒充最终APP内层/外层签名报告。

### 打包差异与防误判

+353驱动DLL62464字节、企业签名；原厂下载71616字节、微软签名。两者`signtool verify /kp /v /c usbmmidd.cat x64/usbmmIdd.dll`均通过且目录成员内容哈希一致。不能只凭文件大小或文件SHA256判断驱动升级或目录签名失效。保留原厂已验证签名与匹配CAT/INF，不把第三方驱动当成自研PE盲目重签。

本案例详细记录位于RustDesk项目`kemi-docs/WINDOWS-BUILD-FAILURE-ROOT-CAUSE-20260927.md`及其`evidence/`。截至本段记录，构建辅助文件签名尚未执行，虚拟屏组件未构建完成，不能宣称修复或发布通过。

## 2026-09-27 16:31：辅助签名后原命令构建成功

上述未完成描述为早期现场记录。当前两个辅助文件已通过58活动会话固定入口签名；02报告2/2有效、嵌入证书一致、时间戳及SignTool全部通过。证据见 `evidence/windows369-helper-signing-20260927/`。A回读一致并按冻结原哈希备份后回填原target目录；原任务、原路径、原命令一次复验成功：`Finished release [optimized] target(s) in 1m 41s`、`EXIT=0`。没有修改应用控制策略、工具链或业务源码。

新 `dylib_virtual_display.dll` 309248字节，SHA256 `6564920CF864BA84E26926B111F9BC680E6882FFF2AC4EA4FEFE5E977F5C3CE9`，生成时间晚于本轮构建开始，已加入+369独立候选。候选97文件、16 PE，清单已归档。最终产品尚未签名、功能验收尚未通过，不等同正式发布。

签名入口另有已知环境坑：仿真启动器继承的PSModulePath可能缺WindowsPowerShell模块，导致Get-FileHash不存在。须沿用+353 outer04固定CMD的进程级PSModulePath，再启动PowerShell；不能将此问题解释为证书失败或修改全局执行策略。本轮01在签名前终止，02复用该成熟设置后成功。

## xzl 原生安装退出0但未安装：错误报告链（只读核验）

369已签候选原生`--silent-install` stdout明确`Failed with error: install failed`，进程退出0、无正式目录，不能算安装成功。18:43身份核验仍是AppData353旧PID8120/23764。

源码证据：

1. 锁定的runas1.2.0 Windows实现`ShellExecuteExW`失败或无进程句柄时返回`0xFFFFFFFF`，但`runas_impl`仍包装为`Ok(ExitStatus)`。A缓存文件与本机分析文件SHA256相同：`53D4FBDCC78D84D2C6C371FF855C79E21A886548B73182A123CFA0866E9DA1E2`。
2. 产品`src/platform/windows.rs::run_cmds`使用`let _ = res?`，忽略ExitStatus是否成功，再凭undone标记给出泛化`install failed`。因此这一字符串**不能证明提权后的cmd或批处理实际执行过**。此前报告中“命令返回即证明已执行”的推断撤回。
3. `src/core_main.rs`安装错误打印后仍返回None，没有将失败映射为非零进程退出，故计划任务显示0也不能证明安装成功。
4. 旧两个产品PID完全未变化，原始bat最早段即taskkill旧产品，说明没有证据表明安装越过最早阶段；不能归因后面的XCOPY/虚拟屏DLL。

未取得的证据：没有原ShellExecuteEx的GetLastError、没有cmd退出码。现有Security4688/4689精确时间窗（17:56:40–18:07）无匹配事件；UAC Operational只有更早历史的两条ERROR_ELEVATION_REQUIRED，不能用于解释本次。当前无live consent.exe。内部日志包装只准备未执行，因此内部log/exit不存在。

结论：**已确定错误被双层掩盖，尚不能断言是UAC取消、超时还是提权执行失败。** 保留已签产物不改源码，不重复无日志安装、不调整UAC/WDAC策略。下一次需现场正常确认一次并采集原bat内部命令输出/提权返回码，才能定位实际失败点。此部分是诊断记录，非修复完成。
