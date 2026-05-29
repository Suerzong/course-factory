# 第2章 覆盖审计表

本表用于审计第2章是否形成稳定闭环。AI 教学第2章时，应以 `learning-path/chapter-02.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch02-00` | 第2章 引言 | `knowledge/teaching-guides/chapter-02/02-00-introduction.teaching.md` | `¶0001-¶0007` | Mitchell定义三关键词；模式识别与ML的关系；手写体数字识别说明"为什么需要ML" | 第2章引言 | `ch02-01` |
| 2 | `ch02-01` | §2.1 基本概念（上） | `knowledge/teaching-guides/chapter-02/02-01-basic-concepts-1.teaching.md` | `¶0008-¶0017` | 特征与标签区别；样本定义；训练集/测试集分工；特征向量与标签标量；IID假设 | 基本概念（上） | `ch02-02` |
| 3 | `ch02-02` | §2.1 基本概念（下） | `knowledge/teaching-guides/chapter-02/02-02-basic-concepts-2.teaching.md` | `¶0018-¶0029` | ℱ与f*的角色关系；两种输出形式（标签值/条件概率）；学习算法角色；测试集评价与IID | 基本概念（下） | `ch02-03` |
| 4 | `ch02-03` | §2.2 三要素与假设空间 | `knowledge/teaching-guides/chapter-02/02-03-three-elements-and-hypothesis-space.teaching.md` | `¶0030-¶0039` | 三要素框架；输入空间𝒳和输出空间𝒴区分；g(x)/ℱ/f*三角关系；参数化函数族 | 三要素与假设空间 | `ch02-04` |
| 5 | `ch02-04` | §2.2.1 线性与非线性模型 | `knowledge/teaching-guides/chapter-02/02-04-linear-and-nonlinear-models.teaching.md` | `¶0040-¶0051` | 线性模型wᵀx+b；非线性模型=非线性基函数+线性组合；可学习基函数→神经网络 | 线性与非线性模型 | `ch02-05` |
| 6 | `ch02-05` | §2.2.2 学习准则与期望风险 | `knowledge/teaching-guides/chapter-02/02-05-learning-criteria-and-expected-risk.teaching.md` | `¶0052-¶0062` | 好模型的两个判断标准（函数值/概率分布）；期望风险定义；IID前提 | 学习准则与期望风险 | `ch02-06` |
| 7 | `ch02-06` | §2.2.2.1 0-1损失与平方损失 | `knowledge/teaching-guides/chapter-02/02-06-0-1-loss-and-quadratic-loss.teaching.md` | `¶0063-¶0072` | 损失函数作用；0-1损失定义和缺点；平方损失定义和适用场景（回归） | 0-1损失与平方损失 | `ch02-07` |
| 8 | `ch02-07` | §2.2.2.1 交叉熵损失函数 | `knowledge/teaching-guides/chapter-02/02-07-cross-entropy-loss.teaching.md` | `¶0073-¶0087` | 交叉熵用于分类；one-hot向量；交叉熵公式与计算；交叉熵=负对数似然 | 交叉熵损失函数 | `ch02-08` |
| 9 | `ch02-08` | §2.2.2.1 Hinge损失 + ERM与过拟合 | `knowledge/teaching-guides/chapter-02/02-08-hinge-loss-and-erm-overfitting.teaching.md` | `¶0088-¶0101` | Hinge损失"边距"直觉；经验风险定义；ERM准则；过拟合现象与三成因 | Hinge损失+ERM与过拟合 | `ch02-09` |
| 10 | `ch02-09` | §2.2.2.2 SRM与欠拟合 | `knowledge/teaching-guides/chapter-02/02-09-srm-and-underfitting.teaching.md` | `¶0102-¶0115` | SRM=ERM+正则化；ℓ₂与ℓ₁正则化区分；欠拟合vs过拟合；ML本质是泛化 | SRM与欠拟合 | `ch02-10` |
| 11 | `ch02-10` | §2.2.3 优化算法+梯度下降法 | `knowledge/teaching-guides/chapter-02/02-10-optimization-and-gradient-descent.teaching.md` | `¶0116-¶0125` | 训练=最优化；参数vs超参数；梯度下降迭代公式；凸vs非凸优化 | 优化算法+梯度下降法 | `ch02-11` |
| 12 | `ch02-11` | §2.2.3.2-§2.2.3.4 提前停止/SGD/Mini-Batch | `knowledge/teaching-guides/chapter-02/02-11-early-stop-sgd-minibatch.teaching.md` | `¶0126-¶0140` | 提前停止与验证集；三集合分工；BGD/SGD/Mini-Batch对比；SGD随机噪声的作用 | 提前停止/SGD/Mini-Batch | `ch02-12` |
| 13 | `ch02-12` | §2.3 线性回归概述 | `knowledge/teaching-guides/chapter-02/02-12-linear-regression-intro.teaching.md` | `¶0141-¶0154` | 线性回归贯穿三要素+四种参数估计；f(x;w,b)=wᵀx+b；增广表示 | 线性回归概述 | `ch02-13` |
| 14 | `ch02-13` | §2.3.1.1 ERM-最小二乘法（上） | `knowledge/teaching-guides/chapter-02/02-13-erm-least-squares-1.teaching.md` | `¶0155-¶0164` | 平方损失适合线性回归；经验风险矩阵形式‖y−Xᵀw‖²/2；y和X的构造 | ERM-最小二乘法（上） | `ch02-14` |
| 15 | `ch02-14` | §2.3.1.1 ERM-最小二乘法（下） | `knowledge/teaching-guides/chapter-02/02-14-erm-least-squares-2.teaching.md` | `¶0165-¶0179` | ℛ(w)凸函数→求导为零；最小二乘闭式解w*=(XXᵀ)⁻¹Xy；不可逆的两种情况；LMS算法 | ERM-最小二乘法（下） | `ch02-15` |
| 16 | `ch02-15` | §2.3.1.2 SRM-岭回归 | `knowledge/teaching-guides/chapter-02/02-15-srm-ridge-regression.teaching.md` | `¶0180-¶0187` | 多重共线性问题；岭回归解(XXᵀ+λI)⁻¹Xy；岭回归=SRM+最小二乘 | SRM-岭回归 | `ch02-16` |
| 17 | `ch02-16` | §2.3.1.3 最大似然估计（上） | `knowledge/teaching-guides/chapter-02/02-16-mle-1.teaching.md` | `¶0188-¶0201` | 建模y=h(x) vs p(y|x)；高斯噪声假设→y的条件分布；似然函数定义；概率vs似然 | 最大似然估计（上） | `ch02-17` |
| 18 | `ch02-17` | §2.3.1.3 最大似然估计（下） | `knowledge/teaching-guides/chapter-02/02-17-mle-2.teaching.md` | `¶0202-¶0209` | 对数似然的目的；MLE直觉；MLE等价于最小二乘（高斯噪声下） | 最大似然估计（下） | `ch02-18` |
| 19 | `ch02-18` | §2.3.1.4 最大后验估计（上） | `knowledge/teaching-guides/chapter-02/02-18-map-1.teaching.md` | `¶0210-¶0222` | MLE的过拟合风险；先验→后验的直觉；贝叶斯估计（区间）vs MAP（点估计）；贝叶斯线性回归 | 最大后验估计（上） | `ch02-19` |
| 20 | `ch02-19` | §2.3.1.4 最大后验估计（下） | `knowledge/teaching-guides/chapter-02/02-19-map-2.teaching.md` | `¶0223-¶0230` | MAP优化目标；MAP↔SRM等价关系；MLE是MAP特例（ν→∞）；频率学派vs贝叶斯学派 | 最大后验估计（下） | `ch02-20` |
| 21 | `ch02-20` | §2.4 偏差-方差分解（上） | `knowledge/teaching-guides/chapter-02/02-20-bias-variance-1.teaching.md` | `¶0231-¶0242` | 拟合能力vs复杂度权衡；偏差-方差分解分析定位；最优模型f*(x)=E[y|x]；固有噪声ε | 偏差-方差分解（上） | `ch02-21` |
| 22 | `ch02-21` | §2.4 偏差-方差分解（中） | `knowledge/teaching-guides/chapter-02/02-21-bias-variance-2.teaching.md` | `¶0243-¶0261` | 训练集随机性→模型随机性；偏差定义（拟合能力）；方差定义（过拟合倾向）；最终分解(bias)²+variance+ε | 偏差-方差分解（中） | `ch02-22` |
| 23 | `ch02-22` | §2.4 偏差-方差分解（下） | `knowledge/teaching-guides/chapter-02/02-22-bias-variance-3.teaching.md` | `¶0262-¶0270` | 四种偏差-方差组合；实操诊断逻辑（训练/验证错误率）；λ调节偏差-方差平衡；过拟合/欠拟合应对策略 | 偏差-方差分解（下） | `ch02-23` |
| 24 | `ch02-23` | §2.5 机器学习算法的类型 | `knowledge/teaching-guides/chapter-02/02-23-ml-algorithm-types.teaching.md` | `¶0271-¶0284` | 监督/无监督/强化学习区分；回归/分类/结构化学习；三类型对比（表2.1） | 机器学习算法的类型 | `ch02-24` |
| 25 | `ch02-24` | §2.6 图像与文本特征表示 | `knowledge/teaching-guides/chapter-02/02-24-image-and-text-features.teaching.md` | `¶0285-¶0297` | 一切数据→向量；图像特征（像素+手工）；BoW模型；N-gram与维数爆炸 | 图像与文本特征表示 | `ch02-25` |
| 26 | `ch02-25` | §2.6 表示学习+§2.6.1.1 特征选择 | `knowledge/teaching-guides/chapter-02/02-25-representation-learning-and-feature-selection.teaching.md` | `¶0298-¶0308` | 原始特征五不足；表示学习动机；特征选择（选子集）；子集搜索（前向/反向）；过滤式vs包裹式 | 表示学习+特征选择 | `ch02-26` |
| 27 | `ch02-26` | §2.6.1.2 特征抽取+§2.6.2 深度学习 | `knowledge/teaching-guides/chapter-02/02-26-feature-extraction-and-dl.teaching.md` | `¶0309-¶0320` | 特征抽取x'=Wx；监督(LDA) vs 无监督(PCA)特征抽取；降维目的；DL=端到端统一表示和预测；贡献度分配问题 | 特征抽取+深度学习 | `ch02-27` |
| 28 | `ch02-27` | §2.7 准确率与错误率 | `knowledge/teaching-guides/chapter-02/02-27-accuracy-and-error-rate.teaching.md` | `¶0321-¶0330` | 评价流程；准确率定义；错误率=1−准确率 | 准确率与错误率 | `ch02-28` |
| 29 | `ch02-28` | §2.7 混淆矩阵 | `knowledge/teaching-guides/chapter-02/02-28-confusion-matrix.teaching.md` | `¶0331-¶0341` | TP/FP/FN/TN定义；混淆矩阵结构 | 混淆矩阵 | `ch02-29` |
| 30 | `ch02-29` | §2.7 精确率、召回率与F值 | `knowledge/teaching-guides/chapter-02/02-29-precision-recall-f1.teaching.md` | `¶0342-¶0350` | 精确率公式与直觉；召回率公式与直觉；精确率/召回率权衡；F值（F1）公式 | 精确率、召回率与F值 | `ch02-30` |
| 31 | `ch02-30` | §2.7 宏平均、微平均与交叉验证 | `knowledge/teaching-guides/chapter-02/02-30-macro-micro-avg-and-cv.teaching.md` | `¶0351-¶0361` | 宏平均vs微平均计算方式；样本不均衡时宏平均更合理；交叉验证流程与目的 | 宏平均、微平均与交叉验证 | `ch02-31` |
| 32 | `ch02-31` | §2.8.1 PAC学习理论（上） | `knowledge/teaching-guides/chapter-02/02-31-pac-learning-1.teaching.md` | `¶0362-¶0369` | 计算学习理论目的；泛化错误定义；大数定律→|𝒟|→∞泛化错误→0；不能学到零错误模型 | PAC学习理论（上） | `ch02-32` |
| 33 | `ch02-32` | §2.8.1 PAC学习理论（下） | `knowledge/teaching-guides/chapter-02/02-32-pac-learning-2.teaching.md` | `¶0370-¶0378` | "近似正确"（ε）和"可能"（δ）含义；PAC公式直观；\|ℱ\|与所需样本数关系 | PAC学习理论（下） | `ch02-33` |
| 34 | `ch02-33` | §2.8.2 NFL+§2.8.3 奥卡姆剃刀 | `knowledge/teaching-guides/chapter-02/02-33-nfl-and-occams-razor.teaching.md` | `¶0379-¶0387` | NFL核心结论与ML意义；奥卡姆剃刀核心思想；MDL原则直觉 | NFL+奥卡姆剃刀 | `ch02-34` |
| 35 | `ch02-34` | §2.8.4 丑小鸭定理+§2.8.5 归纳偏置 | `knowledge/teaching-guides/chapter-02/02-34-ugly-duckling-and-inductive-bias.teaching.md` | `¶0388-¶0391` | 丑小鸭定理核心观点；归纳偏置定义与必要性；kNN/朴素贝叶斯的归纳偏置例子 | 丑小鸭定理+归纳偏置 | `ch02-35` |
| 36 | `ch02-35` | §2.9 总结和深入阅读 | `knowledge/teaching-guides/chapter-02/02-35-summary-and-reading.teaching.md` | `¶0392-¶0396` | 三要素统一框架；同模型+不同准则=不同方法；频率学派vs贝叶斯学派；表示学习承上启下 | 总结和深入阅读 | `ch02-test` |
| 37 | `ch02-test` | 第2章章测 | 无新增讲义；覆盖第2章已通过单元 | 第2章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第2章章测 | 第3章未解锁 |

## 当前审计结论

- 第2章 36 个教学单元（`ch02-00` ~ `ch02-35`）均有教学指引和教材段落。
- `ch02-00` 覆盖引言和 MIT 定义，`¶0006` 为图片，不单独设考点。
- `ch02-07` 交叉熵单元使用 `¶0073-¶0087`，不展开 KL 散度或 softmax 推导（第3章内容）。
- `ch02-08` 同时覆盖 Hinge 损失和 ERM/过拟合，Hinge 损失的 SVM 细节不展开（第3章内容）。
- `ch02-14` ERM（下）覆盖最小二乘闭式解，`¶0170` 伪逆矩阵和 `¶0174` 古汉语说法不进入正式题。
- `ch02-19` MAP（下）覆盖 MAP↔SRM 等价、MLE 是 MAP 特例、频率学派 vs 贝叶斯学派四大核心。
- `ch02-21` 偏差-方差分解（中）覆盖19个段落编号，其中公式编号和交叉引用不单独算正文。
- `ch02-26` 合并了特征抽取（`¶0309-¶0317`）和深度学习方法（`¶0318-¶0320`），12段=9+3，正式考点5个。
- `ch02-34` 合并丑小鸭定理（`¶0388-¶0389`）和归纳偏置（`¶0390-¶0391`），4段=2+2。
- `¶0397-¶0429` 为习题和参考文献，不进入任何教学单元的正式题范围。
- 第3章仍未解锁，待第2章章测通过后再建设详细路线。
