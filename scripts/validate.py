"""核验公开交付的引用、链接、资料边界与可重复生成。"""
import csv,html,json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlparse

ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data/bibliography.json').read_text(encoding='utf-8'))
assert len(rows)==27 and sum(r['selection']=='core' for r in rows)==23
assert sum(r['selection']=='supplement' for r in rows)==4
assert all(r['key_points'] and r['citation_variants'] and r['authority_reason'] for r in rows)
assert not any(r['id']=='D10' for r in rows)
assert all('et al..' not in v['text'] for r in rows for v in r['citation_variants'])
with (ROOT/'data/procurement-template.csv').open(encoding='utf-8-sig') as f:assert len(list(csv.DictReader(f)))==0
ids={r['id'] for r in rows}
chapters=list((ROOT/'manuscript').glob('*.md'))
assert len(chapters)==6
for chapter in chapters:
    text=chapter.read_text(encoding='utf-8')
    cited=set(re.findall(r'\[([ADMP]\d{2})\]',text))
    assert cited and cited<=ids,'章节引用缺失或未选用来源：'+chapter.name
    assert all('literature.html#'+i in text for i in cited),'章节引用不可定位：'+chapter.name
with (ROOT/'data/claims.csv').open(encoding='utf-8-sig') as f:
    claims=list(csv.DictReader(f))
    for c in claims:assert all(i in ids for i in c['source_ids'].split(';') if i)
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.sections=0
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.add(a['id'])
        if t=='a' and a.get('href'):self.links.append(a['href'])
        if t=='section' and 'paper-section' in a.get('class',''):self.sections+=1
pages={}
for path in (ROOT/'docs').glob('*.html'):
    s=path.read_text(encoding='utf-8');p=Links();p.feed(s);pages[path.resolve()]=p
    assert s.startswith('<!DOCTYPE html>') and s.rstrip().endswith('</html>')
    assert not re.search(r'__[A-Z_]+__',s),'未替换模板变量'
    assert not re.search(r'file://|[A-Z]:[/\\]Users|codex-clipboard',s),'公开文件含个人路径'
    assert 'Technocratic Spectacle or Democratic Innovation?' not in s
    if path.name=='index.html':
        assert s.count('class="chapter-link"')==6
        assert '本轮仅打磨以下六部分' in s
        assert 'downloads/paper.md' not in s
for path,p in pages.items():
    for href in p.links:
        u=urlparse(href)
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        assert target.exists(),f'失效链接 {path.name}: {href}'
        if u.fragment and target.suffix=='.html':assert unquote(u.fragment) in pages[target].ids,f'失效锚点 {href}'
for name,count in [('references.ris',23),('supplement.ris',4)]:
    s=(ROOT/'docs/downloads'/name).read_text(encoding='utf-8')
    assert len(re.findall(r'^TY  - ',s,re.M))==count
    assert 'L1  - ' not in s
for path in ROOT.rglob('*'):
    if path.is_file() and '.git' not in path.parts:
        assert path.suffix.lower() not in ['.pdf','.docx','.pptx'],'不应发布的第三方原文件'
        if path.suffix in ['.md','.json','.csv','.ris','.bib']:
            assert not re.search(r'file://|[A-Z]:[/\\]Users|codex-clipboard',path.read_text(encoding='utf-8-sig')),'个人路径：'+str(path)
assert not (ROOT/'paper.md').exists() and not (ROOT/'docs/downloads/paper.md').exists()
result={'date':'2026-10-29','chapter_drafts':6,'scope':'分章节推进，不生成完整报告','core_references':23,'supplement':4,'claims_registered':len(claims),'procurement_observations':0,'local_links':'passed','reference_anchors':'passed','no_personal_paths':'passed','no_third_party_fulltexts':'passed','directory_only_record_absent':'passed','browser_visual_check':'see browser-qa.json'}
(ROOT/'audit/validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
