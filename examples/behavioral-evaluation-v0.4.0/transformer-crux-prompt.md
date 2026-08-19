$crux

使用 coach 模式。你正在辅导一名研究生精读 Vaswani et al. (2017) 的经典论文《Attention Is All You Need》。

原始论文已经下载到当前目录：
- `attention-is-all-you-need.pdf`
- `attention-is-all-you-need.txt`

请以论文第 3.5 节 Positional Encoding 和 Table 3 row (E) 的原文为准，不要依赖二手总结。

学生的问题是：

> 我理解 self-attention 本身不会区分 token 的先后顺序，所以作者把位置编码加到词向量上。但我还是没真正理解：论文说对于固定偏移 k，PE(pos+k) 可以表示成 PE(pos) 的线性函数，这为什么就意味着注意力能够学习“相对位置”？另外，作者说正弦位置编码可能外推到训练时没见过的更长序列，Table 3 只比较了 learned embedding 和 sinusoid 在开发集上的 BLEU，看起来并没有直接测试长度外推。我的理解哪里对，哪里还混在一起？

请像真实论文导师一样直接回复学生。
