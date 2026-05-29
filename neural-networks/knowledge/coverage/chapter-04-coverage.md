# 第4章 覆盖审计表

本表用于审计第4章是否形成稳定闭环。AI 教学第4章时，应以 `learning-path/chapter-04.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch04-00` | 第4章 引言 | `knowledge/teaching-guides/chapter-04/04-00-introduction.teaching.md` | `¶0001-¶0007` | ANN定义（受生物学启发的数学模型）；PDP模型三特性（分布式表示/连接存储/连接学习）；CNN的两个问题（参数太多/局部不变性）过渡到第4章动机 | 第4章引言 | `ch04-01` |
| 2 | `ch04-01` | §4.1 神经元 | `knowledge/teaching-guides/chapter-04/04-01-neuron.teaching.md` | `¶0008-¶0024` | 神经元模型：净输入z=wᵀx+b；激活函数a=f(z)的作用；激活函数必须非线性（否则多层等价于单层）；常见激活函数家族概览 | 神经元 | `ch04-02` |
| 3 | `ch04-02` | §4.1.1 Sigmoid型函数 | `knowledge/teaching-guides/chapter-04/04-02-sigmoid-functions.teaching.md` | `¶0025-¶0037` | Logistic函数σ(z)=1/(1+e⁻ᶻ)性质（值域0-1/单调递增/平滑）；Tanh函数性质（值域-1~1/零中心）；Sigmoid饱和区导致梯度消失的直觉 | Sigmoid型函数 | `ch04-03` |
| 4 | `ch04-03` | §4.1.1.1 Hard-Logistic和Hard-Tanh | `knowledge/teaching-guides/chapter-04/04-03-hard-sigmoid.teaching.md` | `¶0038-¶0057` | Hard-Logistic/Tanh是用分段线性函数近似Sigmoid/Tanh；硬饱和与软饱和的区别；Taylor展开的近似来源（只讲动机，不推导）；计算效率优势 | Hard-Logistic和Hard-Tanh | `ch04-04` |
| 5 | `ch04-04` | §4.1.2 ReLU + §4.1.2.1 带泄露的ReLU | `knowledge/teaching-guides/chapter-04/04-04-relu-and-leaky-relu.teaching.md` | `¶0058-¶0074` | ReLU定义f(z)=max(0,z)；ReLU优点（单侧饱和计算高效/缓解梯度消失/稀疏激活）；ReLU的Dying ReLU问题；Leaky ReLU解决Dying ReLU的思路 | ReLU与Leaky ReLU | `ch04-05` |
| 6 | `ch04-05` | §4.1.2.2 PReLU + §4.1.2.3 ELU + §4.1.2.4 Softplus | `knowledge/teaching-guides/chapter-04/04-05-relu-variants.teaching.md` | `¶0075-¶0088` | PReLU：α可学习（从数据中学）；ELU：负半轴指数衰减→均值更接近零；Softplus：ReLU的平滑近似；三种变体的核心改进方向 | ReLU变体 | `ch04-06` |
| 7 | `ch04-06` | §4.1.3 Swish + §4.1.4 GELU | `knowledge/teaching-guides/chapter-04/04-06-swish-and-gelu.teaching.md` | `¶0089-¶0101` | Swish：自门控机制z·σ(z)；GELU：用高斯累积分布做门控；两种激活函数的共性（平滑自门控）；门控激活函数的概念直觉 | Swish与GELU | `ch04-07` |
| 8 | `ch04-07` | §4.1.5 Maxout单元 | `knowledge/teaching-guides/chapter-04/04-07-maxout.teaching.md` | `¶0102-¶0110` | Maxout：取多组线性映射的最大值；Maxout=分段线性→可逼近任意凸函数；Maxout与ReLU的关系（ReLU是Maxout特例）；参数增加k倍的代价 | Maxout单元 | `ch04-08` |
| 9 | `ch04-08` | §4.2 网络结构（三种类型） | `knowledge/teaching-guides/chapter-04/04-08-network-structures.teaching.md` | `¶0111-¶0126` | 三类网络结构定义；前馈网络（无环有向图/单向信息流）；记忆网络（反馈连接/内部状态）；图网络（节点+边处理图结构数据）；三者区别和适用场景 | 网络结构 | `ch04-09` |
| 10 | `ch04-09` | §4.3 前馈神经网络 | `knowledge/teaching-guides/chapter-04/04-09-feedforward-neural-network.teaching.md` | `¶0127-¶0146` | 前馈神经网络层结构；第l层符号体系（表4.1记号）；信息前向传播a^(l)=f_l(W^(l)a^(l-1)+b^(l))；深层网络=多次非线性变换复合；输出层设计取决于任务类型 | 前馈神经网络 | `ch04-10` |
| 11 | `ch04-10` | §4.3.1 通用近似定理 | `knowledge/teaching-guides/chapter-04/04-10-universal-approximation.teaching.md` | `¶0147-¶0158` | 定理4.1通用近似定理陈述；单隐藏层+足够神经元可逼近任意连续函数；定理只保证"存在"不保证"可学到"；宽度vs深度的逼近效率差异 | 通用近似定理 | `ch04-11` |
| 12 | `ch04-11` | §4.3.2 应用到机器学习 | `knowledge/teaching-guides/chapter-04/04-11-fnn-machine-learning.teaching.md` | `¶0159-¶0173` | 回归任务→恒等输出+平方损失；二分类→Sigmoid输出+交叉熵损失；多分类→Softmax输出+交叉熵损失；输出层设计=任务驱动的选择 | 应用到机器学习 | `ch04-12` |
| 13 | `ch04-12` | §4.3.3 参数学习 | `knowledge/teaching-guides/chapter-04/04-12-fnn-parameter-learning.teaching.md` | `¶0174-¶0188` | 前馈网络参数学习=损失对W和b求梯度；梯度消失是深层网络的梯度计算难题；反向传播的引入动机；计算图与链式法则的关系 | FNN参数学习 | `ch04-13` |
| 14 | `ch04-13` | 反向传播算法（上） | `knowledge/teaching-guides/chapter-04/04-13-backpropagation-1.teaching.md` | `¶0189-¶0206` | 反向传播的梯度计算目标；链式法则分解∂L/∂W=∂L/∂z·∂z/∂W；误差项的定义与可复用作用；∂z/∂w 和 ∂z/∂b 的结果 | 反向传播（上） | `ch04-14` |
| 15 | `ch04-14` | 反向传播算法（中） | `knowledge/teaching-guides/chapter-04/04-14-backpropagation-2.teaching.md` | `¶0207-¶0223` | 误差反向传播的递归公式δ^(l)=f'(z^(l))⊙(W^(l+1))ᵀδ^(l+1)；"反向"的直觉含义（从输出层向前递推）；逐元素乘（⊙）的作用 | 反向传播（中） | `ch04-15` |
| 16 | `ch04-15` | 反向传播算法（下） | `knowledge/teaching-guides/chapter-04/04-15-backpropagation-3.teaching.md` | `¶0224-¶0241` | 最终梯度公式∂L/∂W^(l)=δ^(l)(a^(l-1))ᵀ和∂L/∂b^(l)=δ^(l)；算法4.1反向传播SGD训练流程；前向-反向-更新三步循环 | 反向传播（下） | `ch04-16` |
| 17 | `ch04-16` | §4.5 + §4.5.1 数值微分 + §4.5.2 符号微分 | `knowledge/teaching-guides/chapter-04/04-16-gradient-computation-methods.teaching.md` | `¶0242-¶0258` | 三种梯度计算方式（数值/符号/自动微分）；数值微分=定义法（慢/有舍入误差）；符号微分=公式推导（表达式膨胀问题）；自动微分优于前两种的原因 | 梯度计算方法 | `ch04-17` |
| 18 | `ch04-17` | §4.5.3 自动微分（上） | `knowledge/teaching-guides/chapter-04/04-17-automatic-differentiation-1.teaching.md` | `¶0259-¶0277` | 自动微分核心思想：计算图分解+链式法则自动组合；计算图定义（节点=操作/边=数据流）；表4.2基本操作的导数规则；计算图上的链式法则 | 自动微分（上） | `ch04-18` |
| 19 | `ch04-18` | §4.5.3 自动微分（中） | `knowledge/teaching-guides/chapter-04/04-18-automatic-differentiation-2.teaching.md` | `¶0278-¶0295` | 前向模式自动微分：从输入向输出方向计算梯度；前向模式的雅可比向量积解释；前向模式的计算量与输入维度n成正比 | 自动微分（中） | `ch04-19` |
| 20 | `ch04-19` | §4.5.3 自动微分（下） | `knowledge/teaching-guides/chapter-04/04-19-automatic-differentiation-3.teaching.md` | `¶0296-¶0310` | 反向模式自动微分：从输出向输入方向计算梯度；反向模式与反向传播的关系；前向vs反向选择原则（n≪m用前向/n≫m用反向） | 自动微分（下） | `ch04-20` |
| 21 | `ch04-20` | §4.6 + §4.6.1 非凸优化问题 | `knowledge/teaching-guides/chapter-04/04-20-nonconvex-optimization.teaching.md` | `¶0311-¶0317` | 神经网络损失函数的非凸性；局部极小vs全局极小；鞍点问题（高维空间中更常见）；非凸优化≠无法训练 | 非凸优化 | `ch04-21` |
| 22 | `ch04-21` | §4.6.2 梯度消失问题 | `knowledge/teaching-guides/chapter-04/04-21-vanishing-gradient.teaching.md` | `¶0318-¶0329` | 梯度消失定义（深层梯度指数级衰减）；Sigmoid饱和是梯度消失的主因之一；梯度消失导致浅层参数几乎不更新；ReLU缓解梯度消失的机制 | 梯度消失问题 | `ch04-22` |
| 23 | `ch04-22` | §4.7 总结和深入阅读 | `knowledge/teaching-guides/chapter-04/04-22-summary-and-reading.teaching.md` | `¶0330-¶0336` | 前馈网络核心组件串联（神经元→层→网络→学习算法）；常见激活函数对比（表4.3）；BP+自动微分的统一视角；前馈网络是后续CNN/RNN的基础 | 总结和深入阅读 | `ch04-test` |
| 24 | `ch04-test` | 第4章章测 | 无新增讲义；覆盖第4章已通过单元 | 第4章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第4章章测 | 第5章未解锁 |

## 当前审计结论

- 第4章 23 个教学单元（`ch04-00` ~ `ch04-22`）均有教学指引和教材段落。
- `ch04-03`（Hard-Logistic/Tanh, 20段非公式密集）正式考点控制在≤5个，超过则拆分。
- `ch04-04` 合并 ReLU（`¶0058-¶0067`）和 Leaky ReLU（`¶0068-¶0074`），17段=10+7。
- `ch04-05` 合并 PReLU（`¶0075-¶0078`）+ ELU（`¶0079-¶0083`）+ Softplus（`¶0084-¶0088`），14段=4+5+5。
- `ch04-06` 合并 Swish（`¶0089-¶0095`）和 GELU（`¶0096-¶0101`），13段=7+6。
- `ch04-08` 合并 §4.2/§4.2.1/§4.2.2/§4.2.3（三种网络结构），16段=3+2+3+8。
- `ch04-09`（前馈神经网络, 20段非公式密集）正式考点控制在≤5个，超过则拆分。
- `ch04-13`~`ch04-15` 拆分反向传播算法（53段→18+17+18），均为公式密集，正式题考概念和流程不考完整推导。
- `ch04-16` 合并 §4.5/§4.5.1/§4.5.2（梯度计算方法概述+数值+符号），17段。
- `ch04-17`~`ch04-19` 拆分自动微分（52段→19+18+15），均为公式密集。
- 教材中反向传播算法无小节编号（§4.4缺失），路线以"反向传播算法（上/中/下）"标注。
- `¶0337-¶0346` 为习题，`¶0347-¶0369` 为参考文献，不进入任何教学单元的正式题范围。
- 第5章仍未解锁，待第4章章测通过后再解锁。
