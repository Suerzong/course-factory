# 第14章 覆盖审计表

本表用于审计第14章是否形成稳定闭环。AI 教学第14章时，应以 `learning-path/chapter-14.md` 为主路线，并用本表确认每个单元都能追溯到讲义、教材段落、练习边界和掌握记录。

## 审计规则

- `正式题范围` 只包含教学指引中 `出题权限=正式题` 的核心知识点。
- `课堂识别不计分` 可以在讲解中轻量确认，但不计入正确率和推进依据。
- `掌握追踪行` 必须能在 `progress/mastery-tracker.md` 中用同一 `单元ID` 找到。
- 未达标时必须停留在当前单元，进入补救和再测，不得跳到下一单元。

| 顺序 | 单元ID | 小节 | 教学指引 | 教材段落 | 正式题范围 | 掌握追踪行 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `ch14-00` | 第14章 引言 | `knowledge/teaching-guides/chapter-14/14-00-introduction.teaching.md` | `¶0001-¶0006` | RL动机（标注困境）；RL定义三要素；贡献度分配问题；RL vs 监督学习 | 第14章引言 | `ch14-01` |
| 2 | `ch14-01` | §14.1.1 典型例子 | `knowledge/teaching-guides/chapter-14/14-01-typical-examples.teaching.md` | `¶0007-¶0012` | 多臂赌博机问题设定和目标；悬崖行走问题四要素；RL应用领域 | 典型例子 | `ch14-02` |
| 3 | `ch14-02` | §14.1.2 强化学习定义与策略 | `knowledge/teaching-guides/chapter-14/14-02-rl-definition-policy.teaching.md` | `¶0013-¶0028` | 智能体与环境角色；RL五要素；确定性vs随机性策略；随机性策略两个优点 | RL定义与策略 | `ch14-03` |
| 4 | `ch14-03` | §14.1.3 MDP定义 | `knowledge/teaching-guides/chapter-14/14-03-mdp-definition.teaching.md` | `¶0029-¶0042` | 交互时序循环；马尔可夫性质直觉；MP vs MDP；MDP状态转移概率 | MDP定义 | `ch14-04` |
| 5 | `ch14-04` | §14.1.3 轨迹概率 | `knowledge/teaching-guides/chapter-14/14-04-trajectory-probability.teaching.md` | `¶0043-¶0048` | 轨迹定义；轨迹概率分解公式；奖励不参与轨迹概率 | 轨迹概率 | `ch14-05` |
| 6 | `ch14-05` | §14.1.4 总回报与目标函数 | `knowledge/teaching-guides/chapter-14/14-05-return-and-objective.teaching.md` | `¶0049-¶0061` | 总回报定义；回合式vs持续式任务；折扣因子γ的作用；RL目标函数J(θ) | 总回报与目标函数 | `ch14-06` |
| 7 | `ch14-06` | §14.1.5.1 状态值函数与贝尔曼方程 | `knowledge/teaching-guides/chapter-14/14-06-state-value-function.teaching.md` | `¶0062-¶0077` | V^π(s)定义和直觉；期望回报两步分解；贝尔曼方程递归结构；迭代求解 | 状态值函数 | `ch14-07` |
| 8 | `ch14-07` | §14.1.5.2-§14.1.6 Q函数与深度强化学习 | `knowledge/teaching-guides/chapter-14/14-07-q-function-and-drl.teaching.md` | `¶0078-¶0090` | Q函数定义及与V的关系；Q函数贝尔曼方程；值函数驱动策略改进；DRL必要性（状态爆炸+NN泛化）；DRL基本思路 | Q函数与DRL | `ch14-08` |
| 9 | `ch14-08` | §14.2 基于值函数的方法（引入） | `knowledge/teaching-guides/chapter-14/14-08-value-based-intro.teaching.md` | `¶0091-¶0102` | 评估→改进循环框架；贪心策略改进公式；策略改进定理直觉；动态规划vs MC两种计算方式 | 值函数方法引入 | `ch14-09` |
| 10 | `ch14-09` | §14.2.1.1 策略迭代算法 | `knowledge/teaching-guides/chapter-14/14-09-policy-iteration.teaching.md` | `¶0103-¶0111` | 基于模型RL的含义；策略迭代两步循环（评估+改进）；贝尔曼方程迭代评估 | 策略迭代 | `ch14-10` |
| 11 | `ch14-10` | §14.2.1.2 值迭代算法 | `knowledge/teaching-guides/chapter-14/14-10-value-iteration.teaching.md` | `¶0112-¶0125` | 值迭代vs策略迭代核心区别；贝尔曼最优方程；V*→Q*→π*链条；两种算法复杂度权衡 | 值迭代 | `ch14-11` |
| 12 | `ch14-11` | §14.2.1.2 基于模型方法的限制 | `knowledge/teaching-guides/chapter-14/14-11-model-based-limitations.teaching.md` | `¶0126-¶0130` | 限制一（模型需已知）；限制二（状态数多效率低）；R-max基本思路 | 基于模型限制 | `ch14-12` |
| 13 | `ch14-12` | §14.2.2 蒙特卡罗方法基础 | `knowledge/teaching-guides/chapter-14/14-12-monte-carlo-basics.teaching.md` | `¶0131-¶0140` | Model-Free RL含义；MC近似Q函数公式和直觉；采样→估计→改进迭代框架 | MC方法基础 | `ch14-13` |
| 14 | `ch14-13` | §14.2.2 利用与探索 + 同/异策略 | `knowledge/teaching-guides/chapter-14/14-13-exploration-on-off-policy.teaching.md` | `¶0141-¶0149` | 利用vs探索权衡；ϵ-贪心法机制；同策略vs异策略区分；重要性采样作用 | 利用与探索 | `ch14-14` |
| 15 | `ch14-14` | §14.2.3 TD学习推导 | `knowledge/teaching-guides/chapter-14/14-14-td-learning-derivation.teaching.md` | `¶0150-¶0161` | TD vs MC核心区别；Q函数增量更新公式；TD用r+γQ(s',a')近似G；TD Error含义 | TD学习推导 | `ch14-15` |
| 16 | `ch14-15` | §14.2.3 SARSA算法 | `knowledge/teaching-guides/chapter-14/14-15-sarsa-algorithm.teaching.md` | `¶0162-¶0175` | SARSA更新公式逐项解释；SARSA是同策略算法；SARSA只需五元组；TD与多巴胺类比 | SARSA算法 | `ch14-16` |
| 17 | `ch14-16` | §14.2.3.1 Q学习 | `knowledge/teaching-guides/chapter-14/14-16-q-learning.teaching.md` | `¶0176-¶0183` | Q学习更新公式及max含义；Q学习vs SARSA区别；Q学习是异策略算法 | Q学习 | `ch14-17` |
| 18 | `ch14-17` | §14.2.4 深度Q网络 | `knowledge/teaching-guides/chapter-14/14-17-deep-q-network.teaching.md` | `¶0184-¶0198` | 值函数近似动机；Q学习目标函数L；目标网络冻结；经验回放 | DQN | `ch14-18` |
| 19 | `ch14-18` | §14.3 策略梯度推导（上） | `knowledge/teaching-guides/chapter-14/14-18-policy-gradient-1.teaching.md` | `¶0199-¶0213` | 策略搜索vs值函数方法；策略梯度核心公式直觉；log p_θ梯度与转移概率无关 | 策略梯度推导（上） | `ch14-19` |
| 20 | `ch14-19` | §14.3-§14.3.1 策略梯度（下）+ REINFORCE | `knowledge/teaching-guides/chapter-14/14-19-reinforce-algorithm.teaching.md` | `¶0214-¶0226` | 策略梯度时序展开；REINFORCE算法流程；REINFORCE的MC性质和方差问题 | REINFORCE算法 | `ch14-20` |
| 21 | `ch14-20` | §14.3.2 控制变量法与方差缩减 | `knowledge/teaching-guides/chapter-14/14-20-control-variate-variance-reduction.teaching.md` | `¶0227-¶0238` | REINFORCE方差大的原因；控制变量法原理；方差缩减与相关性关系 | 控制变量法 | `ch14-21` |
| 22 | `ch14-21` | §14.3.2 带基准线的REINFORCE（原理） | `knowledge/teaching-guides/chapter-14/14-21-baseline-reinforce-principle.teaching.md` | `¶0239-¶0248` | 带基准线策略梯度公式；b(s_t)不改变期望的条件；V^π(s)作为好基准线的原因 | 基准线REINFORCE原理 | `ch14-22` |
| 23 | `ch14-22` | §14.3.2 带基准线的REINFORCE（算法） | `knowledge/teaching-guides/chapter-14/14-22-baseline-reinforce-algorithm.teaching.md` | `¶0249-¶0257` | V_φ(s)训练目标；双网络同时更新规则；带基准线REINFORCE≠Actor-Critic原因 | 基准线REINFORCE算法 | `ch14-23` |
| 24 | `ch14-23` | §14.4 演员-评论员算法 | `knowledge/teaching-guides/chapter-14/14-23-actor-critic.teaching.md` | `¶0258-¶0272` | Actor-Critic分工；TD近似回报r+γV(s')；Critic TD error更新；Actor用V做基准线；融合优势总结 | 演员-评论员算法 | `ch14-24` |
| 25 | `ch14-24` | §14.5 总结和深入阅读（上） | `knowledge/teaching-guides/chapter-14/14-24-summary-and-reading-1.teaching.md` | `¶0273-¶0281` | RL与监督学习两个区别；RL历史双源流；RL算法三分法；四种算法三步对比 | 总结和深入阅读（上） | `ch14-25` |
| 26 | `ch14-25` | §14.5 总结和深入阅读（下） | `knowledge/teaching-guides/chapter-14/14-25-advanced-topics.teaching.md` | `¶0282-¶0290` | 全部为课堂识别不计分（DQN/DDPG/A3C/POMDP/IRL/HRL）；不进入正式题、章测或推进依据 | 进阶主题（不计分） | `ch14-test` |
| 27 | `ch14-test` | 第14章章测 | 无新增讲义；覆盖第14章已通过单元 | 第14章已解锁段落 | 只从已达标单元的正式题范围抽取，参考文献、推荐书目、习题和了解即可内容不计入章测。ch14-25不计入章测 | 第14章章测 | 第15章未解锁 |

## 当前审计结论

- 第14章 26 个教学单元（`ch14-00` ~ `ch14-25`）均有教学指引和教材段落。
- `ch14-00` 覆盖引言和图灵引言，不展开MDP或值函数。
- `ch14-01` 覆盖多臂赌博机和悬崖行走两个典型例子，不展开求解算法。
- `ch14-03` 覆盖MDP定义和图模型，¶0035-¶0037为马尔可夫过程形式化定义，不单独设考点。
- `ch14-04` 覆盖轨迹概率分解，6段（其中¶0047为空编号，¶0048为URL）。
- `ch14-05` 覆盖总回报和目标函数，不展开目标函数梯度计算。
- `ch14-07` 合并Q函数和深度强化学习引入，13段=Q函数(¶0078-¶0086)+DRL(¶0088-¶0090)，正式考点5个。
- `ch14-09` 覆盖策略迭代算法，9段（含算法伪代码）。
- `ch14-10` 覆盖值迭代算法，14段=值迭代(¶0112-¶0121)+伪代码(¶0122)+复杂度对比(¶0123-¶0125)。
- `ch14-11` 为短单元（5段），覆盖模型已知的两大限制和R-max。
- `ch14-13` 合并利用与探索和同异策略，9段，正式考点4个。
- `ch14-14` 覆盖TD学习推导，12段（含增量公式推导和贝尔曼近似）。
- `ch14-18` 覆盖策略梯度推导上，15段（含6步链式推导），正式考点3个。
- `ch14-19` 覆盖策略梯度下+REINFORCE，13段=展开(¶0214-¶0222)+REINFORCE(¶0223-¶0226)。
- `ch14-20` 覆盖控制变量法，12段（含方差公式推导）。
- `ch14-24` 覆盖总结上（RL vs SL区别、历史双源流、算法三分法、表14.1对比）。
- `ch14-25` 覆盖进阶主题（DQN/DDPG/A3C/POMDP/IRL/HRL），全部为课堂识别不计分，不进入正式题、章测或推进依据。
- `¶0291-¶0314` 为习题和参考文献，不进入任何教学单元的正式题范围。
- 第15章仍未解锁，待第14章章测通过后再进入。
