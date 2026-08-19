<div align="center">
  <img src="assets/readme-banner.png" alt="Crux：面向论文、科研和决策的证据约束型思考伙伴" width="100%">

  <p><strong>一个知道何时追问、何时查证、何时直接给结论的 AI Skill。</strong></p>
  <p>适用于论文精读、科研辅导，以及存在真实取舍的个人与商业决策。</p>

  <p>
    <a href="https://github.com/Sunrich-HT/crux/actions/workflows/ci.yml"><img src="https://github.com/Sunrich-HT/crux/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F766E.svg" alt="MIT License"></a>
    <a href="skills/crux/SKILL.md"><img src="https://img.shields.io/badge/agent_skill-Crux-E4573D.svg" alt="Crux agent skill"></a>
  </p>

  <p>
    <a href="#安装-skill">安装</a> ·
    <a href="#三个核心场景">场景</a> ·
    <a href="#crux-如何工作">原理</a> ·
    <a href="docs/examples.md">示例</a> ·
    <a href="CONTRIBUTING.md">参与贡献</a> ·
    <a href="README.md">English</a>
  </p>
</div>

---

## Crux 是什么？

`Crux` 的字面意思是“决定成败的关键点”。作为品牌名，它简短、易记，但单独出现确实不够直观，所以完整定位是：

> **Crux：面向论文、科研和决策的证据约束型思考伙伴。**

普通 AI 助手常常走向两个极端：过早把答案全部交出来，或者用没完没了的“苏格拉底式提问”拖住用户。还有一些助手可以把正反两面都写得很漂亮，却没有区分哪一边真的有证据。

Crux 把“这一轮最多帮到什么程度”做成明确契约：先找到会改变结论的关键分歧，再区分事实、价值、预测和约束，最后只执行一个最有价值的认知动作。这个动作可以是一个问题、一次证据核查、一张对照表，也可以是带停止条件的直接建议。

## 安装 Skill

为 Codex 全局安装：

```bash
npx skills add Sunrich-HT/crux --global --agent codex --skill crux --yes --copy
```

然后直接描述需求，或显式调用：

```text
$crux 精读这篇论文。请分开作者实际测量到的结果与作者的推断，
找出最强替代解释，并设计一个成本最低的复现实验。
```

安装前查看仓库中的 Skill：

```bash
npx skills add Sunrich-HT/crux --list
```

## 三个核心场景

| 场景 | Crux 解决什么问题 | 典型产出 |
| --- | --- | --- |
| 论文精读 | 避免把摘要复述误当成理解，也避免替用户做完全部判断 | 主张-证据表、最强替代解释、关键消融、最小复现方案 |
| 科研辅导 | 既不盲目认同研究想法，也不抢走假设与解释的所有权 | 竞争假设、可区分预测、实验设计、继续/修改/停止标准 |
| 个人与商业决策 | 不把价值问题伪装成事实问题，也不在信息足够时继续追问 | 条件化建议、翻转阈值、最小可逆行动、复盘与止损条件 |

你可以指定交互目标：

- `coach`：保留你的归纳、假设和判断工作；
- `collaborate`：共同分析，并标明假设与证据来自哪里；
- `deliver`：直接交付完整分析或建议，不人为设置答题关卡。

更多可直接使用的请求见 [示例文档](docs/examples.md)。

## Crux 如何工作

```mermaid
flowchart LR
    A[用户目标] --> B[当前观点与<br/>最强替代观点]
    B --> C[决定性分歧 Crux]
    C --> D[证据与<br/>不确定性地图]
    D --> E[本轮披露契约<br/>R0-R7]
    E --> F[一个认知动作]
    F --> G[审计、结论<br/>或状态更新]
```

它不是一个更长的 Prompt，而是两个互补层：

- `skills/crux/` 提供可安装的交互行为；
- `src/crux_supervisor/` 提供不依赖模型的确定性策略核心，让应用能够审计本轮允许什么、禁止什么以及原因。

主要原则：

- **双向钢人，但不制造虚假对称。** 认真强化替代观点，再按照证据质量赋权。
- **一轮只做一个关键动作。** 追问、查证、比较或建议，不把问卷塞进一次回复。
- **必须收敛。** 默认连续两轮只提问后，就应带着显式假设继续推进。
- **权限与生成分离。** 自由文本不能直接提高答案披露等级。
- **优先修改，不轻易拒绝。** 输出越界时，降到允许的层级后继续帮助。

## 本地运行策略核心

需要 Python 3.11+：

```bash
git clone https://github.com/Sunrich-HT/crux.git
cd crux
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

crux contract evals/states/research-unknown.json
crux eval evals/policy_cases.jsonl
python -m unittest discover -s tests -v
```

## 研究依据与当前状态

Crux 结合了“双向钢人论证 + 关键分歧发现”与论文 [*Teaching a Large Language Model Tutor to Withhold the Answer*](https://arxiv.org/abs/2608.12292) 中可迁移的工程思想：不要相信一个过载 Prompt 能同时处理教学策略、生成、检测和诊断，而应把不可逆权限交给可检查的状态与代码。

当前项目是 **Alpha 研究原型**。确定性策略约束已有自动化测试，但它尚未证明能带来长期学习迁移、更好的科研成果或更正确的商业决策。完整评估路线见 [研究议程](docs/research-agenda.md)。

## 参与贡献

欢迎贡献对抗性评测、来源审计、模型适配器、论文精读产物和人类评估方案。开始前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，大型改动建议先提交 Proposal。

## License

MIT，见 [LICENSE](LICENSE)。
