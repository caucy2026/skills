# 轻量验证验收器能拒绝故障

从项目根进入client/scripts后运行：

```sh
python3 -m unittest test_pad_surface_evidence test_remote_input_acceptance
```

这是28项既有检查器正负控制，毫秒级运行，不是产品全功能通过。检查器对旧帧/错peer、停帧、混会话、故障后恢复掩盖、少字/重复输入、错屏、外部输入、陈旧/被替换夹具等必须按用例拒绝或标明前置无效。

复用真实按钮XML正负夹具：Mac605 enabled/clickable=true的邻接扩展控件应被extension_control识别，Windows58 enabled/clickable=false应拒绝。该控件观察证明灰显被检测到，不证明灰显的源码原因，也不等同扩展实际出图。

仍需真实设备正例：新首帧、实际窗口/文本和真实释放；不可用纯单测替代。完整计数负例必须用证据副本，把连接100或按键100子步骤送到全功能评估器，结果应保持BLOCK。不要把静态schema校验通过说成技能已经实战全覆盖。
