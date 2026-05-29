# §4.1.3 Swish函数 + §4.1.4 GELU函数 教学指引

## 原文定位

- 原文文件：`textbook/chapters/04-第4章-前馈神经网络.md`
- 标题：§4.1.3 Swish函数 + §4.1.4 GELU函数
- 正文范围：`¶0089-¶0101`
- 公式密集：否
- 需要核对 PDF：否

## 本节教学目标

学完本节后，学习者应该能够：

- 写出Swish函数的公式并解释其自门控机制
- 描述Swish函数在不同$\beta$值下的行为（线性、近似ReLU、中间状态）
- 写出GELU函数的定义并解释其与高斯分布累积分布函数的关系
- 理解GELU与Swish之间的联系（Logistic近似下GELU相当于一种特殊的Swish）

## 知识点分层

### 核心知识点

| 知识点 | 原文依据 | 讲解要求 | 出题权限 |
|---|---|---|---|
| Swish函数的定义与自门控机制 | `¶0089-¶0091` | 必须讲清：$\operatorname{swish}(x) = x\sigma(\beta x)$，其中$\sigma(\cdot)$为Logistic函数，$\beta$为可学习参数或固定超参数；$\sigma(\beta x) \in (0,1)$作为软性门控：接近1时门"开"输出近似$x$，接近0时门"关"输出近似0 | 正式题 |
| Swish函数在不同$\beta$值下的行为 | `¶0094-¶0095` | 必须讲清：$\beta = 0$退化为线性函数$x/2$；$\beta = 1$时$x > 0$近似线性、$x < 0$近似饱和且具非单调性；$\beta \to +\infty$时$\sigma(\beta x)$趋向0-1函数，Swish近似为ReLU；Swish可看作线性与ReLU之间的非线性插值 | 正式题 |
| GELU函数的定义 | `¶0096-¶0098` | 必须讲清：$\operatorname{GELU}(x) = xP(X \le x)$，$P(X \le x)$是高斯分布$\mathcal{N}(\mu, \sigma^2)$的累积分布函数（一般设$\mu=0, \sigma=1$）；通过门控机制调整输出值 | 正式题 |
| GELU与Swish的关系 | `¶0098-¶0101` | 必须讲清：GELU用Tanh或Logistic函数近似高斯CDF；用Logistic近似时，$\operatorname{GELU}(x) \approx x\sigma(1.702x)$，相当于一种特殊的Swish函数 | 正式题 |

### 重要背景

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| Swish函数中$\beta$参数的三种特殊情况 | `¶0094-¶0095` | 帮助理解Swish函数的灵活性，三种极限情况可辅助记忆 |
| GELU的两种近似公式(4.28)和(4.29) | `¶0099-¶0100` | 知道近似公式存在，Logistic近似形式是理解GELU-Swish关系的关键 |

### 了解即可

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 人名年份：Ramachandran et al. 2017, Hendrycks et al. 2016 | `¶0089, ¶0096` | 不要求记忆人名和年份 |
| 图4.5 Swish函数图示 | `¶0092-¶0093` | 了解即可 |

## 本节不要求

- 不要求记忆GELU的Tanh近似公式(4.28)的具体系数
- 不要求推导GELU的累积分布函数
- 不要求记忆Swish和GELU的导数公式

## 覆盖检查模板

- [ ] 已覆盖Swish函数的定义和自门控机制
- [ ] 已覆盖Swish在不同$\beta$值下的四种行为
- [ ] 已覆盖GELU函数的定义和门控机制
- [ ] 已覆盖GELU与Swish的关系（Logistic近似使GELU成为特殊Swish）
- [ ] 已标记人名年份为"了解即可"
