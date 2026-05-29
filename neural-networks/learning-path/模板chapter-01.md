# 第1章 绪论 学习路线

<!--
  范例文件：展示 learning-path/chapter-XX.md 的标准格式。
  生成新章节时，替换所有内容，保留本注释块作为格式参考。
  
  格式规则：
  1. 标题格式：# 第X章 {章标题} 学习路线
  2. 说明段：必须说明本文件是第X章的教学调度表
  3. 表格固定 8 列，列名和顺序不可更改
  4. 单元ID 命名规则：ch{章号}-{节号}[-{子节号}[-{子子节号}]]，章测用 chXX-test
  5. 知识点指引 路径规则：knowledge/teaching-guides/chapter-XX/{单元ID对应文件名}.teaching.md
  6. 教材段落 使用 ¶XXXX 格式，引用 textbook/index.md 中的段落号
  7. 类型 只允许：概念引入 / 核心概念 / 关键概念 / 方法定位 / 历史脉络 / 背景支撑 / 全书地图 / 工具概览 / 章节收束 / 章测
  8. 默认状态 只允许：未开始 / 未解锁 / 待重校准
  9. 最后一行必须是 chXX-test（章测），下一单元指向下一章的 chYY-00
  10. 章末处理 段必须说明章测的覆盖范围和解锁条件
-->

本文件是第1章的教学调度表。AI 讲第1章时，应按表格顺序推进；每个单元先读知识点指引，再读教材原文。

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch01-00` | 第1章 引言 | `knowledge/teaching-guides/chapter-01/01-00-introduction.teaching.md` | `¶0001-¶0011` | 概念引入 | 待重校准 | `ch01-01` |
| 2 | `ch01-01` | §1.1 人工智能 | `knowledge/teaching-guides/chapter-01/01-01-artificial-intelligence.teaching.md` | `¶0012-¶0022` | 核心概念 | 未开始 | `ch01-01-01` |
| 3 | `ch01-01-01` | §1.1.1 人工智能的发展历史 | `knowledge/teaching-guides/chapter-01/01-01-01-ai-history.teaching.md` | `¶0023-¶0032` | 历史脉络 | 未开始 | `ch01-01-02` |
| 4 | `ch01-01-02` | §1.1.2 人工智能的流派 | `knowledge/teaching-guides/chapter-01/01-01-02-ai-schools.teaching.md` | `¶0033-¶0039` | 概念对比 | 未开始 | `ch01-02` |
| 5 | `ch01-02` | §1.2 机器学习 | `knowledge/teaching-guides/chapter-01/01-02-machine-learning.teaching.md` | `¶0040-¶0042` | 核心概念 | 未开始 | `ch01-03` |
| 6 | `ch01-03` | §1.3 表示学习 | `knowledge/teaching-guides/chapter-01/01-03-representation-learning.teaching.md` | `¶0043-¶0052` | 核心概念 | 未开始 | `ch01-03-01` |
| 7 | `ch01-03-01` | §1.3.1 局部表示和分布式表示 | `knowledge/teaching-guides/chapter-01/01-03-01-local-vs-distributed-representation.teaching.md` | `¶0053-¶0068` | 关键概念 | 未开始 | `ch01-03-02` |
| 8 | `ch01-03-02` | §1.3.2 表示学习 | `knowledge/teaching-guides/chapter-01/01-03-02-representation-learning-methods.teaching.md` | `¶0069-¶0072` | 方法定位 | 未开始 | `ch01-04` |
| 9 | `ch01-04` | §1.4 深度学习 | `knowledge/teaching-guides/chapter-01/01-04-deep-learning.teaching.md` | `¶0073-¶0079` | 核心概念 | 未开始 | `ch01-04-01` |
| 10 | `ch01-04-01` | §1.4.1 端到端学习 | `knowledge/teaching-guides/chapter-01/01-04-01-end-to-end-learning.teaching.md` | `¶0080-¶0081` | 关键概念 | 未开始 | `ch01-05` |
| 11 | `ch01-05` | §1.5 神经网络 | `knowledge/teaching-guides/chapter-01/01-05-neural-networks.teaching.md` | `¶0082` | 核心概念 | 未开始 | `ch01-05-01` |
| 12 | `ch01-05-01` | §1.5.1 人脑神经网络 | `knowledge/teaching-guides/chapter-01/01-05-01-brain-neural-network.teaching.md` | `¶0083-¶0092` | 背景支撑 | 未开始 | `ch01-05-02` |
| 13 | `ch01-05-02` | §1.5.2 人工神经网络 | `knowledge/teaching-guides/chapter-01/01-05-02-artificial-neural-network.teaching.md` | `¶0093-¶0095` | 核心概念 | 未开始 | `ch01-05-03` |
| 14 | `ch01-05-03` | §1.5.3 神经网络的发展历史 | `knowledge/teaching-guides/chapter-01/01-05-03-neural-network-history.teaching.md` | `¶0096-¶0114` | 历史脉络 | 未开始 | `ch01-06` |
| 15 | `ch01-06` | §1.6 本书的知识体系 | `knowledge/teaching-guides/chapter-01/01-06-knowledge-system.teaching.md` | `¶0115-¶0123` | 全书地图 | 未开始 | `ch01-07` |
| 16 | `ch01-07` | §1.7 常用的深度学习框架 | `knowledge/teaching-guides/chapter-01/01-07-deep-learning-frameworks.teaching.md` | `¶0124-¶0136` | 工具概览 | 未开始 | `ch01-08` |
| 17 | `ch01-08` | §1.8 总结和深入阅读 | `knowledge/teaching-guides/chapter-01/01-08-summary-and-reading.teaching.md` | `¶0137-¶0147` | 章节收束 | 未开始 | `ch01-test` |
| 18 | `ch01-test` | 第1章章测 | 无新增讲义；覆盖第1章已通过单元 | 第1章已解锁段落 | 章测 | 未开始 | `ch02-00` |

## 章末处理

<!--
  章末处理规则（所有章节通用）：
  1. 最后一行必须是 chXX-test
  2. 章测不对应教材新段落，知识点指引写"无新增讲义"
  3. 章测前必须完成本章所有核心单元
  4. 章测通过后才进入下一章
-->

- `ch01-test` 表示第1章章测，不对应教材新段落。
- 章测前必须完成第1章所有核心单元的覆盖检查。
- 章测通过后，才进入第2章详细路线建设或学习。
