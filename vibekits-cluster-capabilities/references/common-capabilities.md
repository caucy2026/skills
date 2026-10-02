# 通用设备基础能力

默认档案由程序从真实平台、工具注册目录、执行器、平台门禁、运行库/资源和权限生成，不需要本机模型Key。先描述App已实现的本机能力，再描述用户额外自述；不得把两者合并为已验证万能能力。

Windows/macOS/Android/iOS/Linux是OS，PAD是tablet形态；Android PAD与iPad能力不同。现有device-capability/1严格Schema不可擅加形态/工具字段；新增目录模块需独立版本合同，接入前不得猜字段。

fullCatalog表示定义，executableCatalog仍需平台门禁/真实环境/权限检查；capability_check的ready只证明接线范围。PAD可见完整Schema，但ADB/串口/Git/虚拟机及其他桌面专属工具可能返回requiresDesktopNode=true、executed=false，即使外层调用成功也未执行。Android的project.build只读返回PAD组件状态，不是桌面构建成功。

无本机Key可以在通道开启且获授权时直接调用确实可用的确定性工具：设备/资源查询、授权文件读写/比较、计算、HTTP/下载、数据库、音频等按实际目录核验。桌面ADB/串口/构建等还需平台及目标/环境条件。不能仅因OS存在就声称签名、上架或Word转PDF都可用。

区分本机自主规划与远端规划：无可用模型时不承诺自主理解复杂目标；有模型的管理agent可通过真实工具Schema规划，让无Key设备执行受限步骤并回传结果。外部CLI有自己的登录状态，本地免Key模型也可能可用，都需实际检测，不能只看App Key字段。

仿真直接工具调用沿既有授权渠道；只开集群的确定性执行需要新适配接线，未实现时报待接入。任何通道都不跳过本地scope、审批、容量或防重。
