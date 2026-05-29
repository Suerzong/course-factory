# 第15章 覆盖审计表

本表用于审计第15章是否形成稳定闭环。AI 教学第15章时，应以 `learning-path/chapter-15.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch15-00` | 第15章 引言 | `knowledge/teaching-guides/chapter-15/15-00-introduction.teaching.md` | `¶0001-¶0014` | 序列数据的定义与示例；词表概念；联合概率建模序列的动机；自回归生成模型的定义与位置 | 第15章引言 | `ch15-01` |
| 2 | `ch15-01` | §15.1 序列概率模型 | `knowledge/teaching-guides/chapter-15/15-01-sequence-probability-model.teaching.md` | `¶0015-¶0026` | 序列数据两个特点（变长、样本空间大）；乘法公式分解序列概率；自回归方式的含义；MLE训练目标（对数似然）；N元模型与深度序列模型两类方法 | 序列概率模型 | `ch15-02` |
| 3 | `ch15-02` | §15.1.1 序列生成 | `knowledge/teaching-guides/chapter-15/15-02-sequence-generation.teaching.md` | `¶0027-¶0041` | ⟨EOS⟩符号的作用；贪婪搜索的过程与次优性；束搜索的定义与束大小K的含义；束搜索平衡计算复杂度与搜索质量 | 序列生成 | `ch15-03` |
| 4 | `ch15-03` | §15.2 N元模型—定义与一元模型 | `knowledge/teaching-guides/chapter-15/15-03-ngram-definition-and-unigram.teaching.md` | `¶0042-¶0054` | N元模型的马尔可夫假设（N−1阶）；一元/二元模型定义；一元模型中序列概率的表示；多项分布假设 | N元模型—定义与一元模型 | `ch15-04` |
| 5 | `ch15-04` | §15.2 N元模型—MLE与频率估计 | `knowledge/teaching-guides/chapter-15/15-04-ngram-mle-and-frequency.teaching.md` | `¶0055-¶0071` | 一元模型MLE约束优化问题；拉格朗日乘子法求解；MLE等价于频率估计；N元模型条件概率的计数公式 | N元模型—MLE与频率估计 | `ch15-05` |
| 6 | `ch15-05` | §15.2 平滑技术 | `knowledge/teaching-guides/chapter-15/15-05-smoothing.teaching.md` | `¶0072-¶0080` | 数据稀疏问题的含义；Zipf定律的直观；平滑技术的基本思想；加法平滑公式与δ的含义；加1平滑 | 平滑技术 | `ch15-06` |
| 7 | `ch15-06` | §15.3 深度序列模型概述 + §15.3.1.1 嵌入层 | `knowledge/teaching-guides/chapter-15/15-06-deep-sequence-intro-and-embedding.teaching.md` | `¶0081-¶0094` | 深度序列模型的定义（神经网络估计条件概率）；Softmax输出的概率含义；嵌入表/嵌入矩阵的概念；one-hot向量到词向量的映射 | 深度序列模型概述与嵌入层 | `ch15-07` |
| 8 | `ch15-07` | §15.3.1.2 简单平均与前馈神经网络 | `knowledge/teaching-guides/chapter-15/15-07-feature-layer-average-and-ffn.teaching.md` | `¶0095-¶0111` | 特征层的作用；简单平均方法（词向量平均）；前馈神经网络固定窗口的方法（N−1词拼接）；跳层连接的作用 | 简单平均与前馈神经网络 | `ch15-08` |
| 9 | `ch15-08` | §15.3.1.2 循环神经网络 + §15.3.1.3 输出层 | `knowledge/teaching-guides/chapter-15/15-08-feature-layer-rnn-and-output.teaching.md` | `¶0112-¶0122` | RNN接受变长输入的方式；隐藏状态记录历史信息；RNN与前馈NN的对比；输出层Softmax分类器的结构 | RNN特征与输出层 | `ch15-09` |
| 10 | `ch15-09` | §15.3.2 参数学习 | `knowledge/teaching-guides/chapter-15/15-09-parameter-learning.teaching.md` | `¶0123-¶0129` | 训练目标：最大化对数似然；参数范围（嵌入矩阵+网络权重+偏置）；梯度上升法更新公式；学习率α的作用 | 参数学习 | `ch15-10` |
| 11 | `ch15-10` | §15.4.1 困惑度 | `knowledge/teaching-guides/chapter-15/15-10-perplexity.teaching.md` | `¶0130-¶0147` | 困惑度的定义（熵的指数）；困惑度衡量分布差异；测试集困惑度的计算公式；困惑度=几何平均条件概率的倒数；困惑度越低模型越好 | 困惑度 | `ch15-11` |
| 12 | `ch15-11` | §15.4.2 BLEU算法 | `knowledge/teaching-guides/chapter-15/15-11-bleu.teaching.md` | `¶0148-¶0159` | BLEU的用途（衡量生成与参考序列的N元重合度）；N元精度P_N的定义；长度惩罚因子的作用；BLEU=几何加权平均精度；BLEU只关注精度不关注召回率 | BLEU算法 | `ch15-12` |
| 13 | `ch15-12` | §15.4.3 ROUGE算法 | `knowledge/teaching-guides/chapter-15/15-12-rouge.teaching.md` | `¶0160-¶0163` | ROUGE的用途（召回率导向）；ROUGE-N的定义（从参考序列提取N元组合计算召回率）；ROUGE与BLEU的互补关系 | ROUGE算法 | `ch15-13` |
| 14 | `ch15-13` | §15.5.1 曝光偏差问题 | `knowledge/teaching-guides/chapter-15/15-13-exposure-bias.teaching.md` | `¶0164-¶0175` | 教师强制的定义；曝光偏差的原因（训练用真实前缀vs测试用模型生成前缀）；计划采样的思想（混合真实与生成数据）；三种衰减策略（线性/指数/逆Sigmoid）；过度纠正问题 | 曝光偏差问题 | `ch15-14` |
| 15 | `ch15-14` | §15.5.2 训练目标不一致问题 | `knowledge/teaching-guides/chapter-15/15-14-training-objective-mismatch.teaching.md` | `¶0176-¶0189` | 训练目标（MLE）与评价指标（BLEU/ROUGE）的不一致；评价指标不可微问题；MDP建模序列生成（动作/状态/轨迹）；REINFORCE/演员-评论员学习策略；MLE预训练+RL微调流程 | 训练目标不一致问题 | `ch15-15` |
| 16 | `ch15-15` | §15.5.3 计算效率问题概述 | `knowledge/teaching-guides/chapter-15/15-15-computation-efficiency-overview.teaching.md` | `¶0190-¶0202` | Softmax归一化的计算瓶颈；配分函数定义与计算开销；词表规模对训练速度的影响；两类加速方法（层次化Softmax、基于采样） | 计算效率问题概述 | `ch15-16` |
| 17 | `ch15-16` | §15.5.3.1 两层树结构与二叉树编码 | `knowledge/teaching-guides/chapter-15/15-16-two-level-tree-and-binary-encoding.teaching.md` | `¶0203-¶0213` | 两层树结构分组思想；词概率分解为p(c(w)|h̃) × p(w|c(w),h̃)；加速比例√|V|/2；二叉树的叶子/非叶子节点对应关系；路径编码（0/1位向量） | 两层树结构与二叉树编码 | `ch15-17` |
| 18 | `ch15-17` | §15.5.3.1 二叉树概率分解与霍夫曼编码 | `knowledge/teaching-guides/chapter-15/15-17-binary-tree-probability-and-huffman.teaching.md` | `¶0214-¶0227` | 二叉树路径概率的条件分解；二分类问题（Logistic回归替代Softmax）；加速比例|V|/log₂|V|；WordNet IS-A关系与霍夫曼编码两种构建方式；霍夫曼编码=高频短码 | 二叉树概率分解与霍夫曼编码 | `ch15-18` |
| 19 | `ch15-18` | §15.5.3.2 重要性采样—梯度变换 | `knowledge/teaching-guides/chapter-15/15-18-importance-sampling-gradient.teaching.md` | `¶0228-¶0246` | 重要性采样的目标（避免全词表求和）；提议分布的角色；原始分布期望→提议分布期望的变换 | 重要性采样—梯度变换 | `ch15-19` |
| 20 | `ch15-19` | §15.5.3.2 重要性采样—采样近似与配分函数估计 | `knowledge/teaching-guides/chapter-15/15-19-importance-sampling-approximation.teaching.md` | `¶0247-¶0261` | K个样本近似期望；配分函数的重要性采样估计；提议分布的复用策略 | 重要性采样—采样近似 | `ch15-20` |
| 21 | `ch15-20` | §15.5.3.2 重要性采样—综合梯度与总结 | `knowledge/teaching-guides/chapter-15/15-20-importance-sampling-summary.teaching.md` | `¶0262-¶0270` | 综合梯度的最终近似形式；K≈100的实践取值；加速比例|V|/K；提议分布选取对稳定性的影响 | 重要性采样—综合与总结 | `ch15-21` |
| 22 | `ch15-21` | §15.5.3.3 NCE—概念与贝叶斯推导 | `knowledge/teaching-guides/chapter-15/15-21-nce-concept-and-bayes.teaching.md` | `¶0271-¶0283` | NCE的核心思想（密度估计→二分类）；三个分布（pᵣ/p_θ/q）；真实样本与噪声样本的区分；贝叶斯后验概率p(y=1|x)的推导 | NCE—概念与贝叶斯推导 | `ch15-22` |
| 23 | `ch15-22` | §15.5.3.3 NCE—损失函数与自归一化 | `knowledge/teaching-guides/chapter-15/15-22-nce-loss-and-self-normalization.teaching.md` | `¶0284-¶0301` | NCE二分类损失函数；配分函数作为可学习参数z_h̃；自归一化性质（exp(z_h̃)≈1）；未归一化分布可直接替代 | NCE—损失函数与自归一化 | `ch15-23` |
| 24 | `ch15-23` | §15.5.3.3 NCE—简化损失与噪声分布选择 | `knowledge/teaching-guides/chapter-15/15-23-nce-simplified-loss-and-noise.teaching.md` | `¶0302-¶0310` | 简化后的NCE损失（σ与Δs的形式）；噪声分布选取原则；K≈25~100实践取值；三种加速方法对比总结 | NCE—简化损失与噪声分布 | `ch15-24` |
| 25 | `ch15-24` | §15.6 Seq2Seq概念与条件概率框架 | `knowledge/teaching-guides/chapter-15/15-24-seq2seq-concept-and-framework.teaching.md` | `¶0311-¶0323` | Seq2Seq的定义（输入序列→输出序列）；条件序列生成问题；输入/输出长度可不相同；条件概率估计目标p(y_t | y_{1:(t-1)}, x)；MLE训练；贪婪/束搜索生成 | Seq2Seq概念与框架 | `ch15-25` |
| 26 | `ch15-25` | §15.6.1 基于RNN的Seq2Seq | `knowledge/teaching-guides/chapter-15/15-25-rnn-seq2seq.teaching.md` | `¶0324-¶0336` | 编码器-解码器结构；编码器f_enc生成固定维度向量u；解码器f_dec自回归生成；两个缺点（容量问题、长程依赖问题） | 基于RNN的Seq2Seq | `ch15-26` |
| 27 | `ch15-26` | §15.6.2 基于注意力的Seq2Seq | `knowledge/teaching-guides/chapter-15/15-26-attention-seq2seq.teaching.md` | `¶0337-¶0350` | 注意力机制解决信息瓶颈；h_{t-1}^dec作为查询向量；上下文向量c_t的计算；c_t作为解码器额外输入 | 基于注意力的Seq2Seq | `ch15-27` |
| 28 | `ch15-27` | §15.6.3 自注意力与多头自注意力 | `knowledge/teaching-guides/chapter-15/15-27-self-attention-and-multihead.teaching.md` | `¶0351-¶0361` | 自注意力模型的目的（全连接+并行）；缩放点积注意力公式；Q/K/V三个投影矩阵；多头自注意力的思想（多个投影空间）；多头输出的拼接与投影 | 自注意力与多头自注意力 | `ch15-28` |
| 29 | `ch15-28` | §15.6.3.3 位置编码与自注意力序列编码层 | `knowledge/teaching-guides/chapter-15/15-28-positional-encoding-and-encoder.teaching.md` | `¶0362-¶0377` | 位置编码的必要性（自注意力忽略位置信息）；正弦/余弦位置编码公式；残差连接+层归一化；逐位置FFN；多层堆叠的全连接编码结构 | 位置编码与序列编码层 | `ch15-29` |
| 30 | `ch15-29` | §15.6.3.4 Transformer模型 | `knowledge/teaching-guides/chapter-15/15-29-transformer.teaching.md` | `¶0378-¶0392` | Transformer=基于多头自注意力的Seq2Seq；编码器结构（多层多头自注意力→K^enc/V^enc）；解码器三模块（掩蔽自注意力/编码器注意力/FFN）；掩蔽自注意力的作用；右移目标序列训练方式 | Transformer模型 | `ch15-30` |
| 31 | `ch15-30` | §15.7 总结和深入阅读 | `knowledge/teaching-guides/chapter-15/15-30-summary-and-reading.teaching.md` | `¶0393-¶0399` | 序列生成模型=自回归生成模型；曝光偏差/训练目标不一致/计算效率三条问题线；Seq2Seq发展路线（RNN→注意力→Transformer） | 总结和深入阅读 | `ch15-test` |
| 32 | `ch15-test` | 第15章章测 | 无新增讲义；覆盖第15章已通过单元 | 第15章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测 | 第15章章测 | 待解锁下一章 |

## 当前审计结论

- 第15章 31 个教学单元（`ch15-00` ~ `ch15-30`）均有教学指引和教材段落。
- `ch15-00` 覆盖引言，¶0001-¶0006 包含乔姆斯基引语和认知心理学实验背景，不单独设正式考点。
- `ch15-01` 中 `¶0024` 和 `¶0026` 为交叉引用（"参见第6.1.2节"/"参见第D.2.2.1节"），标记为课堂识别不计分。
- `ch15-02` 中 `¶0040` 为习题引用，标记为课堂识别不计分。
- `ch15-04` 中 `¶0059` 为交叉引用（拉格朗日乘子），¶0061/¶0077 为URL，标记为课堂识别不计分和了解即可。
- `ch15-05` 中 `¶0077` 为URL，`¶0079` 提及Good-Turing/Kneser-Ney平滑，`¶0080` 为习题引用，均不进入正式题。
- `ch15-07` 中 `¶0101` 含注意力机制交叉引用和习题引用，标记为课堂识别不计分；`¶0111` 含URL和残差网络交叉引用。
- `ch15-12` 为4段轻量单元，ROUGE与BLEU边界清晰，正式题只考指标用途和召回率直觉。
- `ch15-13` 中 `¶0167` 为交叉引用（协变量偏移）。
- `ch15-14` 中 `¶0178` 为交叉引用（MDP）。
- `ch15-15` 中 `¶0195` 为URL，`¶0199` 为交叉引用（配分函数）。
- `ch15-16` 中 `¶0208` 为URL。
- `ch15-17` 中 `¶0225-¶0226` 含WordNet/Miller和霍夫曼编码人名年份背景，¶0226含交叉引用（熵编码），均不进入正式题；算法15.1伪代码细节为了解即可。
- `ch15-18` 为19段公式密集例外，正式题只考目标/提议分布/梯度近似含义，不考完整推导；`¶0229`/`¶0241` 为交叉引用，`¶0237` 为URL。
- `ch15-21` 中 `¶0289` 为交叉引用（生成对抗网络），`¶0284`/`¶0295`/`¶0300` 为URL。
- `ch15-22` 中 `¶0295` 为URL。
- `ch15-25` 中 `¶0327` 为URL，`¶0336` 为交叉引用（长程依赖）。
- `ch15-26` 中 `¶0338`/`¶0348` 为交叉引用（注意力机制），`¶0342` 为URL。
- `ch15-27` 中 `¶0352` 为交叉引用（自注意力模型）。
- `ch15-28` 中 `¶0367` 为习题引用，`¶0374` 为交叉引用（层归一化）。
- `ch15-29` 中 `¶0379` 为URL，`¶0384` 为交叉引用。
- `ch15-30` 中 `¶0394` 为URL，文献引用[Bengio et al., 2003]等人名年份为课堂识别不计分。Texar框架为了解即可。
- `¶0400-¶0405` 为习题，`¶0406-¶0425` 为参考文献，不进入任何教学单元的正式题范围。
