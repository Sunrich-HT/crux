你抓住了现象，但更准确地说，是“矩估计量 \(m_0,v_0\) 从 0 初始化”，不是矩本身为 0。现在先别背修正公式，把递推展开。

对任一坐标，Algorithm 1 给出

\[
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad m_0=0.
\]

连续代入可得

\[
m_t=(1-\beta_1)\left(g_t+\beta_1g_{t-1}+\cdots+\beta_1^{t-1}g_1\right).
\]

同理，

\[
v_t=(1-\beta_2)\left(g_t^2+\beta_2g_{t-1}^2+\cdots+\beta_2^{t-1}g_1^2\right).
\]

这两式是代数恒等式，只依赖三个条件：零初始化、固定的 \(\beta_1,\beta_2\)，以及 Algorithm 1 的递推形式；不需要梯度独立或同分布。

“偏差修正”则额外涉及概率假设。令

\[
\mu_i=\mathbb E[g_i],\qquad q_i=\mathbb E[g_i^2].
\]

利用期望的线性性，

\[
\mathbb E[m_t]=(1-\beta_1)\sum_{i=1}^{t}\beta_1^{t-i}\mu_i,
\qquad
\mathbb E[v_t]=(1-\beta_2)\sum_{i=1}^{t}\beta_2^{t-i}q_i.
\]

这里仍不要求各步梯度独立。要把它们称为对某个固定矩的无偏估计，关键假设是考察窗口内矩近似平稳，即 \(\mu_i=\mu\)、\(q_i=q\)。若矩随训练变化，修正只能补回零初始化造成的“权重缺口”，不能保证对当前矩严格无偏。

现在请你完成唯一关键一步：计算

\[
C_t(\beta)=(1-\beta)\sum_{i=1}^{t}\beta^{t-i},
\]

然后分别代入上面两个期望式。这个有限等比级数的结果，如何直接解释 Algorithm 1 中的两个除数？