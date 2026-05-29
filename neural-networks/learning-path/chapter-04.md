# 第4章 前馈神经网络 学习路线

本文件是第4章的教学调度表。AI 讲第4章时，应按表格顺序推进；每个单元先读知识点指引，再读教材原文。

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch04-00` | 第4章 引言 | `knowledge/teaching-guides/chapter-04/04-00-introduction.teaching.md` | `¶0001-¶0007` | 概念引入 | 未解锁 | `ch04-01` |
| 2 | `ch04-01` | §4.1 神经元 | `knowledge/teaching-guides/chapter-04/04-01-neuron.teaching.md` | `¶0008-¶0024` | 核心概念 | 未解锁 | `ch04-02` |
| 3 | `ch04-02` | §4.1.1 Sigmoid型函数 | `knowledge/teaching-guides/chapter-04/04-02-sigmoid-functions.teaching.md` | `¶0025-¶0037` | 核心概念 | 未解锁 | `ch04-03` |
| 4 | `ch04-03` | §4.1.1.1 Hard-Logistic和Hard-Tanh | `knowledge/teaching-guides/chapter-04/04-03-hard-sigmoid.teaching.md` | `¶0038-¶0057` | 核心概念 | 未解锁 | `ch04-04` |
| 5 | `ch04-04` | §4.1.2 ReLU + §4.1.2.1 带泄露的ReLU | `knowledge/teaching-guides/chapter-04/04-04-relu-and-leaky-relu.teaching.md` | `¶0058-¶0074` | 核心概念 | 未解锁 | `ch04-05` |
| 6 | `ch04-05` | §4.1.2.2 PReLU + §4.1.2.3 ELU + §4.1.2.4 Softplus | `knowledge/teaching-guides/chapter-04/04-05-relu-variants.teaching.md` | `¶0075-¶0088` | 核心概念 | 未解锁 | `ch04-06` |
| 7 | `ch04-06` | §4.1.3 Swish + §4.1.4 GELU | `knowledge/teaching-guides/chapter-04/04-06-swish-and-gelu.teaching.md` | `¶0089-¶0101` | 核心概念 | 未解锁 | `ch04-07` |
| 8 | `ch04-07` | §4.1.5 Maxout单元 | `knowledge/teaching-guides/chapter-04/04-07-maxout.teaching.md` | `¶0102-¶0110` | 核心概念 | 未解锁 | `ch04-08` |
| 9 | `ch04-08` | §4.2 网络结构（三种类型） | `knowledge/teaching-guides/chapter-04/04-08-network-structures.teaching.md` | `¶0111-¶0126` | 概念对比 | 未解锁 | `ch04-09` |
| 10 | `ch04-09` | §4.3 前馈神经网络 | `knowledge/teaching-guides/chapter-04/04-09-feedforward-neural-network.teaching.md` | `¶0127-¶0146` | 核心概念 | 未解锁 | `ch04-10` |
| 11 | `ch04-10` | §4.3.1 通用近似定理 | `knowledge/teaching-guides/chapter-04/04-10-universal-approximation.teaching.md` | `¶0147-¶0158` | 核心概念 | 未解锁 | `ch04-11` |
| 12 | `ch04-11` | §4.3.2 应用到机器学习 | `knowledge/teaching-guides/chapter-04/04-11-fnn-machine-learning.teaching.md` | `¶0159-¶0173` | 核心概念 | 未解锁 | `ch04-12` |
| 13 | `ch04-12` | §4.3.3 参数学习 | `knowledge/teaching-guides/chapter-04/04-12-fnn-parameter-learning.teaching.md` | `¶0174-¶0188` | 核心概念 | 未解锁 | `ch04-13` |
| 14 | `ch04-13` | 反向传播算法（上） | `knowledge/teaching-guides/chapter-04/04-13-backpropagation-1.teaching.md` | `¶0189-¶0206` | 核心概念 | 未解锁 | `ch04-14` |
| 15 | `ch04-14` | 反向传播算法（中） | `knowledge/teaching-guides/chapter-04/04-14-backpropagation-2.teaching.md` | `¶0207-¶0223` | 核心概念 | 未解锁 | `ch04-15` |
| 16 | `ch04-15` | 反向传播算法（下） | `knowledge/teaching-guides/chapter-04/04-15-backpropagation-3.teaching.md` | `¶0224-¶0241` | 核心概念 | 未解锁 | `ch04-16` |
| 17 | `ch04-16` | §4.5 + §4.5.1 数值微分 + §4.5.2 符号微分 | `knowledge/teaching-guides/chapter-04/04-16-gradient-computation-methods.teaching.md` | `¶0242-¶0258` | 概念对比 | 未解锁 | `ch04-17` |
| 18 | `ch04-17` | §4.5.3 自动微分（上） | `knowledge/teaching-guides/chapter-04/04-17-automatic-differentiation-1.teaching.md` | `¶0259-¶0277` | 核心概念 | 未解锁 | `ch04-18` |
| 19 | `ch04-18` | §4.5.3 自动微分（中） | `knowledge/teaching-guides/chapter-04/04-18-automatic-differentiation-2.teaching.md` | `¶0278-¶0295` | 核心概念 | 未解锁 | `ch04-19` |
| 20 | `ch04-19` | §4.5.3 自动微分（下） | `knowledge/teaching-guides/chapter-04/04-19-automatic-differentiation-3.teaching.md` | `¶0296-¶0310` | 核心概念 | 未解锁 | `ch04-20` |
| 21 | `ch04-20` | §4.6 + §4.6.1 非凸优化问题 | `knowledge/teaching-guides/chapter-04/04-20-nonconvex-optimization.teaching.md` | `¶0311-¶0317` | 核心概念 | 未解锁 | `ch04-21` |
| 22 | `ch04-21` | §4.6.2 梯度消失问题 | `knowledge/teaching-guides/chapter-04/04-21-vanishing-gradient.teaching.md` | `¶0318-¶0329` | 核心概念 | 未解锁 | `ch04-22` |
| 23 | `ch04-22` | §4.7 总结和深入阅读 | `knowledge/teaching-guides/chapter-04/04-22-summary-and-reading.teaching.md` | `¶0330-¶0336` | 章节收束 | 未解锁 | `ch04-test` |
| 24 | `ch04-test` | 第4章章测 | 无新增讲义；覆盖第4章已通过单元 | 第4章已解锁段落 | 章测 | 未解锁 | `ch05-00` |

## 章末处理

- `ch04-test` 表示第4章章测，不对应教材新段落。
- 章测前必须完成第4章所有核心单元的覆盖检查。
- 章测通过后，才进入第5章详细路线建设或学习。
- `¶0337-¶0346` 为习题，`¶0347-¶0369` 为参考文献，不进入任何教学单元。
- 反向传播算法（`¶0189-¶0241`）在教材中未编号（§4.4缺失），路线中以"反向传播算法"标注。
