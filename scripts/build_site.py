"""生成可离线阅读的研究网页；不需要访问网络或原工作区。"""
import csv,html,json,re,shutil
from pathlib import Path
import markdown

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
ROWS=json.loads((ROOT/'data/bibliography.json').read_text(encoding='utf-8'))
BY_ID={r['id']:r for r in ROWS}
DATE='2026-10-29'
esc=lambda s:html.escape(str(s),quote=True)
SECTIONS=[('01-introduction.md','introduction','引言','为什么值得研究'),('02-literature-review.md','literature-review','文献述评','与哪些解释对话'),('03-theory-expectations.md','theory','理论与预期','为什么可能改善或失效'),('04-case-background.md','background','案例背景','哪些制度与时间必须区分'),('05-research-design.md','design','研究设计','怎样用材料回答问题'),('06-data-materials.md','materials','数据与材料','已有证据、缺失与偏差')]

def render_md(text):
    # 引用ID转入文献卡片；原始来源仍可在卡片中直接访问。
    def cite(m):
        i=m.group(1)
        if i not in BY_ID:raise ValueError('引用不在公开书目：'+i)
        return '<a class="citation-ref" href="literature.html#'+i+'" title="'+esc(BY_ID[i]['title'])+'" aria-label="查看文献 '+i+'">'+i+'</a>'
    text=re.sub(r'\[([ADMP]\d{2})\]',cite,text)
    text=text.replace('../docs/literature.html','literature.html').replace('search-scope.md','https://github.com/chenergou847/diella-procurement-accountability/blob/main/research/search-scope.md')
    body=markdown.markdown(text,extensions=['tables','fenced_code','sane_lists'])
    body=re.sub(r'<table>(.*?)</table>',r'<div class="table-wrap"><table>\1</table></div>',body,flags=re.S)
    return body

def page(title,content,active,body_class=''):
    text=(ROOT/'templates/base.html').read_text(encoding='utf-8')
    values={'__TITLE__':esc(title),'__CSS__':(ROOT/'templates/site.css').read_text(encoding='utf-8'),'__JS__':(ROOT/'templates/site.js').read_text(encoding='utf-8'),'__CONTENT__':content,'__BODY_CLASS__':body_class,'__PAPER_ACTIVE__':'aria-current="page"' if active=='paper' else '', '__LIT_ACTIVE__':'aria-current="page"' if active=='lit' else '', '__METHOD_ACTIVE__':'aria-current="page"' if active=='method' else ''}
    for key,value in values.items():text=text.replace(key,value)
    return text

def reference_html(ids):
    return '<ol class="reference-list">'+''.join('<li id="ref-'+i+'"><span class="ref-id">'+i+' · '+esc(BY_ID[i]['selection_label'])+'</span>'+esc(BY_ID[i]['citation'])+' <a href="literature.html#'+i+'">观点与版本 ↗</a></li>' for i in sorted(ids))+'</ol>'

chunks=[];source_chunks=[];used=set()
for n,(filename,anchor,title,question) in enumerate(SECTIONS,1):
    raw=(ROOT/'manuscript'/filename).read_text(encoding='utf-8').strip()
    used.update(re.findall(r'\[([ADMP]\d{2})\]',raw))
    chunks.append('<section class="paper-section" id="'+anchor+'"><div class="section-no">SECTION '+str(n).zfill(2)+'</div>'+render_md(raw)+'</section>')
    source_chunks.append(raw)
unknown=used-set(BY_ID)
if unknown:raise ValueError('未知引用：'+','.join(unknown))
toc='<aside class="toc"><p class="toc-title">阅读目录 / CONTENTS</p><div class="toc-links">'+''.join('<a href="#'+a+'"><span>'+str(n).zfill(2)+'</span>'+t+'</a>' for n,(_,a,t,_) in enumerate(SECTIONS,1))+'</div><div class="toc-extra"><a href="#references">引用书目</a><a href="literature.html">浏览文献索引 ↗</a><a href="methods.html">具体研究方法 ↗</a></div><div class="reading-tools"><button id="font-toggle" aria-pressed="false">大字阅读</button><button id="print-page">打印 / 存为 PDF</button></div></aside>'
hero='''<section class="hero" id="top"><p class="eyebrow">RESEARCH NOTE 01 / ALBANIA · DIELLA</p><h1>AI 能让公共采购<br>更廉洁吗？</h1><p class="subtitle">以阿尔巴尼亚 Diella 为切入的风险识别与问责机制设计</p><div class="statusline"><span class="status">六部分研究设计稿 v0.1</span><span>2026-10-29</span><span>实证分析尚未开展</span></div><div class="hero-actions"><a href="#introduction">开始阅读 ↓</a><a href="downloads/paper.md" download>下载 Markdown 研究稿 ↗</a><a href="literature.html">查看引用与主要观点 ↗</a></div></section><div class="proposal"><div class="label">待检验的核心解释</div><p>AI 的廉洁效应，取决于风险信号能否经过<strong>可追溯的记录、有理由的复核和可执行的纠正</strong>，最终改变具体采购结果。</p></div>'''
content=hero+'<main id="main" class="reading-layout">'+toc+'<article class="article">'+''.join(chunks)+'<section id="references"><div class="section-no">REFERENCES</div><h2>引用书目</h2><p class="evidence-note">以下按本稿实际引用列出。评论与原始制度资料按类型使用；具体阅读深度和引用版本请展开文献索引核对。</p>'+reference_html(used)+'</section></article></main><a class="to-top" href="#top">返回顶部 ↑</a>'
(DOCS/'index.html').write_text(page('AI 能让公共采购更廉洁吗？',content,'paper'),encoding='utf-8')

refs='\n\n'.join('**['+i+']** '+BY_ID[i]['citation']+'\n\n选用类型：'+BY_ID[i]['selection_label']+'。'+BY_ID[i]['authority_label']+'。' for i in sorted(used))
definitions='\n'.join('['+i+']: '+BY_ID[i]['source_url'] for i in sorted(used))
paper='# AI 能让公共采购更廉洁吗？\n\n以阿尔巴尼亚 Diella 为切入的风险识别与问责机制设计\n\n**六部分研究设计稿 v0.1 · '+DATE+'。尚未开展合同级效果估计。**\n\n'+'\n\n'.join(source_chunks)+'\n\n## 引用书目\n\n'+refs+'\n\n'+definitions+'\n'
(ROOT/'paper.md').write_text(paper,encoding='utf-8')
(DOCS/'downloads/paper.md').write_text(paper,encoding='utf-8')

def card(r):
    i=r['id'];v=r['citation_variants'];first=v[0]
    search=json.dumps(r,ensure_ascii=False).lower()
    state=' hidden' if r['selection']=='supplement' else ''
    options='<select class="cite-version" aria-label="'+i+' 引用版本">'+''.join('<option value="'+str(n)+'">'+esc(x['label'])+'</option>' for n,x in enumerate(v))+'</select>' if len(v)>1 else '<span class="citation-label">'+esc(first['label'])+'</span>'
    authorities=' · '.join('<a href="'+esc(u)+'" target="_blank" rel="noopener">核验依据 '+str(n+1)+' ↗</a>' for n,u in enumerate(r['authority_sources']))
    points=''.join('<li>'+esc(p)+'</li>' for p in r['key_points'])
    payload=json.dumps(v,ensure_ascii=False).replace('</','<\\/')
    return f'''<article class="literature-card" id="{i}" data-selection="{esc(r['selection'])}" data-category="{esc(r['category'])}" data-search="{esc(search)}"{state}>
<div class="lit-grid"><div><span class="lit-id">{i} / {esc(r['category'])}</span><div class="lit-badges"><span class="badge {esc(r['selection'])}">{esc(r['selection_label'])}</span></div><h2 class="lit-title">{esc(r['title'])}</h2><div class="lit-meta">{esc(' / '.join(r['authors']))}<br>{esc(r['year'])}<br>{esc(r['type'])}</div><div class="lit-links"><a href="{esc(r['source_url'])}" target="_blank" rel="noopener">原始来源 ↗</a>{('<a href="https://doi.org/'+esc(r['doi'])+'" target="_blank" rel="noopener">DOI ↗</a>') if r.get('doi') else ''}</div></div>
<div class="lit-points"><h3>主要观点 · {esc(r['view_kind'])}</h3><ul>{points}</ul><p class="basis">归纳依据：{esc(r['key_points_basis'])}</p><p class="lit-boundary"><strong>适用边界</strong>　{esc(r['does_not_support'])}</p></div></div>
<details class="citation"><summary>引用格式 · GB/T 7714-2015</summary><div class="cite-actions">{options}<button type="button" class="copy-cite" aria-label="复制 {i} 引文">复制引文</button></div><textarea class="cite-box" readonly spellcheck="false" aria-label="{i} 引用格式">{esc(first['text'])}</textarea><span class="copy-status" aria-live="polite"></span><p class="citation-note">{esc(first.get('note',''))}</p><script class="citation-data" type="application/json">{payload}</script></details>
<details><summary>来源选用与阅读记录</summary><div class="authority-content"><p><strong>{esc(r['authority_label'])}</strong><br>{esc(r['authority_reason'])}</p><p>阅读范围：{esc(r['reading_level'])}</p><p>研究限制：{esc(r.get('limitations',''))}</p><p>{authorities}</p></div></details></article>'''

cats=list(dict.fromkeys(r['category'] for r in ROWS))
options=''.join('<option value="'+esc(c)+'">'+esc(c)+'</option>' for c in cats)
content='''<section class="hero library-hero" id="top"><p class="eyebrow">REFERENCE LIBRARY / READ · COMPARE · CITE</p><h1>文献索引</h1><p class="lead">从作者观点到证据边界，再到可复制的引用。按研究用途浏览，回到原始来源核对。</p><div class="library-summary"><span><strong>23</strong>正式书目</span><span><strong>4</strong>辅助材料</span><span>核验更新 / 2026-10-29</span></div><div class="hero-actions"><a href="downloads/references.ris" download>正式书目 RIS ↓</a><a href="downloads/references.bib" download>BibTeX ↓</a><a href="downloads/bibliography.csv" download>完整索引 CSV ↓</a><a href="downloads/supplement.ris" download>辅助材料 RIS ↓</a></div></section>'''
content+='<main id="main" class="library-main"><div class="filters" role="search"><input id="q" type="search" aria-label="检索文献" placeholder="检索作者、题名、主要观点或方法"><select id="scope" aria-label="选用范围"><option value="core">正式书目</option><option value="all">正式书目 + 辅助材料</option><option value="supplement">仅辅助材料</option></select><select id="cat" aria-label="研究类别"><option value="">全部类别</option>'+options+'</select></div><p id="count" class="filter-count" role="status">显示 23 条 / 正式书目 23 条 · 辅助材料 4 条</p><section id="literature-list" class="library-list" aria-label="文献列表">'+''.join(card(r) for r in ROWS)+'</section><p id="empty-state" class="empty-state" hidden>没有匹配条目，请调整关键词或筛选范围。</p><noscript><p>未启用 JavaScript：可阅读默认的正式书目、展开引用及访问原始来源；筛选和复制按钮需要启用 JavaScript。</p></noscript><p class="library-end">正式书目包含学术文献、专业报告及制度原件，不能统称同行评审论文。工作稿和正式版请按实际阅读版本选择。本页提供原始来源链接，不托管第三方全文。</p></main><a class="to-top" href="#top">返回顶部 ↑</a>'
(DOCS/'literature.html').write_text(page('文献索引',content,'lit','library-page'),encoding='utf-8')

raw=(ROOT/'research/methods.md').read_text(encoding='utf-8');raw=re.sub(r'^# [^\n]+\n','',raw,count=1)
content='<section class="hero" id="top"><p class="eyebrow">METHODS / EVIDENCE BEFORE ESTIMATION</p><h1>公开资料，也能形成经验研究</h1><p class="subtitle">定性取证与具体定量方法的选择条件</p><p class="lead">访谈是一种材料来源，回归是一种估计工具。研究设计首先要回答：观察什么、如何比较，以及什么证据可能推翻解释。</p></section><main id="main" class="article method-article">'+render_md(raw)+'</main><a class="to-top" href="#top">返回顶部 ↑</a>'
(DOCS/'methods.html').write_text(page('方法说明',content,'method'),encoding='utf-8')
(DOCS/'.nojekyll').write_text('',encoding='utf-8')
for name in ['claims.csv','procurement-template.csv','codebook.md']:shutil.copy2(ROOT/'data'/name,DOCS/'downloads'/name)
cols=['id','selection_label','category','title','authors','year','authority_label','key_points','key_points_basis','reading_level','citation','source_url']
with (DOCS/'downloads/bibliography.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader()
    for r in ROWS:
        r=dict(r);r['authors']='; '.join(r['authors']);r['key_points']='；'.join(r['key_points']);w.writerow(r)
print(json.dumps({'sections':len(SECTIONS),'bibliography':len(ROWS),'used_references':len(used),'core':sum(r['selection']=='core' for r in ROWS),'supplement':sum(r['selection']=='supplement' for r in ROWS),'procurement_observations':0},ensure_ascii=False))
