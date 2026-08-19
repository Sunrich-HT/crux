你的理解大体是对的，但这里确实混着三个不同层次：

1. 正弦编码具有一种关于相对位移的代数结构。
2. Transformer 可以利用这种结构。
3. Transformer 实际学会了它，并能外推到更长序列。

论文真正明确给出的主要是第 1 点；第 2 点是作者的设计动机，第 3 点则只是推测。

对第 \(i\) 个频率，令

\[
\omega_i=10000^{-2i/d_{\text{model}}}
\]

对应的两个位置编码分量是

\[
\begin{bmatrix}
\sin(\omega_i pos)\\
\cos(\omega_i pos)
\end{bmatrix}.
\]

当位置增加固定偏移 \(k\) 时，利用三角函数加法公式：

\[
\begin{bmatrix}
\sin(\omega_i(pos+k))\\
\cos(\omega_i(pos+k))
\end{bmatrix}
=
\begin{bmatrix}
\cos(\omega_i k) & \sin(\omega_i k)\\
-\sin(\omega_i k) & \cos(\omega_i k)
\end{bmatrix}
\begin{bmatrix}
\sin(\omega_i pos)\\
\cos(\omega_i pos)
\end{bmatrix}.
\]

右边的矩阵只依赖 \(k\)，不依赖 \(pos\)。把所有频率对应的二维旋转矩阵拼成一个分块对角矩阵 \(R_k\)，就得到

\[
PE(pos+k)=R_k PE(pos).
\]

这就是论文所谓的“对于固定偏移 \(k\)，\(PE(pos+k)\) 是 \(PE(pos)\) 的线性函数”。

但关键是：这不等于“注意力必然学会相对位置”。更准确地说，它让同一个相对位移在任何绝对位置上都表现为同一个线性变换，因此模型不必为“第 10 位到第 13 位”和“第 100 位到第 103 位”分别学习两套规则。

它与点积注意力还有一个更直接的联系。只看位置编码，有

\[
PE(p)^\top PE(q)
=
\sum_i \cos\bigl(\omega_i(p-q)\bigr).
\]

这里用的是

\[
\sin a\sin b+\cos a\cos b=\cos(a-b).
\]

所以这个点积只依赖相对距离 \(p-q\)，而不依赖两个位置分别是多少。经过可学习的 \(W_Q,W_K\) 后，模型还可以旋转、组合或筛选这些频率，从而形成诸如“偏好前一个位置”“偏好大约相隔 \(k\) 个位置”的注意力模式。

因此，最准确的表述是：

> 正弦编码以一种共享的、线性可操作的形式暴露了相对位移，使注意力有可能较容易地学习相对位置规则。

不是：

> 只要满足这个线性关系，注意力就一定会学会相对位置。

还要记住，实际输入是词向量与位置编码之和：

\[
x_{pos}+PE(pos).
\]

注意力分数中会同时出现内容与内容、内容与位置、位置与内容、位置与位置的交互。原版 Transformer 并没有把相对距离作为一个独立变量直接交给注意力；后来的 relative positional encoding、relative bias 等方法才做得更显式。

关于长度外推，你的质疑完全成立。第 3.5 节的原话非常谨慎：

> “We chose the sinusoidal version because it **may allow** the model to extrapolate ...”

这里的 `may allow` 是可能性或归纳偏置，不是实验结论。理由是：

- learned positional embedding 本质上是按位置查表；训练中没出现的位置没有得到有效训练，甚至可能根本没有表项。
- sinusoidal encoding 是一个确定函数，可以直接计算任意位置的编码，而且上述位移关系在训练范围之外仍然成立。

这说明正弦编码在机制上允许输入更长的位置，却不保证整个模型能正确处理更长序列。模型学到的注意力模式、长度分布、softmax 行为以及任务本身都仍可能无法外推。

Table 3 row (E) 只报告了把 sinusoidal encoding 换成 learned positional embedding 后，在 `newstest2013` 开发集上的结果：

- sinusoidal base：PPL 4.92，BLEU 25.8
- learned positional embedding：PPL 4.92，BLEU 25.7

因此它支持的结论只有：在该开发集的常规翻译质量上，两者几乎相同。这也正是论文随后所说的 “nearly identical results”。它没有按长度分组，更没有专门测试超过训练长度的序列，所以不能作为长度外推的证据。

一句话整理：

> 线性关系是数学性质；“容易学习相对位置”是由此提出的建模假设；“可能外推”是正弦函数相对于位置查表的机制优势；Table 3 只验证了常规开发集性能基本不受损，没有验证长度外推。

原文位置可见 [attention-is-all-you-need.txt](/private/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:276) 和 [Table 3 row (E)](/private/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:446)。