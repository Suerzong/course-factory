# 第1章 覆盖审计表

本表用于审计第1章是否形成稳定闭环。AI 教学第1章时，应以 `learning-path/chapter-01.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch01-00` | 第1章 引言 | `knowledge/teaching-guides/chapter-01/01-00-introduction.teaching.md` | `¶0001-¶0011` | 深度学习是机器学习分支；有限样例到未知数据；CAP；ANN 解决 CAP 的定位；神经网络和深度学习不等价 | 第1章引言 | `ch01-01` |
| 2 | `ch01-01` | §1.1 人工智能 | `knowledge/teaching-guides/chapter-01/01-01-artificial-intelligence.teaching.md` | `¶0012-¶0022` | AI 直观定义；不能简单复制人脑；图灵测试；AI 主要能力与子领域；AI 作为计算机科学分支 | 人工智能 | `ch01-01-01` |
| 3 | `ch01-01-01` | §1.1.1 人工智能的发展历史 | `knowledge/teaching-guides/chapter-01/01-01-01-ai-history.teaching.md` | `¶0023-¶0032` | 推理期、知识期、学习期；AI Winter；推理期局限；专家系统；从数据中学习 | 人工智能的发展历史 | `ch01-01-02` |
| 4 | `ch01-01-02` | §1.1.2 人工智能的流派 | `knowledge/teaching-guides/chapter-01/01-01-02-ai-schools.teaching.md` | `¶0033-¶0039` | 流派产生原因；符号主义；连接主义；连接主义特性；深度学习与连接主义关系 | 人工智能的流派 | `ch01-02` |
| 5 | `ch01-02` | §1.2 机器学习 | `knowledge/teaching-guides/chapter-01/01-02-machine-learning.teaching.md` | `¶0040-¶0042` | 机器学习定义；ML 与 AI 关系；预测模型；特征形式；浅层学习 | 机器学习 | `ch01-03` |
| 6 | `ch01-03` | §1.3 表示学习 | `knowledge/teaching-guides/chapter-01/01-03-representation-learning.teaching.md` | `¶0043-¶0052` | 数据形式与特征构造；传统 ML 四步流程；特征处理重要性；表示学习定义；语义鸿沟；两个核心问题 | 表示学习 | `ch01-03-01` |
| 7 | `ch01-03-01` | §1.3.1 局部表示和分布式表示 | `knowledge/teaching-guides/chapter-01/01-03-01-local-vs-distributed-representation.teaching.md` | `¶0053-¶0068` | 好表示的三个优点；局部表示优缺点；分布式表示；嵌入 | 局部表示和分布式表示 | `ch01-03-02` |
| 8 | `ch01-03-02` | §1.3.2 表示学习 | `knowledge/teaching-guides/chapter-01/01-03-02-representation-learning-methods.teaching.md` | `¶0069-¶0072` | 多步非线性转换；深层结构作用；多层次特征表示；传统特征学习局限 | 表示学习方法 | `ch01-04` |
| 9 | `ch01-04` | §1.4 深度学习 | `knowledge/teaching-guides/chapter-01/01-04-deep-learning.teaching.md` | `¶0073-¶0079` | 深度含义；深度学习定义；避免人工特征工程；数据处理流程；CAP；神经网络和反向传播对 CAP 的作用定位 | 深度学习 | `ch01-04-01` |
| 10 | `ch01-04-01` | §1.4.1 端到端学习 | `knowledge/teaching-guides/chapter-01/01-04-01-end-to-end-learning.teaching.md` | `¶0080-¶0081` | 分模块任务；局部目标不一致；错误传播；端到端学习定义；输入-输出训练数据；端到端学习与 CAP | 端到端学习 | `ch01-05` |
| 11 | `ch01-05` | §1.5 神经网络 | `knowledge/teaching-guides/chapter-01/01-05-neural-networks.teaching.md` | `¶0082` | ANN 来源；机器学习中的神经网络定义；连接强度是可学习参数 | 神经网络 | `ch01-05-01` |
| 12 | `ch01-05-01` | §1.5.1 人脑神经网络 | `knowledge/teaching-guides/chapter-01/01-05-01-brain-neural-network.teaching.md` | `¶0083-¶0092` | 神经元基本单元；神经元结构；突触传递；兴奋/抑制与阈值；突触可塑性；赫布规则 | 人脑神经网络 | `ch01-05-02` |
| 13 | `ch01-05-02` | §1.5.2 人工神经网络 | `knowledge/teaching-guides/chapter-01/01-05-02-artificial-neural-network.teaching.md` | `¶0093-¶0095` | ANN 计算模型；节点和连接；权重；激活函数；学习问题；可学习函数/ML 模型；网络容量 | 人工神经网络 | `ch01-05-03` |
| 14 | `ch01-05-03` | §1.5.3 神经网络的发展历史 | `knowledge/teaching-guides/chapter-01/01-05-03-neural-network-history.teaching.md` | `¶0096-¶0114` | 五个发展阶段；两次低潮原因；反向传播复兴；预训练、算力和数据推动深度学习崛起 | 神经网络的发展历史 | `ch01-06` |
| 15 | `ch01-06` | §1.6 本书的知识体系 | `knowledge/teaching-guides/chapter-01/01-06-knowledge-system.teaching.md` | `¶0115-¶0123` | 三大知识块；机器学习章节安排；神经网络章节安排；概率图模型章节安排 | 本书的知识体系 | `ch01-07` |
| 16 | `ch01-07` | §1.7 常用的深度学习框架 | `knowledge/teaching-guides/chapter-01/01-07-deep-learning-frameworks.teaching.md` | `¶0124-¶0136` | 框架出现原因；自动梯度计算定位；CPU/GPU 切换定位 | 常用的深度学习框架 | `ch01-08` |
| 17 | `ch01-08` | §1.8 总结和深入阅读 | `knowledge/teaching-guides/chapter-01/01-08-summary-and-reading.teaching.md` | `¶0137-¶0147` | AI/ML 视角下理解深度学习；特征/表示的重要性；端到端结合；CAP 与神经网络；深度学习主要研究内容 | 总结和深入阅读 | `ch01-test` |
| 18 | `ch01-test` | 第1章章测 | 无新增讲义；覆盖第1章已通过单元 | 第1章已解锁段落 | 只从已达标单元的正式题范围抽取，工具列表、参考文献和了解即可内容不计入章测 | 第1章章测 | 第2章未解锁 |

## 当前审计结论

- 第1章 17 个教学单元均有教学指引和教材段落。
- `ch01-05-03` 覆盖神经网络发展历史，使用 `¶0096-¶0114`；其中 `¶0102` 是抽取粘连出的 ANN 定位句，不作为历史核心题。
- `ch01-06` 只使用 `¶0115-¶0123`，不使用 `¶0096-¶0114` 的神经网络历史内容。
- 第2-15章仍保持未解锁，待第1章章测通过后再建设详细路线。
