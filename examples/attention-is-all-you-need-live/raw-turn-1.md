你的判断基本正确，混在一起的是三件不同的事：**数学上的可表示性、模型是否能学会利用它、以及长度外推是否被实验验证。**

先只看一个频率 \(\omega\)，把对应的两维写成

\[
u_p=
\begin{bmatrix}
\sin(\omega p)\\
\cos(\omega p)
\end{bmatrix}.
\]

利用和角公式：

\[
u_{p+k}=
\begin{bmatrix}
\cos(\omega k)&\sin(\omega k)\\
-\sin(\omega k)&\cos(\omega k)
\end{bmatrix}
u_p.
\]

关键不是“线性函数”这四个字本身，而是：这个变换矩阵只依赖偏移 \(k\)，不依赖绝对位置 \(p\)。因此，同一个相对位移在所有位置上都表现为同一种旋转关系。不同频率各自有一个这样的二维旋转，合起来就是整个位置编码上的分块线性变换。

但这并不逻辑上保证注意力一定会学到相对位置。论文原话是作者“**hypothesized** it would allow the model to easily learn”，即它提供了一种有利的表示结构或归纳偏置；随后还需要查询、键的线性投影和点积真正把这种结构利用起来。[第 3.5 节原文](/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:276)

你可以自己补上最关键的一步：计算同一频率下

\[
u_p^\top u_q
\]

并用三角恒等式化简。然后问自己：结果依赖 \(p,q\) 各自，还是只依赖 \(p-q\)？这一步才真正把“固定偏移的旋转关系”接到“注意力分数可以感知相对位置”上。

关于长度外推，你的质疑完全成立。这里要区分：

- 正弦编码对任意位置都**可以计算**，因此不会像有限位置表那样天然缺少未见位置的参数。
- 模型在更长序列上仍然**表现良好**，则是另一个经验命题；可计算不等于会泛化。

Table 3 row (E) 只显示：在 `newstest2013` 开发集上，sinusoid 的 base model 是 PPL 4.92、BLEU 25.8，learned positional embedding 是 PPL 4.92、BLEU 25.7，支持的是“两者在该开发集上结果近似”，不是长度外推。[Table 3](/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:446) 作者对外推也用了审慎措辞 “**may allow**”，没有声称已经验证。[相关原文](/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:295)

所以更准确的读法是：第 3.5 节给出了一个关于相对位置的结构性动机，以及一个关于长度外推的合理猜想；Table 3 只验证了换成 learned embedding 不会明显改变常规开发集翻译质量。