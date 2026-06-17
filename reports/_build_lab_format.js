// ============================================================================
// LAMS / KSNU lab-format rebuild of the Directional-Causality deck.
// 32 slides, English body + English section/figure headings, Malgun Gothic,
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
  s.addText(en,{x:ML+1.0,y:0.26,w:8.4,h:0.6,fontFace:F,fontSize:23,bold:true,color:INK,valign:"middle",margin:0});
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
function divider(num, en, sub){
  const s=pres.addSlide(); PAGE+=1;
  s.background={color:NAVY};
  s.addText(num,{x:ML+0.3,y:1.7,w:5,h:1.5,fontFace:F,fontSize:96,bold:true,color:WHITE,margin:0});
  s.addShape(RECT,{x:ML+0.4,y:3.3,w:1.4,h:0.05,fill:{color:"E6A23C"},line:{type:"none"}});
  s.addText(en,{x:ML+0.4,y:3.5,w:11,h:0.9,fontFace:F,fontSize:38,bold:true,color:WHITE,margin:0});
  if(sub) s.addText(sub,{x:ML+0.42,y:4.5,w:11.5,h:0.7,fontFace:F,fontSize:18,color:"C8D3E8",margin:0});
  s.addText(String(PAGE),{x:RIGHT-0.8,y:7.06,w:0.72,h:0.3,fontFace:F,fontSize:11,color:"9FB0CF",align:"right",margin:0});
  return s;
}

// ============================================================================
// SLIDE 1 — TITLE (navy, lab format)
// ============================================================================
(function(){
  const s=pres.addSlide(); s.background={color:NAVY};
  s.addText("KWEA 2026 SPRING CONFERENCE",{x:ML+0.2,y:0.95,w:11,h:0.4,fontFace:F,fontSize:14,italic:true,bold:true,color:"C8D3E8",charSpacing:2,margin:0});
  s.addText("Directional Causality Between Load and\nResponse Variables of a FOWT",{x:ML+0.2,y:1.55,w:12.2,h:1.4,fontFace:F,fontSize:33,bold:true,color:WHITE,lineSpacingMultiple:1.08,valign:"top",margin:0});
  s.addText("via Time-Domain Transfer Entropy",{x:ML+0.2,y:2.92,w:12,h:0.7,fontFace:F,fontSize:23,color:"9FB0CF",margin:0});
  s.addText([{text:"2026. 06. 22",options:{bold:true,color:WHITE}},{text:"   |   IEA-15MW · UMaine VolturnUS-S · OpenFAST + IDTxl",options:{color:"9FB0CF"}}],
    {x:ML+0.2,y:3.85,w:12,h:0.4,fontFace:F,fontSize:14.5,margin:0});
  s.addShape(LINE,{x:ML+0.2,y:4.45,w:CW-0.4,h:0,line:{color:"3A5488",width:1}});
  s.addText([
    {text:"Laboratory of Autonomous Maritime Systems (LAMS) · Dept. of Naval Architecture & Ocean Engineering, Kunsan National University\n",options:{bold:true,color:WHITE,breakLine:true,fontSize:13}},
    {text:"Sina Hadadi",options:{bold:true,color:WHITE}},
    {text:"   ·   Advisor — Prof. Jackyou Noh",options:{color:"C8D3E8"}}
  ],{x:ML+0.2,y:4.65,w:11.5,h:1.2,fontFace:F,fontSize:13,lineSpacingMultiple:1.35,valign:"top",margin:0});
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
  const s=pres.addSlide(); chrome(s,"01","Background — RL context");
  bracket(s,ML,1.25,"Design optimization as reinforcement learning");
  const by=2.15, bw=3.7, bh=1.95, agX=ML, enX=RIGHT-bw;
  s.addShape(RR,{x:agX,y:by,w:bw,h:bh,fill:{color:BANDBG},line:{color:NAVY,width:1.25},rectRadius:0.06});
  s.addText("AGENT",{x:agX+0.25,y:by+0.18,w:bw-0.5,h:0.3,fontFace:F,fontSize:13,bold:true,color:NAVY,charSpacing:1,margin:0});
  bullets(s,agX+0.25,by+0.62,bw-0.5,[
    [{t:"Actor",b:true},{t:" — policy π(a|s)"}],
    [{t:"Critic",b:true},{t:" — value V(s)"}],
    [{t:"actor–critic · TD-error updates",c:MUTED}]
  ],12.5);
  s.addShape(RR,{x:enX,y:by,w:bw,h:bh,fill:{color:BANDBG},line:{color:NAVY,width:1.25},rectRadius:0.06});
  s.addText("ENVIRONMENT",{x:enX+0.25,y:by+0.18,w:bw-0.5,h:0.3,fontFace:F,fontSize:13,bold:true,color:NAVY,charSpacing:1,margin:0});
  bullets(s,enX+0.25,by+0.62,bw-0.5,[
    [{t:"RAFT coupled simulator",b:true}],
    [{t:"aero · hydro · servo · moor",c:MUTED}],
    [{t:"evaluates each design",c:MUTED}]
  ],12.5);
  s.addText([{text:"action  ",options:{color:INK}},{text:"aₜ",options:{bold:true}}],{x:agX+bw,y:by+0.25,w:enX-(agX+bw),h:0.3,align:"center",fontFace:F,fontSize:12,margin:0});
  s.addShape(LINE,{x:agX+bw+0.15,y:by+0.7,w:enX-(agX+bw)-0.3,h:0,line:{color:INK,width:1.5,endArrowType:"triangle"}});
  s.addShape(LINE,{x:agX+bw+0.15,y:by+bh-0.55,w:enX-(agX+bw)-0.3,h:0,line:{color:RED,width:2,beginArrowType:"triangle"}});
  s.addText([{text:"state sₜ₊₁    ",options:{color:MUTED}},{text:"reward rₜ₊₁",options:{bold:true,color:RED}}],{x:agX+bw,y:by+bh-0.45,w:enX-(agX+bw),h:0.3,align:"center",fontFace:F,fontSize:12,margin:0});
  s.addShape(LINE,{x:ML,y:4.55,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.7,CW,"THE REWARD  ·  rₜ₊₁ — the one signal the agent maximizes");
  para(s,ML,5.15,CW,[
    {t:"The reward "},
    {t:"encodes the design objectives",b:true,c:RED},
    {t:" (mass ↓, resonance avoidance, peak-response ↓), and its weights decide which objective wins — exactly what we examine next."}
  ],14.5,1.2);
})();

// S3 — weights motivation
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — the problem");
  bracket(s,ML,1.25,"Why these weights? From hand-set to data-driven");
  s.addShape(RECT,{x:ML,y:1.95,w:CW,h:0.95,fill:{color:BANDBG},line:{color:LINEG,width:1}});
  s.addText([
    {text:"Reward = ",options:{color:INK}},
    {text:"X₁",options:{bold:true,color:RED}},{text:"·ΔMass + ",options:{}},
    {text:"X₂",options:{bold:true,color:RED}},{text:"·ΔResonance + ",options:{}},
    {text:"X₃",options:{bold:true,color:RED}},{text:"·ΔPitch_peak + ",options:{}},
    {text:"X₄",options:{bold:true,color:RED}},{text:"·ΔHeave_peak",options:{}}
  ],{x:ML,y:1.95,w:CW,h:0.95,fontFace:F,fontSize:20,align:"center",valign:"middle",margin:0});
  s.addText("Weights X₁…X₄ are set by hand in our RL substructure design optimization (cost, power, constraint priority) — not from data.",
    {x:ML,y:3.0,w:CW,h:0.4,fontFace:F,fontSize:11.5,italic:true,color:MUTED,align:"center",margin:0});
  const cy=3.7, lw=5.6, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,cy,2.7);
  subhead(s,ML,cy,lw,"THE GAP");
  para(s,ML,cy+0.42,lw,[
    {t:"Weights rank variable importance "},{t:"by hand",b:true},
    {t:". No objective basis for which responses matter most, or how strongly each is driven by the environment."}
  ],14.5,2.0);
  subhead(s,rx,cy,rw,"A DATA-DRIVEN BASIS");
  bullets(s,rx,cy+0.42,rw,[
    [{t:"Transfer entropy (TE)",b:true,c:NAVY},{t:" — which environmental drivers causally drive each response"}],
    [{t:"Sobol sensitivity",b:true,c:NAVY},{t:" — which design parameters move each response"}],
    [{t:"Together",b:true,c:NAVY},{t:" — a data-driven basis for the weights"}]
  ],13.5);
})();

// S4 — association to causation
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — association to causation");
  bracket(s,ML,1.25,"From association to directed causation");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"Correlation / coherence");
  para(s,ML,y+0.45,lw,[
    {t:"Symmetric and undirected — quantifies association. γ²(f) tells you wind and a load share power at a frequency, "},
    {t:"not which drives which.",b:true}
  ],14,2.0);
  subhead(s,rx,y,rw,"Transfer entropy");
  para(s,rx,y+0.45,rw,[
    {t:"Directed, nonlinear, model-free. Measures information a source's past adds about a target's future, "},
    {t:"beyond the target's own past.",b:true}
  ],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"THE QUESTION");
  para(s,ML,5.45,CW,[
    {t:"Which environmental driver — wind or wave — causally drives each structural response, and which coupling pathways do linear methods miss?"}
  ],14.5,1.0);
})();

// S5 — correlation is not causation
(function(){
  const s=pres.addSlide(); chrome(s,"01","Background — correlation ≠ causation");
  bracket(s,ML,1.25,"Correlation is not causation");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"The trap");
  para(s,ML,y+0.45,lw,[
    {t:"Ice-cream sales and drownings rise together — both driven by summer heat. Strong correlation, zero causation. corr(A,B) = corr(B,A) carries no arrow."}
  ],14,2.0);
  subhead(s,rx,y,rw,"What direction needs");
  para(s,rx,y+0.45,rw,[
    {t:"A real cause must precede its effect in time, and the link must survive once the target's own history and shared drivers are accounted for."}
  ],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"IN A COUPLED SYSTEM");
  para(s,ML,5.45,CW,[
    {t:"In turbulence or a floating turbine, dozens of channels move together. Eyeballing what drives what is hopeless — we need a directed, model-free measure."}
  ],14.5,1.0);
})();

// ============================================================================
// 02 TRANSFER ENTROPY (theory)
// ============================================================================

// S6 — information theory blocks
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — building blocks");
  bracket(s,ML,1.25,"Entropy and information");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"Shannon entropy");
  s.addText("H(X) = −Σ p(x) log p(x)",{x:ML,y:y+0.42,w:lw,h:0.4,fontFace:F,fontSize:14,bold:true,color:BLUE,margin:0});
  para(s,ML,y+0.9,lw,[{t:"Average uncertainty — the “surprise” in a signal. Zero when the outcome is certain, maximal when all outcomes are equally likely."}],13.5,1.4);
  subhead(s,rx,y,rw,"Mutual information");
  s.addText("I(X;Y) = H(X) + H(Y) − H(X,Y)",{x:rx,y:y+0.42,w:rw,h:0.4,fontFace:F,fontSize:14,bold:true,color:BLUE,margin:0});
  para(s,rx,y+0.9,rw,[{t:"The information shared between X and Y — how much knowing one reduces uncertainty about the other."}],13.5,1.4);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"THE CATCH");
  para(s,ML,5.45,CW,[
    {t:"Mutual information is symmetric: I(X;Y) = I(Y;X). It cannot say which variable drives which — the gap transfer entropy is built to close."}
  ],14.5,1.0);
})();

// S7 — TE defined
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — defined");
  bracket(s,ML,1.25,"Transfer entropy, defined");
  s.addShape(RECT,{x:ML,y:1.95,w:CW,h:0.8,fill:{color:BANDBG},line:{color:LINEG,width:1}});
  s.addText("TE(X→Y) = H(Y_f | Y_p) − H(Y_f | Y_p, X_p)",{x:ML,y:1.95,w:CW,h:0.8,fontFace:F,fontSize:19,bold:true,color:BLUE,align:"center",valign:"middle",margin:0});
  const y=3.0, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,1.7);
  subhead(s,ML,y,lw,"The definition");
  para(s,ML,y+0.42,lw,[{t:"Y_f = target's future · Y_p = target's past · X_p = source's past. How much the source's past sharpens the prediction of the target's next step, beyond its own history."}],13.5,1.4);
  subhead(s,rx,y,rw,"The conditioning trick");
  para(s,rx,y+0.42,rw,[{t:"Conditioning on Y's own past removes self-prediction and shared history — only genuinely new information from X survives. That makes TE directed: TE(X→Y) ≠ TE(Y→X)."}],13.5,1.4);
  s.addShape(LINE,{x:ML,y:5.1,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.25,CW,"KEY PROPERTIES");
  para(s,ML,5.65,CW,[
    {t:"TE ≥ 0, and TE = 0 means no transfer. Asymmetric by design, and for linear-Gaussian signals it reduces exactly to Granger causality (Barnett et al. 2009). Definition: Schreiber (2000)."}
  ],13.5,0.9);
})();

// S8 — estimation KSG
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — estimation");
  bracket(s,ML,1.25,"Estimating TE without binning");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"Nearest neighbours, not bins");
  para(s,ML,y+0.45,lw,[{t:"TE is a conditional mutual information. The Kraskov–Stögbauer–Grassberger (KSG) estimator counts k nearest neighbours (k = 4) in the joint space — no histogram, no bin count to choose."}],14,2.0);
  subhead(s,rx,y,rw,"Why it suits our data");
  para(s,rx,y+0.45,rw,[{t:"Adaptive resolution on continuous signals; captures nonlinear dependence Gaussian methods miss. Reported in nats (natural log), not bits — the same quantity. Kraskov et al. (2004)."}],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"IN THE PIPELINE");
  para(s,ML,5.45,CW,[
    {t:"We run KSG (k = 4) with a non-uniform embedding (max_lag = 150 ≈ one slow-drift cycle), GPU-accelerated through IDTxl (Wollstadt et al. 2019)."}
  ],14.5,1.0);
})();

// S9 — embedding tau
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — embedding");
  bracket(s,ML,1.25,"Time delay τ and the embedding window");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"Delay vectors");
  para(s,ML,y+0.45,lw,[{t:"TE represents the recent past as a delay vector: Y_past = [y(t−τ), y(t−2τ), …, y(t−max_lag)]. τ sets the spacing between lags; max_lag sets how far back the test looks."}],14,2.0);
  subhead(s,rx,y,rw,"Our settings");
  para(s,rx,y+0.45,rw,[{t:"max_lag = 150 samples ≈ 30 s at 5 Hz — one platform slow-drift cycle. τ=1 keeps every lag and a greedy search picks the few that matter; τ=5 thins ~150 candidates to ~30."}],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"WHY BOTH MATTER");
  para(s,ML,5.45,CW,[
    {t:"Too short a window misses slow-drift; too fine a lag grid makes the greedy search explode. Together τ and max_lag decide which lags the causal test can even see."}
  ],14.5,1.0);
})();

// S10 — tau not a free knob
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — τ");
  bracket(s,ML,1.25,"τ is not a free knob");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"A tempting shortcut");
  para(s,ML,y+0.45,lw,[{t:"A common heuristic sets τ from the first minimum of a signal's self-mutual-information (the AIS-optimal delay). It preserves self-predictability (AIS) well."}],14,2.0);
  subhead(s,rx,y,rw,"…that breaks TE");
  para(s,rx,y+0.45,rw,[
    {t:"But a self-MI τ = 10 "},
    {t:"zeroed",b:true,c:RED},
    {t:" the strongest Wave→PtfmPitch edge. Directed couplings live at specific lags that self-prediction heuristics miss — optimal for AIS is not optimal for transfer."}
  ],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"TWO ROLES FOR τ");
  para(s,ML,5.45,CW,[
    {t:"τ is both a modelling choice (which lags the test sees) and a compute lever — the slow-drift platform channels only finish at τ = 5. We validate any τ > 1 against the τ = 1 baseline."}
  ],14.5,1.0);
})();

// S11 — significance
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — significance");
  bracket(s,ML,1.25,"Is the transfer real? Surrogate testing");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"The null hypothesis");
  para(s,ML,y+0.45,lw,[{t:"KSG TE is never exactly zero — finite-sample noise leaves a small positive value. So we ask: is the measured TE larger than chance, if there were no coupling?"}],14,2.0);
  subhead(s,rx,y,rw,"Circular-shift surrogates");
  para(s,rx,y+0.45,rw,[{t:"Rotate the source in time (n = 200), destroying its timing with the target while keeping its spectrum. p = fraction of surrogates beating the real TE; keep edges with p < 0.05."}],14,2.0);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"WHY CIRCULAR");
  para(s,ML,5.45,CW,[
    {t:"A circular shift keeps the source's own spectrum and amplitude intact and removes only the X→Y timing — a strict, honest null that avoids false positives."}
  ],14.5,1.0);
})();

// S12 — toy example
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — intuition");
  bracket(s,ML,1.25,"A toy example: who drives whom?");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.55);
  subhead(s,ML,y,lw,"Setup");
  s.addText("X[i] = 0.5·X[i−1] + noise\nY[i] = 0.5·X[i−1] + noise",{x:ML,y:y+0.42,w:lw,h:0.7,fontFace:F,fontSize:13.5,bold:true,color:BLUE,lineSpacingMultiple:1.2,margin:0});
  para(s,ML,y+1.25,lw,[{t:"X is autonomous; Y responds to X's past. Both look like random noise to the eye."}],13.5,0.9);
  subhead(s,rx,y,rw,"What TE recovers");
  s.addText("TE(X→Y) ≫ TE(Y→X)",{x:rx,y:y+0.42,w:rw,h:0.4,fontFace:F,fontSize:15,bold:true,color:RED,margin:0});
  para(s,rx,y+0.95,rw,[{t:"The asymmetry correctly flags X as the driver — something a symmetric correlation could never reveal."}],13.5,1.2);
  s.addShape(LINE,{x:ML,y:4.85,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,5.0,CW,"THE TAKEAWAY");
  para(s,ML,5.45,CW,[
    {t:"Direction emerges from the conditioning, not from the raw signals — exactly the test we run on wind, wave and structural channels."}
  ],14.5,1.0);
})();

// S13 — three ways
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — comparison");
  bracket(s,ML,1.25,"Three ways to measure dependence");
  const y=2.05, gap=0.5, cw=(CW-2*gap)/3;
  const cols=[
   ["Correlation","Strength of linear association. corr(X,Y) = corr(Y,X) — symmetric.","Directional ✗   Nonlinear ✗"],
   ["Granger causality","Does X's past improve a linear forecast of Y? Directed, but assumes a linear (VAR) model. Granger 1969 · Nobel 2003.","Directional ✓   Nonlinear ✗"],
   ["Transfer entropy","Does X's past reduce uncertainty about Y's future? Model-free, no distributional assumption. Schreiber 2000.","Directional ✓   Nonlinear ✓"]];
  cols.forEach((c,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vline(s,x-gap/2,y,2.3);
    subhead(s,x,y,cw,c[0]);
    para(s,x,y+0.42,cw,[{t:c[1]}],12.5,1.6);
    s.addText(c[2],{x,y:y+2.05,w:cw,h:0.3,fontFace:F,fontSize:11,bold:true,color:(i==2?NAVY:MUTED),margin:0});
  });
  s.addShape(LINE,{x:ML,y:4.7,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.85,CW,"KEY INSIGHT");
  para(s,ML,5.3,CW,[
    {t:"Transfer entropy is the only one that is both directed and nonlinear. For linear-Gaussian processes it reduces exactly to Granger causality (Barnett et al. 2009) — so it earns its keep where the dynamics are nonlinear or non-Gaussian."}
  ],14,1.2);
})();

// S14 — TE vs Granger
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — vs Granger");
  bracket(s,ML,1.25,"Transfer entropy and Granger causality");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.4);
  subhead(s,ML,y,lw,"Granger causality");
  para(s,ML,y+0.45,lw,[{t:"Linear autoregressive (VAR) model. Fast and well-understood, but assumes linearity and (often) Gaussian statistics — misses nonlinear coupling."}],14,1.8);
  subhead(s,rx,y,rw,"Transfer entropy");
  para(s,rx,y+0.45,rw,[{t:"Model-free, no distributional assumption, captures any nonlinearity. Costlier (k-NN estimation) and hungrier for data."}],14,1.8);
  s.addShape(LINE,{x:ML,y:4.7,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.85,CW,"WHEN THEY AGREE");
  para(s,ML,5.3,CW,[
    {t:"For linear-Gaussian processes the two are exactly equivalent (Barnett et al. 2009). TE earns its keep only where the dynamics are nonlinear or non-Gaussian — which is why we run both."}
  ],14,1.2);
})();

// S15 — when to use TE
(function(){
  const s=pres.addSlide(); chrome(s,"02","Transfer Entropy — when it pays off");
  bracket(s,ML,1.25,"When does transfer entropy pay off?");
  const y=2.05, gap=0.5, cw=(CW-2*gap)/3;
  const cols=[
   ["Linear / Gaussian","TE = Granger causality exactly (Barnett 2009). No added value — use the simpler method.",MUTED],
   ["Nonlinear / non-Gaussian","Captures directed structure linear methods cannot see. This is its sweet spot.",NAVY],
   ["Very high-dimensional","Many coupled modes degrade the k-NN estimate — curse of dimensionality, data starvation.",MUTED]];
  cols.forEach((c,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vline(s,x-gap/2,y,2.0);
    subhead(s,x,y,cw,c[0]);
    para(s,x,y+0.42,cw,[{t:c[1],b:(i==1)}],13,1.8);
  });
  s.addShape(LINE,{x:ML,y:4.6,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.75,CW,"KEY INSIGHT");
  para(s,ML,5.2,CW,[
    {t:"A floating turbine in irregular waves with a nonlinear ROSCO controller sits squarely in the middle regime — nonlinear and non-Gaussian — where transfer entropy adds the most."}
  ],14,1.2);
})();

// ============================================================================
// 03 METHOD & DATA
// ============================================================================
divider("03","Method & Data","A coupled wind–wave–structure–mooring system and the simulation campaign");

// S17 — system & data
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — system");
  bracket(s,ML,1.25,"IEA-15MW FOWT, simulated in OpenFAST");
  const fy=1.95, figW=5.5, ar=1.632;
  fig(s,ML,fy,figW,ar,FIG+"openfast.png","OpenFAST — coupled aero-hydro-servo-elastic modules");
  const rx=ML+figW+0.9, rw=RIGHT-(ML+figW+0.9); let ry=2.0;
  [["PLATFORM","IEA-15-240-RWT on the UMaine VolturnUS-S semisubmersible; coupled aero-hydro-servo-elastic OpenFAST model."],
   ["SIGNALS","3600 s simulation · drop 600 s transient · decimate to 5 Hz."],
   ["CHANNELS","2 sources (Wind1VelX, Wave1Elev) → 9 responses (RootMyc1, RootMxc1, TwrBsMyt, PtfmHeave/Surge/Pitch, FAIRTEN1/2/3)."]
  ].forEach(([h,b],i)=>{ if(i>0)s.addShape(LINE,{x:rx,y:ry-0.12,w:rw,h:0,line:{color:LINEG,width:1}}); subhead(s,rx,ry,rw,h); para(s,rx,ry+0.36,rw,[{t:b}],13,1.2); ry+=1.55; });
})();

// S18 — DLC matrix
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — design load cases");
  bracket(s,ML,1.25,"The simulation campaign");
  const figW=7.4, ar=1.852, ix=(W-figW)/2;
  fig(s,ix,1.95,figW,ar,FIG+"dlc-matrix.png","DLC-A / DLC-B / DLC-1.6 across the operating-point sweep (8/11/15/20 m/s, 6 seeds) — 54 cases");
})();

// S19 — env conditions
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — environment");
  bracket(s,ML,1.25,"Wind and wave inputs");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.4);
  subhead(s,ML,y,lw,"Wind — TurbSim");
  para(s,ML,y+0.45,lw,[{t:"IEC Kaimal (IECKAI) spectrum, Normal Turbulence Model, class B, power-law shear, referenced at hub height. URef = 8 / 11 / 15 / 20 m/s."}],14,1.9);
  subhead(s,rx,y,rw,"Waves — JONSWAP");
  para(s,rx,y+0.45,rw,[{t:"Irregular JONSWAP sea (SeaState). Hs/Tp scale with wind: (3.5 m, 9 s) → (8.0 m, 13 s). DLC-1.6 severe sea: Hs = 8.3 m, Tp = 12.95 s."}],14,1.9);
  s.addShape(LINE,{x:ML,y:4.7,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.85,CW,"ON THE RANDOM SEEDS");
  para(s,ML,5.3,CW,[
    {t:"DLC-A/1.6 reuse the wind seed for the wave generator; DLC-B draws an independent one. In OpenFAST, wind (TurbSim) and waves (HydroDyn) are generated separately, so the seed fixes reproducibility — not wind–wave correlation."}
  ],14,1.2);
})();

// S20 — preprocessing
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — preprocessing");
  bracket(s,ML,1.25,"Why 5 Hz is enough");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,2.5);
  subhead(s,ML,y,lw,"Environment · platform (low freq.)");
  para(s,ML,y+0.45,lw,[{t:"Slow-drift 0.01–0.1 Hz · wave 1st-order 0.05–0.3 Hz (JONSWAP peak 0.077) · eigenmodes pitch 0.0345 / heave 0.05 / surge 0.01 Hz · wind low-freq. eddies 0.01–1 Hz"}],12.5,2.0);
  subhead(s,rx,y,rw,"Rotor · structure (high freq.)");
  para(s,rx,y+0.45,rw,[{t:"1P / 3P rotor ~0.15 / 0.45 Hz · tower fore-aft 1st mode ~0.5 Hz · blade-flap mode ~0.6 Hz"}],12.5,2.0);
  s.addShape(LINE,{x:ML,y:4.8,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.95,CW,"BOTTOM LINE");
  para(s,ML,5.4,CW,[
    {t:"Down-sample 40 Hz → 5 Hz (×8). Nyquist = 2.5 Hz sits well above the highest band (~0.6 Hz), so every causal signal is preserved while the KSG sweep drops ~8×."}
  ],14,1.1);
})();

// S21 — method directed transfer
(function(){
  const s=pres.addSlide(); chrome(s,"03","Method & Data — pipeline");
  bracket(s,ML,1.25,"Directed transfer, with linear baselines");
  const steps=[
   ["1","KSG transfer entropy","Kraskov estimator (k = 4), non-uniform embedding, max_lag = 150 (30 s — one slow-drift cycle)."],
   ["2","Significance · effect size","Circular-shift surrogates ×200, p < 0.05 (max-stat). Normalized: te_frac = TE / (H(Y) − AIS(Y))."],
   ["3","Linear baselines, same pipeline","Gaussian / Granger (estimator swap) + magnitude-squared coherence γ²(f)."],
   ["4","Compute","OpenCL on 2× A100; GPU validated vs CPU (AIS RootMyc1 1.50 vs 1.49)."]];
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
  const s=pres.addSlide(); chrome(s,"03","Method & Data — what TE measures");
  bracket(s,ML,1.25,"What transfer entropy measures");
  const figW=6.4, ar=2.043, ix=(W-figW)/2;
  fig(s,ix,1.9,figW,ar,FIG+"concept.png");
  s.addShape(LINE,{x:ML,y:5.35,w:CW,h:0,line:{color:LINEG,width:1}});
  para(s,ML,5.55,CW,[
    {t:"In one line — ",b:true,c:NAVY},
    {t:"if the source's past sharpens the prediction of the target beyond the target's own history, information flows source → target. Directed (X→Y ≠ Y→X) and nonlinear — what correlation and coherence cannot see."}
  ],14,1.2);
})();

// ============================================================================
// 04 RESULTS & CONCLUSION
// ============================================================================
divider("04","Results & Conclusion","A wave-dominated causal structure, and the wind paradox");

// S24 — wave-dominated network
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — causal network");
  bracket(s,ML,1.25,"A wave-dominated causal graph");
  const figW=6.0, ar=1.517;
  fig(s,ML,1.95,figW,ar,FIG+"te-network.png","TE causal network · bivariate KSG, weight = mean te_frac across all 54 cases");
  const rx=ML+figW+0.75, rw=RIGHT-(ML+figW+0.75); let ry=2.1;
  subhead(s,rx,ry,rw,"READING"); ry+=0.42;
  para(s,rx,ry,rw,[{t:"Wave elevation drives every significant response (pitch · heave · surge · tower base · mooring). ",b:true},{t:"Wind shows no significant directed transfer to the structure.",}],13,1.5); ry+=1.55;
  s.addShape(LINE,{x:rx,y:ry,w:rw,h:0,line:{color:LINEG,width:1}}); ry+=0.12;
  s.addText("7 / 7",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:34,bold:true,color:NAVY,valign:"middle",margin:0}); ry+=0.62;
  s.addText("significant edges — every one from wave",{x:rx,y:ry,w:rw,h:0.3,fontFace:F,fontSize:11,color:MUTED,margin:0}); ry+=0.5;
  s.addText("0",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:34,bold:true,color:RED,valign:"middle",margin:0}); ry+=0.62;
  s.addText("significant wind → structure edges",{x:rx,y:ry,w:rw,h:0.3,fontFace:F,fontSize:11,color:MUTED,margin:0});
})();

// S25 — significant edges bars
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — significant edges");
  bracket(s,ML,1.25,"The significant edges — 7 of 18");
  const figW=6.7, ar=2.165;
  fig(s,ML,2.2,figW,ar,FIG+"conf-windwave-bars.png","Significant directed transfer (nats) — wave only, mean across 54 cases");
  const rx=ML+figW+0.7, rw=RIGHT-(ML+figW+0.7); let ry=2.3;
  subhead(s,rx,ry,rw,"WAVE DRIVES THE STRUCTURE"); ry+=0.42;
  para(s,rx,ry,rw,[
    {t:"The five strongest edges (pitch, heave, the forward fairleads and surge) cluster at 0.11–0.12 nats. "},
    {t:"No wind → structure edge is significant anywhere in the campaign.",b:true}
  ],13,2.0); ry+=2.1;
  s.addShape(LINE,{x:rx,y:ry,w:rw,h:0,line:{color:LINEG,width:1}}); ry+=0.12;
  s.addText("0 / 18",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:30,bold:true,color:NAVY,valign:"middle",margin:0}); ry+=0.6;
  s.addText("significant wind edges — wave drives all seven",{x:rx,y:ry,w:rw,h:0.4,fontFace:F,fontSize:11,color:MUTED,margin:0});
})();

// S26 — triangulation
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — triangulation");
  bracket(s,ML,1.25,"TE vs. coherence vs. Granger");
  const y=2.05, gap=0.5, cw=(CW-2*gap)/3;
  const cols=[
   ["Coherence γ²(f)","Undirected spectral ceiling. Shared power, no direction.",MUTED],
   ["Gaussian / Granger","Directional but linear. Over-detects under correlated wind–wave.",MUTED],
   ["Transfer entropy","Directed AND nonlinear. Catches couplings the others miss.",NAVY]];
  cols.forEach((c,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vline(s,x-gap/2,y,2.0);
    subhead(s,x,y,cw,c[0]);
    para(s,x,y+0.42,cw,[{t:c[1],b:(i==2)}],13,1.8);
  });
  s.addShape(LINE,{x:ML,y:4.6,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.75,CW,"READING THE TRIANGLE");
  para(s,ML,5.2,CW,[
    {t:"Where TE is significant but the linear baselines are not = nonlinear directed coupling unique to TE (e.g. the wave 2nd-order difference-frequency forcing of pitch). Where all three agree, the embedding is validated."}
  ],14,1.2);
})();

// S27 — wind paradox
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — the wind paradox");
  bracket(s,ML,1.25,"The wind paradox");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,1.6);
  subhead(s,ML,y,lw,"THE PUZZLE");
  para(s,ML,y+0.42,lw,[{t:"Wind → structure ≈ 0 across 8–20 m/s",b:true},{t:" — yet wind is what drives the turbine. Counter-intuitive, and it holds at every operating point."}],14,1.4);
  subhead(s,rx,y,rw,"NOT AN ARTIFACT");
  para(s,rx,y+0.42,rw,[{t:"Wind decorrelates at ~11.6 s — well inside the 30 s embedding window. The wind signal is sampled; it simply isn't transferring information to the structure."}],14,1.6);
  s.addShape(LINE,{x:ML,y:4.4,w:CW,h:0,line:{color:LINEG,width:1}});
  subhead(s,ML,4.55,CW,"HYPOTHESIS — A CONTROLLER “FIREWALL”");
  para(s,ML,5.0,CW,[
    {t:"The blade-pitch controller (ROSCO) regulates rotor thrust so tightly that wind fluctuations are rejected before they reach the platform. The controller acts as a causal firewall — wind energizes the rotor, not the structure."}
  ],14,1.4);
})();

// S28 — firewall ablation
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — firewall ablation");
  bracket(s,ML,1.25,"Testing the firewall — controller-off ablation");
  const figW=7.0, ar=2.323;
  fig(s,ML,2.15,figW,ar,FIG+"conf-ablation.png","Re-ran the same case with blade-pitch control frozen (open-loop)");
  const rx=ML+figW+0.7, rw=RIGHT-(ML+figW+0.7); let ry=2.3;
  subhead(s,rx,ry,rw,"VERDICT"); ry+=0.42;
  para(s,rx,ry,rw,[{t:"Suggestive but inconclusive. ",b:true,c:RED},{t:"The wind→heave edge appears, but open-loop overspeed inflates AIS and masks wind in bivariate TE."}],13,2.0); ry+=2.0;
  s.addShape(LINE,{x:rx,y:ry,w:rw,h:0,line:{color:LINEG,width:1}}); ry+=0.16;
  s.addText("NEXT",{x:rx,y:ry,w:rw,h:0.5,fontFace:F,fontSize:24,bold:true,color:NAVY,valign:"middle",margin:0}); ry+=0.55;
  s.addText("conditional TE  TE(wind→Y | wave)  +  a non-overspeeding ablation",{x:rx,y:ry,w:rw,h:0.6,fontFace:F,fontSize:11,color:MUTED,margin:0});
})();

// S29 — methods lessons
(function(){
  const s=pres.addSlide(); chrome(s,"04","Results — methods lessons");
  bracket(s,ML,1.25,"What made it work — and what nearly broke it");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,3.0);
  subhead(s,ML,y,lw,"GPU MADE THE SWEEP TRACTABLE");
  s.addText("~35 h",{x:ML,y:y+0.35,w:lw,h:0.85,fontFace:F,fontSize:44,bold:true,color:NAVY,valign:"middle",margin:0});
  para(s,ML,y+1.3,lw,[{t:"per case on a single A100-batched run. The OpenCL KSG estimator (validated vs CPU) is what brings the full DLC sweep into reach."}],13.5,1.2);
  subhead(s,rx,y,rw,"CAUTION — EMBEDDING DELAY MATTERS");
  s.addText("0.12 → 0",{x:rx,y:y+0.35,w:rw,h:0.85,fontFace:F,fontSize:40,bold:true,color:RED,valign:"middle",margin:0});
  para(s,rx,y+1.3,rw,[{t:"A data-driven τ from self-MI preserved AIS but collapsed the TE edges (τ = 10 zeroed the strongest Wave→PtfmPitch). Directed couplings live at specific lags — AIS heuristics don't transfer to TE."}],13.5,1.5);
})();

// S30 — hybrid TE + Sobol
(function(){
  const s=pres.addSlide(); chrome(s,"04","Conclusion — TE + Sobol");
  bracket(s,ML,1.25,"Closing the loop: TE + Sobol → data-driven weights");
  const cw=5.5, car=1.570, ch=cw/car, cy=1.95;
  fig(s,ML,cy,cw,car,FIG+"combined.png","COMBINED GRAPH — TE + Sobol");
  const rx=ML+cw+0.9, rw=RIGHT-(ML+cw+0.9);
  fig(s,rx,cy,rw-0.3,2.209,FIG+"sobol.png","Sobol Sₜ — design sensitivity");
  para(s,rx,cy+ (rw-0.3)/2.209 +0.7,rw,[
    {t:"Mooring length (L_u) and stiffness (EA)",b:true},{t:" dominate fairlead tensions and several motions. "},
    {t:"Column geometry (D_OCol, R_MO)",b:true},{t:" drives surge, sway and heave."}
  ],12,1.0);
  s.addShape(LINE,{x:ML,y:6.05,w:CW,h:0,line:{color:LINEG,width:1}});
  para(s,ML,6.2,CW,[
    {t:"Two directed importance maps in one graph — "},
    {t:"TE for environment-driven dynamics, Sobol for design sensitivity",b:true,c:NAVY},
    {t:" — a data-driven basis for the optimization weights (proposed next step)."}
  ],13,0.8);
})();

// S31 — limitations & future
(function(){
  const s=pres.addSlide(); chrome(s,"04","Conclusion — limitations & future");
  bracket(s,ML,1.25,"Where this goes next");
  const y=2.05, lw=5.5, rx=ML+6.2, rw=CW-6.2;
  vline(s,ML+5.85,y,3.4);
  subhead(s,ML,y,lw,"LIMITATIONS");
  bullets(s,ML,y+0.45,lw,[
    "Single platform (UMaine VolturnUS-S), simulation-only — no field validation.",
    "max_lag = 150 (30 s) may be short for PtfmSurge (decorrelates ~24.6 s).",
    "Firewall mechanism (controller) is preliminary and confounded — the wind decoupling is shown, its cause is not."
  ],13);
  subhead(s,rx,y,rw,"NEXT STEPS");
  bullets(s,rx,y+0.45,rw,[
    "Conditional TE — TE(wind→Y | wave) — to test the firewall beyond the bivariate estimate.",
    "A non-overspeeding controller-off ablation to settle the mechanism.",
    "Hybrid graph: add Sobol design-parameter sensitivity.",
    [{t:"Feed the ranked TE driver→load pathways",b:true},{t:" into structural/fatigue load weighting for design optimization."}]
  ],13);
})();

// S32 — conclusion (navy)
(function(){
  const s=pres.addSlide(); PAGE+=1;
  s.background={color:NAVY};
  s.addText("Conclusion",{x:ML+0.2,y:0.7,w:8,h:0.5,fontFace:F,fontSize:16,bold:true,color:"9FB0CF",margin:0});
  s.addText([
    {text:"Transfer entropy reveals a ",options:{color:WHITE}},
    {text:"wave-dominated causal structure",options:{color:"7FB0FF",bold:true}},
    {text:" in FOWT response that linear methods only partially capture.",options:{color:WHITE}}
  ],{x:ML+0.2,y:1.45,w:12,h:1.6,fontFace:F,fontSize:28,bold:true,lineSpacingMultiple:1.15,valign:"top",margin:0});
  s.addShape(LINE,{x:ML+0.2,y:3.4,w:CW-0.4,h:0,line:{color:"3A5488",width:1}});
  const items=[
    "Wave drives platform pitch, heave, surge, tower base and mooring; no significant wind → structure edge across the 54-case campaign.",
    "The wind decoupling is robust and non-obvious — holding across 8–20 m/s — yet whether the controller causes it is an open, testable question.",
    "Conditional TE and a non-overspeeding ablation are the path to settle it.",
    "Next: pair this ranking with Sobol design sensitivities to set data-driven weights for design optimization."
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
