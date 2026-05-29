# 附录数学基础 覆盖审计表

本表用于审计附录数学基础各模块的覆盖情况。附录模块不进入主线推进依据，默认状态为 `按需查阅`。

## 审计规则

- 附录中所有检测项统一为 `课堂识别不计分`，不进入正式题。
- 附录练习称为"诊断题/补救检测"，不计入正确率和推进依据。
- 每个模块可独立诊断、独立进入、独立退出，不做强制推进链。
- `appendix-math-00` 为轻量讲义，只含诊断流程图、模块入口链接和按需查阅规则。

| 顺序 | 单元ID | 模块 | 教学指引 | 教材段落 | 诊断范围 | 掌握追踪行 | 建议补救入口 |
|---:|---|---|---|---|---|---|---|
| 1 | `appendix-math-00` | 数学基础诊断入口 | `knowledge/teaching-guides/appendix-math/appendix-math-00-diagnostic-entry.teaching.md` | 无新增段落 | 诊断流程图、模块入口链接、按需查阅规则 | 无（不进入mastery-tracker） | 诊断后按需跳转 |
| 2 | `appendix-math-A1` | 向量基础与范数 | `knowledge/teaching-guides/appendix-math/appendix-math-A1-vector-basics-and-norms.teaching.md` | `¶0001-¶0044` | 向量空间、基、内积、范数、one-hot编码 | 无（不进入mastery-tracker） | 诊断入口或Ch3-Ch5主线关联 |
| 3 | `appendix-math-A2` | 矩阵与线性映射 | `knowledge/teaching-guides/appendix-math/appendix-math-A2-matrices-and-linear-maps.teaching.md` | `¶0045-¶0100` | 矩阵操作、仿射变换、逆/正交/对角矩阵 | 无（不进入mastery-tracker） | 诊断入口或Ch3-Ch5主线关联 |
| 4 | `appendix-math-A3` | 特征值与矩阵分解 | `knowledge/teaching-guides/appendix-math/appendix-math-A3-eigenvalues-and-decompositions.teaching.md` | `¶0101-¶0148` | 特征值、特征分解、SVD、Gram矩阵 | 无（不进入mastery-tracker） | 诊断入口或Ch2,Ch4,Ch9主线关联 |
| 5 | `appendix-math-B1` | 微分与积分基础 | `knowledge/teaching-guides/appendix-math/appendix-math-B1-differential-and-integral.teaching.md` | `¶0149-¶0179` | 导数、微分、泰勒展开、黎曼积分 | 无（不进入mastery-tracker） | 诊断入口或Ch4主线关联 |
| 6 | `appendix-math-B2` | 矩阵微积分 | `knowledge/teaching-guides/appendix-math/appendix-math-B2-matrix-calculus.teaching.md` | `¶0180-¶0236` | 雅可比、Hessian、矩阵导数法则、链式法则 | 无（不进入mastery-tracker） | 诊断入口或Ch4,Ch7主线关联 |
| 7 | `appendix-math-B3` | 常见函数导数 | `knowledge/teaching-guides/appendix-math/appendix-math-B3-common-function-derivatives.teaching.md` | `¶0237-¶0269` | Logistic导数、Softmax导数 | 无（不进入mastery-tracker） | 诊断入口或Ch3-Ch5,Ch15主线关联 |
| 8 | `appendix-math-C1` | 优化基础与梯度下降 | `knowledge/teaching-guides/appendix-math/appendix-math-C1-optimization-and-gradient-descent.teaching.md` | `¶0270-¶0293` | 优化分类、迭代思想、梯度下降法 | 无（不进入mastery-tracker） | 诊断入口或Ch2,Ch7主线关联 |
| 9 | `appendix-math-C2` | 局部最优与约束优化 | `knowledge/teaching-guides/appendix-math/appendix-math-C2-local-optima-and-constrained-optimization.teaching.md` | `¶0294-¶0372` | 局部/全局最优、KKT条件、拉格朗日乘数法、对偶 | 无（不进入mastery-tracker） | 诊断入口或Ch2,Ch3,Ch7主线关联 |
| 10 | `appendix-math-D1` | 概率基础与常见分布 | `knowledge/teaching-guides/appendix-math/appendix-math-D1-probability-and-distributions.teaching.md` | `¶0373-¶0519` | 条件概率、贝叶斯、伯努利/二项/正态/多项/狄利克雷、期望方差 | 无（不进入mastery-tracker） | 诊断入口或Ch2,Ch11-Ch13主线关联 |
| 11 | `appendix-math-D2` | 随机过程 | `knowledge/teaching-guides/appendix-math/appendix-math-D2-stochastic-processes.teaching.md` | `¶0520-¶0562` | 马尔可夫链、平稳分布、高斯过程回归 | 无（不进入mastery-tracker） | 诊断入口或Ch14,Ch15主线关联 |
| 12 | `appendix-math-E1` | 熵与互信息 | `knowledge/teaching-guides/appendix-math/appendix-math-E1-entropy-and-mutual-info.teaching.md` | `¶0563-¶0598` | 自信息、熵、联合熵、条件熵、互信息 | 无（不进入mastery-tracker） | 诊断入口或Ch7,Ch15主线关联 |
| 13 | `appendix-math-E2` | 交叉熵与散度 | `knowledge/teaching-guides/appendix-math/appendix-math-E2-cross-entropy-and-divergence.teaching.md` | `¶0599-¶0630` | 交叉熵、KL散度、JS散度、Wasserstein距离 | 无（不进入mastery-tracker） | 诊断入口或Ch2,Ch7,Ch9,Ch13主线关联 |

## 当前审计结论

- 附录数学基础 13 个导航单元（`appendix-math-00` + A1/A2/A3/B1/B2/B3/C1/C2/D1/D2/E1/E2）均有教学指引和教材段落。
- `appendix-math-00` 为诊断入口轻量讲义，不讲正文知识点，只含诊断流程图和模块入口。
- 附录模块不做强制推进链，`appendix-math-*` 之间不设"下一单元"推进关系。
- 附录所有检测项统一为 `课堂识别不计分`，不写入 `mastery-tracker`，不进入章测。
- 附录练习称为"诊断题/补救检测"，不作为主线推进依据。
- C2 模块79段偏大，D1 模块147段偏大，均作为参考库按子话题分段查阅。
- `¶0631-¶0636`（E.4 总结和深入阅读）和 `¶0637-¶0648`（参考文献）不进入任何教学单元。
- E2 中的推荐书目和参考资料只进"了解即可"，不进入诊断题/补救检测。
