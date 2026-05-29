# 第3章 覆盖审计表

本表用于审计第3章是否形成稳定闭环。AI 教学第3章时，应以 `learning-path/chapter-03.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch03-00` | 第3章 引言 | `knowledge/teaching-guides/chapter-03/03-00-introduction.teaching.md` | `¶0001-¶0015` | 线性模型定义（特征的线性组合）；权重向量w和偏置b的角色；线性模型是ML最广泛应用模型；本章结构概览 | 第3章引言 | `ch03-01` |
| 2 | `ch03-01` | §3.1.1 二分类 | `knowledge/teaching-guides/chapter-03/03-01-binary-classification.teaching.md` | `¶0017-¶0032` | 线性判别函数f(x)=wᵀx+b；决策边界是D-1维超平面；权重w是法向量；两类线性可分定义（定义3.1）；多分类线性判别的困难 | 二分类 | `ch03-02` |
| 3 | `ch03-02` | §3.1.2 多分类 | `knowledge/teaching-guides/chapter-03/03-02-multi-class-classification.teaching.md` | `¶0033-¶0049` | 一对多（OvR）策略；一对一（OvO）策略；argmax判别函数；多类线性可分定义（定义3.2）；软max函数引入 | 多分类 | `ch03-03` |
| 4 | `ch03-03` | §3.2 Logistic回归 | `knowledge/teaching-guides/chapter-03/03-03-logistic-regression.teaching.md` | `¶0050-¶0068` | Logistic回归解决二分类；sigmoid函数σ(z)=1/(1+e⁻ᶻ)及性质；预测后验概率P(y=1|x)；决策边界wᵀx+b=0；odds和log-odds | Logistic回归 | `ch03-04` |
| 5 | `ch03-04` | §3.2.1 参数学习（Logistic） | `knowledge/teaching-guides/chapter-03/03-04-logistic-parameter-learning.teaching.md` | `¶0069-¶0087` | 交叉熵损失函数用于Logistic回归；负对数似然与交叉熵等价；梯度下降更新公式；损失函数凸性保证全局最优 | Logistic参数学习 | `ch03-05` |
| 6 | `ch03-05` | §3.3 Softmax回归 | `knowledge/teaching-guides/chapter-03/03-05-softmax-regression.teaching.md` | `¶0088-¶0107` | Softmax回归是多类Logistic回归；softmax函数定义及输出解释；C类权重向量W=[w₁,...,w_C]；向量形式ŷ=softmax(Wᵀx)；Softmax与Logistic关系（C=2时等价） | Softmax回归 | `ch03-06` |
| 7 | `ch03-06` | §3.3.1 参数学习（Softmax）（上） | `knowledge/teaching-guides/chapter-03/03-06-softmax-parameter-learning-1.teaching.md` | `¶0108-¶0128` | one-hot标签表示；Softmax交叉熵损失函数定义；负对数似然形式；损失函数的概率解释 | Softmax参数学习（上） | `ch03-07` |
| 8 | `ch03-07` | §3.3.1 参数学习（Softmax）（下） | `knowledge/teaching-guides/chapter-03/03-07-softmax-parameter-learning-2.teaching.md` | `¶0129-¶0148` | 交叉熵损失对权重的梯度∂L/∂w_c；梯度下降更新规则；正则化项的加入；损失函数凸性 | Softmax参数学习（下） | `ch03-08` |
| 9 | `ch03-08` | §3.4 感知器 | `knowledge/teaching-guides/chapter-03/03-08-perceptron.teaching.md` | `¶0149-¶0155` | 感知器是最简单的神经网络；sign激活函数；硬阈值分类vs概率分类；感知器和Logistic回归的本质区别 | 感知器 | `ch03-09` |
| 10 | `ch03-09` | §3.4.1 参数学习（感知器） | `knowledge/teaching-guides/chapter-03/03-09-perceptron-parameter-learning.teaching.md` | `¶0156-¶0174` | 感知器使用0-1损失的经验风险最小化；感知器学习算法（算法3.1）；误分类驱动更新w←w+yx；算法直觉："修正错误" | 感知器参数学习 | `ch03-10` |
| 11 | `ch03-10` | §3.4.2 感知器收敛性（上） | `knowledge/teaching-guides/chapter-03/03-10-perceptron-convergence-1.teaching.md` | `¶0175-¶0192` | 感知器收敛定理（定理3.1）陈述；收敛前提条件（线性可分）；收敛上界r²R²/γ²的含义；参数r,R,γ的定义 | 感知器收敛性（上） | `ch03-11` |
| 12 | `ch03-11` | §3.4.2 感知器收敛性（下） | `knowledge/teaching-guides/chapter-03/03-11-perceptron-convergence-2.teaching.md` | `¶0193-¶0209` | 收敛上界的推导思路（不要求完整证明）；可分性越强（γ越大）收敛越快；收敛性只保证存在上界不保证找到最优解；收敛后的解取决于初始值和样本顺序 | 感知器收敛性（下） | `ch03-12` |
| 13 | `ch03-12` | §3.4.3 参数平均感知器（上） | `knowledge/teaching-guides/chapter-03/03-12-averaged-perceptron-1.teaching.md` | `¶0210-¶0220` | 感知器对样本顺序敏感的问题；投票感知器概念：用多轮训练的多数投票预测 | 平均感知器（上） | `ch03-13` |
| 14 | `ch03-13` | §3.4.3 参数平均感知器（下） | `knowledge/teaching-guides/chapter-03/03-13-averaged-perceptron-2.teaching.md` | `¶0221-¶0231` | 平均感知器：参数平均=投票的近似实现；算法3.2流程；平均感知器比标准感知器更稳定鲁棒；不需要存储中间模型 | 平均感知器（下） | `ch03-14` |
| 15 | `ch03-14` | §3.4.4 扩展到多分类 | `knowledge/teaching-guides/chapter-03/03-14-multi-class-perceptron.teaching.md` | `¶0232-¶0245` | 广义感知器：C类各一个权重向量；argmax判别规则；算法3.3（广义感知器学习）；多分类感知器更新规则 | 多分类感知器 | `ch03-15` |
| 16 | `ch03-15` | §3.4.4.1 广义感知器收敛性 | `knowledge/teaching-guides/chapter-03/03-15-generalized-perceptron-convergence.teaching.md` | `¶0246-¶0254` | 广义线性可分定义（定义3.3）；定理3.2广义感知器收敛性陈述；与二分类收敛定理的对应关系 | 广义感知器收敛性 | `ch03-16` |
| 17 | `ch03-16` | §3.5 支持向量机 | `knowledge/teaching-guides/chapter-03/03-16-svm-intro.teaching.md` | `¶0255-¶0271` | SVM核心思想：最大化分类间隔；间隔定义（支持向量到超平面距离）；支持向量概念；SVM优化问题的几何直觉 | SVM概述 | `ch03-17` |
| 18 | `ch03-17` | §3.5.1 参数学习（SVM） | `knowledge/teaching-guides/chapter-03/03-17-svm-parameter-learning.teaching.md` | `¶0272-¶0291` | SVM原始优化问题（硬间隔）；约束优化形式；拉格朗日对偶性基本思路（不要求完整推导）；对偶问题形式；支持向量在解中的作用 | SVM参数学习 | `ch03-18` |
| 19 | `ch03-18` | §3.5.2 核函数 + §3.5.3 软间隔 | `knowledge/teaching-guides/chapter-03/03-18-kernel-and-soft-margin.teaching.md` | `¶0292-¶0308` | 核技巧：用核函数隐式映射到高维空间；多项式核例子展示低维计算等价于高维内积；软间隔SVM允许少量违反约束；松弛变量ξ和惩罚参数C的含义 | 核函数与软间隔 | `ch03-19` |
| 20 | `ch03-19` | §3.6 损失函数对比（上） | `knowledge/teaching-guides/chapter-03/03-19-loss-comparison-1.teaching.md` | `¶0309-¶0319` | 0-1损失、Hinge损失、Logistic损失、交叉熵损失各自定义回顾；各损失函数形状与特性 | 损失函数对比（上） | `ch03-20` |
| 21 | `ch03-20` | §3.6 损失函数对比（下） | `knowledge/teaching-guides/chapter-03/03-20-loss-comparison-2.teaching.md` | `¶0320-¶0330` | 损失函数与模型对应关系（Logistic↔交叉熵, SVM↔Hinge, 感知器↔0-1替代）；不同损失对离群点的敏感性；损失函数选择指导原则 | 损失函数对比（下） | `ch03-21` |
| 22 | `ch03-21` | §3.7 总结和深入阅读 | `knowledge/teaching-guides/chapter-03/03-21-summary-and-reading.teaching.md` | `¶0331-¶0336` | 线性模型统一框架（表3.1对比）；Logistic/Softmax/感知器/SVM在"模型+损失+优化"框架下的统一视角；各模型适用场景 | 总结和深入阅读 | `ch03-test` |
| 23 | `ch03-test` | 第3章章测 | 无新增讲义；覆盖第3章已通过单元 | 第3章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第3章章测 | 第4章未解锁 |

## 当前审计结论

- 第3章 22 个教学单元（`ch03-00` ~ `ch03-21`）均有教学指引和教材段落。
- `¶0017` 为 §3.1.1 小节标题，不单独设考点。
- `¶0033` 为 §3.1.2 小节标题，不单独设考点。
- `ch03-06` 和 `ch03-07` 拆分 §3.3.1 参数学习（41段 → 21+20），均为公式密集。
- `ch03-10` 和 `ch03-11` 拆分 §3.4.2 感知器收敛性（35段 → 18+17），均为公式密集，正式题只考定理陈述和结论含义，不考完整证明。
- `ch03-12` 和 `ch03-13` 拆分 §3.4.3 参数平均感知器（22段 → 11+11）。
- `ch03-18` 合并核函数（`¶0292-¶0299`）和软间隔（`¶0300-¶0308`），17段=8+9，正式考点4-5个。
- `ch03-19` 和 `ch03-20` 拆分 §3.6 损失函数对比（22段 → 11+11），均为公式密集。
- `¶0337-¶0347` 为习题，`¶0348-¶0355` 为参考文献，不进入任何教学单元的正式题范围。
- `¶0356-¶0357` 为分部标记，不进入任何教学单元。
- 第4章仍未解锁，待第3章章测通过后再解锁。
