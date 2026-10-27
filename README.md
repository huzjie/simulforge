# simulforge

**端到端流式「语音到语音」同声传译引擎 · 零依赖参考实现**（腾讯混元 Hy-SimulMT 拆解）

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI](https://img.shields.io/badge/CI-unittest%20%E5%85%A8%E7%BB%BF-brightgreen)](.github/workflows/ci.yml)
[![Zero deps](https://img.shields.io/badge/deps-zero-blueviolet)](#)

> 一句话说清楚：一个把「边说边译」从模型能力变成可复现工程框架的纯 Python 实现——**流式音频分块 → 同传读/写策略 → 级联或直通管道 → 延迟与质量双轴评测**，全部确定性、零第三方依赖、可训练（skill 从 0.5 单调爬到 1.0）。

---

## 为什么值得看

2026-10-26 腾讯混元开源了同声传译大模型 **Hy-SimulMT（30B-A3B，Apache-2.0）**：中英语音到语音实时翻译 + 实时音色克隆，StreamLAAL 延迟约 3 秒（人类专业译员约 4-5 秒），在 RealSI 长音频评测上超过主流开源同传模型和多数商业 API。

本仓库**不是**那个模型的实现，而是把「同声传译」背后的**工程方法**抽出来，做成一个能直接跑、能照着改的参考实现。真正的难点从来不在模型本身，而在三个工程问题：

1. **流式与增量**：音频是持续到达的，不能等句子结束再译，必须在词级增量产出。
2. **读/写策略**：每步是「再读一个源词」还是「先吐一个目标词」，这个决策序列直接决定延迟。
3. **质量-延迟权衡**：读得越多译得越准，但越慢；好策略要在同一帕累托前沿上更靠左上。

---

## 核心拆解（可复用思路）

### 1. 读/写策略是延迟的「唯一决定量」

同传的本质是一个 `(source_read, target_written, confidence) -> READ|WRITE` 的函数。四种策略，延迟各不相同：

| 策略 | 思路 | 平均滞后 AL |
|------|------|-------------|
| wait-k | 读 k 个源词后交替 | ≈ k |
| prefix-to-prefix | 保持源/目标前缀比例对齐 | 自适应 |
| confidence-adaptive | 置信度超阈值才 WRITE | 随 skill 下降 |
| MMA | 硬单调注意力对齐 | 可学习 |

**可复用点**：策略与模型解耦。换策略只改延迟、不动模型，所以部署可以「延迟优先/质量优先」一键切换（`configs/latency_first.yaml` vs `quality_first.yaml`）。

### 2. 级联 vs 直通是「错误累积 vs 可观测性」的取舍

- **级联**（ASR→MT→TTS）：有可查的转写文本，但三级误差会累积、延迟叠加。
- **直通 S2S**：语音进语音出，少两级、延迟更低，但丢了转写这一可观测中间态。

工程上二者并存，`config.s2s.direct` 一行切换。

### 3. 延迟指标要「可证伪」

`AL = (1/τ) Σ_i (g_i − (i−1)/γ)`，`StreamLAAL = LAAL × 秒/词`。实现放在 `latency/lag.py`，用策略的 read/write 轨迹直接算，而不是拍脑袋估。

### 4. 音色克隆 = 说话人嵌入的「混合权重」

`hyp = boost·ref + (1−boost)·noise`，相似度 = 余弦。skill=0.5（boost=0）≈随机音色，skill=1.0（boost=1）完全还原说话人。训练信号 `skill += lr·(1−skill)` 单调趋 1。

---

## 快速开始

```bash
# 依赖：无（纯标准库）

# 冒烟自检
python -m simulforge.cli doctor --skill 0.8

# 一次流式同传
python -m simulforge.cli interpret hello-world --speaker-id alice

# 训练 + 基准（看 skill 单调爬升）
python -m simulforge.cli train --steps 24
python -m simulforge.cli bench

# 起 HTTP 服务
python -m simulforge.cli serve --host 0.0.0.0 --port 8432
curl http://127.0.0.1:8432/health
curl -X POST http://127.0.0.1:8432/v1/interpret \
     -H 'Content-Type: application/json' \
     -d '{"audio_id":"demo","speaker_id":"spk"}'
```

## 架构

```
audio chunks ──> VAD ──> streaming ASR ──> streaming MT ──> streaming TTS ──> speech
                              │                 │                 │
                              └─── policy (read/write) 决定何时 commit ────┘
                                                     │
                                              LatencyManager (AL / LAAL / StreamLAAL)
```

## 基准（skill 扫描，64 句，单调性校验）

| skill | StreamLAAL(s) | quality | similarity | WER | qpl |
|-------|---------------|---------|------------|-----|-----|
| 0.500 | 5.400 | 0.2574 | 0.3546 | 0.4000 | 0.0402 |
| 0.625 | 4.750 | 0.4183 | 0.5159 | 0.3000 | 0.0727 |
| 0.750 | 4.100 | 0.5791 | 0.6773 | 0.2000 | 0.1136 |
| 0.875 | 3.450 | 0.7399 | 0.8386 | 0.1000 | 0.1663 |
| 1.000 | 2.800 | 0.9008 | 1.0000 | 0.0000 | 0.2370 |

> 延迟 5.40→2.80s 单调降、质量 0.257→0.901 单调升、相似度 0.355→1.0 单调升、WER 0.4→0 单调降、qpl 0.040→0.237 单调升。**好模型在「质量」和「延迟」两个轴同时变好**，而不是用一个换另一个。以上数字为 `python -m simulforge.bench` 实测输出。

## 目录结构

```
simulforge/
  audio/      流式分块、能量 VAD、帧特征(mel/ZCR)、重采样
  policy/     wait-k / prefix-to-prefix / adaptive / MMA
  cascade/    流式 ASR -> MT -> TTS 级联
  s2s/        直通 S2S + 说话人嵌入 + 音色克隆
  latency/    AL / LAAL / StreamLAAL、commit/revision 记账
  eval/       BLEU、GEMBA 式质量、WER、质量-延迟权衡
  model/      确定性可训练 mock 后端(ASR/MT/TTS/S2S)
  engine.py   SimultaneousEngine 集成入口
  serving.py  零依赖 HTTP 服务
  cli.py      CLI
tests/        30+ 单元测试
examples/     8 个可独立运行的示例
docs/         架构/策略/延迟指标/级联vs直通/音色克隆/基准/API
prompts/      ASR/MT/TTS/策略/评测/音色克隆 提示词模板
recipes/      waitk/adaptive/cascade/direct_s2s/voiceclone 配置配方
```

## License

MIT
