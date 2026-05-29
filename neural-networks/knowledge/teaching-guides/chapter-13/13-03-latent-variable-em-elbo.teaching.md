# §13.2.1 潜变量生成模型：EM+ELBO 教学指引

## 原文定位

- 原文文件：`textbook/chapters/13-第13章-深度生成模型.md`
- 标题：§13.2.1 含隐变量的生成模型（标题不编号）
- 正文范围：`¶0027-¶0043`
- 公式密集：是
- 需要核对 PDF：否

## 本节教学目标

学完本节后，学习者应该能够：

- 写出含隐变量生成模型的联合概率分解：$p(\mathbf{x},\mathbf{z};\theta) = p(\mathbf{x}|\mathbf{z};\theta)p(\mathbf{z};\theta)$。
- 写出对数边际似然的ELBO分解：$\log p(\mathbf{x};\theta) = \mathrm{ELBO}(q,\mathbf{x};\theta,\phi) + \mathrm{KL}(q(\mathbf{z};\phi), p(\mathbf{z}|\mathbf{x};\theta))$。
- 解释ELBO的含义及其与对数边际似然的关系。
- 描述EM算法的两步：E步（找$q$接近后验）和M步（最大化ELBO）。

## 知识点分层

### 核心知识点

| 知识点 | 原文依据 | 讲解要求 | 出题权限 |
|---|---|---|---|
| 联合概率分解：$p(\mathbf{x},\mathbf{z};\theta) = p(\mathbf{x}|\mathbf{z};\theta)p(\mathbf{z};\theta)$，其中$p(\mathbf{z};\theta)$为先验，$p(\mathbf{x}|\mathbf{z};\theta)$为条件概率 | `¶0032-¶0034` | 讲清这是有向图模型的自然分解——先验×条件。 | 正式题 |
| 对数边际似然分解：$\log p(\mathbf{x};\theta) = \mathrm{ELBO}(q,\mathbf{x};\theta,\phi) + \mathrm{KL}(q(\mathbf{z};\phi), p(\mathbf{z}|\mathbf{x};\theta))$ | `¶0035-¶0037` | 讲清ELBO是$\log p(\mathbf{x};\theta)$的下界，KL散度≥0保证了下界性质。 | 正式题 |
| ELBO定义：$\mathrm{ELBO}(q,\mathbf{x};\theta,\phi) = \mathbb{E}_{\mathbf{z}\sim q(\mathbf{z};\phi)}[\log\frac{p(\mathbf{x},\mathbf{z};\theta)}{q(\mathbf{z};\phi)}]$ | `¶0039` | 讲清ELBO是"对数联合概率-对数变分分布"的期望。 | 正式题 |
| EM两步：E步=固定$\theta$找$q$近似后验$p(\mathbf{z}|\mathbf{x};\theta)$；M步=固定$q$最大化ELBO求$\theta$ | `¶0040-¶0043` | 讲清两步交替进行直到收敛。 | 正式题 |

### 重要背景

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 公式(13.3)参见公式(11.49) | `¶0038` | 课堂识别不计分；不进入正式题、正确率、章测或推进依据。 |
| EM算法参见第11.2.2.1节 | `¶0041` | 课堂识别不计分；不进入正式题、正确率、章测或推进依据。 |

### 了解即可

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 图13.3 VAE图模型示意 | `¶0029-¶0031` | 用图辅助理解，不考图。 |
| $\mathbf{x}$和$\mathbf{z}$都是连续随机向量 | `¶0028` | 一句带过。 |

## 本节不要求

- 不要求推导ELBO分解的完整过程。
- 不要求证明ELBO是$\log p(\mathbf{x};\theta)$的下界。
- 不要求EM算法的收敛性证明。

## 覆盖检查模板

- [ ] 已讲清联合概率$p(\mathbf{x},\mathbf{z};\theta)$的分解。
- [ ] 已讲清对数边际似然的ELBO分解及KL散度≥0保证下界的直觉。
- [ ] 已讲清ELBO的定义公式。
- [ ] 已讲清EM两步算法（E步找$q$、M步优化$\theta$）。
