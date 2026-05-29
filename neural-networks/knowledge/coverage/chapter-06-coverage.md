# 第6章 覆盖审计表

本表用于审计第6章是否形成稳定闭环。AI 教学第6章时，应以 `learning-path/chapter-06.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch06-00` | 第6章 引言 | `knowledge/teaching-guides/chapter-06/06-00-introduction.teaching.md` | `¶0001-¶0005` | 前馈网络两个局限（单向传递、固定维数）；RNN环路结构与短期记忆；RNN长程依赖问题与门控改进方向 | 第6章引言 | `ch06-01` |
| 2 | `ch06-01` | §6.1+6.1.1+6.1.2 TDNN与NARX | `knowledge/teaching-guides/chapter-06/06-01-tdnn-narx.teaching.md` | `¶0006-¶0019` | 三种增加记忆能力方法框架；TDNN延时器和权值共享原理；TDNN与CNN等价关系；NARX双延时路径结构 | TDNN与NARX | `ch06-02` |
| 3 | `ch06-02` | §6.1.3 循环神经网络初识 | `knowledge/teaching-guides/chapter-06/06-02-rnn-first-look.teaching.md` | `¶0020-¶0028` | RNN公式h_t=f(h_{t-1},x_t)各符号含义；隐状态h_t作为动力系统状态；RNN两层计算能力概述（通用近似+模拟程序）；RNN与RecNN术语区分 | RNN初识 | `ch06-03` |
| 4 | `ch06-03` | §6.2 简单循环网络 | `knowledge/teaching-guides/chapter-06/06-03-simple-rn.teaching.md` | `¶0029-¶0037` | SRN与前馈网络的结构差异（自反馈连接）；U、W、b三个参数的维度和角色；常用激活函数Logistic/Tanh；按时间展开与权值共享思想 | 简单循环网络 | `ch06-04` |
| 5 | `ch06-04` | §6.2.1.1 通用近似定理（上） | `knowledge/teaching-guides/chapter-06/06-04-universal-approximation-1.teaching.md` | `¶0038-¶0055` | 完全连接RNN完整结构（输入→隐藏→输出）；定理6.1内容与直觉；动力系统两个函数（g和o）；证明第一步思路（两层前馈网络近似g和o） | 通用近似定理（上） | `ch06-05` |
| 6 | `ch06-05` | §6.2.1.1（下）+§6.2.1.2 图灵完备 | `knowledge/teaching-guides/chapter-06/06-05-universal-approximation-2-turing.teaching.md` | `¶0056-¶0071` | 两个网络合并为一个RNN的核心思想；图灵完备定义与直觉；定理6.2含义（RNN可模拟所有图灵机） | 通用近似定理（下）+图灵完备 | `ch06-06` |
| 7 | `ch06-06` | §6.3概述+§6.3.1+§6.3.2 序列到类别与同步seq2seq | `knowledge/teaching-guides/chapter-06/06-06-seq-to-class-and-sync.teaching.md` | `¶0072-¶0088` | RNN三种应用模式分类框架；序列到类别两种序列表示方法（最后时刻/平均池化）；同步seq2seq模式工作原理 | 序列到类别与同步seq2seq | `ch06-07` |
| 8 | `ch06-07` | §6.3.3 异步seq2seq（编码器-解码器） | `knowledge/teaching-guides/chapter-06/06-07-async-seq2seq.teaching.md` | `¶0089-¶0103` | 异步seq2seq与同步seq2seq区别；编码器与解码器分工；解码器自回归动机；三个公式的完整编码-解码流程 | 异步seq2seq | `ch06-08` |
| 9 | `ch06-08` | §6.4 参数学习概述 | `knowledge/teaching-guides/chapter-06/06-08-param-learning-intro.teaching.md` | `¶0104-¶0113` | 序列损失函数结构（各时刻求和）；参数梯度分解逻辑（∂L/∂U=Σ∂L_t/∂U）；RNN参数梯度计算特殊性（递归调用f）；BPTT与RTRL基本区分 | 参数学习概述 | `ch06-09` |
| 10 | `ch06-09` | §6.4.1 BPTT（上）—误差项推导 | `knowledge/teaching-guides/chapter-06/06-09-bptt-1.teaching.md` | `¶0114-¶0127` | BPTT三个核心思想（展开、共享、求和）；梯度累加所有时刻的原因；"直接"偏导数∂⁺的含义；误差项δ_{t,k}递推公式与方向 | BPTT（上） | `ch06-10` |
| 11 | `ch06-10` | §6.4.1 BPTT（下）—参数梯度与复杂度 | `knowledge/teaching-guides/chapter-06/06-10-bptt-2.teaching.md` | `¶0128-¶0139` | ∂L_t/∂U矩阵形式（外积之和）；完整序列L对U的梯度（双重求和）；对W和b的梯度公式；BPTT批处理特性 | BPTT（下） | `ch06-11` |
| 12 | `ch06-11` | §6.4.2 RTRL算法 | `knowledge/teaching-guides/chapter-06/06-11-rtrl.teaching.md` | `¶0140-¶0153` | RTRL前向传播原理；∂h/∂u递推结构；BPTT与RTRL三维度对比（方向/空间/场景） | RTRL算法 | `ch06-12` |
| 13 | `ch06-12` | §6.5 长程依赖问题 | `knowledge/teaching-guides/chapter-06/06-12-long-range-dependency.teaching.md` | `¶0154-¶0165` | 长程依赖问题定义与直觉；误差项连乘积展开；γ的作用与梯度消失/爆炸判断条件；梯度消失在RNN中的特殊含义（∂L_t/∂h_k消失） | 长程依赖问题 | `ch06-13` |
| 14 | `ch06-13` | §6.5.1 改进方案 | `knowledge/teaching-guides/chapter-06/06-13-improvement-schemes.teaching.md` | `¶0166-¶0182` | 梯度爆炸两种解决方法（权重衰减/梯度截断）；恒等连接消除梯度消失的原理与代价；残差式改进公式(6.50)的设计思想；残差式改进两个遗留问题（梯度爆炸+记忆容量） | 改进方案 | `ch06-14` |
| 15 | `ch06-14` | §6.6.1 LSTM（上）—内部状态与候选状态 | `knowledge/teaching-guides/chapter-06/06-14-lstm-internal-state.teaching.md` | `¶0183-¶0193` | 门控机制设计思想；c_t与h_t的角色分离；c_t更新公式（遗忘+输入）结构；候选状态~c_t计算 | LSTM内部状态与候选状态 | `ch06-15` |
| 16 | `ch06-15` | §6.6.1 LSTM（中）—三门定义与作用 | `knowledge/teaching-guides/chapter-06/06-15-lstm-gates.teaching.md` | `¶0194-¶0205` | 遗忘门作用与极端行为；输入门作用与极端行为；输出门作用与极端行为；三个门的sigmoid计算公式；LSTM完整两步计算流程 | LSTM三门定义与作用 | `ch06-16` |
| 17 | `ch06-16` | §6.6.1 LSTM（下）—统一公式与记忆概念 | `knowledge/teaching-guides/chapter-06/06-16-lstm-unified.teaching.md` | `¶0206-¶0215` | LSTM统一公式紧凑表示思想；三层记忆（h_t/c_t/网络参数）时间尺度区分；遗忘门偏置初始化特殊设置原因 | LSTM统一公式与记忆 | `ch06-17` |
| 18 | `ch06-17` | §6.6.2 LSTM变体 | `knowledge/teaching-guides/chapter-06/06-17-lstm-variants.teaching.md` | `¶0216-¶0226` | 无遗忘门LSTM的饱和问题；Peephole连接设计动机与公式修改；耦合输入遗忘门的简化思路 | LSTM变体 | `ch06-18` |
| 19 | `ch06-18` | §6.6.3 GRU（上）—更新门 | `knowledge/teaching-guides/chapter-06/06-18-gru-update-gate.teaching.md` | `¶0227-¶0233` | GRU不引入额外记忆单元的设计选择；更新门z_t在状态更新公式中的作用；z_t计算公式；z_t极端取值行为直觉 | GRU更新门 | `ch06-19` |
| 20 | `ch06-19` | §6.6.3 GRU（下）—重置门与状态更新 | `knowledge/teaching-guides/chapter-06/06-19-gru-reset-gate.teaching.md` | `¶0234-¶0245` | 候选状态~h_t中重置门r_t的作用；r_t计算公式；r_t极端取值行为；GRU各种退化情况分析（z_t/r_t四种组合） | GRU重置门与状态更新 | `ch06-20` |
| 21 | `ch06-20` | §6.7 深层循环神经网络 | `knowledge/teaching-guides/chapter-06/06-20-deep-rnn.teaching.md` | `¶0246-¶0262` | RNN"既深又浅"直觉；堆叠RNN信息流（时间方向+层级方向）；双向RNN设计动机；Bi-RNN公式与结构（正序+逆序+拼接） | 深层循环神经网络 | `ch06-21` |
| 22 | `ch06-21` | §6.8+6.8.1 递归神经网络 | `knowledge/teaching-guides/chapter-06/06-21-recursive-nn.teaching.md` | `¶0263-¶0280` | 消息传递推广思想（链式→图式）；RecNN树状结构与权值共享；h_i=f(h_{π_i})计算公式；链式退化时RecNN等价于SRN | 递归神经网络 | `ch06-22` |
| 23 | `ch06-22` | §6.8.2 图神经网络 | `knowledge/teaching-guides/chapter-06/06-22-gnn.teaching.md` | `¶0281-¶0288` | GNN应用场景（图结构数据）；消息聚合与状态更新两步公式；同步更新与异步更新区分 | 图神经网络 | `ch06-23` |
| 24 | `ch06-23` | §6.9 总结和深入阅读 | `knowledge/teaching-guides/chapter-06/06-23-summary.teaching.md` | `¶0289-¶0295` | 第6章主线演进逻辑框架；LSTM与GRU核心设计对比；"线性连接+门控"思想跨架构迁移 | 总结和深入阅读 | `ch06-test` |
| 25 | `ch06-test` | 第6章章测 | 无新增讲义；覆盖第6章已通过单元 | 第6章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第6章章测 | 第7章未解锁 |

## 当前审计结论

- 第6章 24 个教学单元（`ch06-00` ~ `ch06-23`）均有教学指引和教材段落。
- 以下单元超过 15 段，已在覆盖备注中说明原因：
  - `ch06-04`（18段）：通用近似定理前半，公式密集（(6.8)-(6.14)共7个公式），推导连续不宜拆分。
  - `ch06-05`（16段）：通用近似定理后半（合并证明）+图灵完备，概念连续不宜拆分。
  - `ch06-06`（17段）：序列建模三种任务类型连续对比，组内信息紧凑不宜拆分。
  - `ch06-13`（17段）：长程依赖改进方案演进逻辑连续，从爆炸→消失→线性连接→残差→遗留问题，一条因果链不宜拆分。
  - `ch06-20`（17段）：深层 RNN 两种方式（堆叠+双向）结构互补，同在 §6.7 内。
  - `ch06-21`（18段）：递归神经网络从消息传递思想到树结构具体计算再到退化等价，公式连续（(6.74)-(6.78)），不宜拆分。
- `ch06-00` 覆盖引言，`¶0001-¶0002` 为谚语，不设考点。
- `ch06-23`（总结单元）不将参考文献、推荐书目、人名/年份、外部链接纳入正式题。仅考核章节框架回顾和核心概念的演进理解。
- 所有跨章引用（第5章残差连接、第7章梯度截断、第8章注意力机制/外部记忆/图灵机、第15章异步seq2seq）均标注为课堂识别不计分或了解即可。
- `ch06-13` 中 `¶0168`（参见第7.2.4.4节）、`¶0182`（参见第8.5节）为跨章引用，课堂识别不计分。
- `ch06-21` 中 `¶0278`（参见习题6-7）、`¶0279`（RecNN应用于NLP）、`¶0280`（Tree-LSTM）不进入正式题。
- `ch06-22` 中 `¶0288` 的读出函数仅作了解即可，不进入正式题。
- `¶0296-¶0302` 为习题，`¶0303-¶0341` 为参考文献，不进入任何教学单元的正式题范围。
- 第7章仍未解锁，待第6章章测通过后再建设详细路线。
