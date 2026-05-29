# 第13章 深度生成模型 学习路线

本文件是第13章的教学调度表。AI 讲第13章时，应按表格顺序推进；每个单元先读知识点指引，再读教材原文。

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch13-00` | 第13章 引言 | `knowledge/teaching-guides/chapter-13/13-00-introduction.teaching.md` | `¶0001-¶0007` | 概念引入 | 未解锁 | `ch13-01` |
| 2 | `ch13-01` | §13.1.1 密度估计 + §13.1.2 生成样本 | `knowledge/teaching-guides/chapter-13/13-01-density-estimation-sampling.teaching.md` | `¶0008-¶0020` | 核心概念 | 未解锁 | `ch13-02` |
| 3 | `ch13-02` | §13.1.3 应用于监督学习 | `knowledge/teaching-guides/chapter-13/13-02-generative-vs-discriminative.teaching.md` | `¶0021-¶0026` | 概念对比 | 未解锁 | `ch13-03` |
| 4 | `ch13-03` | §13.2.1 潜变量生成模型：EM+ELBO | `knowledge/teaching-guides/chapter-13/13-03-latent-variable-em-elbo.teaching.md` | `¶0027-¶0043` | 核心概念 | 未解锁 | `ch13-04` |
| 5 | `ch13-04` | §13.2.1 推断难题+VAE方案概述 | `knowledge/teaching-guides/chapter-13/13-04-inference-challenge-vae.teaching.md` | `¶0044-¶0055` | 核心概念 | 未解锁 | `ch13-05` |
| 6 | `ch13-05` | §13.2.2 推断网络结构 | `knowledge/teaching-guides/chapter-13/13-05-inference-network-structure.teaching.md` | `¶0056-¶0065` | 核心概念 | 未解锁 | `ch13-06` |
| 7 | `ch13-06` | §13.2.2 推断网络目标：KL→ELBO | `knowledge/teaching-guides/chapter-13/13-06-inference-objective-kl-elbo.teaching.md` | `¶0066-¶0079` | 核心概念 | 未解锁 | `ch13-07` |
| 8 | `ch13-07` | §13.2.3 生成网络 | `knowledge/teaching-guides/chapter-13/13-07-generative-network.teaching.md` | `¶0080-¶0093` | 核心概念 | 未解锁 | `ch13-08` |
| 9 | `ch13-08` | §13.2.4 模型汇总 | `knowledge/teaching-guides/chapter-13/13-08-model-summary.teaching.md` | `¶0094-¶0110` | 核心概念 | 未解锁 | `ch13-09` |
| 10 | `ch13-09` | §13.2.5 重参数化 | `knowledge/teaching-guides/chapter-13/13-09-reparameterization.teaching.md` | `¶0111-¶0120` | 核心概念 | 未解锁 | `ch13-10` |
| 11 | `ch13-10` | §13.2.6 训练 | `knowledge/teaching-guides/chapter-13/13-10-training.teaching.md` | `¶0121-¶0133` | 核心概念 | 未解锁 | `ch13-11` |
| 12 | `ch13-11` | §13.3.1 显式/隐式密度+§13.3.2.1 判别器 | `knowledge/teaching-guides/chapter-13/13-11-explicit-implicit-discriminator.teaching.md` | `¶0134-¶0147` | 核心概念 | 未解锁 | `ch13-12` |
| 13 | `ch13-12` | §13.3.2.2 生成器+§13.3.3 训练+§13.3.4 DCGAN | `knowledge/teaching-guides/chapter-13/13-12-generator-training-dcgan.teaching.md` | `¶0148-¶0160` | 核心概念 | 未解锁 | `ch13-13` |
| 14 | `ch13-13` | §13.3.5 Minimax+最优D*+JS散度 | `knowledge/teaching-guides/chapter-13/13-13-minimax-optimal-d-js.teaching.md` | `¶0161-¶0175` | 核心概念 | 未解锁 | `ch13-14` |
| 15 | `ch13-14` | §13.3.5.1 训练稳定性+§13.3.5.2 模型坍塌 | `knowledge/teaching-guides/chapter-13/13-14-training-stability-collapse.teaching.md` | `¶0176-¶0189` | 核心概念 | 未解锁 | `ch13-15` |
| 16 | `ch13-15` | §13.3.5 正向KL vs 逆向KL | `knowledge/teaching-guides/chapter-13/13-15-forward-vs-reverse-kl.teaching.md` | `¶0190-¶0204` | 核心概念 | 未解锁 | `ch13-16` |
| 17 | `ch13-16` | §13.3.6 Wasserstein距离与对偶动机 | `knowledge/teaching-guides/chapter-13/13-16-wasserstein-distance.teaching.md` | `¶0205-¶0214` | 核心概念 | 未解锁 | `ch13-17` |
| 18 | `ch13-17` | §13.3.6 Lipschitz约束与WGAN目标 | `knowledge/teaching-guides/chapter-13/13-17-lipschitz-wgan-objective.teaching.md` | `¶0215-¶0224` | 核心概念 | 未解锁 | `ch13-18` |
| 19 | `ch13-18` | §13.3.6 WGAN评价/生成网络与训练 | `knowledge/teaching-guides/chapter-13/13-18-wgan-critic-training.teaching.md` | `¶0225-¶0236` | 核心概念 | 未解锁 | `ch13-19` |
| 20 | `ch13-19` | §13.4 总结和深入阅读 | `knowledge/teaching-guides/chapter-13/13-19-summary-and-reading.teaching.md` | `¶0237-¶0240` | 章节收束 | 未解锁 | `ch13-test` |
| 21 | `ch13-test` | 第13章章测 | 无新增讲义；覆盖第13章已通过单元 | 第13章已解锁段落 | 章测 | 未解锁 | `ch14-00` |

## 章末处理

- `ch13-test` 表示第13章章测，不对应教材新段落。
- 章测前必须完成第13章所有核心单元的覆盖检查。
- 章测通过后，才进入第14章详细路线建设或学习。
- ch13-19仅4段，为短收束单元，正式题只做本章VAE/GAN/WGAN框架回顾。
- VAE 8单元（ch13-03~ch13-10），GAN/WGAN 8单元（ch13-11~ch13-18）。
- 习题 `¶0241-¶0256` 和参考文献 `¶0257-¶0265` 不进入任何单元。
