#!/usr/bin/env python3
"""Rebuild the eleven README files from the public case and translation data."""
import argparse,html,json,pathlib,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
LANGS=[('en','English','README.md'),('es','Español','README_es.md'),('pt','Português','README_pt.md'),('ja','日本語','README_ja.md'),('ko','한국어','README_ko.md'),('de','Deutsch','README_de.md'),('fr','Français','README_fr.md'),('tr','Türkçe','README_tr.md'),('zh-TW','繁體中文','README_zh-TW.md'),('zh-CN','简体中文','README_zh-CN.md'),('ru','Русский','README_ru.md')]
CATEGORIES=[('computer','🖱️'),('editing','✂️'),('visual','🎮'),('comparison','🔬'),('benchmarks','📈'),('workflows','🔄'),('integrations','🔌'),('limits','⚠️')]
BADGES='\n'.join(f'[![{n}](https://img.shields.io/badge/{urllib.parse.quote(n)}-2563eb)]({f})' for _,n,f in LANGS)
def utm(path,medium,content):return 'https://evolink.ai'+path+'?utm_source=github&utm_medium='+medium+'&utm_campaign=gpt-6-1-terra-usecases&utm_content='+content
def render(data,locale):
 g=locale['copy'];cases=data['cases'];tr=locale['cases']
 assert len(cases)==len(tr)==data['case_count']
 cover=f'<a href="{utm("","banner","readme_banner")}"><img src="{data["banner_url"]}" alt="GPT-6.1 Terra — {html.escape(g["collection"])}" width="760"></a>\n\n' if data.get('banner_url') else ''
 cover+=f'[{g["model_page_browser"]}]({utm("/gpt-6-1-terra","badge","model_try")})\n\n'
 chunks=['<div align="center">\n\n<h1>GPT-6.1 Terra · '+g['collection']+'</h1>\n\n'+cover+'[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](LICENSE)\n\n'+BADGES+'\n\n</div>\n',f'## 🍌 {g["introduction"]}\n\n{g["intro"]}\n\n**{g["purpose"]}**\n',f'<a id="overview"></a>\n## 📊 {g["overview"]}\n\n{g["stats"]}\n\n> [!NOTE]\n> {g["evidence"]}\n',f'<a id="quick-start"></a>\n## ⚡ {g["quick_start"]}\n\n{g["steps"]}\n\n[{g["model_page"]}]({utm("/gpt-6-1-terra","quickstart","model-detail")})\n',f'<a id="menu"></a>\n## 📑 {g["menu"]}\n\n| {g["case"]} | {g["category"]} | {g["type"]} |\n|---|---|---|']
 for c,t in zip(cases,tr):chunks.append(f'| [{c["number"]}. {t[0]}](#case-{c["number"]}) | {g["categories"][c["category"]]} | {c["type"]} |')
 chunks.append('\n'+f'[{g["overview"]}](#overview) · [{g["quick_start"]}](#quick-start) · [{g["related"]}](#related-repositories) · [{g["acknowledge"]}](#acknowledge)\n')
 for category,emoji in CATEGORIES:
  group=[(c,t) for c,t in zip(cases,tr) if c['category']==category]
  if not group:continue
  chunks.append(f'<a id="{category}"></a>\n## {emoji} {g["categories"][category]}\n')
  for c,t in group:
   chunks.append(f'<a id="case-{c["number"]}"></a>\n### {g["case"]} {c["number"]}: [{t[0]}]({c["source_url"]}) ({g["by"]} [@{c["author_handle"]}]({c["author_url"]}))\n\n**{t[1]}**\n\n{t[2]}\n')
   if c.get('prompt'):chunks.append('**'+g['prompt']+':**\n\n```\n'+c['prompt']+'\n```\n')
   if c.get('supporting_url'):chunks.append(f'[{g["supporting"]}]({c["supporting_url"]})\n')
   cells=[]
   for i,m in enumerate(c['media'],1):
    video=m['type']=='video';dest=m['playable_url'] if video else m['image_url'];poster=m['poster_url'] if video else m['image_url'];label=g['video'] if video else g['image'];alt=html.escape(t[0]+f' — {i}',quote=True)
    extra=('<br>'+html.escape(m['model']+' / '+m['effort'])) if m.get('model') else ''
    cells.append(f'<td align="center"><a href="{html.escape(dest,quote=True)}"><img src="{html.escape(poster,quote=True)}" alt="{alt}" width="480"></a><br>{label}{extra}</td>')
   if c['source_id']=='supplemental:simon-pelican':
    models=['gpt-6-astra','gpt-6.1-sol','gpt-6.1-terra','gpt-6-luna'];lookup={(m['model'],m['effort']):cell.replace('width="480"','width="180"') for m,cell in zip(c['media'],cells)}
    table='<table><thead><tr><th></th>'+''.join('<th>'+html.escape(model)+'</th>' for model in models)+'</tr></thead><tbody>'
    for effort in ['max','xhigh','high','medium','low','none']:table+='<tr><th>'+effort+'</th>'+''.join(lookup.get((model,effort),'<td>—</td>') for model in models)+'</tr>'
    chunks.append(table+'</tbody></table>\n')
   else:
    for start in range(0,len(cells),2):chunks.append('<table><tr>'+''.join(cells[start:start+2])+'</tr></table>\n')
   chunks.append(f'{g["type"]}: {c["type"]} | {g["date"]}: {c["date"]}\n\n---\n')
 chunks.append(f'<a id="related-repositories"></a>\n## {g["related"]}\n\n- [Kimi K3.1 — {g["collection"]}](https://github.com/cheercheung/awesome-kimi-k3.1-guide-and-use-cases)\n- [Gemini 4 Carbon — {g["collection"]}](https://github.com/cheercheung/awesome-gemini-4-carbon-guide-and-use-cases)\n')
 authors=list(dict.fromkeys((c['author_handle'],c['author_url']) for c in cases))
 chunks.append(f'<a id="acknowledge"></a>\n## 🙏 {g["acknowledge"]}\n\n{g["thanks"]}\n\n'+', '.join(f'[@{h}]({u})' for h,u in authors)+f'\n\n{g["corrections"]}\n')
 return '\n'.join(chunks).rstrip()+'\n'
def main():
 p=argparse.ArgumentParser();p.add_argument('--english-only',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();d=json.loads((ROOT/'data/gpt-6-1-terra-usecase-curated.json').read_text());errors=[]
 for code,_,filename in LANGS:
  if a.english_only and code!='en':continue
  out=render(d,json.loads((ROOT/f'data/locales/{code}.json').read_text()));path=ROOT/filename
  if a.check:
   if not path.exists() or path.read_text()!=out:errors.append(filename)
  else:path.write_text(out)
 if errors:raise SystemExit('README drift: '+', '.join(errors))
 print('PASS: README generation check' if a.check else 'README files generated')
if __name__=='__main__':main()
