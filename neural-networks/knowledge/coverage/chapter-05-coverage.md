# 第5章 覆盖审计表

本表用于审计第5章是否形成稳定闭环。AI 教学第5章时，应以 `learning-path/chapter-05.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch05-00` | 第5章 引言 | `knowledge/teaching-guides/chapter-05/05-00-introduction.teaching.md` | `¶0001-¶0011` | CNN定义（局部连接+权重共享的深层前馈网络）；全连接网络处理图像的两大问题（参数爆炸/忽略局部不变性）；感受野概念启发；CNN三大核心思想概览 | 第5章引言 | `ch05-01` |
| 2 | `ch05-01` | §5.1.1.1 一维卷积（上） | `knowledge/teaching-guides/chapter-05/05-01-1d-convolution-1.teaching.md` | `¶0013-¶0023` | 一维卷积定义y_t=Σx_{t-k+1}w_k；卷积核（滤波器）w的概念；卷积运算的滑动窗口直觉；信号处理中的"翻转+滑动"解释 | 一维卷积（上） | `ch05-02` |
| 3 | `ch05-02` | §5.1.1.1 一维卷积（下） | `knowledge/teaching-guides/chapter-05/05-02-1d-convolution-2.teaching.md` | `¶0024-¶0034` | 不同滤波器提取不同特征；移动平均滤波器提取低频/平滑信息；二阶微分滤波器提取高频/变化信息；图5.1滤波结果解释 | 一维卷积（下） | `ch05-03` |
| 4 | `ch05-03` | §5.1.1.2 二维卷积 | `knowledge/teaching-guides/chapter-05/05-03-2d-convolution.teaching.md` | `¶0035-¶0045` | 二维卷积定义（图像处理中的标准卷积）；卷积核在二维平面上的滑动扫描；多通道卷积的求和方式；卷积核大小与输出尺寸关系 | 二维卷积 | `ch05-04` |
| 5 | `ch05-04` | §5.1.2 互相关 | `knowledge/teaching-guides/chapter-05/05-04-cross-correlation.teaching.md` | `¶0046-¶0056` | 互相关vs卷积（是否翻转卷积核）；深度学习中"卷积"实际是互相关（不翻转）；互相关的数学定义；为什么DL中不翻转（可学习参数不需要严格数学卷积） | 互相关 | `ch05-05` |
| 6 | `ch05-05` | §5.1.3 卷积的变种 | `knowledge/teaching-guides/chapter-05/05-05-convolution-variants.teaching.md` | `¶0057-¶0068` | 步长（stride）概念及对输出尺寸的影响；零填充（zero-padding）控制边界与输出长度；输出长度公式；窄卷积/宽卷积/等宽卷积的参数组合 | 卷积的变种 | `ch05-06` |
| 7 | `ch05-06` | §5.1.4.1 交换性 | `knowledge/teaching-guides/chapter-05/05-06-convolution-commutativity.teaching.md` | `¶0070-¶0077` | 卷积运算的交换律（在一定条件下）；窄卷积的交换性条件；交换性在CNN设计中的含义 | 卷积交换性 | `ch05-07` |
| 8 | `ch05-07` | §5.1.4.2 导数 | `knowledge/teaching-guides/chapter-05/05-07-convolution-derivative.teaching.md` | `¶0078-¶0094` | 卷积对输入X的导数（涉及旋转180°的卷积核）；卷积对卷积核W的导数；∂Y/∂X = rot180(W)卷积∂f/∂Y的形式（不要求完整推导）；导数形状在反向传播中的意义 | 卷积导数 | `ch05-08` |
| 9 | `ch05-08` | §5.2.1 用卷积代替全连接 | `knowledge/teaching-guides/chapter-05/05-08-convolution-vs-dense.teaching.md` | `¶0096-¶0106` | 全连接→卷积的两大优势：局部连接（每个神经元只看局部区域）和权重共享（同一卷积核在整个输入上共享参数）；参数数量的大幅减少；局部连接+权重共享的直觉 | 卷积代替全连接 | `ch05-09` |
| 10 | `ch05-09` | §5.2.2 卷积层 | `knowledge/teaching-guides/chapter-05/05-09-convolutional-layer.teaching.md` | `¶0107-¶0123` | 卷积层三要素：卷积核大小/步长/零填充；输入通道数×输出通道数×核大小的参数结构；多个卷积核提取不同特征；特征图（feature map）概念 | 卷积层 | `ch05-10` |
| 11 | `ch05-10` | §5.2.3 汇聚层 | `knowledge/teaching-guides/chapter-05/05-10-pooling-layer.teaching.md` | `¶0124-¶0141` | 汇聚层目的：降维+增强平移不变性；最大汇聚（max pooling）和平均汇聚（average pooling）；汇聚层的超参数（窗口大小/步长）；汇聚层无学习参数 | 汇聚层 | `ch05-11` |
| 12 | `ch05-11` | §5.2.4 整体结构 + §5.3 参数学习 | `knowledge/teaching-guides/chapter-05/05-11-cnn-structure-and-parameter-learning.teaching.md` | `¶0142-¶0161` | CNN典型结构：卷积层→汇聚层→...→全连接层→输出；特征提取+分类的两阶段范式；CNN参数学习的梯度下降框架 | CNN结构与参数学习 | `ch05-12` |
| 13 | `ch05-12` | §5.3.1 CNN反向传播算法 | `knowledge/teaching-guides/chapter-05/05-12-cnn-backpropagation.teaching.md` | `¶0162-¶0182` | 卷积层反向传播：∂L/∂X = ∂L/∂Y 与 rot180(W)的卷积；∂L/∂W = ∂L/∂Y 与 X的卷积（互相关形式）；汇聚层反向传播：梯度按汇聚方式回传（max→传最大值位置/avg→均分） | CNN反向传播 | `ch05-13` |
| 14 | `ch05-13` | §5.4.1 LeNet-5 | `knowledge/teaching-guides/chapter-05/05-13-lenet5.teaching.md` | `¶0184-¶0200` | LeNet-5是CNN的奠基架构；Conv-Pool-Conv-Pool-FC-FC的层级范式；局部连接+权重共享的核心设计；LeNet在手写数字识别上的成功 | LeNet-5 | `ch05-14` |
| 15 | `ch05-14` | §5.4.2 AlexNet | `knowledge/teaching-guides/chapter-05/05-14-alexnet.teaching.md` | `¶0201-¶0216` | AlexNet的深度突破：更深的CNN+更大数据集；ReLU替代Sigmoid加速训练；Dropout防止过拟合；多GPU训练的策略动机 | AlexNet | `ch05-15` |
| 16 | `ch05-15` | §5.4.3 Inception网络 | `knowledge/teaching-guides/chapter-05/05-15-inception.teaching.md` | `¶0217-¶0228` | Inception模块核心思想：并行多尺度卷积+1×1卷积降维；1×1卷积的作用：通道维度降维（减少参数）+增加非线性；Inception=让网络自己选择最佳卷积核大小 | Inception网络 | `ch05-16` |
| 17 | `ch05-16` | §5.4.4 残差网络 | `knowledge/teaching-guides/chapter-05/05-16-resnet.teaching.md` | `¶0229-¶0237` | ResNet核心动机：更深网络反而性能退化→不是过拟合而是优化困难；残差连接F(x)+x（跳跃连接/恒等映射）；残差学习H(x)-x比直接学H(x)更容易；残差连接使梯度通过跳跃路径直接传回浅层 | 残差网络 | `ch05-17` |
| 18 | `ch05-17` | §5.5.1 转置卷积（上） | `knowledge/teaching-guides/chapter-05/05-17-transposed-convolution-1.teaching.md` | `¶0239-¶0255` | 转置卷积目的：低维特征→高维输出（上采样）；转置卷积=前向卷积的"反向"操作（不是逆操作）；从全连接转置到卷积转置的类比 | 转置卷积（上） | `ch05-18` |
| 19 | `ch05-18` | §5.5.1 转置卷积（下） | `knowledge/teaching-guides/chapter-05/05-18-transposed-convolution-2.teaching.md` | `¶0256-¶0273` | 转置卷积的实现（通过卷积操作而非矩阵转置）；微步卷积=转置卷积的一种实现方式；2D转置卷积与上采样的关系 | 转置卷积（下） | `ch05-19` |
| 20 | `ch05-19` | §5.5.2 空洞卷积 | `knowledge/teaching-guides/chapter-05/05-19-dilated-convolution.teaching.md` | `¶0274-¶0285` | 空洞卷积定义（卷积核元素间插入空洞/间隔）；空洞率（dilation rate）的含义；空洞卷积=在不增加参数的情况下扩大感受野；语义分割等密集预测任务中替代汇聚层的下采样 | 空洞卷积 | `ch05-20` |
| 21 | `ch05-20` | §5.6 总结和深入阅读 | `knowledge/teaching-guides/chapter-05/05-20-summary-and-reading.teaching.md` | `¶0286-¶0291` | CNN核心思想串联（局部连接/权重共享/汇聚）；经典架构演变线（LeNet→AlexNet→Inception→ResNet）；卷积变种的应用场景总结；CNN从前馈网络继承的共性 | 总结和深入阅读 | `ch05-test` |
| 22 | `ch05-test` | 第5章章测 | 无新增讲义；覆盖第5章已通过单元 | 第5章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第5章章测 | 第6章未解锁 |

## 当前审计结论

- 第5章 21 个教学单元（`ch05-00` ~ `ch05-20`）均有教学指引和教材段落。
- `ch05-01` 和 `ch05-02` 拆分 §5.1.1.1 一维卷积（22段→11+11），均为公式密集，正式题不考完整公式推导。
- `ch05-10`（汇聚层, 18段非公式密集）正式考点控制在≤5个，超过则拆分。
- `ch05-11` 合并 §5.2.4 整体结构（3段）和 §5.3 参数学习（17段），20段=3+17，正式考点≤5个。
- `ch05-17` 和 `ch05-18` 拆分 §5.5.1 转置卷积（35段→17+18），均为公式密集。
- **经典架构单元（ch05-13~ch05-16）特殊约束**：不考年份、不考比赛背景（ILSVRC等）、不考配置表记忆（层数/通道数/参数量），只考结构动机和核心机制。LeNet-5 C3连接表（`¶0196`）标为"了解即可"。
- `ch05-06`（卷积交换性, 8段）正式考点3个，为低段数单元。
- `¶0292-¶0299` 为习题，`¶0300-¶0319` 为参考文献，不进入任何教学单元的正式题范围。
- `¶0069`、`¶0095`、`¶0183`、`¶0238` 为小节标题段，不单独设考点。
- 第6章仍未解锁，待第5章章测通过后再解锁。
