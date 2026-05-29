# 第12章 覆盖审计表

本表用于审计第12章是否形成稳定闭环。AI 教学第12章时，应以 `learning-path/chapter-12.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch12-00` | 第12章 引言 | `knowledge/teaching-guides/chapter-12/12-00-introduction.teaching.md` | `¶0001-¶0006` | DBN定位（概率图模型、学习变量间复杂依赖）；多层隐变量+内部特征表示+非线性降维；BM/DBN都是生成模型；推断学习需MCMC近似；BM/DBN与神经网络对应→SNN | 第12章引言 | `ch12-01` |
| 2 | `ch12-01` | §12.1 BM定义与能量函数 | `knowledge/teaching-guides/chapter-12/12-01-bm-definition-energy.teaching.md` | `¶0007-¶0020` | BM三个性质（二值、全连接、对称）；联合概率$p(x)=(1/Z)\exp(-E(x)/T)$；能量函数$E(x)$的定义和两项含义；权重$w_{ij}$正负对能量和概率的影响 | BM定义与能量函数 | `ch12-02` |
| 3 | `ch12-02` | §12.1 玻尔兹曼分布背景 | `knowledge/teaching-guides/chapter-12/12-02-boltzmann-background.teaching.md` | `¶0021-¶0028` | 权重作为假设间弱约束（正=支持、负=互斥）；BM两类问题（搜索问题vs学习问题） | 玻尔兹曼分布背景 | `ch12-03` |
| 4 | `ch12-03` | §12.1.1 BM生成模型与全条件概率 | `knowledge/teaching-guides/chapter-12/12-03-bm-generative-conditional.teaching.md` | `¶0029-¶0035` | 配分函数Z难以计算→需要MCMC近似；全条件概率$p(x_i\mid x_{\backslash i})$定义；Theorem 12.1结论公式的含义 | BM生成模型与全条件概率 | `ch12-04` |
| 5 | `ch12-04` | §12.1.1 Theorem 12.1证明链 | `knowledge/teaching-guides/chapter-12/12-04-theorem-12-1-proof.teaching.md` | `¶0036-¶0049` | 能量差$\Delta E_i$的定义和推导；$E(x)=-T\log p(x)-T\log Z$的桥梁作用；能量差→概率比→sigmoid的完整逻辑链 | Theorem 12.1证明链 | `ch12-05` |
| 6 | `ch12-05` | §12.1.1 Gibbs采样 + §12.1.2 模拟退火 | `knowledge/teaching-guides/chapter-12/12-05-gibbs-simulated-annealing.teaching.md` | `¶0050-¶0065` | Gibbs采样流程和热平衡概念；温度T对随机性/收敛速度的影响；T→0时BM退化为Hopfield网络；模拟退火基本思想 | Gibbs采样与模拟退火 | `ch12-06` |
| 7 | `ch12-06` | §12.1.3 BM参数学习：梯度推导 | `knowledge/teaching-guides/chapter-12/12-06-bm-param-learning-gradient.teaching.md` | `¶0066-¶0078` | 对数似然函数定义和边际分布；梯度两项期望结构（正相/负相）；精确计算不可行的原因 | BM参数学习：梯度推导 | `ch12-07` |
| 8 | `ch12-07` | §12.1.3 BM更新规则与Hebb类比 | `knowledge/teaching-guides/chapter-12/12-07-bm-update-hebb.teaching.md` | `¶0079-¶0087` | $w_{ij}$更新公式中$\langle\cdot\rangle_{\mathrm{data}}$和$\langle\cdot\rangle_{\mathrm{model}}$的含义；偏置更新的对称结构；BM更新规则与Hebb规则的类比 | BM更新规则与Hebb类比 | `ch12-08` |
| 9 | `ch12-08` | §12.2 RBM定义与能量函数 | `knowledge/teaching-guides/chapter-12/12-08-rbm-definition-energy.teaching.md` | `¶0088-¶0103` | RBM二分图结构（同层无连接、不同层全连接）；RBM能量函数三项含义；联合概率与能量函数的关系；RBM与全连接BM的结构差异 | RBM定义与能量函数 | `ch12-09` |
| 10 | `ch12-09` | §12.2.1 RBM条件独立与定理陈述 | `knowledge/teaching-guides/chapter-12/12-09-rbm-conditional-independence.teaching.md` | `¶0104-¶0113` | RBM条件独立性的来源（二分图结构）；条件独立性的数学公式；Theorem 12.2两个条件概率sigmoid公式 | RBM条件独立与定理陈述 | `ch12-10` |
| 11 | `ch12-10` | §12.2.1 Theorem 12.2证明 | `knowledge/teaching-guides/chapter-12/12-10-theorem-12-2-proof.teaching.md` | `¶0114-¶0131` | 边际概率写法（第一步）；分配律交换的关键作用（第二步，依赖条件独立性）；固定$h_j=1$求联合→除边际→得条件的技巧 | Theorem 12.2证明 | `ch12-11` |
| 12 | `ch12-11` | §12.2.1 RBM Block Gibbs采样 | `knowledge/teaching-guides/chapter-12/12-11-rbm-block-gibbs.teaching.md` | `¶0132-¶0143` | $p(v_i=1\mid\mathbf{h})$与$p(h_j=1\mid\mathbf{v})$的对称性；向量形式与并行采样能力；Block Gibbs采样交替流程；RBM并行采样比BM高效的原因 | RBM Block Gibbs采样 | `ch12-12` |
| 13 | `ch12-12` | §12.2.2 RBM参数学习 | `knowledge/teaching-guides/chapter-12/12-12-rbm-param-learning.teaching.md` | `¶0144-¶0160` | 三参数梯度的"数据期望-模型期望"结构；$w_{ij},a_i,b_j$三个更新规则的差异；RBM采样效率比BM高的原因；$\langle\cdot\rangle_{\mathrm{data}}$和$\langle\cdot\rangle_{\mathrm{model}}$的含义 | RBM参数学习 | `ch12-13` |
| 14 | `ch12-13` | §12.2.2.1 CD + §12.2.3 RBM类型 | `knowledge/teaching-guides/chapter-12/12-13-cd-rbm-types.teaching.md` | `¶0161-¶0174` | CD算法核心思想（训练样本初始化+k步采样）；CD-k流程中的正向/反向梯度；BB-RBM/GB-RBM/BG-RBM三种类型的能量函数差异 | CD与RBM类型 | `ch12-14` |
| 15 | `ch12-14` | §12.3 DBN结构与联合概率 | `knowledge/teaching-guides/chapter-12/12-14-dbn-structure-joint.teaching.md` | `¶0175-¶0190` | DBN混合图结构（有向边+无向顶层）；联合概率分解公式每项含义；Sigmoid信念网络条件概率形式；DBN自顶向下生成采样流程 | DBN结构与联合概率 | `ch12-15` |
| 16 | `ch12-15` | §12.3.2 参数学习+逐层预训练 | `knowledge/teaching-guides/chapter-12/12-15-dbn-pretraining.teaching.md` | `¶0191-¶0204` | 贡献度分配问题的本质；SBN→RBM转换的关键好处（后验独立）；逐层预训练自下而上流程；逐层预训练的历史意义 | DBN逐层预训练 | `ch12-16` |
| 17 | `ch12-16` | §12.3.2.2 精调 | `knowledge/teaching-guides/chapter-12/12-16-dbn-finetuning.teaching.md` | `¶0205-¶0212` | 两种精调模式（生成精调vs判别精调）；Wake-Sleep算法两阶段；判别精调中预训练的作用；双向权重概念 | DBN精调 | `ch12-17` |
| 18 | `ch12-17` | §12.4 总结和深入阅读 | `knowledge/teaching-guides/chapter-12/12-17-summary-and-reading.teaching.md` | `¶0213-¶0219` | BM→RBM→DBN发展脉络；DBN历史贡献（预训练+开启深度学习浪潮）；CDBN/DBM/自编码器等替代方案的存在；现代方法使预训练不再必需 | 总结和深入阅读 | `ch12-test` |
| 19 | `ch12-test` | 第12章章测 | 无新增讲义；覆盖第12章已通过单元 | 第12章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第12章章测 | 第13章未解锁 |

## 当前审计结论

- 第12章共19个单元（18教学 + 1章测），覆盖教学段落 `¶0001-¶0219`。
- 玻尔兹曼分布侧栏（¶0023-¶0028）在ch12-02中标记为了解即可，不进入正式题。
- 习题 `¶0220-¶0228` 和参考文献 `¶0229-¶0246` 不进入任何单元。
- "参见第11.5.4.3/8.6.1/11.1.2.1节" 等交叉引用已标记为课堂识别不计分，不进入正式题。
- 所有人名、年份在总结单元（ch12-17）中均为了解即可。
