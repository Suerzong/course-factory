# 第13章 覆盖审计表

本表用于审计第13章是否形成稳定闭环。AI 教学第13章时，应以 `learning-path/chapter-13.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch13-00` | 第13章 引言 | `knowledge/teaching-guides/chapter-13/13-00-introduction.teaching.md` | `¶0001-¶0007` | 生成模型定义和双重功能（密度估计+生成样本）；高维空间建模两大困难；深度生成模型核心思路（神经网络作为分布逼近器）；本章两种模型预告 | 第13章引言 | `ch13-01` |
| 2 | `ch13-01` | §13.1.1 密度估计 + §13.1.2 生成样本 | `knowledge/teaching-guides/chapter-13/13-01-density-estimation-sampling.teaching.md` | `¶0008-¶0020` | 密度估计定义和无监督学习性质；隐变量简化动机和$p(z)\sim\mathcal{N}(0,I)$假设；两步采样流程；GAN跳过密度估计直接生成的基本思路 | 密度估计与生成样本 | `ch13-02` |
| 3 | `ch13-02` | §13.1.3 应用于监督学习 | `knowledge/teaching-guides/chapter-13/13-02-generative-vs-discriminative.teaching.md` | `¶0021-¶0026` | 生成模型通过贝叶斯公式应用于监督学习；生成模型vs判别模型（联合分布vs条件分布）；典型生成/判别模型举例 | 生成模型vs判别模型 | `ch13-03` |
| 4 | `ch13-03` | §13.2.1 潜变量生成模型：EM+ELBO | `knowledge/teaching-guides/chapter-13/13-03-latent-variable-em-elbo.teaching.md` | `¶0027-¶0043` | 联合概率$p(x,z;\theta)$的分解；对数边际似然的ELBO分解和KL≥0的下界性质；ELBO定义；EM两步算法 | EM与ELBO | `ch13-04` |
| 5 | `ch13-04` | §13.2.1 推断难题+VAE方案概述 | `knowledge/teaching-guides/chapter-13/13-04-inference-challenge-vae.teaching.md` | `¶0044-¶0055` | 后验$p(z\mid x;\theta)$难计算的原因（分母积分）；变分推断局限（简单分布近似复杂后验效果差）；VAE双网络结构；VAE与自编码器的本质区别 | VAE方案概述 | `ch13-05` |
| 6 | `ch13-05` | §13.2.2 推断网络结构 | `knowledge/teaching-guides/chapter-13/13-05-inference-network-structure.teaching.md` | `¶0056-¶0065` | $q(z\mid x;\phi)$为对角化协方差高斯分布的假设；推断网络输入输出关系（$x\to\mu_I,\sigma_I^2$）；softplus激活函数确保方差非负 | 推断网络结构 | `ch13-06` |
| 7 | `ch13-06` | §13.2.2 推断网络目标：KL→ELBO | `knowledge/teaching-guides/chapter-13/13-06-inference-objective-kl-elbo.teaching.md` | `¶0066-¶0079` | 推断网络原始目标（最小化KL）；直接计算KL不可行的原因；KL=$\log p(x;\theta)$-ELBO的关键关系；从最小化KL到最大化ELBO的转换逻辑 | 推断网络目标 | `ch13-07` |
| 8 | `ch13-07` | §13.2.3 生成网络 | `knowledge/teaching-guides/chapter-13/13-07-generative-network.teaching.md` | `¶0080-¶0093` | 生成模型先验（固定标准高斯）和条件概率（生成网络建模）；两种输出分布类型（伯努利→二值，高斯→连续）；生成网络目标（最大化ELBO） | 生成网络 | `ch13-08` |
| 9 | `ch13-08` | §13.2.4 模型汇总 | `knowledge/teaching-guides/chapter-13/13-08-model-summary.teaching.md` | `¶0094-¶0110` | VAE总目标=重构项-KL正则化项；重构项采样近似原理；KL散度可闭式计算的原因；VAE与EM的对应关系 | 模型汇总 | `ch13-09` |
| 10 | `ch13-09` | §13.2.5 重参数化 | `knowledge/teaching-guides/chapter-13/13-09-reparameterization.teaching.md` | `¶0111-¶0120` | 重参数化动机（采样不可微）；$z=\mu_I+\sigma_I\odot\epsilon$公式和符号含义；重参数化如何恢复梯度流 | 重参数化 | `ch13-10` |
| 11 | `ch13-10` | §13.2.6 训练 | `knowledge/teaching-guides/chapter-13/13-10-training.teaching.md` | `¶0121-¶0133` | VAE训练目标函数的批量形式；单样本高斯假设下简化目标（MSE+KL正则）；VAE与自编码器的形似神不似；MNIST隐空间可视化含义 | VAE训练 | `ch13-11` |
| 12 | `ch13-11` | §13.3.1 显式/隐式密度+§13.3.2.1 判别器 | `knowledge/teaching-guides/chapter-13/13-11-explicit-implicit-discriminator.teaching.md` | `¶0134-¶0147` | 显式vs隐式密度模型区分；GAN对抗思想（$D$判别真假、$G$以假乱真）；判别网络目标函数（二分类交叉熵） | 显式/隐式密度与判别器 | `ch13-12` |
| 13 | `ch13-12` | §13.3.2.2 生成器+§13.3.3 训练+§13.3.4 DCGAN | `knowledge/teaching-guides/chapter-13/13-12-generator-training-dcgan.teaching.md` | `¶0148-¶0160` | 生成网络两个等价目标及实际选择$\max\log D$的梯度原因；GAN交替训练模式；DCGAN五技巧动机（稳定训练） | 生成器训练与DCGAN | `ch13-13` |
| 14 | `ch13-13` | §13.3.5 Minimax+最优D*+JS散度 | `knowledge/teaching-guides/chapter-13/13-13-minimax-optimal-d-js.teaching.md` | `¶0161-¶0175` | GAN的Minimax目标函数；最优判别器$D^*(x)$的公式和含义；GAN损失等价于$2\cdot\mathrm{JS}(p_r,p_\theta)-2\log 2$ | Minimax与JS散度 | `ch13-14` |
| 15 | `ch13-14` | §13.3.5.1 训练稳定性+§13.3.5.2 模型坍塌 | `knowledge/teaching-guides/chapter-13/13-14-training-stability-collapse.teaching.md` | `¶0176-¶0189` | JS散度导致梯度消失的原因（无重叠→JS=$\log 2$常数）；梯度消失vs梯度错误平衡困境；模型坍塌定义和逆向KL主导机制 | 训练稳定性与模型坍塌 | `ch13-15` |
| 16 | `ch13-15` | §13.3.5 正向KL vs 逆向KL | `knowledge/teaching-guides/chapter-13/13-15-forward-vs-reverse-kl.teaching.md` | `¶0190-¶0204` | 前向$\mathrm{KL}(p_r,p_\theta)$和逆向$\mathrm{KL}(p_\theta,p_r)$的定义；前向KL"覆盖"行为（惩罚遗漏）；逆向KL"回避"行为（惩罚多余）；逆向KL→模型坍塌的因果连接 | 正向KL vs 逆向KL | `ch13-16` |
| 17 | `ch13-16` | §13.3.6 Wasserstein距离与对偶动机 | `knowledge/teaching-guides/chapter-13/13-16-wasserstein-distance.teaching.md` | `¶0205-¶0214` | JS散度不适合衡量生成分布距离的原因；1st-Wasserstein距离定义和"推土机"直觉；Wasserstein距离优势（无重叠仍可衡量）；KR对偶形式 | Wasserstein距离 | `ch13-17` |
| 18 | `ch13-17` | §13.3.6 Lipschitz约束与WGAN目标 | `knowledge/teaching-guides/chapter-13/13-17-lipschitz-wgan-objective.teaching.md` | `¶0215-¶0224` | K-Lipschitz约束下Wasserstein距离的缩放公式；Lipschitz连续的直观含义（斜率有界） | Lipschitz与WGAN目标 | `ch13-18` |
| 19 | `ch13-18` | §13.3.6 WGAN评价/生成网络与训练 | `knowledge/teaching-guides/chapter-13/13-18-wgan-critic-training.teaching.md` | `¶0225-¶0236` | 评价网络（线性输出）vs判别网络（sigmoid输出）；参数裁剪近似Lipschitz约束原理；WGAN生成网络梯度不消失原因；WGAN两个关键区别 | WGAN评价/生成网络与训练 | `ch13-19` |
| 20 | `ch13-19` | §13.4 总结和深入阅读 | `knowledge/teaching-guides/chapter-13/13-19-summary-and-reading.teaching.md` | `¶0237-¶0240` | 深度生成模型本质（神经网络作为分布逼近器）；VAE→GAN→WGAN演进逻辑；生成模型缺乏客观评价的局限 | 总结和深入阅读 | `ch13-test` |
| 21 | `ch13-test` | 第13章章测 | 无新增讲义；覆盖第13章已通过单元 | 第13章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第13章章测 | 第14章未解锁 |

## 当前审计结论

- 第13章共21个单元（20教学 + 1章测），覆盖教学段落 `¶0001-¶0240`。
- ch13-19仅4段，为短收束单元，正式题只做本章VAE/GAN/WGAN框架回顾。
- VAE 8单元（ch13-03~ch13-10），GAN/WGAN 8单元（ch13-11~ch13-18）。
- Lipschitz侧栏（¶0215-¶0220）在ch13-17中标记为了解即可，不进入正式题。
- DCGAN五技巧只考架构动机（稳定训练），不考具体参数。
- 习题 `¶0241-¶0256` 和参考文献 `¶0257-¶0265` 不进入任何单元。
- "参见第9.2/11.2.2.1/11.4/5.5.1/E.3.3/E.3.4节" 等交叉引用已标记为课堂识别不计分。
