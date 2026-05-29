# 第7章 覆盖审计表

本表用于审计第7章是否形成稳定闭环。AI 教学第7章时，应以 `learning-path/chapter-07.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch07-00` | 第7章 引言 | `knowledge/teaching-guides/chapter-07/ch07-00-introduction.teaching.md` | `¶0001-¶0007` | 深度神经网络两大难点（优化+泛化）；优化问题三成因；泛化问题成因；本章两大部分结构 | 第7章引言 | `ch07-01` |
| 2 | `ch07-01` | §7.1+7.1.1+7.1.2 高维非凸优化 | `knowledge/teaching-guides/chapter-07/ch07-01-high-dim-nonconvex-optimization.teaching.md` | `¶0008-¶0023` | 非凸优化挑战；鞍点问题（高维空间主要难点）；平坦最小值与鲁棒性关系；局部最小解等价性 | 高维非凸优化 | `ch07-02` |
| 3 | `ch07-02` | §7.1.3 网络优化改善方法 | `knowledge/teaching-guides/chapter-07/ch07-02-optimization-improvement-methods.teaching.md` | `¶0024-¶0032` | 改善方法的四类方向；优化地形概念；四类方法对应的书中章节 | 网络优化改善方法 | `ch07-03` |
| 4 | `ch07-03` | §7.2+7.2.1 小批量梯度下降 | `knowledge/teaching-guides/chapter-07/ch07-03-mini-batch-gradient-descent.teaching.md` | `¶0033-¶0047` | 梯度下降三种形式（BGD/SGD/Mini-Batch）；小批量梯度估计公式(7.1)；影响小批量梯度下降的三因素；参数更新差值Δθ_t定义 | 小批量梯度下降 | `ch07-04` |
| 5 | `ch07-04` | §7.2.2 批量大小选择 | `knowledge/teaching-guides/chapter-07/ch07-04-batch-size-selection.teaching.md` | `¶0048-¶0058` | 批量大小对梯度方差的影响；线性缩放规则；Epoch与Iteration关系；小批量→平坦最小值 | 批量大小选择 | `ch07-05` |
| 6 | `ch07-05` | §7.2.3+§7.2.3.1 学习率衰减（上） | `knowledge/teaching-guides/chapter-07/ch07-05-learning-rate-decay-1.teaching.md` | `¶0059-¶0071` | 学习率衰减动机；分段常数衰减；逆时衰减公式(7.5)；指数衰减公式(7.6) | 学习率衰减（上） | `ch07-06` |
| 7 | `ch07-06` | §7.2.3.1（下）+§7.2.3.2 | `knowledge/teaching-guides/chapter-07/ch07-06-cosine-decay-and-warmup.teaching.md` | `¶0072-¶0084` | 自然指数衰减公式(7.7)；余弦衰减公式(7.8)；学习率预热动机与公式(7.9) | 余弦衰减与学习率预热 | `ch07-07` |
| 8 | `ch07-07` | §7.2.3.3 周期性学习率调整 | `knowledge/teaching-guides/chapter-07/ch07-07-cyclic-learning-rate.teaching.md` | `¶0085-¶0101` | 周期性增大学习率的动机；三角循环学习率机制；SGDR热重启机制与公式(7.13) | 周期性学习率调整 | `ch07-08` |
| 9 | `ch07-08` | §7.2.3.4+7.2.3.5 | `knowledge/teaching-guides/chapter-07/ch07-08-adagrad-and-rmsprop.teaching.md` | `¶0102-¶0120` | AdaGrad自适应机制与公式(7.14)-(7.15)；AdaGrad学习率单调下降缺点；RMSprop指数衰减移动平均(7.16)；RMSprop vs AdaGrad关键区别 | AdaGrad与RMSprop | `ch07-09` |
| 10 | `ch07-09` | §7.2.3.6 AdaDelta | `knowledge/teaching-guides/chapter-07/ch07-09-adadelta.teaching.md` | `¶0121-¶0128` | AdaDelta与RMSprop的关系；Δθ平方的指数衰减移动平均；AdaDelta无需初始学习率 | AdaDelta | `ch07-10` |
| 11 | `ch07-10` | §7.2.4 概述+§7.2.4.1 动量法 | `knowledge/teaching-guides/chapter-07/ch07-10-momentum.teaching.md` | `¶0129-¶0136` | 梯度估计修正的动机；动量法物理直觉；动量法参数更新公式(7.21)；动量因子ρ的作用 | 动量法 | `ch07-11` |
| 12 | `ch07-11` | §7.2.4.2 Nesterov加速梯度 | `knowledge/teaching-guides/chapter-07/ch07-11-nesterov-accelerated-gradient.teaching.md` | `¶0137-¶0148` | NAG与动量法的区别；两步更新的"超前"思想；NAG合并更新公式(7.24) | Nesterov加速梯度 | `ch07-12` |
| 13 | `ch07-12` | §7.2.4.3 Adam算法 | `knowledge/teaching-guides/chapter-07/ch07-12-adam.teaching.md` | `¶0149-¶0161` | Adam=动量法+RMSprop；一阶矩M_t和二阶矩G_t；偏差修正公式(7.27)-(7.28)；Adam更新公式(7.29)；Nadam | Adam算法 | `ch07-13` |
| 14 | `ch07-13` | §7.2.4.4 梯度截断 | `knowledge/teaching-guides/chapter-07/ch07-13-gradient-clipping.teaching.md` | `¶0162-¶0172` | 梯度爆炸问题；按值截断公式(7.30)；按模截断公式(7.31)；梯度截断在RNN中的重要性 | 梯度截断 | `ch07-14` |
| 15 | `ch07-14` | §7.2.5 优化算法小结 | `knowledge/teaching-guides/chapter-07/ch07-14-optimization-summary.teaching.md` | `¶0173-¶0183` | 优化算法两大类；统一框架公式(7.32)-(7.34)；α_t/G_t/M_t各自含义 | 优化算法统一框架与小结 | `ch07-15` |
| 16 | `ch07-15` | §7.3 概述+§7.3.1 | `knowledge/teaching-guides/chapter-07/ch07-15-fixed-variance-initialization.teaching.md` | `¶0184-¶0194` | 三种初始化方式（预训练/随机/固定值）；对称权重现象；高斯/均匀分布初始化；方差过大/过小的问题 | 固定方差初始化 | `ch07-16` |
| 17 | `ch07-16` | §7.3.2 概述+方差缩放动机 | `knowledge/teaching-guides/chapter-07/ch07-16-variance-scaling-motivation.teaching.md` | `¶0195-¶0205` | 方差缩放动机（输入输出方差一致）；固定方差的问题（信号衰减/饱和） | 方差缩放动机 | `ch07-17` |
| 18 | `ch07-17` | §7.3.2.1 Xavier初始化（上） | `knowledge/teaching-guides/chapter-07/ch07-17-xavier-forward.teaching.md` | `¶0206-¶0217` | Xavier前向推导（恒等函数假设）；前向方差保持条件var(w)=1/M_{l-1} | Xavier初始化（上） | `ch07-18` |
| 19 | `ch07-18` | §7.3.2.1 Xavier（下）+§7.3.2.2 | `knowledge/teaching-guides/chapter-07/ch07-18-xavier-backward-and-he.teaching.md` | `¶0218-¶0235` | Xavier反向方差条件；折中公式var(w)=2/(M_{l-1}+M_l)；He初始化公式var(w)=2/M_{l-1}；表7.2对比 | Xavier（下）+He初始化 | `ch07-19` |
| 20 | `ch07-19` | §7.3.3 正交初始化 | `knowledge/teaching-guides/chapter-07/ch07-19-orthogonal-initialization.teaching.md` | `¶0236-¶0247` | 正交初始化动机（范数保持性）；实现方法（SVD分解）；在RNN中的应用；缩放系数ρ | 正交初始化 | `ch07-20` |
| 21 | `ch07-20` | §7.4 数据预处理（上） | `knowledge/teaching-guides/chapter-07/ch07-20-data-preprocessing-1.teaching.md` | `¶0248-¶0257` | 尺度不变性定义；尺度差异对训练的影响；等高线图直觉；最小最大值归一化公式(7.47) | 数据预处理（上） | `ch07-21` |
| 22 | `ch07-21` | §7.4 数据预处理（下） | `knowledge/teaching-guides/chapter-07/ch07-21-data-preprocessing-2.teaching.md` | `¶0258-¶0267` | 标准化公式(7.50)；均值和方差计算(7.48)-(7.49)；标准差为0时的处理；白化的目的与PCA实现 | 数据预处理（下） | `ch07-22` |
| 23 | `ch07-22` | §7.5 逐层归一化概述 | `knowledge/teaching-guides/chapter-07/ch07-22-layer-wise-normalization-intro.teaching.md` | `¶0268-¶0275` | 内部协变量偏移的定义；逐层归一化的两个好处（尺度不变性+平滑优化地形）；四种逐层归一化方法名称 | 逐层归一化概述 | `ch07-23` |
| 24 | `ch07-23` | §7.5.1 BN（上） | `knowledge/teaching-guides/chapter-07/ch07-23-batch-normalization-1.teaching.md` | `¶0276-¶0288` | BN操作位置（仿射变换后、激活函数前）；标准化公式(7.52)；小批量均值和方差近似；∑_B和σ_B²的公式 | 批量归一化（上） | `ch07-24` |
| 25 | `ch07-24` | §7.5.1 BN（下） | `knowledge/teaching-guides/chapter-07/ch07-24-batch-normalization-2.teaching.md` | `¶0289-¶0298` | 缩放平移参数γ和β的作用；BN作为特殊神经层；训练/测试时均值方差区别；BN的隐形正则化效应 | 批量归一化（下） | `ch07-25` |
| 26 | `ch07-25` | §7.5.2 层归一化 | `knowledge/teaching-guides/chapter-07/ch07-25-layer-normalization.teaching.md` | `¶0299-¶0316` | LN与BN的归一化维度区别（按行vs按列）；LN在RNN中的应用公式(7.62)-(7.63)；LN缓解RNN梯度问题 | 层归一化 | `ch07-26` |
| 27 | `ch07-26` | §7.5.3+7.5.4 权重归一化与LRN | `knowledge/teaching-guides/chapter-07/ch07-26-weight-normalization-and-lrn.teaching.md` | `¶0317-¶0330` | 权重归一化再参数化思想(7.64)；LRN的生物学动机（侧抑制）；LRN与层归一化的区别 | 权重归一化与LRN | `ch07-27` |
| 28 | `ch07-27` | §7.6+7.6.1+7.6.2 超参数优化—网格与随机搜索 | `knowledge/teaching-guides/chapter-07/ch07-27-hyperparameter-optimization-1.teaching.md` | `¶0331-¶0343` | 超参数三类；超参数优化两困难；网格搜索原理与局限性；随机搜索优势 | 网格与随机搜索 | `ch07-28` |
| 29 | `ch07-28` | §7.6.3+7.6.4+7.6.5 贝叶斯优化、动态资源与NAS | `knowledge/teaching-guides/chapter-07/ch07-28-bayesian-opt-and-nas.teaching.md` | `¶0344-¶0360` | 贝叶斯优化思想；EI收益函数；逐次减半方法核心思想 | 贝叶斯优化与动态资源 | `ch07-29` |
| 30 | `ch07-29` | §7.7 概述+§7.7.1 L1/L2正则化 | `knowledge/teaching-guides/chapter-07/ch07-29-l1-l2-regularization.teaching.md` | `¶0361-¶0374` | 正则化定义与目标；L1/L2正则化优化目标(7.68)；正则项作为约束的直觉；过度参数化概念 | L1/L2正则化 | `ch07-30` |
| 31 | `ch07-30` | §7.7.1（续）+7.7.2+7.7.3 | `knowledge/teaching-guides/chapter-07/ch07-30-elastic-net-weight-decay-early-stop.teaching.md` | `¶0375-¶0391` | 弹性网络正则化(7.72)；权重衰减公式(7.73)；权重衰减vs L2正则化的等价/不等价；提前停止原理 | 弹性网络、权重衰减、早停 | `ch07-31` |
| 32 | `ch07-31` | §7.7.4+7.7.4.1 Dropout | `knowledge/teaching-guides/chapter-07/ch07-31-dropout.teaching.md` | `¶0392-¶0407` | Dropout训练机制（伯努利掩码）；推理时p倍缩放；集成学习解释；贝叶斯学习近似解释 | Dropout | `ch07-32` |
| 33 | `ch07-32` | §7.7.5+7.7.6 数据增强与标签平滑 | `knowledge/teaching-guides/chapter-07/ch07-32-data-augmentation-and-label-smoothing.teaching.md` | `¶0408-¶0422` | 数据增强五种方法；标签平滑动机与软目标公式；知识蒸馏概念 | 数据增强与标签平滑 | `ch07-33` |
| 34 | `ch07-33` | §7.8 总结和深入阅读 | `knowledge/teaching-guides/chapter-07/ch07-33-summary-and-reading.teaching.md` | `¶0423-¶0427` | 优化与正则化对立统一关系；三类提高训练效率的方法；深度神经网络泛化能力尚无完善理论 | 总结和深入阅读 | `ch07-test` |
| 35 | `ch07-test` | 第7章章测 | 无新增讲义；覆盖第7章已通过单元 | 第7章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第7章章测 | 第8章未解锁 |

## 当前审计结论

- 第7章 34 个教学单元（`ch07-00` ~ `ch07-33`）均有教学指引和教材段落。
- `ch07-00` 覆盖引言和两大难点框架，¶0001-¶0003为名言引用，不单独设考点。
- `ch07-01` 为16段超限单元：鞍点概率论证+平坦最小值+改善方法四类，概念连续不宜拆分。其中¶0015、¶0021-¶0022为图片，不单独设考点。
- `ch07-07` 为17段超限单元：三角波周期+SGDR重启，公式密集且概念闭环。其中¶0100-¶0101为图片。
- `ch07-08` 为19段超限单元：AdaGrad→RMSprop演化对比，公式密集且对比教学不宜拆分。
- `ch07-18` 为17段超限单元：Xavier反向条件+He ReLU修正，公式密集且对比表7.2需同单元。
- `ch07-25` 为18段超限单元：LN公式+RNN应用+BN对比，公式密集且RNN特化内容无法独立成单元。
- `ch07-28` 为17段超限单元：贝叶斯优化GP建模+动态资源+NAS概述。§7.6.5 NAS（¶0358-¶0360）仅3段，设为"了解即可"不进入正式题。
- `ch07-30` 为17段超限单元：弹性网络+权重衰减+早停，三个轻量正则方法概念连续不宜拆分。
- `ch07-31` 为16段超限单元：Dropout训练/推理+集成解释+RNN变体。§7.7.4.1 RNN dropout（¶0404-¶0407）设为"了解即可"。
- `ch07-33` 为章节收束单元：不考参考文献、具体人名年份、VC维/Rademacher复杂度细节。
- `¶0428-¶0439` 为习题，`¶0440-¶0486` 为参考文献，不进入任何教学单元的正式题范围。
- 所有单元中引用的习题、后文章节、附录均为"了解即可"或"课堂识别不计分"。
- 第8章仍未解锁，待第7章章测通过后再建设详细路线。
