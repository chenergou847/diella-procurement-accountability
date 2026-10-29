(()=>{
 const fontButton=document.getElementById('font-toggle');
 fontButton?.addEventListener('click',()=>{const large=document.body.classList.toggle('large-reading');fontButton.setAttribute('aria-pressed',String(large));fontButton.textContent=large?'标准字号':'大字阅读';});
 document.getElementById('print-page')?.addEventListener('click',()=>window.print());
 const sections=document.querySelectorAll('.paper-section');
 if(sections.length&&'IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){document.querySelectorAll('.toc-links a').forEach(a=>{const on=a.getAttribute('href')==='#'+e.target.id;a.classList.toggle('active',on);if(on)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}},{rootMargin:'-8% 0px -72% 0px'});sections.forEach(s=>observer.observe(s));}
 const q=document.getElementById('q'),scope=document.getElementById('scope'),cat=document.getElementById('cat'),list=document.getElementById('literature-list');
 if(!list)return;
 const cards=[...list.querySelectorAll('.literature-card')];
 function resize(box){box.style.height='auto';box.style.height=Math.min(Math.max(box.scrollHeight+4,100),260)+'px';}
 function draw(){const terms=q.value.toLowerCase().trim().split(/\s+/).filter(Boolean);let count=0;for(const card of cards){const show=(scope.value==='all'||card.dataset.selection===scope.value)&&(!cat.value||card.dataset.category===cat.value)&&terms.every(t=>card.dataset.search.includes(t));card.hidden=!show;if(show){count++;card.querySelectorAll('.cite-box').forEach(resize);}}document.getElementById('count').textContent='显示 '+count+' 条 / 正式书目 23 条 · 辅助材料 4 条';document.getElementById('empty-state').hidden=count>0;}
 q.addEventListener('input',draw);scope.addEventListener('change',draw);cat.addEventListener('change',draw);
 async function copy(value){try{if(navigator.clipboard){await navigator.clipboard.writeText(value);return true;}}catch(error){}const temp=document.createElement('textarea');temp.value=value;temp.style.position='fixed';temp.style.left='-10000px';temp.setAttribute('readonly','');document.body.append(temp);temp.select();let ok=false;try{ok=document.execCommand('copy');}catch(error){}temp.remove();return ok;}
 list.addEventListener('click',async event=>{const button=event.target.closest('.copy-cite');if(!button)return;const card=button.closest('.literature-card'),box=card.querySelector('.cite-box'),status=card.querySelector('.copy-status'),ok=await copy(box.value);status.textContent=ok?'已复制引文':'请选中引文并按 Ctrl+C 复制';if(!ok){box.focus();box.select();}});
 list.addEventListener('change',event=>{if(!event.target.matches('.cite-version'))return;const card=event.target.closest('.literature-card'),data=JSON.parse(card.querySelector('.citation-data').textContent),v=data[Number(event.target.value)],box=card.querySelector('.cite-box');box.value=v.text;card.querySelector('.citation-note').textContent=v.note||'';card.querySelector('.copy-status').textContent='';resize(box);});
 list.addEventListener('toggle',event=>{if(event.target.tagName==='DETAILS'&&event.target.open)event.target.querySelectorAll('.cite-box').forEach(resize);},true);
 function revealHash(){const id=decodeURIComponent(location.hash.slice(1)),target=cards.find(c=>c.id===id);if(!target)return;if(target.dataset.selection==='supplement')scope.value='all';q.value='';cat.value='';draw();target.scrollIntoView({block:'start'});}
 draw();if(location.hash)revealHash();window.addEventListener('hashchange',revealHash);
})();
