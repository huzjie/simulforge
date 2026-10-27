# FAQ

**Q: 为什么是「零依赖」？**
A: 为了能在任何 Python 3.8+ 环境（含受限/离线运行时）直接跑，不装 numpy/torch。

**Q: skill 是什么？**
A: 一个 [0.5, 1.0] 的可训练标量。0.5 = 未训练（≈随机），1.0 = 完美。训练规则
`skill += lr * (1 - skill)` 单调爬升，所以所有指标都单调朝最优走。

**Q: 这些数字是真的吗？**
A: 是确定性 mock 后端 + 单点 oracle 的可复现输出，跑 `python -m simulforge.bench`
即可复现。声明规模（30B-A3B、~3s）是「设计目标」，参考实现用小张量在毫秒级跑通。

**Q: 能接真实模型吗？**
A: `model/` 是抽象接口（transcribe / translate / synthesize），把 mock 换成真实
ASR/MT/TTS 即可，策略层、延迟层、评测层无需改动。
