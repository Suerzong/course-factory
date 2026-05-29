# 第8章 注意力机制与外部记忆 学习路线

本文件是第8章的教学调度表。AI 讲第8章时，应按表格顺序推进；每个单元先读知识点指引，再读教材原文。

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch08-00` | 第8章 引言 | `knowledge/teaching-guides/chapter-08/ch08-00-introduction.teaching.md` | `¶0001-¶0010` | 概念引入 | 未解锁 | `ch08-01` |
| 2 | `ch08-01` | §8.1 认知神经学中的注意力 | `knowledge/teaching-guides/chapter-08/ch08-01-cognitive-neuroscience-attention.teaching.md` | `¶0011-¶0018` | 核心概念 | 未解锁 | `ch08-02` |
| 3 | `ch08-02` | §8.2 注意力机制—注意力分布 | `knowledge/teaching-guides/chapter-08/ch08-02-attention-distribution.teaching.md` | `¶0019-¶0028` | 核心概念 | 未解锁 | `ch08-03` |
| 4 | `ch08-03` | §8.2（续）—打分函数 | `knowledge/teaching-guides/chapter-08/ch08-03-scoring-functions.teaching.md` | `¶0029-¶0040` | 核心概念 | 未解锁 | `ch08-04` |
| 5 | `ch08-04` | §8.2（续）—加权平均与软性注意力 | `knowledge/teaching-guides/chapter-08/ch08-04-weighted-average-soft-attention.teaching.md` | `¶0041-¶0047` | 核心概念 | 未解锁 | `ch08-05` |
| 6 | `ch08-05` | §8.2.1+8.2.1.1 变体概述与硬性注意力 | `knowledge/teaching-guides/chapter-08/ch08-05-variants-and-hard-attention.teaching.md` | `¶0048-¶0055` | 核心概念 | 未解锁 | `ch08-06` |
| 7 | `ch08-06` | §8.2.1.2+8.2.1.3+8.2.1.4 KV注意力、多头与结构化 | `knowledge/teaching-guides/chapter-08/ch08-06-kv-multihead-structured.teaching.md` | `¶0056-¶0065` | 核心概念 | 未解锁 | `ch08-07` |
| 8 | `ch08-07` | §8.2.1.5 指针网络 | `knowledge/teaching-guides/chapter-08/ch08-07-pointer-networks.teaching.md` | `¶0066-¶0078` | 核心概念 | 未解锁 | `ch08-08` |
| 9 | `ch08-08` | §8.3 自注意力模型（上）—QKV映射 | `knowledge/teaching-guides/chapter-08/ch08-08-self-attention-qkv.teaching.md` | `¶0079-¶0095` | 核心概念 | 未解锁 | `ch08-09` |
| 10 | `ch08-09` | §8.3 自注意力（下）—计算与位置编码 | `knowledge/teaching-guides/chapter-08/ch08-09-self-attention-computation-position.teaching.md` | `¶0096-¶0110` | 核心概念 | 未解锁 | `ch08-10` |
| 11 | `ch08-10` | §8.4 人脑中的记忆机制 | `knowledge/teaching-guides/chapter-08/ch08-10-human-memory.teaching.md` | `¶0111-¶0125` | 核心概念 | 未解锁 | `ch08-11` |
| 12 | `ch08-11` | §8.5 记忆增强神经网络概述 | `knowledge/teaching-guides/chapter-08/ch08-11-memory-augmented-nn.teaching.md` | `¶0126-¶0140` | 核心概念 | 未解锁 | `ch08-12` |
| 13 | `ch08-12` | §8.5.1 端到端记忆网络（MemN2N） | `knowledge/teaching-guides/chapter-08/ch08-12-end-to-end-memory-network.teaching.md` | `¶0141-¶0156` | 核心概念 | 未解锁 | `ch08-13` |
| 14 | `ch08-13` | §8.5.2 NTM（上）—架构 | `knowledge/teaching-guides/chapter-08/ch08-13-ntm-architecture.teaching.md` | `¶0157-¶0167` | 核心概念 | 未解锁 | `ch08-14` |
| 15 | `ch08-14` | §8.5.2 NTM（下）—读写操作 | `knowledge/teaching-guides/chapter-08/ch08-14-ntm-read-write.teaching.md` | `¶0168-¶0178` | 核心概念 | 未解锁 | `ch08-15` |
| 16 | `ch08-15` | §8.6+8.6.1 Hopfield（上）—结构与更新 | `knowledge/teaching-guides/chapter-08/ch08-15-hopfield-structure-update.teaching.md` | `¶0179-¶0197` | 核心概念（公式密集） | 未解锁 | `ch08-16` |
| 17 | `ch08-16` | §8.6.1 Hopfield（下）—能量函数与吸引点 | `knowledge/teaching-guides/chapter-08/ch08-16-hopfield-energy-attractors.teaching.md` | `¶0198-¶0208` | 核心概念 | 未解锁 | `ch08-17` |
| 18 | `ch08-17` | §8.6.1（续）+8.6.2+8.7 存储容量与章总结 | `knowledge/teaching-guides/chapter-08/ch08-17-storage-capacity-summary.teaching.md` | `¶0209-¶0219` | 章节收束 | 未解锁 | `ch08-test` |
| 19 | `ch08-test` | 第8章章测 | 无新增讲义；覆盖第8章已通过单元 | 第8章已解锁段落 | 章测 | 未解锁 | `ch09-00` |

## 章末处理

- `ch08-test` 表示第8章章测，不对应教材新段落。
- 章测前必须完成第8章所有核心单元的覆盖检查。
- 章测通过后，才进入第9章详细路线建设或学习。

## 特别说明

- 本章涉及自注意力（Self-Attention）、多头注意力（Multi-Head Attention）、位置编码（Positional Encoding）和Hopfield网络等内容，这些均是教材原文内容，属于正式教学范围。
- 教学范围限于教材原文，不扩展到教材未涉及的LLM、GPT/BERT、prompt engineering或Transformer工程框架。
- ch08-08（17段）公式/结构连续，拆分会破坏对自注意力QKV映射的完整理解。
- ch08-12（16段）MemN2N多跳记忆读取流程连续，不宜拆分。
- ch08-15（19段）Hopfield结构与更新规则公式密集，正式题只考结构与更新含义，不考完整推导。
- ch08-17合并§8.6.1后半(存储容量)、§8.6.2(联想记忆增加容量，仅1段)和§8.7(总结，4段)，因后两节各自段数过少不构成独立教学单元。
