# 第9章 覆盖审计表

本表用于审计第9章是否形成稳定闭环。AI 教学第9章时，应以 `learning-path/chapter-09.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch09-00` | 第9章 引言 | `knowledge/teaching-guides/chapter-09/09-00-introduction.teaching.md` | `¶0001-¶0011` | 无监督学习定义；三类无监督学习问题（特征学习、密度估计、聚类）；无监督特征学习用途；参数与非参数密度估计的区别；无监督学习三要素 | 第9章引言 | `ch09-01` |
| 2 | `ch09-01` | §9.1.1 主成分分析（投影与方差最大化） | `knowledge/teaching-guides/chapter-09/09-01-pca-projection.teaching.md` | `¶0012-¶0022` | PCA 定义与目标（投影方差最大）；投影向量约束 w^T w=1；投影表示公式 z^(n)=w^T x^(n)；投影方差公式；协方差矩阵 Σ | PCA投影与方差最大化 | `ch09-02` |
| 3 | `ch09-02` | §9.1.1 主成分分析（特征分解与多维投影） | `knowledge/teaching-guides/chapter-09/09-02-pca-eigendecomposition.teaching.md` | `¶0023-¶0033` | 拉格朗日方法推导 Σw=λw；PCA 转化为特征值分解；λ 即为投影方差；多维投影取前 D' 个最大特征值对应特征向量；PCA 不保证类别可分性 | PCA特征分解与多维投影 | `ch09-03` |
| 4 | `ch09-03` | §9.1.2 稀疏编码（动机与编码定义） | `knowledge/teaching-guides/chapter-09/09-03-sparse-coding-motivation.teaching.md` | `¶0034-¶0044` | 稀疏编码生物学动机（视觉皮层稀疏性）；编码定义（基向量 A 的线性组合 x = Az）；完备与过完备基向量的概念；过完备+稀疏性限制得到唯一编码 | 稀疏编码动机与编码定义 | `ch09-04` |
| 5 | `ch09-04` | §9.1.2 稀疏编码（目标函数与稀疏性度量） | `knowledge/teaching-guides/chapter-09/09-04-sparse-coding-objective.teaching.md` | `¶0045-¶0059` | 稀疏编码目标函数 L(A,Z)；η 控制稀疏性强度的超参数；ℓ₀ 范数定义（不连续可导难以优化）；ℓ₁ 范数作为替代；对数函数和指数函数的稀疏性度量形式 | 稀疏编码目标函数与稀疏性度量 | `ch09-05` |
| 6 | `ch09-05` | §9.1.2.1 训练方法 / §9.1.2.2 优点 | `knowledge/teaching-guides/chapter-09/09-05-sparse-coding-training.teaching.md` | `¶0060-¶0070` | 交替优化两步骤（固定 A 优化 z，固定 z 优化 A）；稀疏编码三个优点（计算量、可解释性、特征选择） | 稀疏编码训练方法与优点 | `ch09-06` |
| 7 | `ch09-06` | §9.1.3 自编码器（结构与重构错误） | `knowledge/teaching-guides/chapter-09/09-06-autoencoder-structure.teaching.md` | `¶0071-¶0079` | 自编码器定义；编码器与解码器角色；最小化重构错误的学习目标；M<D 为降维/特征抽取；M≥D 需附加约束才有意义 | 自编码器结构与重构错误 | `ch09-07` |
| 8 | `ch09-07` | §9.1.3 自编码器（两层网络与捆绑权重） | `knowledge/teaching-guides/chapter-09/09-07-two-layer-autoencoder.teaching.md` | `¶0080-¶0091` | 两层自编码器网络结构；编码公式与解码公式；捆绑权重定义与作用；重构错误损失函数；训练后去掉解码器只保留编码器 | 两层自编码器与捆绑权重 | `ch09-08` |
| 9 | `ch09-08` | §9.1.4 稀疏自编码器 | `knowledge/teaching-guides/chapter-09/09-08-sparse-autoencoder.teaching.md` | `¶0092-¶0104` | 稀疏自编码器定义（M>D 且 z 稀疏）；稀疏自编码器目标函数三部分；神经元平均活性值 ρ̂_j；KL 距离衡量稀疏性；ρ(Z) 的 KL 求和形式 | 稀疏自编码器 | `ch09-09` |
| 10 | `ch09-09` | §9.1.5 堆叠自编码器 / §9.1.6 降噪自编码器 | `knowledge/teaching-guides/chapter-09/09-09-stacked-denoising-autoencoder.teaching.md` | `¶0105-¶0111` | 堆叠自编码器：深层网络逐层训练；降噪自编码器：引入噪声增加鲁棒性；损坏比例 μ 随机置零部分维度；从损坏输入 x̃ 重构原始 x | 堆叠与降噪自编码器 | `ch09-10` |
| 11 | `ch09-10` | §9.2.1 参数密度估计（MLE） | `knowledge/teaching-guides/chapter-09/09-10-density-estimation-mle.teaching.md` | `¶0112-¶0119` | 概率密度估计定义；参数与非参数密度估计分类；对数似然函数；最大似然估计（MLE）的优化形式 | 密度估计与MLE | `ch09-11` |
| 12 | `ch09-11` | §9.2.1.1 正态分布的最大似然估计 | `knowledge/teaching-guides/chapter-09/09-11-normal-distribution-mle.teaching.md` | `¶0120-¶0127` | 正态分布假设的概率密度函数形式；正态分布对数似然函数；均值 μ^ML 的 MLE 解；协方差矩阵 Σ^ML 的 MLE 解 | 正态分布MLE | `ch09-12` |
| 13 | `ch09-12` | §9.2.1.2 多项分布的最大似然估计 | `knowledge/teaching-guides/chapter-09/09-12-multinomial-distribution-mle.teaching.md` | `¶0128-¶0141` | 多项分布的 one-hot 表示；概率密度函数 p(x|μ)；约束条件 Σμ_k=1；拉格朗日乘子法处理约束优化；μ_k^ML = m_k/N 的 MLE 解 | 多项分布MLE | `ch09-13` |
| 14 | `ch09-13` | §9.2.1 参数估计问题 / §9.2.2 非参数密度估计引入 | `knowledge/teaching-guides/chapter-09/09-13-parametric-issues-nonparametric-intro.teaching.md` | `¶0142-¶0159` | 参数密度估计三个问题（模型选择、不可观测变量、维度灾难）；非参数密度估计定义；核心公式 p(x)≈K/(NV)；两种非参数方式（固定V、固定K） | 参数估计问题与非参数引入 | `ch09-14` |
| 15 | `ch09-14` | §9.2.2.1 直方图方法 | `knowledge/teaching-guides/chapter-09/09-14-histogram-method.teaching.md` | `¶0160-¶0167` | 直方图方法的区间划分与密度计算 p_m=K_m/(NΔ_m)；区间宽度 Δ 对估计结果的影响（太小→随机性大，太大→过于平滑）；直方图方法在高维的维度灾难 | 直方图方法 | `ch09-15` |
| 16 | `ch09-15` | §9.2.2.2 核方法 / §9.2.2.3 K近邻方法 | `knowledge/teaching-guides/chapter-09/09-15-kernel-knn.teaching.md` | `¶0168-¶0184` | 核密度估计定义（Parzen窗方法）；超立方体核函数；密度估计公式 p(x)=K/(NH^D)；高斯核函数；K近邻方法的可变宽度思想 | 核方法与K近邻 | `ch09-16` |
| 17 | `ch09-16` | §9.3 总结和深入阅读 | `knowledge/teaching-guides/chapter-09/09-16-summary-and-reading.teaching.md` | `¶0185-¶0190` | 无监督学习三大问题类型；无监督特征学习作为表示学习；参数与非参数密度估计方法分类；无监督学习缺少客观评价方法 | 总结和深入阅读 | `ch09-test` |
| 18 | `ch09-test` | 第9章章测 | 无新增讲义；覆盖第9章已通过单元 | 第9章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献和了解即可内容不计入章测 | 第9章章测 | 第10章未解锁 |

## 当前审计结论

- 第9章 17 个教学单元均有教学指引和教材段落。
- `ch09-13` 18 段非公式密集：参数估计问题收束与非参数估计引入连续，作为密度估计方法切换单元，不宜拆分。
- 总教学单元 17 个 + 章测 = 18 行。
- `ch09-16` 为章节收束，只串联本章已学核心概念，不引入新算法细节。
- 所有对后文的引用（EM 算法→第11章、玻尔兹曼机→第12章、VAE/GAN→第13章、序列生成→第15章）均归入了解即可，不出正式题。
- 习题段 `¶0191-¶0197` 和参考文献段 `¶0198-¶0206` 不在任何教学单元段落范围内。
