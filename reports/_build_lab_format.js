// ============================================================================
// LAMS / KSNU lab-format rebuild of the Directional-Causality deck.
// 31 slides, Korean body + English section/figure headings, Malgun Gothic,
// navy #0B2F6D, KSNU + LAMS logos. Mirrors te-conference-talk-v2 content.
// ============================================================================
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "W", width: 13.333, height: 7.5 });
pres.layout = "W";
pres.author = "Sina Hadadi";
pres.title = "Directional Causality Between Load and Response Variables of a FOWT";

// ---- design tokens ---------------------------------------------------------
const NAVY="0B2F6D", INK="1A1A1A", MUTED="7A7A7A", WHITE="FFFFFF",
      BLUE="1F4E96", RED="C00000", LINEG="D6D6D6", BANDBG="F2F4F8";
const F="맑은 고딕";
const W=13.333, H=7.5, ML=0.62, MR=0.62, RIGHT=W-MR, CW=W-ML-MR;
const FIG="figs/v2_assets/", LAB="figs/lab_assets/";
const KSNU_AR=477/207, LAMS_AR=501/250;
const RECT=pres.shapes.RECTANGLE, LINE=pres.shapes.LINE, RR=pres.shapes.ROUNDED_RECTANGLE;

let PAGE=1;

// ---- chrome on every content slide -----------------------------------------
function chrome(s, sec, en){
  PAGE+=1;
  s.background={color:WHITE};
  s.addText(sec,{x:ML,y:0.26,w:0.95,h:0.6,fontFace:F,fontSize:30,bold:true,color:NAVY,valign:"middle",margin:0});
  s.addShape(LINE,{x:ML+0.04,y:0.86,w:0.58,h:0,line:{color:NAVY,width:2.5}});
  s.addText(en,{x:ML+1.0,y:0.26,w:7.6,h:0.6,fontFace:F,fontSize:23,bold:true,color:INK,valign:"middle",margin:0});
  // logos top-right: LAMS then KSNU
  const lh=0.50, kh=0.50, lw=lh*LAMS_AR, kw=kh*KSNU_AR;
  s.addImage({path:LAB+"ksnu.png", x:RIGHT-kw, y:0.30, w:kw, h:kh});
  s.addImage({path:LAB+"lams.png", x:RIGHT-kw-lw-0.18, y:0.30, w:lw, h:lh});
  s.addShape(LINE,{x:ML,y:1.06,w:CW,h:0,line:{color:LINEG,width:1.25}});
  s.addText(String(PAGE),{x:RIGHT-0.8,y:7.06,w:0.72,h:0.3,fontFace:F,fontSize:11,color:MUTED,align:"right",margin:0});
}

function bracket(s,x,y,txt,w){
  s.addText("[ "+txt+" ]",{x,y,w:w||CW,h:0.4,fontFace:F,fontSize:15.5,bold:true,color:NAVY,margin:0});
}
function subhead(s,x,y,w,txt){
  s.addText(txt,{x,y,w,h:0.36,fontFace:F,fontSize:15,bold:true,color:NAVY,margin:0});
}
// rich runs: {t, b:bold, c:color}
function runs(list){ return list.map(r=>({text:r.t,options:Object.assign({color:r.c||INK},r.b?{bold:true}:{})})); }
function bullets(s,x,y,w,items,size){
  const arr=[];
  items.forEach((it)=>{
    arr.push({text:"•  ",options:{color:NAVY,bold:true}});
    const rs = Array.isArray(it)?it:[{t:it}];
    rs.forEach(r=>arr.push({text:r.t,options:Object.assign({color:r.c||INK},r.b?{bold:true}:{})}));
    arr[arr.length-1].options.breakLine=true;
  });
  s.addText(arr,{x,y,w,h:4.6,fontFace:F,fontSize:size||14.5,color:INK,lineSpacingMultiple:1.32,paraSpaceAfter:8,valign:"top",margin:0});
}
function para(s,x,y,w,rich,size,h){
  s.addText(runs(rich),{x,y,w,h:h||1.6,fontFace:F,fontSize:size||14.5,color:INK,lineSpacingMultiple:1.3,valign:"top",margin:0});
}
function fig(s,x,y,w,ar,img,cap){
  const h=w/ar;
  s.addShape(RECT,{x,y,w:w+0.3,h:h+0.3,fill:{color:WHITE},line:{color:LINEG,width:1.25}});
  s.addImage({path:img,x:x+0.15,y:y+0.15,w,h});
  if(cap) s.addText(cap,{x:x,y:y+h+0.42,w:w+0.3,h:0.34,fontFace:F,fontSize:11.5,bold:true,color:INK,align:"center",margin:0});
  return h;
}
function vline(s,x,y,h){ s.addShape(LINE,{x,y,w:0,h,line:{color:LINEG,width:1}}); }

// ---- navy divider / hero ---------------------------------------------------
function divider(num, en, ko){
  const s=pres.addSlide(); PAGE+=1;
  s.background={color:NAVY};
  s.addText(num,{x:ML+0.3,y:1.7,w:5,h:1.5,fontFace:F,fontSize:96,bold:true,color:WHITE,margin:0});
  s.addShape(RECT,{x:ML+0.4,y:3.3,w:1.4,h:0.05,fill:{color:"E6A23C"},line:{type:"none"}});
  s.addText(en,{x:ML+0.4,y:3.5,w:11,h:0.9,fontFace:F,fontSize:38,bold:true,color:WHITE,margin:0});
  if(ko) s.addText(ko,{x:ML+0.42,y:4.5,w:11,h:0.7,fontFace:F,fontSize:18,color:"C8D3E8",margin:0});
  // small logos bottom-right
  const kh=0.46,kw=kh*KSNU_AR,lh=0.46,lw=lh*LAMS_AR;
  s.addText(String(PAGE),{x:RIGHT-0.8,y:7.06,w:0.72,h:0.3,fontFace:F,fontSize:11,color:"9FB0CF",align:"right",margin:0});
  return s;
}

// ============================================================================
// SLIDE 1 — TITLE (navy, lab format)
// ============================================================================
(function(){
  const s=pres.addSlide(); s.background={color:NAVY};
  s.addText("한국풍력에너지학회 2026 춘계학술대회",{x:ML+0.2,y:0.95,w:11,h:0.4,fontFace:F,fontSize:15,italic:true,bold:true,color:"C8D3E8",margin:0});
  s.addText("부유식 해상풍력터빈 하중–응답 변수 간\n방향성 인과관계",{x:ML+0.2,y:1.55,w:12.2,h:1.4,fontFace:F,fontSize:33,bold:true,color:WHITE,lineSpacingMultiple:1.08,valign:"top",margin:0});
  s.addText("시간영역 전달 엔트로피(Transfer Entropy) 기반 분석",{x:ML+0.2,y:2.92,w:12,h:0.7,fontFace:F,fontSize:23,color:"9FB0CF",margin:0});
  s.addText([{text:"2026. 06. 22",options:{bold:true,color:WHITE}},{text:"   |   IEA-15MW · UMaine VolturnUS-S · OpenFAST + IDTxl",options:{color:"9FB0CF"}}],
    {x:ML+0.2,y:3.85,w:12,h:0.4,fontFace:F,fontSize:14.5,margin:0});
  s.addShape(LINE,{x:ML+0.2,y:4.45,w:CW-0.4,h:0,line:{color:"3A5488",width:1}});
  s.addText([
    {text:"국립군산대학교 자율운항해양시스템연구실(LAMS) · 조선해양공학과\n",options:{bold:true,color:WHITE,breakLine:true,fontSize:14}},
    {text:"Sina Hadadi",options:{bold:true,color:WHITE}},
    {text:"   ·   지도교수  노재규",options:{color:"C8D3E8"}}
  ],{x:ML+0.2,y:4.65,w:11,h:1.0,fontFace:F,fontSize:13.5,lineSpacingMultiple:1.3,valign:"top",margin:0});
  // white logo band at bottom
  s.addShape(RECT,{x:0,y:6.55,w:W,h:0.95,fill:{color:WHITE},line:{type:"none"}});
  const kh=0.55,kw=kh*KSNU_AR,lh=0.55,lw=lh*LAMS_AR;
  s.addImage({path:LAB+"ksnu.png",x:ML,y:6.74,w:kw,h:kh});
  s.addImage({path:LAB+"lams.png",x:RIGHT-lw,y:6.74,w:lw,h:lh});
})();

// ============================================================================
// 01 BACKGROUND
// ============================================================================

// S2 — RL context (reward)
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — RL 맥락");
  bracket(s,ML,1.25,"설계 최적화를 강화학습으로");
  const by=2.15, bw=3.7, bh=1.95, agX=ML, enX=RIGHT-bw;
  s.addShape(RR,{x:agX,y:by,w:bw,h:bh,fill:{color:BANDBG},line:{color:NAVY,width:1.25},rectRadius:0.06});
  s.addText("에이전트 (Agent)",{x:agX+0.25,y:by+0.18,w:bw-0.5,h:0.3,fontFace:F,fontSize:13,bold:true,color:NAVY,margin:0});
  bullets(s,agX+0.25,by+0.62,bw-0.5,[
    [{t:"Actor",b:true},{t:" — 정책 π(a|s)"}],
    [{t:"Critic",b:true},{t:" — 가치함수 V(s)"}],
    [{t:"actor–critic · TD-오차 갱신",c:MUTED}]
  ],12.5);
  s.addShape(RR,{x:enX,y:by,w:bw,h:bh,fill:{color:BANDBG},line:{color:NAVY,width:1.25},rectRadius:0.06});
  s.addText("환경 (Environment)",{x:enX+0.25,y:by+0.18,w:bw-0.5,h:0.3,fontFace:F,fontSize:13,bold:true,color:NAVY,margin:0});
  bullets(s,enX+0.25,by+0.62,bw-0.5,[
    [{t:"RAFT 연성 시뮬레이터",b:true}],
    [{t:"aero · hydro · servo · moor",c:MUTED}],
    [{t:"각 설계안을 평가",c:MUTED}]
  ],12.5);
  s.addText([{text:"action  ",options:{color:INK}},{text:"aₜ",options:{bold:true}}],{x:agX+bw,y:by+0.25,w:enX-(agX+bw),h:0.3,align:"center",fontFace:F,fontSize:12,margin:0});
  s.addShape(LINE,{x:agX+bw+0.15,y:by+0.7,w:enX-(agX+bw)-0.3,h:0,line:{color:INK,width:1.5,endArrowType:"triangle"}});
  s.addShape(LINE,{x:agX+bw+0.15,y:by+bh-0.55,w:enX-(agX+bw)-0.3,h:0,line:{color:RED,width:2,beginArrowType:"triangle"}});
  s.addText([{text:"state sₜ₊₁    ",options:{color:MUTED}},{text:"reward rₜ₊₁",options:{bold:true,color:RED}}],{x:agX+bw,y:by+bh-0.45,w:enX-(agX+bw),h:0.3,align:"center",fontFace:F,fontSize:12,margin:0});
  s.addShape(LINE,{x:ML,y:4.55,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.7,CW,"보상(reward) rₜ₊₁ — 에이전트가 최대화하는 단 하나의 신호");
  para(s,ML,5.15,CW,[
    {t:"보상은 설계 목표(질량 ↓, 공진 회피, 응답 피크 ↓)를 "},
    {t:"인코딩",b:true,c:RED},
    {t:"하며, 그 가중치가 어떤 목표가 우선되는지를 결정한다 — 바로 다음 장에서 다루는 문제."}
  ],14.5,1.2);
})();

// S3 — weights motivation
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — 문제 정의");
  bracket(s,ML,1.25,"왜 이 가중치인가? 수작업에서 데이터 기반으로");
  s.addShape(RECT,{x:ML,y:1.95,w:CW,h:0.95,fill:{color:BANDBG},line:{color:LINEG,width:1}});
  s.addText([
    {text:"Reward = ",options:{color:INK}},
    {text:"X₁",options:{bold:true,color:RED}},{text:"·ΔMass + ",options:{}},
    {text:"X₂",options:{bold:true,color:RED}},{text:"·ΔResonance + ",options:{}},
    {text:"X₃",options:{bold:true,color:RED}},{text:"·ΔPitch_peak + ",options:{}},
    {text:"X₄",options:{bold:true,color:RED}},{text:"·ΔHeave_peak",options:{}}
  ],{x:ML,y:1.95,w:CW,h:0.95,fontFace:F,fontSize:20,align:"center",valign:"middle",margin:0});
  s.addText("가중치 X₁…X₄ 는 현재 RL 하부구조물 설계 최적화에서 수작업으로 설정된다 (비용·출력·제약 우선순위) — 데이터에 근거하지 않음.",
    {x:ML,y:3.0,w:CW,h:0.4,fontFace:F,fontSize:11.5,italic:true,color:MUTED,align:"center",margin:0});
  const cy=3.7, lw=5.6, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,cy,2.7);
  subhead(s,ML,cy,lw,"THE GAP — 무엇이 빠졌나");
  para(s,ML,cy+0.42,lw,[
    {t:"가중치는 변수 중요도를 "},{t:"수작업으로",b:true},
    {t:" 매긴다. 어떤 응답이 가장 중요한지, 각 응답이 환경에 의해 얼마나 강하게 구동되는지에 대한 객관적 근거가 없다."}
  ],14.5,2.0);
  subhead(s,rx,cy,rw,"데이터 기반 근거");
  bullets(s,rx,cy+0.42,rw,[
    [{t:"전달 엔트로피(TE)",b:true,c:NAVY},{t:" — 어떤 환경 구동원이 각 응답을 인과적으로 구동하는가"}],
    [{t:"Sobol 민감도",b:true,c:NAVY},{t:" — 어떤 설계 변수가 각 응답을 움직이는가"}],
    [{t:"두 가지를 결합",b:true,c:NAVY},{t:" — 가중치의 데이터 기반 근거"}]
  ],13.5);
})();

// S4 — association to causation
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — 연관에서 인과로");
  bracket(s,ML,1.25,"From association to directed causation");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"상관 / 코히어런스 (Correlation)");
  para(s,ML,y+0.45,lw,[
    {t:"대칭적·무방향 — 연관성만 정량화. γ²(f) 는 바람과 하중이 한 주파수에서 파워를 공유함을 알려줄 뿐, "},
    {t:"어느 쪽이 구동하는지는 말하지 못한다.",b:true}
  ],14,2.0);
  subhead(s,rx,y,rw,"전달 엔트로피 (Transfer Entropy)");
  para(s,rx,y+0.45,rw,[
    {t:"방향성·비선형·모델 무가정. 소스의 과거가 타깃의 미래에 대해 추가로 주는 정보를 측정한다 — "},
    {t:"타깃 자신의 과거를 넘어서.",b:true}
  ],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"THE QUESTION — 핵심 질문");
  para(s,ML,5.45,CW,[
    {t:"어떤 환경 구동원(바람 또는 파랑)이 각 구조 응답을 인과적으로 구동하며, 선형 기법이 놓치는 연성 경로는 무엇인가?"}
  ],14.5,1.0);
})();

// S5 — correlation is not causation
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — 상관 ≠ 인과");
  bracket(s,ML,1.25,"Correlation is not causation");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"함정 (The trap)");
  para(s,ML,y+0.45,lw,[
    {t:"아이스크림 판매와 익사 사고는 함께 증가한다 — 둘 다 여름 더위가 원인. 강한 상관, 인과는 0. corr(A,B)=corr(B,A) 에는 방향(화살표)이 없다."}
  ],14,2.0);
  subhead(s,rx,y,rw,"방향이 요구하는 것");
  para(s,rx,y+0.45,rw,[
    {t:"진짜 원인은 결과보다 시간적으로 앞서야 하고, 타깃 자신의 이력과 공통 구동원을 고려한 뒤에도 그 연결이 살아남아야 한다."}
  ],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"연성 시스템에서");
  para(s,ML,5.45,CW,[
    {t:"난류나 부유식 풍력터빈에서는 수십 개 채널이 함께 움직인다. 무엇이 무엇을 구동하는지 눈으로 가늠하기란 불가능 — 방향성·모델 무가정 척도가 필요하다."}
  ],14.5,1.0);
})();

// ============================================================================
// 02 TRANSFER ENTROPY (theory)
// ============================================================================

// S6 — information theory blocks
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 정보이론 기초");
  bracket(s,ML,1.25,"Entropy and information");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"섀넌 엔트로피 (Shannon entropy)");
  s.addText("H(X) = −Σ p(x) log p(x)",{x:ML,y:y+0.42,w:lw,h:0.4,fontFace:F,fontSize:14,bold:true,color:BLUE,margin:0});
  para(s,ML,y+0.9,lw,[{t:"신호에 담긴 평균 불확실성(‘놀라움’). 결과가 확실하면 0, 모든 결과가 동등하면 최대."}],13.5,1.4);
  subhead(s,rx,y,rw,"상호정보량 (Mutual information)");
  s.addText("I(X;Y) = H(X) + H(Y) − H(X,Y)",{x:rx,y:y+0.42,w:rw,h:0.4,fontFace:F,fontSize:14,bold:true,color:BLUE,margin:0});
  para(s,rx,y+0.9,rw,[{t:"X 와 Y 가 공유하는 정보 — 하나를 알면 다른 하나의 불확실성이 얼마나 줄어드는가."}],13.5,1.4);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"THE CATCH — 한계");
  para(s,ML,5.45,CW,[
    {t:"상호정보량은 대칭이다: I(X;Y)=I(Y;X). 어느 변수가 어느 쪽을 구동하는지 말할 수 없다 — 바로 전달 엔트로피가 메우는 간극."}
  ],14.5,1.0);
})();

// S7 — TE defined
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 정의");
  bracket(s,ML,1.25,"Transfer entropy, defined");
  s.addShape(RECT,{x:ML,y:1.95,w:CW,h:0.8,fill:{color:BANDBG},line:{color:LINEG,width:1}});
  s.addText("TE(X→Y) = H(Y_f | Y_p) − H(Y_f | Y_p, X_p)",{x:ML,y:1.95,w:CW,h:0.8,fontFace:F,fontSize:19,bold:true,color:BLUE,align:"center",valign:"middle",margin:0});
  const y=3.0, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,1.7);
  subhead(s,ML,y,lw,"정의");
  para(s,ML,y+0.42,lw,[{t:"Y_f = 타깃의 미래 · Y_p = 타깃의 과거 · X_p = 소스의 과거. 소스의 과거가 타깃 자신의 이력을 넘어 다음 스텝 예측을 얼마나 날카롭게 하는가."}],13.5,1.4);
  subhead(s,rx,y,rw,"조건부의 묘수");
  para(s,rx,y+0.42,rw,[{t:"Y 자신의 과거로 조건화하면 자기예측·공유 이력이 제거되고, X 에서 온 ‘진짜 새 정보’만 남는다. 그래서 방향성을 갖는다: TE(X→Y) ≠ TE(Y→X)."}],13.5,1.4);
  s.addShape(LINE,{x:ML,y:5.1,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.25,CW,"핵심 성질");
  para(s,ML,5.65,CW,[
    {t:"TE ≥ 0 이며 TE = 0 이면 전달 없음. 설계상 비대칭이며, 선형-가우시안 신호에서는 Granger 인과성과 정확히 일치(Barnett et al. 2009). 정의: Schreiber (2000)."}
  ],13.5,0.9);
})();

// S8 — estimation KSG
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 추정");
  bracket(s,ML,1.25,"Estimating TE without binning");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"구간 나눔 대신 최근접 이웃");
  para(s,ML,y+0.45,lw,[{t:"TE 는 조건부 상호정보량이다. Kraskov–Stögbauer–Grassberger(KSG) 추정기는 결합 공간에서 k 개 최근접 이웃(k=4)을 센다 — 히스토그램도, 고를 구간 수도 없다."}],14,2.0);
  subhead(s,rx,y,rw,"우리 데이터에 적합한 이유");
  para(s,rx,y+0.45,rw,[{t:"연속 신호에 적응적 해상도; 가우시안 기법이 놓치는 비선형 의존을 포착. 비트가 아닌 나츠(nats, 자연로그) 단위로 보고 — 같은 양. Kraskov et al. (2004)."}],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"파이프라인에서");
  para(s,ML,5.45,CW,[
    {t:"KSG(k=4) + 비균일 임베딩(max_lag = 150 ≈ 1 슬로우드리프트 주기)을 IDTxl(Wollstadt et al. 2019)로 GPU 가속해 실행."}
  ],14.5,1.0);
})();

// S9 — embedding tau
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 임베딩");
  bracket(s,ML,1.25,"Time delay τ and the embedding window");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"지연 벡터 (delay vectors)");
  para(s,ML,y+0.45,lw,[{t:"TE 는 최근 과거를 지연 벡터로 표현: Y_past = [y(t−τ), y(t−2τ), …, y(t−max_lag)]. τ 는 시차 간격을, max_lag 는 얼마나 멀리 보는지를 정한다."}],14,2.0);
  subhead(s,rx,y,rw,"우리 설정");
  para(s,rx,y+0.45,rw,[{t:"max_lag = 150 샘플 ≈ 5 Hz 에서 30 초 — 플랫폼 슬로우드리프트 한 주기. τ=1 은 모든 시차 유지 후 그리디 탐색; τ=5 는 ~150 후보를 ~30 으로 솎는다."}],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"둘 다 중요한 이유");
  para(s,ML,5.45,CW,[
    {t:"창이 너무 짧으면 슬로우드리프트를 놓치고, 시차 격자가 너무 촘촘하면 그리디 탐색이 폭발한다. τ 와 max_lag 가 인과 검정이 볼 수 있는 시차를 함께 결정한다."}
  ],14.5,1.0);
})();

// S10 — tau not a free knob
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — τ");
  bracket(s,ML,1.25,"τ is not a free knob");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"솔깃한 지름길");
  para(s,ML,y+0.45,lw,[{t:"흔한 휴리스틱은 자기-상호정보량의 첫 최소(AIS 최적 지연)에서 τ 를 정한다. 자기예측가능성(AIS)은 잘 보존한다."}],14,2.0);
  subhead(s,rx,y,rw,"…그러나 TE 를 깨뜨린다");
  para(s,rx,y+0.45,rw,[
    {t:"하지만 self-MI τ=10 은 지배적 Wave→PtfmPitch 엣지를 "},
    {t:"0 으로 만들었다",b:true,c:RED},
    {t:". 방향성 연성은 특정 시차에 살아 있어 자기예측 휴리스틱이 놓친다 — AIS 에 최적이 TE 에 최적은 아니다."}
  ],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"τ 의 두 역할");
  para(s,ML,5.45,CW,[
    {t:"τ 는 모델링 선택(검정이 보는 시차)이자 계산 레버 — 슬로우드리프트 플랫폼 채널은 τ=5 에서만 끝난다. τ>1 은 모두 τ=1 기준선과 검증한다."}
  ],14.5,1.0);
})();

// S11 — significance
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 유의성");
  bracket(s,ML,1.25,"Is the transfer real? Surrogate testing");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"귀무가설 (null hypothesis)");
  para(s,ML,y+0.45,lw,[{t:"KSG TE 는 정확히 0 이 되지 않는다 — 유한표본 잡음이 작은 양수를 남긴다. 그래서 묻는다: 연성이 없다면 우연보다 큰가?"}],14,2.0);
  subhead(s,rx,y,rw,"순환 이동 대리표본 (circular-shift)");
  para(s,rx,y+0.45,rw,[{t:"소스를 시간축으로 회전(n=200)해 타깃과의 타이밍은 깨고 스펙트럼은 유지. p = 실제 TE 를 이긴 대리표본 비율; p<0.05 엣지만 유지."}],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"왜 순환 이동인가");
  para(s,ML,5.45,CW,[
    {t:"순환 이동은 소스의 스펙트럼·진폭을 그대로 두고 X→Y 타이밍만 제거한다 — 거짓 양성을 피하는 엄격하고 정직한 귀무."}
  ],14.5,1.0);
})();

// S12 — toy example
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 직관");
  bracket(s,ML,1.25,"A toy example: who drives whom?");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"설정 (Setup)");
  s.addText("X[i] = 0.5·X[i−1] + noise\nY[i] = 0.5·X[i−1] + noise",{x:ML,y:y+0.42,w:lw,h:0.7,fontFace:F,fontSize:13.5,bold:true,color:BLUE,lineSpacingMultiple:1.2,margin:0});
  para(s,ML,y+1.25,lw,[{t:"X 는 자율, Y 는 X 의 과거에 반응. 눈으로는 둘 다 무작위 잡음처럼 보인다."}],13.5,0.9);
  subhead(s,rx,y,rw,"TE 가 복원하는 것");
  s.addText("TE(X→Y) ≫ TE(Y→X)",{x:rx,y:y+0.42,w:rw,h:0.4,fontFace:F,fontSize:15,bold:true,color:RED,margin:0});
  para(s,rx,y+0.95,rw,[{t:"이 비대칭이 X 를 구동원으로 정확히 지목한다 — 대칭인 상관으로는 결코 드러낼 수 없는 것."}],13.5,1.2);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"교훈");
  para(s,ML,5.45,CW,[
    {t:"방향은 원신호가 아니라 조건화에서 나온다 — 바람·파랑·구조 채널에 대해 우리가 실행하는 바로 그 검정."}
  ],14.5,1.0);
})();

// S13 — three ways
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 비교");
  bracket(s,ML,1.25,"Three ways to measure dependence");
  const y=2.05, gap=0.5, cw=(CW-2*gap)/3;
  const cols=[
   ["상관 (Correlation)","선형 연관의 세기. corr(X,Y)=corr(Y,X) — 대칭.","방향 ✗   비선형 ✗"],
   ["Granger 인과성","X 의 과거가 Y 의 선형 예측을 개선하는가? 방향성 있으나 선형(VAR) 가정. Granger 1969 · Nobel 2003.","방향 ✓   비선형 ✗"],
   ["전달 엔트로피","X 의 과거가 Y 의 미래 불확실성을 줄이는가? 모델 무가정. Schreiber 2000.","방향 ✓   비선형 ✓"]];
  cols.forEach((c,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vline(s,x-gap/2,y,2.3);
    subhead(s,x,y,cw,c[0]);
    para(s,x,y+0.42,cw,[{t:c[1]}],12.5,1.6);
    s.addText(c[2],{x,y:y+2.05,w:cw,h:0.3,fontFace:F,fontSize:12,bold:true,color:(i==2?NAVY:MUTED),margin:0});
  });
  s.addShape(LINE,{x:ML,y:4.7,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.85,CW,"핵심");
  para(s,ML,5.3,CW,[
    {t:"전달 엔트로피만이 방향성과 비선형을 동시에 갖는다. 선형-가우시안 과정에서는 Granger 와 정확히 일치(Barnett et al. 2009) — 동역학이 비선형·비가우시안일 때 제 값을 한다."}
  ],14,1.2);
})();

// S14 — TE vs Granger
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — vs Granger");
  bracket(s,ML,1.25,"Transfer entropy and Granger causality");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.4);
  subhead(s,ML,y,lw,"Granger 인과성");
  para(s,ML,y+0.45,lw,[{t:"선형 자기회귀(VAR) 모델. 빠르고 잘 이해되어 있으나 선형·가우시안을 가정 — 비선형 연성을 놓친다."}],14,1.8);
  subhead(s,rx,y,rw,"전달 엔트로피");
  para(s,rx,y+0.45,rw,[{t:"모델 무가정, 분포 가정 없음, 모든 비선형성 포착. 더 비싸고(k-NN 추정) 데이터를 더 요구."}],14,1.8);
  s.addShape(LINE,{x:ML,y:4.7,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.85,CW,"둘이 일치할 때");
  para(s,ML,5.3,CW,[
    {t:"선형-가우시안 과정에서 둘은 정확히 동등(Barnett et al. 2009). TE 는 동역학이 비선형·비가우시안일 때만 제 값을 한다 — 그래서 둘 다 실행한다."}
  ],14,1.2);
})();

// S15 — when to use TE
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — 적용 영역");
  bracket(s,ML,1.25,"When does transfer entropy pay off?");
  const y=2.05, gap=0.5, cw=(CW-2*gap)/3;
  const cols=[
   ["선형 / 가우시안","TE = Granger 와 정확히 동일(Barnett 2009). 추가 가치 없음 — 더 단순한 방법 사용.",MUTED],
   ["비선형 / 비가우시안","선형 기법이 볼 수 없는 방향 구조를 포착. 가장 빛나는 영역.",NAVY],
   ["초고차원","결합 모드가 많으면 k-NN 추정이 저하 — 차원의 저주, 데이터 기근.",MUTED]];
  cols.forEach((c,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vline(s,x-gap/2,y,2.0);
    subhead(s,x,y,cw,c[0]);
    para(s,x,y+0.42,cw,[{t:c[1],c:(i==1?INK:INK),b:(i==1)}],13,1.8);
  });
  s.addShape(LINE,{x:ML,y:4.6,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.75,CW,"핵심");
  para(s,ML,5.2,CW,[
    {t:"불규칙 파랑과 비선형 ROSCO 제어기를 가진 부유식 터빈은 정확히 중간 영역 — 비선형·비가우시안 — 에 놓이며, 전달 엔트로피가 가장 큰 가치를 더한다."}
  ],14,1.2);
})();

// ============================================================================
// 03 METHOD & DATA
// ============================================================================
divider("03","Method & Data","연성 wind–wave–structure–mooring 시스템과 시뮬레이션 캠페인");

// S17 — system & data
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — 시스템");
  bracket(s,ML,1.25,"IEA-15MW FOWT, simulated in OpenFAST");
  const fy=1.95, figW=5.5, ar=1.632;
  const fh=fig(s,ML,fy,figW,ar,FIG+"openfast.png","OpenFAST — 연성 aero-hydro-servo-elastic 모듈");
  const rx=ML+figW+0.9, rw=RIGHT-(ML+figW+0.9); let ry=2.0;
  [["플랫폼","IEA-15-240-RWT + UMaine VolturnUS-S 반잠수식; 연성 aero-hydro-servo-elastic OpenFAST 모델."],
   ["신호","3600 s 시뮬레이션 · 600 s 과도 제거 · 5 Hz 로 데시메이션."],
   ["채널","소스 2 (Wind1VelX, Wave1Elev) → 응답 9 (RootMyc1, RootMxc1, TwrBsMyt, PtfmHeave/Surge/Pitch, FAIRTEN1/2/3)."]
  ].forEach(([h,b],i)=>{ if(i>0)s.addShape(LINE,{x:rx,y:ry-0.12,w:rw,h:0,line:{color:LINEG,width:1}}); subhead(s,rx,ry,rw,h); para(s,rx,ry+0.36,rw,[{t:b}],13,1.2); ry+=1.55; });
})();

// S18 — DLC matrix
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — 설계하중조건");
  bracket(s,ML,1.25,"The simulation campaign");
  const figW=7.4, ar=1.852, ix=(W-figW)/2;
  fig(s,ix,1.95,figW,ar,FIG+"dlc-matrix.png","DLC-A / DLC-B / DLC-1.6, 운전점 스윕 (8/11/15/20 m/s, 6 시드) — 총 54 케이스");
})();

// S19 — env conditions
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — 환경 조건");
  bracket(s,ML,1.25,"Wind and wave inputs");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.4);
  subhead(s,ML,y,lw,"바람 — TurbSim");
  para(s,ML,y+0.45,lw,[{t:"IEC Kaimal(IECKAI) 스펙트럼, 정규난류모델(NTM), class B, 멱법칙 전단, 허브높이 기준. URef = 8 / 11 / 15 / 20 m/s."}],14,1.9);
  subhead(s,rx,y,rw,"파랑 — JONSWAP");
  para(s,rx,y+0.45,rw,[{t:"불규칙 JONSWAP 해상(SeaState). Hs/Tp 는 바람과 함께 변화: (3.5 m, 9 s) → (8.0 m, 13 s). DLC-1.6 극한해상: Hs = 8.3 m, Tp = 12.95 s."}],14,1.9);
  s.addShape(LINE,{x:ML,y:4.7,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.85,CW,"랜덤 시드에 관하여");
  para(s,ML,5.3,CW,[
    {t:"DLC-A/1.6 는 바람 시드를 파랑 생성에 재사용, DLC-B 는 독립 시드. OpenFAST 에서 바람(TurbSim)·파랑(HydroDyn)은 별도 생성되므로 시드는 재현성을 고정할 뿐 wind–wave 상관을 만들지 않는다."}
  ],14,1.2);
})();

// S20 — preprocessing
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — 전처리");
  bracket(s,ML,1.25,"Why 5 Hz is enough");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.5);
  subhead(s,ML,y,lw,"환경 · 플랫폼 (저주파)");
  para(s,ML,y+0.45,lw,[{t:"슬로우드리프트 0.01–0.1 Hz · 파랑 1차 0.05–0.3 Hz(JONSWAP 피크 0.077) · 고유모드 pitch 0.0345 / heave 0.05 / surge 0.01 Hz · 바람 저주파 에디 0.01–1 Hz"}],12.5,2.0);
  subhead(s,rx,y,rw,"로터 · 구조 (고주파)");
  para(s,rx,y+0.45,rw,[{t:"1P / 3P 로터 ~0.15 / 0.45 Hz · 타워 전후 1차 모드 ~0.5 Hz · 블레이드 플랩 모드 ~0.6 Hz"}],12.5,2.0);
  s.addShape(LINE,{x:ML,y:4.8,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.95,CW,"결론");
  para(s,ML,5.4,CW,[
    {t:"40 Hz → 5 Hz 로 8× 다운샘플. Nyquist = 2.5 Hz 가 최고 대역(~0.6 Hz)보다 충분히 높아 모든 인과 신호를 보존하면서 KSG 스윕은 ~8× 감소."}
  ],14,1.1);
})();

// S21 — method directed transfer
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — 파이프라인");
  bracket(s,ML,1.25,"Directed transfer, with linear baselines");
  const steps=[
   ["1","KSG 전달 엔트로피","Kraskov 추정기(k=4), 비균일 임베딩, max_lag = 150 (30 s — 슬로우드리프트 1 주기)."],
   ["2","유의성 · 효과크기","순환이동 대리표본 ×200, p<0.05(max-stat). 정규화: te_frac = TE / (H(Y) − AIS(Y))."],
   ["3","선형 기준선(동일 파이프라인)","Gaussian / Granger(추정기 교체) + 크기제곱 코히어런스 γ²(f)."],
   ["4","계산","2× A100 OpenCL; GPU vs CPU 검증(AIS RootMyc1 1.50 vs 1.49)."]];
  let y=1.95;
  steps.forEach(([n,h,b])=>{
    s.addText(n,{x:ML,y:y-0.02,w:0.5,h:0.55,fontFace:F,fontSize:26,bold:true,color:NAVY,valign:"top",margin:0});
    subhead(s,ML+0.6,y,5.0,h);
    para(s,ML+0.6,y+0.36,5.1,[{t:b}],12,0.7);
    y+=1.18;
  });
  fig(s,ML+6.5,2.2,5.0,1.759,FIG+"pipeline.png","the TE pipeline");
})();

// S22 — what TE measures
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — TE 의 의미");
  bracket(s,ML,1.25,"What transfer entropy measures");
  const figW=6.4, ar=2.043, ix=(W-figW)/2;
  fig(s,ix,1.9,figW,ar,FIG+"concept.png");
  s.addShape(LINE,{x:ML,y:5.35,w:CW,h:0,line:{color:LINEG,width:1}});
  para(s,ML,5.55,CW,[
    {t:"한 줄로 — ",b:true,c:NAVY},
    {t:"소스의 과거가 타깃 자신의 이력을 넘어 타깃 예측을 날카롭게 하면, 정보가 소스 → 타깃으로 흐른다. 방향성(X→Y ≠ Y→X)·비선형 — 상관과 코히어런스가 볼 수 없는 것."}
  ],14,1.2);
})();

// ============================================================================
// 04 RESULTS & CONCLUSION
// ============================================================================
divider("04","Results & Conclusion","파랑이 지배하는 인과 구조와 바람의 역설");

// S24 — wave-dominated network
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — 인과 네트워크");
  bracket(s,ML,1.25,"A wave-dominated causal graph");
  const figW=6.0, ar=1.517;
  fig(s,ML,1.95,figW,ar,FIG+"te-network.png","TE 인과 네트워크 · bivariate KSG, 가중치 = 전 54 케이스 평균 te_frac");
  const rx=ML+figW+0.75, rw=RIGHT-(ML+figW+0.75); let ry=2.1;
  subhead(s,rx,ry,rw,"READING — 읽는 법"); ry+=0.42;
  para(s,rx,ry,rw,[{t:"파랑 표고가 모든 유의 응답(pitch·heave·surge·타워베이스·계류)을 구동. ",b:true},{t:"바람은 구조로의 유의한 방향 전달이 없다.",}],13,1.5); ry+=1.55;
  s.addShape(LINE,{x:rx,y:ry,w:rw,h:0,line:{color:LINEG,width:1}}); ry+=0.12;
  s.addText("7 / 7",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:34,bold:true,color:NAVY,valign:"middle",margin:0}); ry+=0.62;
  s.addText("유의 엣지 — 모두 파랑에서 시작",{x:rx,y:ry,w:rw,h:0.3,fontFace:F,fontSize:11,color:MUTED,margin:0}); ry+=0.5;
  s.addText("0",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:34,bold:true,color:RED,valign:"middle",margin:0}); ry+=0.62;
  s.addText("유의한 wind → structure 엣지",{x:rx,y:ry,w:rw,h:0.3,fontFace:F,fontSize:11,color:MUTED,margin:0});
})();

// S25 — significant edges bars
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — 유의 엣지");
  bracket(s,ML,1.25,"The significant edges — 7 of 18");
  const figW=6.7, ar=2.165;
  fig(s,ML,2.2,figW,ar,FIG+"conf-windwave-bars.png","유의 방향 전달(nats) — 파랑만, 54 케이스 평균");
  const rx=ML+figW+0.7, rw=RIGHT-(ML+figW+0.7); let ry=2.3;
  subhead(s,rx,ry,rw,"WAVE DRIVES THE STRUCTURE"); ry+=0.42;
  para(s,rx,ry,rw,[
    {t:"가장 강한 5개 엣지(pitch, heave, 전방 계류선, surge)가 0.11–0.12 nats 에 모여 있다. "},
    {t:"유의한 wind → structure 엣지는 캠페인 전체에서 없다.",b:true}
  ],13,2.0); ry+=2.1;
  s.addShape(LINE,{x:rx,y:ry,w:rw,h:0,line:{color:LINEG,width:1}}); ry+=0.12;
  s.addText("0 / 18",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:30,bold:true,color:NAVY,valign:"middle",margin:0}); ry+=0.6;
  s.addText("유의한 wind 엣지 — 파랑이 7개 모두 구동",{x:rx,y:ry,w:rw,h:0.4,fontFace:F,fontSize:11,color:MUTED,margin:0});
})();

// S26 — triangulation
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — 삼각검증");
  bracket(s,ML,1.25,"TE vs. coherence vs. Granger");
  const y=2.05, gap=0.5, cw=(CW-2*gap)/3;
  const cols=[
   ["코히어런스 γ²(f)","무방향 스펙트럼 상한. 공유 파워, 방향 없음.",MUTED],
   ["Gaussian / Granger","방향성 있으나 선형. 상관된 wind–wave 에서 과검출.",MUTED],
   ["전달 엔트로피","방향성 AND 비선형. 다른 기법이 놓치는 연성 포착.",NAVY]];
  cols.forEach((c,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vline(s,x-gap/2,y,2.0);
    subhead(s,x,y,cw,c[0]);
    para(s,x,y+0.42,cw,[{t:c[1],b:(i==2)}],13,1.8);
  });
  s.addShape(LINE,{x:ML,y:4.6,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.75,CW,"삼각형 읽기");
  para(s,ML,5.2,CW,[
    {t:"TE 는 유의하나 선형 기준선은 아닌 곳 = TE 만 잡는 비선형 방향 연성(예: 파랑 2차 차주파수의 pitch 강제력). 셋이 일치하는 곳 = 임베딩이 검증됨."}
  ],14,1.2);
})();

// S27 — wind paradox
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — 바람의 역설");
  bracket(s,ML,1.25,"The wind paradox");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,1.6);
  subhead(s,ML,y,lw,"THE PUZZLE — 수수께끼");
  para(s,ML,y+0.42,lw,[{t:"Wind → structure ≈ 0, 8–20 m/s 전 구간",b:true},{t:" — 정작 터빈을 구동하는 건 바람인데. 반직관적이며 모든 운전점에서 성립."}],14,1.4);
  subhead(s,rx,y,rw,"NOT AN ARTIFACT — 인공물 아님");
  para(s,rx,y+0.42,rw,[{t:"바람은 ~11.6 s 에 탈상관 — 30 s 임베딩 창 안. 바람 신호는 샘플링되지만 구조로 정보를 전달하지 않을 뿐."}],14,1.6);
  s.addShape(LINE,{x:ML,y:4.4,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.55,CW,"HYPOTHESIS — 제어기 ‘방화벽’");
  para(s,ML,5.0,CW,[
    {t:"블레이드 피치 제어기(ROSCO)가 로터 추력을 매우 단단히 조절해, 바람 변동이 플랫폼에 도달하기 전에 거부된다. 제어기가 인과적 방화벽으로 작용 — 바람은 로터를 가진화하지 구조를 가진화하지 않는다."}
  ],14,1.4);
})();

// S28 — firewall ablation
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — 방화벽 검정");
  bracket(s,ML,1.25,"Testing the firewall — controller-off ablation");
  const figW=7.0, ar=2.323;
  fig(s,ML,2.15,figW,ar,FIG+"conf-ablation.png","블레이드 피치 제어를 동결(개루프)하고 동일 케이스 재실행");
  const rx=ML+figW+0.7, rw=RIGHT-(ML+figW+0.7); let ry=2.3;
  subhead(s,rx,ry,rw,"VERDICT — 판정"); ry+=0.42;
  para(s,rx,ry,rw,[{t:"시사적이나 결론적이지 않음. ",b:true,c:RED},{t:"wind→heave 엣지가 나타나지만, 개루프 과회전이 AIS 를 부풀려 bivariate TE 에서 바람을 가린다."}],13,2.0); ry+=2.0;
  s.addShape(LINE,{x:rx,y:ry,w:rw,h:0,line:{color:LINEG,width:1}}); ry+=0.16;
  s.addText("NEXT",{x:rx,y:ry,w:rw,h:0.5,fontFace:F,fontSize:24,bold:true,color:NAVY,valign:"middle",margin:0}); ry+=0.55;
  s.addText("조건부 TE  TE(wind→Y | wave)  +  과회전 없는 ablation",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:11,color:MUTED,margin:0});
})();

// S29 — methods lessons
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — 방법론 교훈");
  bracket(s,ML,1.25,"What made it work — and what nearly broke it");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,3.0);
  subhead(s,ML,y,lw,"GPU 가 스윕을 가능케 했다");
  s.addText("~35 h",{x:ML,y:y+0.35,w:lw,h:0.85,fontFace:F,fontSize:44,bold:true,color:NAVY,valign:"middle",margin:0});
  para(s,ML,y+1.3,lw,[{t:"단일 A100 배치 실행 케이스당. OpenCL KSG 추정기(CPU 대비 검증)가 전체 DLC 스윕을 현실화한다."}],13.5,1.2);
  subhead(s,rx,y,rw,"주의 — 임베딩 지연이 중요하다");
  s.addText("0.12 → 0",{x:rx,y:y+0.35,w:rw,h:0.85,fontFace:F,fontSize:40,bold:true,color:RED,valign:"middle",margin:0});
  para(s,rx,y+1.3,rw,[{t:"self-MI 의 데이터 기반 τ 는 AIS 는 보존했으나 TE 엣지를 붕괴(τ=10 이 지배적 Wave→PtfmPitch 를 0 으로). 방향성 연성은 특정 시차에 산다 — AIS 휴리스틱은 TE 로 전이되지 않는다."}],13.5,1.5);
})();

// S30 — hybrid TE + Sobol
(function(){
  const s=pres.addSlide(); chrome(s,"04","Conclusion — TE + Sobol");
  bracket(s,ML,1.25,"Closing the loop: TE + Sobol → data-driven weights");
  const cw=5.5, car=1.570, ch=cw/car, cy=1.95;
  fig(s,ML,cy,cw,car,FIG+"combined.png","COMBINED GRAPH — TE + Sobol");
  const rx=ML+cw+0.9, rw=RIGHT-(ML+cw+0.9);
  fig(s,rx,cy,rw-0.3,2.209,FIG+"sobol.png","Sobol Sₜ — 설계 민감도");
  para(s,rx,cy+ (rw-0.3)/2.209 +0.7,rw,[
    {t:"계류 길이(L_u)·강성(EA)",b:true},{t:" 가 fairlead 장력과 여러 운동을 지배. "},
    {t:"기둥 형상(D_OCol, R_MO)",b:true},{t:" 이 surge·sway·heave 를 구동."}
  ],12,1.0);
  s.addShape(LINE,{x:ML,y:6.05,w:CW,h:0,line:{color:LINEG,width:1}});
  para(s,ML,6.2,CW,[
    {t:"한 그래프에 두 개의 방향 중요도 지도 — "},
    {t:"환경 구동 동역학은 TE, 설계 민감도는 Sobol",b:true,c:NAVY},
    {t:" — 최적화 가중치의 데이터 기반 근거(다음 단계 제안)."}
  ],13,0.8);
})();

// S31 — limitations & future
(function(){
  const s=pres.addSlide(); chrome(s,"04","Conclusion — 한계와 향후");
  bracket(s,ML,1.25,"Where this goes next");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,3.4);
  subhead(s,ML,y,lw,"LIMITATIONS — 한계");
  bullets(s,ML,y+0.45,lw,[
    "단일 플랫폼(UMaine VolturnUS-S), 시뮬레이션 한정 — 현장 검증 없음.",
    "max_lag = 150(30 s)은 PtfmSurge(탈상관 ~24.6 s)에 짧을 수 있음.",
    "방화벽 메커니즘(제어기)은 예비적·교란됨 — 바람 탈동조는 보였으나 원인은 미확정."
  ],13);
  subhead(s,rx,y,rw,"NEXT STEPS — 향후");
  bullets(s,rx,y+0.45,rw,[
    "조건부 TE — TE(wind→Y | wave) — 로 bivariate 추정을 넘어 방화벽 검정.",
    "과회전 없는 controller-off ablation 으로 메커니즘 규명.",
    "하이브리드 그래프: Sobol 설계변수 민감도 추가.",
    [{t:"순위화된 TE 구동→하중 경로",b:true},{t:" 를 구조/피로 하중 가중에 투입해 설계 최적화로."}]
  ],13);
})();

// S32 — conclusion (navy)
(function(){
  const s=pres.addSlide(); PAGE+=1;
  s.background={color:NAVY};
  s.addText("Conclusion",{x:ML+0.2,y:0.7,w:8,h:0.5,fontFace:F,fontSize:16,bold:true,color:"9FB0CF",margin:0});
  s.addText([
    {text:"전달 엔트로피는 부유식 풍력터빈 응답에서 ",options:{color:WHITE}},
    {text:"파랑이 지배하는 인과 구조",options:{color:"7FB0FF",bold:true}},
    {text:"를 드러내며, 이는 선형 기법이 부분적으로만 포착한다.",options:{color:WHITE}}
  ],{x:ML+0.2,y:1.45,w:12,h:1.6,fontFace:F,fontSize:28,bold:true,lineSpacingMultiple:1.15,valign:"top",margin:0});
  s.addShape(LINE,{x:ML+0.2,y:3.4,w:CW-0.4,h:0,line:{color:"3A5488",width:1}});
  const items=[
    "파랑이 pitch·heave·surge·타워베이스·계류를 구동; 54 케이스 캠페인 전체에서 유의한 wind → structure 엣지는 없다.",
    "바람 탈동조는 견고하고 비자명하며 8–20 m/s 전 구간에서 성립 — 다만 제어기가 원인인지는 열린·검증 가능한 질문.",
    "조건부 TE 와 과회전 없는 ablation 이 이를 규명하는 길.",
    "다음: 이 순위를 Sobol 설계 민감도와 짝지어 설계 최적화의 데이터 기반 가중치를 설정."
  ];
  const arr=[];
  items.forEach(t=>{ arr.push({text:"—  ",options:{color:"E6A23C",bold:true}}); arr.push({text:t,options:{color:"DDE5F2",breakLine:true}}); });
  s.addText(arr,{x:ML+0.2,y:3.6,w:CW-0.4,h:2.6,fontFace:F,fontSize:14.5,lineSpacingMultiple:1.25,paraSpaceAfter:9,valign:"top",margin:0});
  // logo band
  s.addShape(RECT,{x:0,y:6.7,w:W,h:0.8,fill:{color:WHITE},line:{type:"none"}});
  const kh=0.48,kw=kh*KSNU_AR,lh=0.48,lw=lh*LAMS_AR;
  s.addImage({path:LAB+"ksnu.png",x:ML,y:6.85,w:kw,h:kh});
  s.addImage({path:LAB+"lams.png",x:RIGHT-lw,y:6.85,w:lw,h:lh});
  s.addText("github.com/sinahdme/fowt-te-causal",{x:W/2-2.5,y:6.95,w:5,h:0.3,fontFace:F,fontSize:11,color:MUTED,align:"center",margin:0});
})();

pres.writeFile({ fileName: "te-conference-talk-lab.pptx" }).then(f=>console.log("wrote",f));
