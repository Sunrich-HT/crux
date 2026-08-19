你前半段理解是对的：没有位置编码时，self-attention 对输入排列本身是等变的，无法仅凭机制区分先后；作者因此把位置信息加到 embedding 中。论文原文也确实只说，他们“假设”线性关系会让模型更容易按相对位置进行注意，而不是证明模型必然学会相对位置。[第 3.5 节](/private/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:276)

你后半段的证据判断也准确。Table 3 row (E) 比较的是同一开发集 `newstest2013` 上：

- sinusoidal：PPL 4.92，BLEU 25.8
- learned positional embedding：PPL 4.92，BLEU 25.7

它支持的只是“两种编码在该翻译开发集上结果近似”，没有按长度分组，更没有测试超过训练长度的序列。[Table 3](/private/tmp/crux-real-paper-test.WM6NqQ/attention-is-all-you-need.txt:446) 因此，“可能外推到更长序列”仍是作者给出的设计动机或假说，row (E) 并未验证它。这里不要把“函数在任意位置都有定义”与“训练后的模型在那些位置仍能正确工作”混为一谈。

现在真正需要你打通的是另一层：**可表达性不等于一定学会，但它能说明相对偏移是否以一种统一、容易被线性投影和点积读取的形式存在。**

只看一个频率，不考虑完整向量。令

\[
p(x)=[\sin(\omega x),\cos(\omega x)].
\]

用正弦、余弦的加法公式，计算

\[
p(\mathrm{pos})^\top p(\mathrm{pos}+k).
\]

请把它化到不能再化，然后用一句话回答：结果还依赖绝对位置 `pos` 吗？这一步做出来，我们再判断它与 dot-product attention 的 \(QK^\top\) 到底是什么关系。