# AI 能让公共采购更廉洁吗？

以阿尔巴尼亚 Diella 为切入的风险识别与问责机制设计。

**状态：六部分研究设计稿 v0.1，2026-10-29。未开展合同级效果估计。**

[阅读研究网页](https://chenergou847.github.io/diella-procurement-accountability/) · [浏览文献索引](https://chenergou847.github.io/diella-procurement-accountability/literature.html) · [阅读 Markdown 研究稿](paper.md)

本项目服务于《人工智能与国家治理》课堂研究。主问题是 Diella 的实际采购应用是否以及通过什么机制使采购更廉洁；不预设肯定或否定结论。研究区分政治宣布、技术建设与具体采购的真实使用，也区分程序透明、风险变化与经核实的采购问题。

## 已有产出

| 部分 | 内容 | 入口 |
|---|---|---|
| 引言 | 现实问题、解释缺口、待检验答案与预期贡献 | [正文](manuscript/01-introduction.md) |
| 文献述评 | 按技术反腐、检测与效果、采购改革及算法问责组织对话 | [正文](manuscript/02-literature-review.md) |
| 理论与预期 | 概念、机制链、条件、竞争解释及可反驳预期 | [正文](manuscript/03-theory-expectations.md) |
| 案例背景 | 可核时间节点、制度约束与共同改革 | [正文](manuscript/04-case-background.md) |
| 研究设计 | 公开资料的过程追踪、测量、条件性的定量路线 | [正文](manuscript/05-research-design.md) |
| 数据与材料 | 已有资料、阅读深度、缺口、编码和选择偏差 | [正文](manuscript/06-data-materials.md) |

文献索引含 **23 条正式书目和 4 条辅助材料**。正式书目包括学术出版、专业研究报告及制度原件，不能统称同行评审论文。每条提供主要观点、归纳依据、选用理由、适用边界和 GB/T 7714-2015 引用；实际档案中的工作稿与正式版可切换。

## 目录

- `manuscript/`：六部分可编辑的 Markdown 源稿。
- `paper.md`：由六部分合并生成的研究稿及引用书目。
- `docs/`：可直接打开、适配窄屏与打印的静态网页；GitHub Pages 发布目录。
- `data/bibliography.json`：筛选后的公开书目，不含个人电脑路径或未纳入条目。
- `data/claims.csv`：当前稿件的事实、政府主张、研究预期和资料缺口登记。
- `data/procurement-template.csv`：采购数据字段模板，**只有表头，没有实际采购数据**。
- `data/codebook.md`：证据和采购字段的编码规则草案。
- `research/`：已有范围综述、研究设计和方法说明的公开适配版本。
- `scripts/build_site.py`：生成研究稿、网页及引用下载。
- `audit/`：来源核读范围、发布核验及交付状态。

## 使用与生成

打开 `docs/index.html` 可阅读完整六部分，`docs/literature.html` 可筛选、检索和复制引用。正文与样式使用内嵌内容，基础阅读和检索不依赖联网获取数据；原始来源访问外网。

```bash
python -m pip install -r requirements.txt
python scripts/build_site.py
python scripts/validate.py
```

修改正文后重新生成；书目、事实登记和研究判断的更新仍须回到原始来源核对。数据模板不是已经完成的采集，研究预期也不是统计发现。

## 下一步经验工作

先用小规模公开档案核实采购编号、AI 实际使用、复核及结果字段是否可得。能够建立证据链时开展机制分析；如取得分批上线、可比对照和足够多期数据，再评估 DiD 等因果设计。未取得条件时报告具体缺口，不用任命日期或政务服务交互量替代处理与廉洁结果。

## 来源与贡献说明

用户提出研究问题、质疑不可经验研究的表述并要求提高来源质量；Codex 辅助公开检索、文件核验、文献整理、稿件与网页制作。本项目尚未开展访谈、正式采购样本编码或 Diella 政策效果估计。课堂使用时应按实际核验和修改说明贡献。

第三方原始 PDF 和全文网页快照保留在原工作区，公开仓库提供引用与原站链接，不代为再分发。原作者及机构对第三方内容保留相应权利。
