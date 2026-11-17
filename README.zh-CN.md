# Awesome Post-Training Atlas(后训练图谱)

> 一个结构化、持续更新的后训练研究图谱,覆盖语言、推理、智能体、
> 多模态模型、生成式模型与具身智能。

**[English](README.md)** · 简体中文

[![Codex Radar: 每日 08:00 CT](https://img.shields.io/badge/Codex_Radar-%E6%AF%8F%E6%97%A5_08%3A00_CT-10a37f)](CODEX_RADAR.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🔎 **[打开可搜索的研究网站](https://undefinted.github.io/Awesome-Post-Training-Atlas/)**(网站右上角可切换 EN / 中文)· [浏览受控标签目录](LABELS.md)

> 本文件是 [README.md](README.md) 的中文译文,英文版为准。下文表格中的
> 论文数量与日期由自动化流水线生成,以英文版实时数据为准。

大多数论文列表回答的是“发表了什么”。本图谱试图回答三个更有用的问题:

1. 这项工作改变了后训练流水线的哪个环节?
2. 它使用了什么样的反馈、数据与优化机制?
3. 它与之前和之后的方法之间是什么关系?

主索引按 **方向 → 年份 → 月份 → 论文** 组织。每个月内,论文按发表日期
排序。精选条目来自 [`data/papers.yaml`](data/papers.yaml);直接来自学术搜索
的结果来自 [`data/candidates.yaml`](data/candidates.yaml),在各方向页面上
以醒目的 🔎 `discovery candidate`(发现候选)标记展示,直到其原始论文
经过人工审核。

## 范围

我们对“后训练”(post-training)采取宽泛但审慎的定义:通过额外的学习
或反馈回路,对预训练基础模型进行适配、对齐、专精、改进或评估的方法。
范围涵盖语言模型、VLM/MLLM、智能体、扩散与视频模型,以及具身/VLA
系统。

收录标准与边界案例见 [TAXONOMY.md](TAXONOMY.md)。自动生成的
[覆盖矩阵](COVERAGE.md) 会把稀疏的月份与方向直接暴露出来,而不是
用庞大的论文总数掩盖空白。[发现覆盖报告](DISCOVERY_COVERAGE.md)
则单独记录学术搜索的时间窗口、查询次数与未解决的积压。

精选层还带有一个可选的方法演进视图:方法家族、有据可查的前序工作、
变化轴(change axes)以及明确的可迁移思路(idea surfaces)。网站会把这些
标注与大得多的发现池分开可视化,避免临时性记录看起来像已确认的
方法谱系。

## 研究方向

每个方向都有独立的编年页面。数量包含精选论文与带醒目标记的学术
发现候选。

| 方向 | 精选 | 发现候选 | 总数 |
|---|---:|---:|---:|
| [监督适配与数据](directions/supervised-adaptation.md) | — | — | 见英文版 |
| [偏好优化与对齐](directions/preference-alignment.md) | — | — | 见英文版 |
| [奖励模型与验证器](directions/reward-verifiers.md) | — | — | 见英文版 |
| [强化学习与可验证奖励(RLVR)](directions/reinforcement-learning.md) | — | — | 见英文版 |
| [蒸馏与策略迁移](directions/distillation.md) | — | — | 见英文版 |
| [推理与自我改进](directions/reasoning-self-improvement.md) | — | — | 见英文版 |
| [智能体与交互式后训练](directions/agentic.md) | — | — | 见英文版 |
| [多模态 / VLM / MLLM 后训练](directions/multimodal.md) | — | — | 见英文版 |
| [生成式媒体后训练](directions/generative-media.md) | — | — | 见英文版 |
| [具身智能与 VLA 后训练](directions/embodied-vla.md) | — | — | 见英文版 |

各方向的最新论文数量与日期请见 [README.md](README.md) 中的实时表格,
或直接在[研究网站](https://undefinted.github.io/Awesome-Post-Training-Atlas/)上
按方向浏览。

## Codex 论文雷达

论文发现已经迁移到 **Codex 维护的雷达**，不再由 GitHub Actions 定时触发。
维护者本机的 Codex 任务设为每天 **08:00（America/Chicago）** 运行；运行时
需要电脑处于开机登录状态，并且 GitHub CLI 授权有效。

当前工作方式如下：

1. 每日轻量扫描检索近期 arXiv 后训练论文的一手元数据，并记录可追溯候选；
2. 按 arXiv ID、DOI 和规范化标题去重，再映射到本图谱的研究方向；
3. 晋升前核验论文链接、日期、作者、会议/期刊信息和代码仓库；
4. 边界不明确的结果继续保留为醒目标记的发现候选，不会自动进入精选层；
5. 深度评审通过后才写入 `data/papers.yaml`，并维持
   **方向 → 年份 → 月份 → 论文** 的层级；
6. GitHub Actions 仅保留为手动验证、渲染与部署的备用入口，不再负责
   定时检索论文。

最近一次有记录的运行是
[2026-11-16 Codex 雷达报告](data/codex-radar/2026-11-16.md)。完整频率、
审核规则与安全约束见 [CODEX_RADAR.md](CODEX_RADAR.md)。

手动运行仓库流水线：

```bash
python -m pip install -r requirements.txt
python -m radar.main --days 7
python -m radar.backfill --max-new 180
python -m radar.labels
python -m radar.render --check
python -m radar.coverage --check
python -m unittest discover -s tests
```

来源分级、新鲜度目标以及中外社区信号的策略见 [SOURCES.md](SOURCES.md)。

## 贡献

请使用论文提议 issue 模板,或直接编辑 `data/papers.yaml`。好的条目
会说明这篇论文为什么属于后训练,而不仅仅是它用了基础模型。自动化
候选只是提议,不代表背书。

## 致谢

本项目受到研究社区众多优秀论文列表的启发。它的独特关注点在于:
跨模态的分类体系、每个方向内部的编年阅读路径,以及经人工评审的
发现流水线。
