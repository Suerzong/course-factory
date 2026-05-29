# §12.2.1 RBM Block Gibbs采样 教学指引

## 原文定位

- 原文文件：`textbook/chapters/12-第12章-深度信念网络.md`
- 标题：§12.2.1 生成模型（标题不编号）
- 正文范围：`¶0132-¶0143`
- 公式密集：是
- 需要核对 PDF：否

## 本节教学目标

学完本节后，学习者应该能够：

- 写出 $p(v_i=1|\mathbf{h})$ 的公式，理解其与 $p(h_j=1|\mathbf{v})$ 的对称性。
- 写出条件概率的向量形式：$p(\mathbf{h}=\mathbf{1}|\mathbf{v}) = \sigma(W^\top\mathbf{v}+\mathbf{b})$ 和 $p(\mathbf{v}=\mathbf{1}|\mathbf{h}) = \sigma(W\mathbf{h}+\mathbf{a})$。
- 描述RBM的Block Gibbs采样流程，解释为什么RBM可以并行采样而BM不行。

## 知识点分层

### 核心知识点

| 知识点 | 原文依据 | 讲解要求 | 出题权限 |
|---|---|---|---|
| $p(v_i=1|\mathbf{h}) = \sigma(a_i + \sum_j w_{ij} h_j)$，与$p(h_j=1|\mathbf{v})$结构对称 | `¶0132-¶0133` | 讲清对称性——两层条件概率公式结构完全一致，只是参数不同。 | 正式题 |
| 向量形式：$p(\mathbf{h}=\mathbf{1}|\mathbf{v}) = \sigma(W^\top\mathbf{v}+\mathbf{b})$，$p(\mathbf{v}=\mathbf{1}|\mathbf{h}) = \sigma(W\mathbf{h}+\mathbf{a})$ | `¶0134-¶0136` | 讲清向量形式可以一次性计算整层的激活概率，实现并行采样。 | 正式题 |
| Block Gibbs采样流程：$\mathbf{v}_0 \to \mathbf{h}_0 \to \mathbf{v}_1 \to \mathbf{h}_1 \to \cdots$，交替对整层进行并行采样 | `¶0137-¶0141` | 讲清"Block"的含义——一次采样整层而非一个变量；同层节点条件独立是并行的关键。 | 正式题 |
| RBM采样比BM高效——因为同层独立可并行，更快达到热平衡 | `¶0137,¶0141` | 对比BM的逐个变量采样，突出RBM效率优势。 | 正式题 |

### 重要背景

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 当$t\to\infty$时采样服从$p(\mathbf{v},\mathbf{h})$分布 | `¶0141` | 一句带过，强调这是Gibbs采样的收敛性质。 |

### 了解即可

| 内容 | 原文依据 | 处理方式 |
|---|---|---|
| 图12.4 RBM采样过程示意 | `¶0142-¶0143` | 用图辅助理解，不考图。 |

## 本节不要求

- 不要求证明 $p(v_i=1|\mathbf{h})$（结构对称于Theorem 12.2）。
- 不要求讨论收敛速度的数学分析。
- 不要求对比不同采样步数k的效果。

## 覆盖检查模板

- [ ] 已讲清 $p(v_i=1|\mathbf{h})$ 与 $p(h_j=1|\mathbf{v})$ 的对称性。
- [ ] 已讲清向量形式的含义和并行采样的能力。
- [ ] 已讲清Block Gibbs采样的交替流程（v→h→v→h→...）。
- [ ] 已讲清RBM并行采样比BM串行采样高效的原因。
