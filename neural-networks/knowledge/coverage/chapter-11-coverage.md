# 第11章 覆盖审计表

本表用于审计第11章是否形成稳定闭环。AI 教学第11章时，应以 `learning-path/chapter-11.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch11-00` | 第11章 引言 | `knowledge/teaching-guides/chapter-11/11-00-pgm-motivation.teaching.md` | `¶0001-¶0009` | PGM 定义与目的；高维联合概率的参数量爆炸问题；独立性假设减少参数量的基本思想；链式法则分解形式 | 第11章引言 | `ch11-01` |
| 2 | `ch11-01` | 条件独立性 | `knowledge/teaching-guides/chapter-11/11-01-conditional-independence.teaching.md` | `¶0010-¶0018` | 条件独立的直观含义；四变量例子的条件独立关系；条件独立如何减少参数量(15到9) | 条件独立性 | `ch11-02` |
| 3 | `ch11-02` | 图模型基本问题 | `knowledge/teaching-guides/chapter-11/11-02-graphical-model-basics.teaching.md` | `¶0019-¶0025` | 图模型三大基本问题(表示/学习/推断)；图模型作为机器学习新视角的意义 | 图模型基本问题 | `ch11-03` |
| 4 | `ch11-03` | §11.1 图类型与贝叶斯网络 | `knowledge/teaching-guides/chapter-11/11-03-graph-types-and-bayesian-network.teaching.md` | `¶0026-¶0037` | 有向图与无向图的区别；贝叶斯网络的定义；联合概率的因子分解 | 图类型与贝叶斯网络 | `ch11-04` |
| 5 | `ch11-04` | §11.1.1 条件独立关系 | `knowledge/teaching-guides/chapter-11/11-04-conditional-independence-relations.teaching.md` | `¶0038-¶0053` | 四种条件独立关系(间接因果/间接果因/共因/共果)的判断与命名；局部马尔可夫性质 | 条件独立关系 | `ch11-05` |
| 6 | `ch11-05` | §11.1.2.1 Sigmoid信念网络 | `knowledge/teaching-guides/chapter-11/11-05-sigmoid-belief-network.teaching.md` | `¶0054-¶0063` | SBN 的定义与参数化建模动机；SBN 条件概率的 Logistic 形式；SBN 与 Logistic 回归的区别(生成vs判别) | Sigmoid信念网络 | `ch11-06` |
| 7 | `ch11-06` | §11.1.2.2 朴素贝叶斯分类器 | `knowledge/teaching-guides/chapter-11/11-06-naive-bayes-classifier.teaching.md` | `¶0064-¶0074` | NB 的朴素条件独立假设；NB 的图模型结构；NB 的实际有效性 | 朴素贝叶斯分类器 | `ch11-07` |
| 8 | `ch11-07` | §11.1.2.3 隐马尔可夫模型 | `knowledge/teaching-guides/chapter-11/11-07-hidden-markov-model.teaching.md` | `¶0075-¶0082` | HMM 的图结构(隐变量链+观测变量)；HMM 联合概率分解；转移概率与输出概率的含义 | 隐马尔可夫模型 | `ch11-08` |
| 9 | `ch11-08` | §11.1.3 马尔可夫随机场 | `knowledge/teaching-guides/chapter-11/11-08-markov-random-field.teaching.md` | `¶0083-¶0090` | MRF 的定义；无向图的局部马尔可夫性质；MRF 中的条件独立关系判断 | 马尔可夫随机场 | `ch11-09` |
| 10 | `ch11-09` | §11.1.4 团与Hammersley-Clifford | `knowledge/teaching-guides/chapter-11/11-09-clique-and-hammersley-clifford.teaching.md` | `¶0091-¶0101` | 团与最大团的定义；Hammersley-Clifford 定理的意义；势能函数与配分函数的概念；配分函数的计算复杂度 | 团与Hammersley-Clifford | `ch11-10` |
| 11 | `ch11-10` | §11.1.4 吉布斯与玻尔兹曼分布 | `knowledge/teaching-guides/chapter-11/11-10-gibbs-and-boltzmann-distribution.teaching.md` | `¶0102-¶0111` | Gibbs 分布与 MRF 的等价关系；能量函数与势能函数的关系；玻尔兹曼分布的形式 | 吉布斯与玻尔兹曼分布 | `ch11-11` |
| 12 | `ch11-11` | §11.1.5.1 对数线性模型 | `knowledge/teaching-guides/chapter-11/11-11-log-linear-model.teaching.md` | `¶0112-¶0123` | 对数线性模型的势能函数形式；对数线性模型与Softmax回归的关系；条件对数线性模型的因子分解 | 对数线性模型 | `ch11-12` |
| 13 | `ch11-12` | §11.1.5.2 条件随机场 | `knowledge/teaching-guides/chapter-11/11-12-conditional-random-field.teaching.md` | `¶0124-¶0133` | CRF 的定义与直接建模条件概率的特点；线性链CRF的因子分解结构；状态特征与转移特征的含义 | 条件随机场 | `ch11-13` |
| 14 | `ch11-13` | §11.1.6 道德化 | `knowledge/teaching-guides/chapter-11/11-13-moralization.teaching.md` | `¶0134-¶0141` | 道德化的定义与目的；道德图中独立性的丢失；有向图转无向图的应用场景 | 道德化 | `ch11-14` |
| 15 | `ch11-14` | §11.2 学习概述与有向图参数 | `knowledge/teaching-guides/chapter-11/11-14-learning-overview-and-directed-parameter.teaching.md` | `¶0142-¶0152` | 图模型学习的两个部分(结构/参数)；有向图参数估计的独立性分解；离散与连续变量的参数化选择 | 学习概述与有向图参数 | `ch11-15` |
| 16 | `ch11-15` | §11.2.1 无向图参数估计 | `knowledge/teaching-guides/chapter-11/11-15-undirected-parameter-estimation.teaching.md` | `¶0153-¶0170` | 无向图参数估计的梯度形式；经验分布期望=模型分布期望的最优条件；无向图参数估计复杂度来源 | 无向图参数估计 | `ch11-16` |
| 17 | `ch11-16` | §11.2.2 隐变量与边际似然 | `knowledge/teaching-guides/chapter-11/11-16-latent-variables-and-marginal-likelihood.teaching.md` | `¶0171-¶0180` | 含隐变量时的边际似然函数；对数内求和的困难；盘子表示法的含义 | 隐变量与边际似然 | `ch11-17` |
| 18 | `ch11-17` | §11.2.2.1 ELBO与EM框架 | `knowledge/teaching-guides/chapter-11/11-17-elbo-and-em-framework.teaching.md` | `¶0181-¶0191` | ELBO的定义与Jensen不等式的推导；ELBO与对数边际似然的关系；EM算法两阶段框架 | ELBO与EM框架 | `ch11-18` |
| 19 | `ch11-18` | §11.2.2.1 EM的E步和M步 | `knowledge/teaching-guides/chapter-11/11-18-em-e-step-and-m-step.teaching.md` | `¶0192-¶0200` | E步的目标(找q使ELBO等于log p)；M步的目标(最大化ELBO求参数)；E步中后验推断的困难 | EM的E步和M步 | `ch11-19` |
| 20 | `ch11-19` | §11.2.2.1 EM收敛性与信息论视角 | `knowledge/teaching-guides/chapter-11/11-19-em-convergence-and-information-theory.teaching.md` | `¶0201-¶0214` | EM收敛性的证明逻辑(每次迭代边际似然不降)；log p = ELBO + KL的分解；KL散度视角下EM的直观理解 | EM收敛性与信息论视角 | `ch11-20` |
| 21 | `ch11-20` | §11.2.2.1 EM迭代图示 | `knowledge/teaching-guides/chapter-11/11-20-em-iteration-illustration.teaching.md` | `¶0215-¶0224` | EM迭代的三个阶段(E步前/E步/M步)图示理解；KL散度与ELBO在迭代中的变化 | EM迭代图示 | `ch11-21` |
| 22 | `ch11-21` | §11.2.2.2 GMM定义 | `knowledge/teaching-guides/chapter-11/11-21-gmm-definition.teaching.md` | `¶0225-¶0240` | GMM作为多个高斯加权组合的定义；隐变量z的多项分布先验；GMM的生成过程；GMM的图模型结构 | GMM定义 | `ch11-22` |
| 23 | `ch11-22` | §11.2.2.2 GMM的E步 | `knowledge/teaching-guides/chapter-11/11-22-gmm-e-step.teaching.md` | `¶0241-¶0250` | GMM-E步的后验概率计算；责任值的含义；后验概率公式的贝叶斯推导 | GMM的E步 | `ch11-23` |
| 24 | `ch11-23` | §11.2.2.2 GMM的M步与算法 | `knowledge/teaching-guides/chapter-11/11-23-gmm-m-step-and-algorithm.teaching.md` | `¶0251-¶0266` | GMM-M步的ELBO形式；拉格朗日乘数法求解参数更新公式；GMM完整EM算法流程 | GMM的M步与算法 | `ch11-24` |
| 25 | `ch11-24` | §11.2.2.2 GMM训练示例 | `knowledge/teaching-guides/chapter-11/11-24-gmm-training-example.teaching.md` | `¶0267-¶0273` | GMM训练过程中高斯分布逐渐拟合数据的直观理解；迭代收敛的视觉变化 | GMM训练示例 | `ch11-25` |
| 26 | `ch11-25` | §11.3 推断问题定义 | `knowledge/teaching-guides/chapter-11/11-25-inference-problem-definition.teaching.md` | `¶0274-¶0281` | 推断问题的形式化定义(求p(q|e))；边际概率计算是推断的核心；精确推断与近似推断的分类 | 推断问题定义 | `ch11-26` |
| 27 | `ch11-26` | §11.3.1.1 变量消除法 | `knowledge/teaching-guides/chapter-11/11-26-variable-elimination.teaching.md` | `¶0282-¶0296` | 变量消除法的动态规划思想；乘法分配律减少计算量的原理；消除顺序对复杂度的影响；重复计算问题 | 变量消除法 | `ch11-27` |
| 28 | `ch11-27` | §11.3.1.2 信念传播链式结构 | `knowledge/teaching-guides/chapter-11/11-27-belief-propagation-chain.teaching.md` | `¶0297-¶0309` | BP算法的基本思想(保存消息避免重复)；链式结构MRF的联合概率形式；直接计算边际概率的指数级复杂度 | 信念传播链式结构 | `ch11-28` |
| 29 | `ch11-28` | §11.3.1.2 链式消息传递 | `knowledge/teaching-guides/chapter-11/11-28-chain-message-passing.teaching.md` | `¶0310-¶0322` | 前向与反向消息的递归定义；消息传递的计算复杂度O(TK^2)；配分函数的计算 | 链式消息传递 | `ch11-29` |
| 30 | `ch11-29` | §11.3.1.2 树结构信念传播 | `knowledge/teaching-guides/chapter-11/11-29-tree-belief-propagation.teaching.md` | `¶0323-¶0328` | 树结构图模型的条件；树结构消息传递的两阶段过程；环路时的联合树算法 | 树结构信念传播 | `ch11-30` |
| 31 | `ch11-30` | §11.3.2 近似推断概述 | `knowledge/teaching-guides/chapter-11/11-30-approximate-inference-overview.teaching.md` | `¶0329-¶0334` | 近似推断的三种主要方法(LBP/变分推断/采样法)；每种方法的基本思想和适用场景 | 近似推断概述 | `ch11-31` |
| 32 | `ch11-31` | §11.4 变分推断公式化 | `knowledge/teaching-guides/chapter-11/11-31-variational-inference-formulation.teaching.md` | `¶0335-¶0348` | 变分法的基本概念(函数vs泛函)；变分推断的目标(用q(z)近似p(z|x))；KL散度最小化的优化问题形式 | 变分推断公式化 | `ch11-32` |
| 33 | `ch11-32` | §11.4 ELBO最大化 | `knowledge/teaching-guides/chapter-11/11-32-elbo-maximization.teaching.md` | `¶0349-¶0356` | log p = ELBO + KL 分解在变分推断中的作用；KL最小化等价于ELBO最大化；变分推断与EM算法的关系 | ELBO最大化 | `ch11-33` |
| 34 | `ch11-33` | §11.4 平均场 | `knowledge/teaching-guides/chapter-11/11-33-mean-field.teaching.md` | `¶0357-¶0364` | 平均场分布族的定义(各组分独立)；平均场下ELBO的分解形式；候选分布族复杂度与优化复杂度的关系 | 平均场 | `ch11-34` |
| 35 | `ch11-34` | §11.4 坐标上升与VAE | `knowledge/teaching-guides/chapter-11/11-34-coordinate-ascent-and-vae.teaching.md` | `¶0365-¶0380` | 坐标上升法优化q_j的迭代过程；最优q_j与对数联合概率期望的关系；变分推断在EM中的应用；VAE的基本思想(仅限¶0379-¶0380提及) | 坐标上升与VAE | `ch11-35` |
| 36 | `ch11-35` | §11.5 蒙特卡罗原理 | `knowledge/teaching-guides/chapter-11/11-35-monte-carlo-principles.teaching.md` | `¶0381-¶0391` | 采样法的目标和基本思想；蒙特卡罗方法的定义和历史背景；期望计算的采样近似原理 | 蒙特卡罗原理 | `ch11-36` |
| 37 | `ch11-36` | §11.5.1 大数定律与随机采样 | `knowledge/teaching-guides/chapter-11/11-36-law-of-large-numbers.teaching.md` | `¶0392-¶0403` | 大数定律是采样法的理论依据；样本均值收敛于期望；逆CDF采样法；复杂分布难以直接采样的原因 | 大数定律与随机采样 | `ch11-37` |
| 38 | `ch11-37` | §11.5.2 拒绝采样 | `knowledge/teaching-guides/chapter-11/11-37-rejection-sampling.teaching.md` | `¶0404-¶0414` | 拒绝采样的基本思想(提议分布+接受概率)；接受概率的公式；采样效率与kq(x)和p(x)的关系；高维空间效率低的局限 | 拒绝采样 | `ch11-38` |
| 39 | `ch11-38` | §11.5.3 重要性采样 | `knowledge/teaching-guides/chapter-11/11-38-importance-sampling.teaching.md` | `¶0415-¶0430` | 重要性采样的基本思想(重要性权重)；期望变换公式；未归一化分布下的重要性采样 | 重要性采样 | `ch11-39` |
| 40 | `ch11-39` | §11.5.4 MCMC引入与MH动机 | `knowledge/teaching-guides/chapter-11/11-39-mcmc-intro-and-mh-motivation.teaching.md` | `¶0431-¶0439` | MCMC的核心思想(马尔可夫链平稳分布)；平稳分布与目标分布的关系；预烧期与样本独立性问题；MH算法的动机(修正提议分布) | MCMC引入与MH动机 | `ch11-40` |
| 41 | `ch11-40` | §11.5.4.1 MH算法与Metropolis | `knowledge/teaching-guides/chapter-11/11-40-mh-algorithm-and-metropolis.teaching.md` | `¶0440-¶0457` | MH算法的接受概率公式；细致平稳条件的证明思路；Metropolis算法作为MH特例(对称提议分布时) | MH算法与Metropolis | `ch11-41` |
| 42 | `ch11-41` | §11.5.4.3 吉布斯采样 | `knowledge/teaching-guides/chapter-11/11-41-gibbs-sampling.teaching.md` | `¶0458-¶0475` | Gibbs采样作为MH特例(全条件概率为提议分布,接受率=1)；全条件概率的定义；逐维采样的迭代过程；细致平稳条件的验证 | 吉布斯采样 | `ch11-42` |
| 43 | `ch11-42` | §11.6 总结和深入阅读 | `knowledge/teaching-guides/chapter-11/11-42-summary-and-reading.teaching.md` | `¶0476-¶0483` | 图模型的核心优势(条件独立性可视化)；图模型与神经网络的异同；生成vs判别的定位 | 总结和深入阅读 | `ch11-test` |
| 44 | `ch11-test` | 第11章章测 | 无新增讲义；覆盖第11章已通过单元 | 第11章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、习题、了解即可内容不计入章测 | 第11章章测 | 下一章未解锁 |

## 覆盖审计备注

- `ch11-04` (¶0038-¶0053)：四种条件独立关系与局部马尔可夫性质必须连续讲解，不宜拆分。16段非公式密集，但四种关系(间接因果/间接果因/共因/共果)需要在同一单元内对比讲清。
- `ch11-18` = ¶0192-¶0200, `ch11-19` = ¶0201-¶0214：段落不重叠，为两个独立教学单元。ch11-18聚焦E步/M步的操作定义，ch11-19聚焦收敛性证明和信息论视角。
- `ch11-34`：VAE仅按教材当前段落 ¶0379-¶0380 作连接性提及，不作为正式题，不展开第13章内容。
- 总教学单元：43个教学单元 + 1个章测 = 44行。

## 当前审计结论

- 第11章 43 个教学单元均有教学指引和教材段落。
- ¶0484-¶0499 为习题，¶0500-¶0516 为参考文献，均不进入正式题范围。
- 后文章节引用(Boltzmann→Ch12, VAE/GAN→Ch13, GNN等)在对应单元中标注为"了解即可"，不出正式题。
