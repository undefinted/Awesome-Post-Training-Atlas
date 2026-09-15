# Awesome Post-Training Atlas(后训练图谱)

> 一个结构化、持续更新的后训练研究图谱,覆盖语言、推理、智能体、
> 多模态模型、生成式模型与具身智能。

**[English](README.md)** · 简体中文

[![Paper Radar](https://github.com/undefinted/Awesome-Post-Training-Atlas/actions/workflows/paper-radar.yml/badge.svg)](https://github.com/undefinted/Awesome-Post-Training-Atlas/actions/workflows/paper-radar.yml)
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

## Paper Radar(论文雷达)

本仓库包含互补的发现与精选自动化代理:

1. 每日雷达(Daily Radar)以分页方式检索 31 个方向专属的 arXiv 查询,
   并叠加 Hugging Face Daily Papers 的热度与代码信号;
2. 方向-月份覆盖雷达(Direction-Month Coverage Radar)直接在 arXiv 上
   审计每一个“方向 × 月份”格子,记录精确的查询、扫描上限、计数与
   失败情况,然后在它的 pull request 中重建全部编年页面与网站;
3. 历史回填雷达(Backfill Radar)在声明的日期范围内遍历分页的
   arXiv 结果,并为每条分类查询持久化游标;
4. 候选名额按方向均衡分配,避免高产出的主题挤占多模态、智能体、
   生成式媒体或具身方向的名额;
5. 所有代理都会对精选、已拒绝与已排队记录去重,并保留学术查询与
   一手来源的出处信息;
6. 一个受控词表提取器会赋予可审计的标签,如 OPD、OPSD、
   counterfactual(反事实)、distillation(蒸馏)、RLVR、agent、VLM、
   VLA;网站支持多标签的 ANY/ALL 组合过滤,并可与年月筛选联用;
7. 可选的 LLM 负责判断范围、分类方向,并起草一句话要点;
8. 一个小红书关键词实时扫描器通过公开网页搜索(无需登录或 API key)
   发现笔记级别的技术讨论,并以 `source: xiaohongshu`、命中的关键词
   以及摘要中提到的 arXiv ID 记录在 `data/community_signals.yaml` 中;
   推广性质的转载会按社区来源策略被排除;
9. 每次运行都会开启一个可评审的 pull request,而不是悄悄修改精选
   列表。

无需 API key 即可运行。如需启用语义分诊,请在 GitHub Actions secret
中添加 `OPENAI_API_KEY`,`OPENAI_MODEL` 可选。

```bash
python -m pip install -r requirements.txt
python -m radar.main --days 7
python -m radar.xiaohongshu --dry-run   # 小红书关键词实时扫描,不写入任何内容
python -m radar.xiaohongshu             # 将新的笔记信号合并进 data/community_signals.yaml
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
