# §13.2.2 推断网络目标：KL→ELBO 教学指引

## 原文定位

- 原文文件：`textbook/chapters/13-第13章-深度生成模型.md`
- 标题：§13.2.2 推断网络（标题不编号）
- 正文范围：`¶0066-¶0079`
- 公式密集：是
- 需要核对 PDF：否

## 本节教学目标

学完本节后，学习者应该能够：

- 写出推断网络的原始目标——最小化$\mathrm{KL}(q(\mathbf{z}|\mathbf{x};\phi), p(\mathbf{z}|\mathbf{x};\theta))$。
- 解释为什么直接最小化KL散度不可行（$p(\mathbf{z}|\mathbf{x};\theta)$无法计算）。
- 写出KL散度与ELBO的关系：$\mathrm{KL} = \log p(\mathbf{x};\theta) - \mathrm{ELBO}$。
- 理解推断网络目标从最小化KL转换为最大化ELBO的逻辑链。

## 知识点分层

### 核心知识点

| 知识点 | 原文依据 | 讲解要求 | 出题权限 |
|---|---|---|---|
| 推断网络原始目标：$\phi^* = \arg\min_\phi \mathrm{KL}(q(\mathbf{z}|\mathbf{x};\phi), p(\mathbf{z}|\mathbf{x};\theta))$，使$q$接近真实后验 | `¶0066-¶0067` | 讲清"为什么是这个目标"——推断网络的使命就是近似后验。 | 正式题 |
| 直接计算不可行的原因：$p(\mathbf{z}|\mathbf{x};\theta)$一般无法计算，采样法效率低，变分法近似效果差 | `¶0068` | 讲清三条路径都走不通，因此需要间接方法。 | 正式题 |
| KL与ELBO的关系：$\mathrm{KL}(q(\mathbf{z}|\mathbf{x};\phi), p(\mathbf{z}|\mathbf{x};\theta)) = \log p(\mathbf{x};\theta) - \mathrm{ELBO}(q,\mathbf{x};\theta,\phi)$ | `¶0070-¶0071` | 讲清$\log p(\mathbf{x};\theta)$与$\phi$无关→最小化KL等价于最大化ELBO。这是关键转换。 | 正式题 |
| 目标转换：$\arg\min_\phi \mathrm{KL} \to \arg\max_\phi \mathrm{ELBO}(q,\mathbf{x};\theta,\phi)$ | `¶0074-¶0078` | 讲清三步转换：KL→$\log p$-ELBO→$\max$ ELBO（因为$\log p$不含$\phi$）。 | 正式题 |

### 重要背景

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 变分推断参见第11.4节 | `¶0069` | 课堂识别不计分；不进入正式题、正确率、章测或推进依据。 |
| 公式(11.85) | `¶0079` | 课堂识别不计分；不进入正式题、正确率、章测或推进依据。 |

### 了解即可

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 传统方法：采样/变分法近似推断 | `¶0068` | 一句提及作为动机，不展开。 |

## 本节不要求

- 不要求推导KL散度与ELBO关系的具体步骤。
- 不要求比较采样法和变分法的优劣。
- 不要求展开变分推断的数学细节。

## 覆盖检查模板

- [ ] 已讲清推断网络的原始目标（最小化KL散度）。
- [ ] 已讲清直接计算KL不可行的三个原因。
- [ ] 已讲清KL= $\log p(\mathbf{x};\theta)$ - ELBO的关键关系。
- [ ] 已讲清从最小化KL到最大化ELBO的转换逻辑。
