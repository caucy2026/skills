# Mac 仿真原位更新：2026-10-01 已验证方法

适用：已有授权、原仿真ID可连、待安装的是同Bundle/Team已签名公证完整App。项目实录：VibeKits docs/acceptance/MAC_DEV368_R14_FLEET_2026-10-01.md；固定脚本 tool/cluster_mac445_dev368_r14_handoff_20261001.sh 和 cluster_mac605_dev368_r14_handoff_20261001.sh。这些路径、PID、版本是本次现场，下一次必须核验并生成新版本脚本，不能直接重跑旧入口。

## 最短成熟步骤

1. 用仿真ID核对可信主机指纹，再实际SSH读运行进程完整路径及Info.plist整数build。Mac249实际在用户Caches，605在/Applications；不能只覆盖默认目录。
2. 固定精确签名ZIP hash/字节，复用已配置notary profile并记录提交ID。上传完成不等于Accepted；只查询同一ID，不因观察超时重新提交。Accepted后在独立副本staple、validate、deep strict验签与Gatekeeper。不得在控制端还承担通道时运行会自动退出同Bundle App的全套签名启动脚本。
3. 大包通过原ID上传。较慢时读实际目标文件大小和原SCP进程，增长则继续等待；本次Mac目标为/tmp/vibekits-simulator-ID，不是Windows的用户.vibekits-simulator。上传回执必须匹配完整SHA与字节。
4. 旧App保持运行，复制完整回滚副本并验签。暂存新App，核对Bundle ID、Team、designated requirement和entitlements相同（双方空entitlements是合法情况，不送空值到plutil）。目标Gatekeeper必须通过。
5. 固定独立LaunchAgent运行本次handoff：检查精确旧PID和版本，再正常TERM；只关闭该App路径下的辅助进程。原App移至held，再移入完整新App；替换、验签、open或新进程检查失败则把held恢复原路径并启动。不得依赖将被退出App的子进程继续安装。
6. 原ID重连后读真实日志、新进程路径/build，调用cluster.rooms，再核服务端新鲜心跳、名称与双方ID。connect缓存、上传回执、scheduled或目录名均不是运行版本证据。Harness需真实模型应答；缺Key应默认设备描述，不能拿VM/proxy状态代替模型健康。

## SSH255的真实处理

249暂存阶段回执255，但原ID立即仍能读文件；现场已有29357个文件、票据和Info.plist，deep签名通过，原ditto/spctl进程已无。只续做票据hash、Gatekeeper与暂存移动，未重解压。更新期间连接关闭时先查独立任务日志/进程和文件，不重复安装；未知结果保留回滚与原实例，不能当失败重做。

## 没有Xcode时

不要为了stapler安装开发工具。xcrun查询本身可能触发系统安装提示，应在需要前核实际环境。此次249采用同一Accepted包在控制端staple后的原始苹果票据：对比两个ZIP证明全部原条目CRC/字节不变、无删除，仅新增Contents/CodeResources及其资源元数据；票据小包逐字节核对与已validate副本一致，通过ID传输并hash验证，再只在独立暂存App合入。之后目标deep验签和Gatekeeper显示Notarized Developer ID。这不是自行生成或伪造票据；不能对不同签名/不同hash包套票据。通常直接传完整已装订最终ZIP更简单；只有已经在传相同原包且差异已精确核验时使用小包。

## 本次证据边界

249/605实际原路径运行build2368、原ID通信、房间approved、新鲜心跳通过；249模型真实应答通过。605模型MISSING_CREDENTIAL在旧历史也存在，其默认描述符合无Key分支，不能称模型就绪。长时间稳定、完整集群办公更新、六台全部最新仍未完成。办公五台当前与商城同版，不能降级制造升级或把未发生安装描述成更新成功。
