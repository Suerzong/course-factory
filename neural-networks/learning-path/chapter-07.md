# 第7章 网络优化与正则化 学习路线

本文件是第7章的教学调度表。AI 讲第7章时，应按表格顺序推进；每个单元先读知识点指引，再读教材原文。

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch07-00` | 第7章 引言 | `knowledge/teaching-guides/chapter-07/ch07-00-introduction.teaching.md` | `¶0001-¶0007` | 概念引入 | 未解锁 | `ch07-01` |
| 2 | `ch07-01` | §7.1+7.1.1+7.1.2 高维非凸优化 | `knowledge/teaching-guides/chapter-07/ch07-01-high-dim-nonconvex-optimization.teaching.md` | `¶0008-¶0023` | 核心概念（公式密集） | 未解锁 | `ch07-02` |
| 3 | `ch07-02` | §7.1.3 网络优化改善方法 | `knowledge/teaching-guides/chapter-07/ch07-02-optimization-improvement-methods.teaching.md` | `¶0024-¶0032` | 核心概念 | 未解锁 | `ch07-03` |
| 4 | `ch07-03` | §7.2+7.2.1 小批量梯度下降 | `knowledge/teaching-guides/chapter-07/ch07-03-mini-batch-gradient-descent.teaching.md` | `¶0033-¶0047` | 核心概念 | 未解锁 | `ch07-04` |
| 5 | `ch07-04` | §7.2.2 批量大小选择 | `knowledge/teaching-guides/chapter-07/ch07-04-batch-size-selection.teaching.md` | `¶0048-¶0058` | 核心概念 | 未解锁 | `ch07-05` |
| 6 | `ch07-05` | §7.2.3+§7.2.3.1 学习率衰减（上）—分段、逆时、指数衰减 | `knowledge/teaching-guides/chapter-07/ch07-05-learning-rate-decay-1.teaching.md` | `¶0059-¶0071` | 核心概念 | 未解锁 | `ch07-06` |
| 7 | `ch07-06` | §7.2.3.1（下）+§7.2.3.2 余弦衰减与学习率预热 | `knowledge/teaching-guides/chapter-07/ch07-06-cosine-decay-and-warmup.teaching.md` | `¶0072-¶0084` | 核心概念 | 未解锁 | `ch07-07` |
| 8 | `ch07-07` | §7.2.3.3 周期性学习率调整 | `knowledge/teaching-guides/chapter-07/ch07-07-cyclic-learning-rate.teaching.md` | `¶0085-¶0101` | 核心概念（公式密集） | 未解锁 | `ch07-08` |
| 9 | `ch07-08` | §7.2.3.4+7.2.3.5 AdaGrad与RMSprop | `knowledge/teaching-guides/chapter-07/ch07-08-adagrad-and-rmsprop.teaching.md` | `¶0102-¶0120` | 核心概念（公式密集） | 未解锁 | `ch07-09` |
| 10 | `ch07-09` | §7.2.3.6 AdaDelta | `knowledge/teaching-guides/chapter-07/ch07-09-adadelta.teaching.md` | `¶0121-¶0128` | 核心概念 | 未解锁 | `ch07-10` |
| 11 | `ch07-10` | §7.2.4 概述+§7.2.4.1 动量法 | `knowledge/teaching-guides/chapter-07/ch07-10-momentum.teaching.md` | `¶0129-¶0136` | 核心概念 | 未解锁 | `ch07-11` |
| 12 | `ch07-11` | §7.2.4.2 Nesterov加速梯度 | `knowledge/teaching-guides/chapter-07/ch07-11-nesterov-accelerated-gradient.teaching.md` | `¶0137-¶0148` | 核心概念 | 未解锁 | `ch07-12` |
| 13 | `ch07-12` | §7.2.4.3 Adam算法 | `knowledge/teaching-guides/chapter-07/ch07-12-adam.teaching.md` | `¶0149-¶0161` | 核心概念 | 未解锁 | `ch07-13` |
| 14 | `ch07-13` | §7.2.4.4 梯度截断 | `knowledge/teaching-guides/chapter-07/ch07-13-gradient-clipping.teaching.md` | `¶0162-¶0172` | 核心概念 | 未解锁 | `ch07-14` |
| 15 | `ch07-14` | §7.2.5 优化算法统一框架与小结 | `knowledge/teaching-guides/chapter-07/ch07-14-optimization-summary.teaching.md` | `¶0173-¶0183` | 核心概念 | 未解锁 | `ch07-15` |
| 16 | `ch07-15` | §7.3 概述+§7.3.1 固定方差初始化 | `knowledge/teaching-guides/chapter-07/ch07-15-fixed-variance-initialization.teaching.md` | `¶0184-¶0194` | 核心概念 | 未解锁 | `ch07-16` |
| 17 | `ch07-16` | §7.3.2 概述+方差缩放动机 | `knowledge/teaching-guides/chapter-07/ch07-16-variance-scaling-motivation.teaching.md` | `¶0195-¶0205` | 核心概念 | 未解锁 | `ch07-17` |
| 18 | `ch07-17` | §7.3.2.1 Xavier初始化（上）—前向推导 | `knowledge/teaching-guides/chapter-07/ch07-17-xavier-forward.teaching.md` | `¶0206-¶0217` | 核心概念 | 未解锁 | `ch07-18` |
| 19 | `ch07-18` | §7.3.2.1 Xavier（下）+§7.3.2.2 He初始化 | `knowledge/teaching-guides/chapter-07/ch07-18-xavier-backward-and-he.teaching.md` | `¶0218-¶0235` | 核心概念（公式密集） | 未解锁 | `ch07-19` |
| 20 | `ch07-19` | §7.3.3 正交初始化 | `knowledge/teaching-guides/chapter-07/ch07-19-orthogonal-initialization.teaching.md` | `¶0236-¶0247` | 核心概念 | 未解锁 | `ch07-20` |
| 21 | `ch07-20` | §7.4 数据预处理（上）—尺度不变性与归一化 | `knowledge/teaching-guides/chapter-07/ch07-20-data-preprocessing-1.teaching.md` | `¶0248-¶0257` | 核心概念 | 未解锁 | `ch07-21` |
| 22 | `ch07-21` | §7.4 数据预处理（下）—标准化与白化 | `knowledge/teaching-guides/chapter-07/ch07-21-data-preprocessing-2.teaching.md` | `¶0258-¶0267` | 核心概念 | 未解锁 | `ch07-22` |
| 23 | `ch07-22` | §7.5 逐层归一化概述 | `knowledge/teaching-guides/chapter-07/ch07-22-layer-wise-normalization-intro.teaching.md` | `¶0268-¶0275` | 核心概念 | 未解锁 | `ch07-23` |
| 24 | `ch07-23` | §7.5.1 BN（上）—标准归一化 | `knowledge/teaching-guides/chapter-07/ch07-23-batch-normalization-1.teaching.md` | `¶0276-¶0288` | 核心概念 | 未解锁 | `ch07-24` |
| 25 | `ch07-24` | §7.5.1 BN（下）—缩放平移与正则化效应 | `knowledge/teaching-guides/chapter-07/ch07-24-batch-normalization-2.teaching.md` | `¶0289-¶0298` | 核心概念 | 未解锁 | `ch07-25` |
| 26 | `ch07-25` | §7.5.2 层归一化 | `knowledge/teaching-guides/chapter-07/ch07-25-layer-normalization.teaching.md` | `¶0299-¶0316` | 核心概念（公式密集） | 未解锁 | `ch07-26` |
| 27 | `ch07-26` | §7.5.3+7.5.4 权重归一化与LRN | `knowledge/teaching-guides/chapter-07/ch07-26-weight-normalization-and-lrn.teaching.md` | `¶0317-¶0330` | 核心概念 | 未解锁 | `ch07-27` |
| 28 | `ch07-27` | §7.6+7.6.1+7.6.2 超参数优化—网格与随机搜索 | `knowledge/teaching-guides/chapter-07/ch07-27-hyperparameter-optimization-1.teaching.md` | `¶0331-¶0343` | 核心概念 | 未解锁 | `ch07-28` |
| 29 | `ch07-28` | §7.6.3+7.6.4+7.6.5 贝叶斯优化、动态资源与NAS | `knowledge/teaching-guides/chapter-07/ch07-28-bayesian-opt-and-nas.teaching.md` | `¶0344-¶0360` | 核心概念 | 未解锁 | `ch07-29` |
| 30 | `ch07-29` | §7.7 概述+§7.7.1 L1/L2正则化 | `knowledge/teaching-guides/chapter-07/ch07-29-l1-l2-regularization.teaching.md` | `¶0361-¶0374` | 核心概念 | 未解锁 | `ch07-30` |
| 31 | `ch07-30` | §7.7.1（续）+7.7.2+7.7.3 弹性网络、权重衰减、早停 | `knowledge/teaching-guides/chapter-07/ch07-30-elastic-net-weight-decay-early-stop.teaching.md` | `¶0375-¶0391` | 核心概念 | 未解锁 | `ch07-31` |
| 32 | `ch07-31` | §7.7.4+7.7.4.1 Dropout | `knowledge/teaching-guides/chapter-07/ch07-31-dropout.teaching.md` | `¶0392-¶0407` | 核心概念 | 未解锁 | `ch07-32` |
| 33 | `ch07-32` | §7.7.5+7.7.6 数据增强与标签平滑 | `knowledge/teaching-guides/chapter-07/ch07-32-data-augmentation-and-label-smoothing.teaching.md` | `¶0408-¶0422` | 核心概念 | 未解锁 | `ch07-33` |
| 34 | `ch07-33` | §7.8 总结和深入阅读 | `knowledge/teaching-guides/chapter-07/ch07-33-summary-and-reading.teaching.md` | `¶0423-¶0427` | 章节收束 | 未解锁 | `ch07-test` |
| 35 | `ch07-test` | 第7章章测 | 无新增讲义；覆盖第7章已通过单元 | 第7章已解锁段落 | 章测 | 未解锁 | `ch08-00` |

## 章末处理

- `ch07-test` 表示第7章章测，不对应教材新段落。
- 章测前必须完成第7章所有核心单元的覆盖检查。
- 章测通过后，才进入第8章详细路线建设或学习。

## 超15段单元说明

以下单元超过15段，原因已在coverage文件中注明：

- `ch07-01`（16段）: 鞍点概率论证+平坦最小值+改善方法四类，概念连续不宜拆分
- `ch07-07`（17段）: 三角波周期+SGDR重启，公式密集且概念闭环
- `ch07-08`（19段）: AdaGrad→RMSprop演化对比，公式密集且对比教学不宜拆分
- `ch07-18`（17段）: Xavier反向条件+He ReLU修正，公式密集且对比表7.2需同单元
- `ch07-25`（18段）: LN公式+RNN应用+BN对比，公式密集且RNN特化内容无法独立成单元
- `ch07-28`（17段）: 贝叶斯优化GP建模+动态资源+NAS概述，NAS仅3段为了解即可
- `ch07-30`（17段）: 弹性网络+权重衰减+早停，三个轻量正则方法概念连续
- `ch07-31`（16段）: Dropout训练/推理+集成解释+RNN变体，概念连续不宜拆
