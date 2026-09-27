import {spawn} from 'node:child_process';import fs from 'node:fs';
import os from 'node:os';const SP=os.tmpdir();
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';const PORT=9800+Math.floor(Math.random()*100);
const url='file://'+process.cwd()+'/index.html';
const chrome=spawn(CHROME,['--headless=new','--use-angle=swiftshader','--enable-unsafe-swiftshader','--hide-scrollbars','--remote-debugging-port='+PORT,'--user-data-dir='+SP+'/cdp/s'+PORT,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));let wsUrl;
for(let i=0;i<120;i++){try{await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json();wsUrl=(await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`,{method:'PUT'})).json()).webSocketDebuggerUrl;break;}catch{}await sleep(500);}
const ws=new WebSocket(wsUrl);await new Promise(r=>ws.onopen=r);let id=0;const pend={};const events=[];
ws.onmessage=m=>{const d=JSON.parse(m.data);if(d.id&&pend[d.id]){pend[d.id](d);delete pend[d.id];}else events.push(d);};
const send=(method,params={})=>new Promise(r=>{const i=++id;pend[i]=r;ws.send(JSON.stringify({id:i,method,params}));});
const ev=e=>send('Runtime.evaluate',{expression:e,returnByValue:true,awaitPromise:true}).then(d=>d.result&&d.result.result?d.result.result.value:JSON.stringify(d));
await send('Runtime.enable');await send('Log.enable');await send('Page.enable');
fs.mkdirSync('shots',{recursive:true});
async function shot(name,m,scrollTo){await send('Emulation.setDeviceMetricsOverride',m);await send('Page.navigate',{url});await sleep(3500);
  if(scrollTo==null){await send('Input.dispatchMouseEvent',{type:'mouseMoved',x:m.width*0.28,y:m.height*0.58});await sleep(900);}
  if(scrollTo!=null){await ev(`window.scrollTo(0,${scrollTo})`);await sleep(1200);}
  const d=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync('shots/'+name+'.png',Buffer.from(d.result.data,'base64'));}
const D={width:1440,height:900,deviceScaleFactor:1,mobile:false};
const total=await ev('document.documentElement.scrollHeight');const worksTop=await ev('document.getElementById("works").offsetTop');
const M={width:390,height:844,deviceScaleFactor:2,mobile:true};await shot('m_hero',M,null);const mw=await ev('document.getElementById("works").offsetTop');await shot('m_works',M,mw+300);const ms=await ev('document.getElementById("services").offsetTop');await shot('m_services',M,ms);
console.log('total height',total,'overflow',await ev('document.documentElement.scrollWidth-innerWidth'));
const errs=[];for(const e of events){if(e.method==='Runtime.exceptionThrown')errs.push((e.params.exceptionDetails.exception||{}).description||e.params.exceptionDetails.text);if(e.method==='Log.entryAdded'&&e.params.entry.level==='error')errs.push('LOG '+e.params.entry.text.slice(0,160));if(e.method==='Runtime.consoleAPICalled'&&e.params.type==='warning')errs.push('WARN '+e.params.args.map(a=>a.value||'').join(' ').slice(0,200));}
console.log('errors',JSON.stringify(errs,null,1));
ws.close();chrome.kill();
