#!/usr/bin/env python3
"""v1 → v2: featured+grid works, explicit actions, calmer motion, mobile fixes, variable-font headline."""
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
p='index.html'; s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)>=1, a[:60]
    s=s.replace(a,b,cnt)

rep('family=Inter+Tight:wght@500;700;800;900&','family=Inter+Tight:wght@500;700;800;900&family=Roboto+Flex:opsz,wdth,wght,GRAD@8..144,25..151,100..1000,-200..150&')
rep('<div class="loader" id="loader" aria-hidden="true"><span class="l">Hiroshift≈ — Tokyo</span><span class="n" id="ln">00</span></div>\n','')
rep('<h1 aria-label="Hiroshift≈"><span class="w" data-split>Hiroshift≈</span></h1>','<h1 aria-label="Hiroshift≈" id="vf"><span class="w" data-split>Hiroshift≈</span></h1>')
rep('''      <div class="en">Music, film, <em>and</em> code.<br><span class="roles" id="roles"><span class="on">AI prototyping</span><span>Web apps</span><span>Video</span><span>Songwriting</span></span></div>
      <p class="ja">ステージに立つ仕事から始まり、製造の現場を20年、映像の会社を一つ。いまは AI と一緒に、動くものを一人で作っています。ここは、個人で作ってきたものの置き場です。</p>''',
'''      <div class="en">誰かの「面倒」を、<br>動くものに変える。<span class="sub-en">Music, film, <em>and</em> code.</span></div>
      <div><p class="ja">ステージに立つ仕事から始まり、製造の現場を20年、映像の会社を一つ。いまは AI と一緒に、動くものを一人で作っています。ここは、個人で作ってきたものの置き場です。</p><a class="go" href="#works">作品を見る<i></i></a></div>''')

ws=s.index('<section id="works"'); we=s.index('<section id="about"')
works='''<section id="works" class="sec works">
  <div class="wrap">
    <div class="head rv"><span class="no">01</span><h2>Selected<br>works<small>個人で作ってきたもの。触れるものは、そのまま開きます。</small></h2></div>
    <article class="feat rv" data-url="https://udify.app/workflow/wY2Xn88ZCgYMkR0M" data-desc="電話対応のときに、相手の情報と状況を入力するだけで、一次返信の文面・現場への調査依頼・記録台帳を自動で作るエージェント。記録にかかる時間を計測し、削減を定量で検証した。業務効率化アプリコンテストで優秀作品賞。">
      <div class="img"><img src="assets/img/claim.webp" width="600" height="334" alt="クレーム一次対応AIエージェントの入力画面" loading="lazy"><span class="st">Award</span></div>
      <div class="txt">
        <span class="k">Featured — 01</span>
        <h3>クレーム一次対応・台帳自動化 AI エージェント</h3>
        <dl class="psr">
          <div><dt>問題</dt><dd>電話を受けた人が、返信文・現場への依頼・台帳の記入を、別々に手で書いていた。</dd></div>
          <div><dt>解決</dt><dd>相手の情報と状況を三つ入れると、三つの文書が同時にできあがる。最後に人が確かめて送る。</dd></div>
          <div><dt>結果</dt><dd>記入にかかる時間を計測して削減を確かめ、業務効率化アプリコンテストで優秀作品賞。</dd></div>
        </dl>
        <div class="acts"><a class="act fill" href="https://udify.app/workflow/wY2Xn88ZCgYMkR0M" target="_blank" rel="noopener">アプリを開く</a><button type="button" class="act" data-detail>詳細を見る</button><span class="tags">Dify · Gemini 2.5 · GAS · Sheets</span></div>
      </div>
    </article>
    <div class="grid rv">
'''
CARDS=[
 ('https://www.youtube.com/@makemehappy818','3年続けている YouTube Shorts のチャンネル。生成AIの進化（要約→画像→動画）をそのまま体験し、Canva で仕上げる。自分の「好き」を形にするための実験場。','makemehappy.webp','600','400','Make me happy チャンネルのサムネイル','Live','02','Make me happy','生成AIの進化を、3年ぶんの短い動画で追いかけているチャンネル。','Shorts · Canva · Veo','チャンネルを開く'),
 ('https://setsuyaku-income-v2.onrender.com','「節約した金額」を「収入」として記録し、それが何分の労働に相当するかを見せる PWA。電卓式のワンタップ入力、連続記録、週次サマリー、年間予測。RSpec 89 テスト。','setsuyaku.webp','600','400','節約は収入 v2 の画面','Beta','03','節約は収入 v2','節約を、収入として数える。何分ぶん働いたことになるかまで出す。','Rails · PWA · RSpec','アプリを開く'),
 ('https://github.com/Hiroshift/furima-41448','AWS に載せたフリマ EC。Pay.jp の決済まで実装し、出品と購入が一通り回る。検証を終えたのでサーバーは休止中、コードは GitHub に。','furima.webp','600','400','FURIMA のトップ画面','Paused','04','FURIMA','決済まで通したフリマ。いまはコードだけが残っている。','Rails · MySQL · AWS · Pay.jp','コードを見る'),
 ('https://hiroshift.github.io/woop/','WOOP（Wish・Outcome・Obstacle・Plan）の順に書き出すと、目標が計画に変わる。研究で裏付けのある方法を、そのまま画面にした。','woop.webp','600','370','WOOP アプリの画面','Live','05','WOOP','願いを、結果、障害、計画の順にほどく。四つの欄だけのアプリ。','HTML · CSS · JS','アプリを開く'),
 ('https://hiroshift.github.io/principle-generator-/','名前を入れると、その人のための行動指針が一枚できる。読み上げつき。ナポレオン・ヒルの考え方をもとにしている。','principle.webp','600','400','行動指針ジェネレーターの画面','Live','06','行動指針ジェネレーター','名前を入れると、声で読み上げる一枚が返ってくる。','JS · Web Speech','アプリを開く'),
 ('https://hiroshift.github.io/ukehi/','2025年の夏至に合わせて作った、誓いを立てるための一枚。宇宙の節目に、自分の言葉を置く。','ukehi.webp','635','400','UKEHI の画面','Live','07','UKEHI','夏至の日の、誓い。一年に一度だけ開く画面。','HTML · CSS · JS','アプリを開く'),
]
for url,desc,img,w,h,alt,st,idx,title,short,tags,act in CARDS:
    works+=f'''      <article class="card" data-url="{url}" data-desc="{desc}">
        <div class="img"><img src="assets/img/{img}" width="{w}" height="{h}" alt="{alt}" loading="lazy"><span class="st">{st}</span></div>
        <div class="in"><span class="idx">{idx}</span><h3>{title}</h3><p>{short}</p><span class="tags">{tags}</span>
        <div class="acts"><a class="act" href="{url}" target="_blank" rel="noopener">{act}</a><button type="button" class="act ghost" data-detail>詳細</button></div></div>
      </article>
'''
works+='''    </div>
  </div>
</section>

'''
s=s[:ws]+works+s[we:]

cs=s.index('/* works: horizontal on scroll */'); ce=s.index('/* about (paper) */')
works_css='''/* works: featured + grid */
.feat{display:grid;grid-template-columns:1.15fr .85fr;gap:clamp(24px,4vw,64px);align-items:center;padding-bottom:clamp(40px,6vw,96px);margin-bottom:clamp(40px,6vw,96px);border-bottom:1px solid var(--line)}
@media (max-width:900px){.feat{grid-template-columns:1fr}}
.img{position:relative;overflow:hidden;background:var(--ink-2);border-radius:6px}
.feat .img{aspect-ratio:16/10}
.img img{width:100%;height:100%;object-fit:cover;object-position:left top;transform:scale(1.02);transition:transform 1.4s var(--ease)}
.feat:hover .img img,.card:hover .img img{transform:scale(1.06)}
.st{position:absolute;left:14px;top:14px;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;padding:7px 11px;background:var(--ink);color:var(--paper);border-radius:999px}
.feat .txt{display:grid;gap:18px}
.feat .k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--fog)}
.feat h3{font-family:var(--disp);font-size:clamp(28px,3.6vw,56px);letter-spacing:-.035em;line-height:1.02}
.psr{display:grid;gap:0;margin-top:6px}
.psr div{display:grid;grid-template-columns:52px 1fr;gap:14px;padding:12px 0;border-top:1px solid var(--line)}
.psr dt{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--fog);padding-top:4px}
.psr dd{font-size:14px;line-height:1.8;color:var(--fog-2)}
.acts{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:6px}
.act{display:inline-flex;align-items:center;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;padding:12px 18px;border:1px solid rgba(243,241,234,.28);border-radius:999px;transition:background .4s,color .4s,border-color .4s}
.act:hover{background:var(--paper);color:var(--ink);border-color:var(--paper)}
.act.fill{background:var(--paper);color:var(--ink);border-color:var(--paper)}
.act.fill:hover{background:var(--sig);border-color:var(--sig);color:#fff}
.act.ghost{border-color:transparent;color:var(--fog);padding-inline:10px}
.tags{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--fog)}
.feat .acts .tags{margin-left:auto}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2.5vw,36px) clamp(18px,2vw,28px)}
@media (max-width:1000px){.grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:600px){.grid{grid-template-columns:1fr;gap:40px}}
.card{display:grid;gap:14px;align-content:start}
.card .img{aspect-ratio:4/3}
.card .in{display:grid;gap:8px}
.card .idx{font-family:var(--serif);font-style:italic;font-size:18px;color:var(--fog)}
.card h3{font-family:var(--disp);font-size:clamp(20px,1.8vw,26px);letter-spacing:-.03em;line-height:1.1}
.card p{color:var(--fog-2);font-size:13.5px;line-height:1.8}
.card .acts{margin-top:4px}
'''
s=s[:cs]+works_css+s[ce:]

rep(".hero .sub .en{font-family:var(--disp);font-size:clamp(22px,2.6vw,38px);font-weight:700;letter-spacing:-.03em;line-height:1.1;color:var(--paper)}",
    ".hero .sub .en{font-family:var(--jp);font-size:clamp(22px,2.6vw,40px);font-weight:700;letter-spacing:-.02em;line-height:1.25;color:var(--paper)}\n.hero .sub-en{display:block;font-family:var(--disp);font-size:.62em;font-weight:700;letter-spacing:-.03em;color:var(--fog-2);margin-top:12px}\n.go{display:inline-flex;align-items:center;gap:12px;margin-top:18px;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:14px 22px;border:1px solid rgba(243,241,234,.3);border-radius:999px;transition:background .4s,color .4s}\n.go i{width:6px;height:6px;border-radius:50%;background:var(--sig)}\n.go:hover{background:var(--paper);color:var(--ink)}")
rep("@media (max-width:820px){.hero .sub{grid-template-columns:1fr}}","@media (max-width:820px){.hero .sub{grid-template-columns:1fr;gap:20px}.hero{min-height:auto}.hero .body{padding-top:clamp(120px,22vh,180px);padding-bottom:40px}}")
s=re.sub(r"\.roles\{.*?\n\.roles span\.off\{[^\n]*\}\n","",s,flags=re.S)
s=re.sub(r"/\* loader \*/\n\.loader\{.*?html\.no-js \.loader,html\.reduce \.loader\{display:none\}\n","",s,flags=re.S)
rep(".hero h1{font-family:var(--disp);font-size:clamp(56px,11.5vw,200px);line-height:.88;letter-spacing:-.045em;font-weight:900;display:flex;flex-wrap:wrap;column-gap:.12em}",
    ".hero h1{font-family:'Roboto Flex','Inter Tight','Noto Sans JP',sans-serif;font-size:clamp(56px,11.5vw,200px);line-height:.88;letter-spacing:-.04em;font-weight:900;display:flex;flex-wrap:wrap;column-gap:.06em;font-variation-settings:'wght' 800,'wdth' 100,'GRAD' 0,'opsz' 144}\n.hero h1 .c{font-variation-settings:'wght' var(--w,800),'wdth' var(--d,100),'GRAD' var(--g,0),'opsz' 144;will-change:font-variation-settings}")
rep("@media (max-width:720px){.top nav{display:none}}","@media (max-width:720px){.top nav a:not([href='#works']):not([href='#contact']){display:none}.top nav{gap:16px}}")
rep(".stmt .w{opacity:.14;transition:opacity .6s var(--ease)}\n.stmt .w.on{opacity:1}\n","")
rep('<p class="stmt" data-words>','<p class="stmt">')
rep(".svc .row .ar{font-family:var(--mono);font-size:11px;color:var(--fog);letter-spacing:.14em;text-transform:uppercase;padding-top:8px}",
    ".svc .row .ar{font-family:var(--mono);font-size:11px;color:var(--fog);letter-spacing:.14em;text-transform:uppercase;padding-top:8px}\n@media (max-width:640px){.svc .row{grid-template-columns:1fr;gap:6px}.svc .row .no{font-size:16px}.svc .row .ar{display:none}}")
rep(".rv{opacity:0;transform:translateY(28px);transition:opacity 1.2s var(--ease),transform 1.2s var(--ease)}",".rv{opacity:0;transform:translateY(12px);transition:opacity .9s var(--ease),transform .9s var(--ease)}")
rep(".cur.big{width:72px;height:72px}",".cur.big{width:28px;height:28px}")

# ---- JS
js0=s.index('<script>\n(()=>{')
head,js=s[:js0],s[js0:]
js=re.sub(r"/\* loader \*/\n.*?\n\n","\n",js,flags=re.S,count=1)
js=js.replace("$$('[data-split]').forEach(el=>{const t=el.textContent;el.textContent='';[...t].forEach((ch,i)=>{const s=document.createElement('span');s.className='c';s.textContent=ch;s.style.transitionDelay=(0.08*i+0.1)+'s';el.appendChild(s);});});",
 "$$('[data-split]').forEach(el=>{const t=el.textContent;el.textContent='';[...t].forEach((ch,i)=>{const s=document.createElement('span');s.className='c';s.textContent=ch;s.style.transitionDelay=(0.06*i+0.05)+'s';el.appendChild(s);});});\nrequestAnimationFrame(()=>requestAnimationFrame(()=>H.classList.add('ready')));")
js=re.sub(r"/\* roles \*/\n.*?\n\n","\n",js,flags=re.S,count=1)
js=re.sub(r"/\* statement: word-by-word \*/\n.*?function words\(\)\{[^\n]*\}\n","",js,flags=re.S,count=1)
js=re.sub(r"/\* works horizontal \*/\n.*?setTimeout\(\(\)=>\{layoutWorks\(\);scrollWorks\(\);\},600\);\n","",js,flags=re.S,count=1)
mi=js.index("/* modal */"); me=js.index("/* WebGL2 background")
new_modal='''/* modal（「詳細」ボタンからだけ開く） */
const modal=$('#modal');
$$('[data-detail]').forEach(b=>b.addEventListener('click',()=>{const c=b.closest('article');$('#mImg').src=c.querySelector('img').src;$('#mImg').alt=c.querySelector('img').alt;$('#mTitle').textContent=c.querySelector('h3').textContent;$('#mTag').textContent=c.querySelector('.tags').textContent+' — '+c.querySelector('.st').textContent;$('#mDesc').textContent=c.dataset.desc;const o=$('#mOpen');o.href=c.dataset.url;o.textContent=/github\\.com/.test(c.dataset.url)?'コードを見る':'開く';modal.showModal();}));
$('#mClose').addEventListener('click',()=>modal.close());modal.addEventListener('click',e=>{if(e.target===modal)modal.close();});

/* 見出し＝可変フォント。ポインタに近い文字ほど太く・広く（レンズのように）。何もしなくても静かに呼吸する */
(()=>{const h=$('#vf');if(!h||reduce)return;const cs=$$('.c',h);let px=-1e4,py=-1e4;
 addEventListener('pointermove',e=>{px=e.clientX;py=e.clientY;},{passive:true});
 document.addEventListener('mouseleave',()=>{px=-1e4;py=-1e4;});
 const cur=cs.map(()=>({w:800,d:100,g:0}));let vis=true;new IntersectionObserver(es=>{vis=es[0].isIntersecting;}).observe(h);
 function tick(){if(vis){const t=performance.now()/1000;cs.forEach((c,i)=>{const r=c.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;const dist=Math.hypot(px-cx,py-cy);const R=Math.max(220,innerWidth*.22);const k=Math.max(0,1-dist/R);const breathe=Math.sin(t*1.1+i*.55)*.5+.5;
  const tw=760+breathe*60+k*240,td=100-breathe*4+k*38,tg=k*120;const o=cur[i];o.w+=(tw-o.w)*.12;o.d+=(td-o.d)*.12;o.g+=(tg-o.g)*.12;
  c.style.setProperty('--w',o.w.toFixed(1));c.style.setProperty('--d',o.d.toFixed(1));c.style.setProperty('--g',o.g.toFixed(0));});}
  requestAnimationFrame(tick);}
 requestAnimationFrame(tick);})();

'''
js=js[:mi]+new_modal+js[me:]
js=js.replace("$$('a,button,.card').forEach(el=>","$$('a,button').forEach(el=>")
js=js.replace("scrollWorks();words();","")
s=head+js
open(p,'w',encoding='utf-8').write(s); print('v2 written', len(s))
