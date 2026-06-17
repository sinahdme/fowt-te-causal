// ============================================================================
// Directional Causality — Editorial / Swiss-grid redesign (v2), all 30 slides
// ============================================================================
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.defineLayout({ name: "W", width: 13.333, height: 7.5 });
pres.layout = "W";
pres.author = "Sina Hadadi";
pres.title = "Directional Causality Between Load and Response Variables of a FOWT";

// ---- design system ---------------------------------------------------------
const PAPER="FAF9F6", INK="17181C", MUTED="6E6B64", HAIR="DAD7CF",
      FAINT="CEC9BE", TINT="F1EFE9", ACCENT="BE3A34", INK2="3A3A36";
const F_DISP="Segoe UI Semibold", F_LIGHT="Segoe UI Light",
      F_BODY="Segoe UI", F_SB="Segoe UI Semibold";
const W=13.333, H=7.5, ML=0.92, MR=0.92, CW=W-ML-MR, RIGHT=W-MR;
const A="figs/v2_assets/";

let SN=1; const TOTAL=31;
function autonum(){ SN+=1; return String(SN).padStart(2,"0"); }
function chromeAuto(s,kicker,footer){ const n=autonum(); chrome(s,kicker,n,footer,n+" / "+TOTAL); }

function hair(s,x,y,w){ s.addShape(pres.shapes.LINE,{x,y,w,h:0,line:{color:HAIR,width:1}}); }
function vhair(s,x,y,h){ s.addShape(pres.shapes.LINE,{x,y,w:0,h,line:{color:HAIR,width:1}}); }
function tick(s,x,y){ s.addShape(pres.shapes.RECTANGLE,{x,y,w:0.11,h:0.11,fill:{color:ACCENT},line:{type:"none"}}); }

function chrome(s,kicker,num,footer,pager){
  s.background={color:PAPER};
  tick(s,ML,0.585);
  s.addText(kicker,{x:ML+0.24,y:0.46,w:9,h:0.34,fontFace:F_SB,fontSize:10.5,color:ACCENT,charSpacing:3,valign:"middle",margin:0});
  if(num) s.addText(num,{x:RIGHT-2.2,y:0.14,w:2.2,h:0.95,fontFace:F_LIGHT,fontSize:46,color:FAINT,align:"right",valign:"middle",margin:0});
  hair(s,ML,1.0,CW);
  hair(s,ML,6.98,CW);
  if(footer) s.addText(footer,{x:ML,y:7.04,w:9.6,h:0.3,fontFace:F_BODY,fontSize:9,color:MUTED,valign:"middle",margin:0});
  if(pager) s.addText(pager,{x:RIGHT-2.4,y:7.04,w:2.4,h:0.3,align:"right",fontFace:F_BODY,fontSize:9,color:MUTED,valign:"middle",margin:0});
}
function H1(s,txt,size){ s.addText(txt,{x:ML,y:1.16,w:11.5,h:0.72,fontFace:F_DISP,fontSize:size||29,color:INK,valign:"middle",margin:0}); }
function subHead(s,x,y,w,txt){ s.addText(txt,{x,y,w,h:0.34,fontFace:F_SB,fontSize:15.5,color:INK,margin:0}); }
function body(s,x,y,w,runs,size){ s.addText(runs,{x,y,w,h:1.8,fontFace:F_BODY,fontSize:size||13.5,color:INK,lineSpacingMultiple:1.2,valign:"top",margin:0}); }
function kickerLine(s,x,y,w,txt){ s.addText(txt,{x,y,w,h:0.3,fontFace:F_SB,fontSize:10.5,color:ACCENT,charSpacing:2.2,margin:0}); }

function insight(s,y,kick,runs){
  hair(s,ML,y,CW);
  tick(s,ML,y+0.2);
  s.addText(kick,{x:ML+0.24,y:y+0.11,w:9,h:0.3,fontFace:F_SB,fontSize:10.5,color:ACCENT,charSpacing:2.2,valign:"middle",margin:0});
  s.addText(runs,{x:ML,y:y+0.52,w:CW,h:0.9,fontFace:F_BODY,fontSize:14.5,color:INK,lineSpacingMultiple:1.18,valign:"top",margin:0});
}

// two-panel + insight ---------------------------------------------------------
function twoPanel(c){
  const s=pres.addSlide(); chromeAuto(s,c.kicker,c.footer); H1(s,c.title);
  const y=2.45, lw=5.15, rx=ML+6.0, rw=5.3;
  vhair(s,ML+5.55,y,2.7);
  subHead(s,ML,y,lw,c.L.h); body(s,ML,y+0.45,lw,c.L.body,c.bodySize);
  subHead(s,rx,y,rw,c.R.h); body(s,rx,y+0.45,rw,c.R.body,c.bodySize);
  insight(s,5.55,c.key.kicker,c.key.runs);
  return s;
}
// three-column + insight ------------------------------------------------------
function threeCol(c){
  const s=pres.addSlide(); chromeAuto(s,c.kicker,c.footer); H1(s,c.title);
  const y=2.45, gap=0.5, cw=(CW-2*gap)/3;
  c.cols.forEach((col,i)=>{
    const x=ML+i*(cw+gap);
    if(i>0) vhair(s,x-gap/2,y,2.5);
    subHead(s,x,y,cw,col.h); body(s,x,y+0.42,cw,col.body,12.5);
  });
  insight(s,5.45,c.key.kicker,c.key.runs);
  return s;
}
// figure plate + right rail ---------------------------------------------------
function figureRail(c){
  const s=pres.addSlide(); chromeAuto(s,c.kicker,c.footer); H1(s,c.title);
  const figW=c.figW||6.0, figH=figW/c.ar, matX=ML, matY=c.matY||2.18;
  s.addShape(pres.shapes.RECTANGLE,{x:matX,y:matY,w:figW+0.3,h:figH+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:c.img,x:matX+0.15,y:matY+0.15,w:figW,h:figH});
  if(c.caption) s.addText(c.caption,{x:matX,y:matY+figH+0.4,w:figW+0.3,h:0.3,fontFace:F_BODY,fontSize:9.5,italic:true,color:MUTED,margin:0});
  const rx=matX+figW+0.7, rw=RIGHT-(matX+figW+0.7);
  let ry=matY+0.05;
  if(c.railHead){ kickerLine(s,rx,ry,rw,c.railHead); ry+=0.34; }
  s.addText(c.railBody,{x:rx,y:ry,w:rw,h:1.6,fontFace:F_BODY,fontSize:13,color:INK,lineSpacingMultiple:1.2,valign:"top",margin:0});
  ry+=c.railBodyH||1.55;
  (c.stats||[]).forEach(st=>{
    hair(s,rx,ry,rw); ry+=0.16;
    s.addText(st.big,{x:rx,y:ry,w:rw,h:0.62,fontFace:F_LIGHT,fontSize:38,color:st.color||ACCENT,valign:"middle",margin:0});
    ry+=0.64;
    s.addText(st.label,{x:rx,y:ry,w:rw,h:0.3,fontFace:F_BODY,fontSize:10.5,color:MUTED,margin:0}); ry+=0.42;
  });
  return s;
}
// dashed bullet list ----------------------------------------------------------
function dashList(s,x,y,w,items,size){
  const arr=[];
  items.forEach((it,i)=>{
    arr.push({text:"—  ",options:{color:ACCENT,fontFace:F_SB}});
    if(it.lead) arr.push({text:it.lead+"  ",options:{color:INK,fontFace:F_SB}});
    arr.push({text:it.text,options:{color:INK,breakLine:true}});
  });
  s.addText(arr,{x,y,w,h:3.0,fontFace:F_BODY,fontSize:size||13.5,color:INK,lineSpacingMultiple:1.15,paraSpaceAfter:9,valign:"top",margin:0});
}

// ============================================================================
// SLIDE 1 — TITLE
// ============================================================================
(function(){
  const s=pres.addSlide(); s.background={color:PAPER};
  tick(s,ML,0.92);
  s.addText("TRANSFER ENTROPY   —   FLOATING OFFSHORE WIND",{x:ML+0.24,y:0.8,w:11,h:0.34,fontFace:F_SB,fontSize:11.5,color:ACCENT,charSpacing:3,valign:"middle",margin:0});
  s.addText("Directional Causality",{x:ML,y:2.0,w:11.5,h:1.05,fontFace:F_DISP,fontSize:52,color:INK,valign:"middle",margin:0});
  s.addShape(pres.shapes.RECTANGLE,{x:ML,y:3.22,w:1.35,h:0.045,fill:{color:ACCENT},line:{type:"none"}});
  s.addText([
    {text:"between Load and Response Variables of a Floating Offshore Wind Turbine,\n",options:{color:INK2,breakLine:true}},
    {text:"via ",options:{color:INK2}},
    {text:"Time-Domain Transfer Entropy",options:{color:ACCENT}}
  ],{x:ML,y:3.5,w:11.0,h:1.1,fontFace:F_LIGHT,fontSize:21,lineSpacingMultiple:1.12,valign:"top",margin:0});
  hair(s,ML,5.95,CW);
  s.addText([
    {text:"Sina Hadadi, Ph.D.",options:{fontFace:F_SB,fontSize:14,color:INK,breakLine:true}},
    {text:"Research Assistant · Laboratory of Autonomous Maritime Systems (LAMS)",options:{fontFace:F_BODY,fontSize:10.5,color:MUTED,breakLine:true}},
    {text:"Dept. of Naval Architecture & Ocean Engineering · Kunsan National University",options:{fontFace:F_BODY,fontSize:10.5,color:MUTED,breakLine:true}},
    {text:"Supervisor — Prof. Jackyou Noh",options:{fontFace:F_BODY,fontSize:10.5,color:MUTED}}
  ],{x:ML,y:6.15,w:8.5,h:1.0,lineSpacingMultiple:1.15,valign:"top",margin:0});
  s.addText([
    {text:"KWEA 2026",options:{fontFace:F_SB,fontSize:14,color:INK,breakLine:true,align:"right"}},
    {text:"2026.06.22",options:{fontFace:F_BODY,fontSize:10.5,color:MUTED,align:"right"}}
  ],{x:RIGHT-4,y:6.15,w:4,h:0.7,align:"right",lineSpacingMultiple:1.2,valign:"top",margin:0});
})();

// ============================================================================
// SLIDE 2 — RL CONTEXT (where the reward lives)
// ============================================================================
(function(){
  const s=pres.addSlide(); chromeAuto(s,"MOTIVATION  ·  RL CONTEXT","RL-based FOWT substructure optimization · Jeon, Lee & Noh (2025) — LAMS / KSNU");
  H1(s,"Design optimization as reinforcement learning");
  const by=2.92, bw=3.5, bh=1.95, agX=ML, enX=RIGHT-bw, BORD="8A877F";
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:agX,y:by,w:bw,h:bh,fill:{color:"FFFFFF"},line:{color:BORD,width:1.25},rectRadius:0.07});
  s.addText("AGENT",{x:agX+0.3,y:by+0.2,w:bw-0.6,h:0.3,fontFace:F_SB,fontSize:11,color:ACCENT,charSpacing:2.5,margin:0});
  s.addText([
    {text:"Actor",options:{fontFace:F_SB,color:INK}},{text:"  —  policy π(a | s)",options:{color:INK,breakLine:true}},
    {text:"Critic",options:{fontFace:F_SB,color:INK}},{text:"  —  value V(s)",options:{color:INK,breakLine:true}},
    {text:"actor–critic, TD-error updates",options:{color:MUTED,fontSize:11}}
  ],{x:agX+0.3,y:by+0.62,w:bw-0.6,h:1.2,fontFace:F_BODY,fontSize:13,lineSpacingMultiple:1.28,valign:"top",margin:0});
  s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:enX,y:by,w:bw,h:bh,fill:{color:"FFFFFF"},line:{color:BORD,width:1.25},rectRadius:0.07});
  s.addText("ENVIRONMENT",{x:enX+0.3,y:by+0.2,w:bw-0.6,h:0.3,fontFace:F_SB,fontSize:11,color:ACCENT,charSpacing:2.5,margin:0});
  s.addText([
    {text:"RAFT coupled simulator",options:{fontFace:F_SB,color:INK,breakLine:true}},
    {text:"aero · hydro · servo · moor",options:{color:MUTED,breakLine:true}},
    {text:"evaluates each design",options:{color:MUTED,fontSize:11}}
  ],{x:enX+0.3,y:by+0.62,w:bw-0.6,h:1.2,fontFace:F_BODY,fontSize:13,lineSpacingMultiple:1.28,valign:"top",margin:0});
  const chL=agX+bw, chR=enX, chW=chR-chL;
  s.addText([{text:"action  ",options:{color:INK}},{text:"aₜ",options:{fontFace:F_SB,color:INK}}],{x:chL,y:by+0.12,w:chW,h:0.3,align:"center",fontFace:F_BODY,fontSize:12.5,margin:0});
  s.addShape(pres.shapes.LINE,{x:chL+0.12,y:by+0.55,w:chW-0.24,h:0,line:{color:INK,width:1.5,endArrowType:"triangle"}});
  s.addText("7 design variables  (D_MCol, D_OCol, R_MO, …)",{x:chL,y:by+0.66,w:chW,h:0.3,align:"center",fontFace:F_BODY,fontSize:10,italic:true,color:MUTED,margin:0});
  s.addShape(pres.shapes.LINE,{x:chL+0.12,y:by+bh-0.6,w:chW-0.24,h:0,line:{color:ACCENT,width:2.25,beginArrowType:"triangle"}});
  s.addText([{text:"state  sₜ₊₁          ",options:{color:MUTED}},{text:"reward  rₜ₊₁",options:{fontFace:F_SB,color:ACCENT}}],{x:chL,y:by+bh-0.46,w:chW,h:0.3,align:"center",fontFace:F_BODY,fontSize:12.5,margin:0});
  insight(s,5.35,"THE REWARD  ·  rₜ₊₁",[
    {text:"The reward is the one signal the agent maximizes — it ",options:{color:INK}},
    {text:"encodes the design objectives",options:{fontFace:F_SB,color:ACCENT}},
    {text:" (mass ↓, resonance avoidance, peak-response ↓). Its weights decide which objective wins — exactly what we examine next.",options:{color:INK}}
  ]);
})();

// ============================================================================
// SLIDE 3 — MOTIVATION (weights)
// ============================================================================
(function(){
  const s=pres.addSlide(); chromeAuto(s,"MOTIVATION  ·  THE PROBLEM","Variable-importance weighting for FOWT design optimization");
  H1(s,"Why these weights? From hand-set to data-driven");
  hair(s,ML,2.34,CW);
  const Xw=(n)=>([{text:"X",options:{color:ACCENT,fontFace:F_SB}},{text:n,options:{color:ACCENT,fontFace:F_SB,fontSize:14,subscript:true}}]);
  s.addText([
    {text:"Reward  =  ",options:{color:INK}},
    ...Xw("1"),{text:" · ΔMass   +   ",options:{color:INK}},
    ...Xw("2"),{text:" · ΔResonance   +   ",options:{color:INK}},
    ...Xw("3"),{text:" · ΔPitch",options:{color:INK}},
    {text:"peak",options:{color:INK,fontSize:13,subscript:true}},{text:"   +   ",options:{color:INK}},
    ...Xw("4"),{text:" · ΔHeave",options:{color:INK}},
    {text:"peak",options:{color:INK,fontSize:13,subscript:true}}
  ],{x:ML,y:2.45,w:CW,h:0.72,fontFace:F_LIGHT,fontSize:23,align:"center",valign:"middle",margin:0});
  hair(s,ML,3.2,CW);
  s.addText("The weights X₁…X₄ are set by hand in our RL substructure design optimization (cost, power, constraint priority) — not from data.   LAMS, KSNU.",{x:ML,y:3.3,w:CW,h:0.34,fontFace:F_BODY,fontSize:11,italic:true,color:MUTED,align:"center",valign:"middle",margin:0});
  const colY=4.05; vhair(s,ML+5.55,colY,2.5);
  kickerLine(s,ML,colY,5.2,"THE GAP");
  s.addText([
    {text:"Weights rank variable importance ",options:{color:INK}},
    {text:"by hand",options:{color:INK,fontFace:F_SB}},
    {text:". No objective basis for which responses matter most — or how strongly each is driven by the environment.",options:{color:INK}}
  ],{x:ML,y:colY+0.42,w:5.2,h:1.8,fontFace:F_BODY,fontSize:14.5,lineSpacingMultiple:1.22,valign:"top",margin:0});
  kickerLine(s,ML+6.0,colY,5.3,"A DATA-DRIVEN BASIS");
  s.addText([
    {text:"Transfer entropy",options:{color:INK,fontFace:F_SB}},{text:"  —  ",options:{color:ACCENT}},{text:"which environmental drivers causally drive each response.",options:{color:INK,breakLine:true}},
    {text:"Sobol sensitivity",options:{color:INK,fontFace:F_SB}},{text:"  —  ",options:{color:ACCENT}},{text:"which design parameters move each response.",options:{color:INK,breakLine:true}},
    {text:"Together",options:{color:INK,fontFace:F_SB}},{text:"  —  ",options:{color:ACCENT}},{text:"a data-driven basis for the weights.",options:{color:INK}}
  ],{x:ML+6.0,y:colY+0.42,w:5.3,h:1.9,fontFace:F_BODY,fontSize:14.5,lineSpacingMultiple:1.18,paraSpaceAfter:10,valign:"top",margin:0});
})();

const FP="TE causal discovery on a FOWT (IEA-15MW on UMaine VolturnUS-S) · preliminary, 11 m/s";
const FC="TE causal discovery on a FOWT (IEA-15MW on UMaine VolturnUS-S) · full campaign: DLC-A / DLC-B / DLC-1.6";
const FD="TE causal discovery on a FOWT (IEA-15MW on UMaine VolturnUS-S) · DLC-1.6 (11 m/s, severe sea)";

// SLIDE 3 — From association to directed causation
twoPanel({kicker:"MOTIVATION",num:"03",title:"From association to directed causation",footer:FP,pager:"03 / 30",
  L:{h:"Correlation / coherence",body:[{text:"Symmetric and undirected — quantifies association. γ²(f) tells you wind and a load share power at a frequency, ",options:{color:INK}},{text:"not which drives which.",options:{color:INK,fontFace:F_SB}}]},
  R:{h:"Transfer entropy",body:[{text:"Directed, nonlinear, model-free. Measures information that a source's past adds about a target's future, ",options:{color:INK}},{text:"beyond the target's own past.",options:{color:INK,fontFace:F_SB}}]},
  key:{kicker:"THE QUESTION",runs:[{text:"Which environmental driver — wind or wave — causally drives each structural response, and which coupling pathways do linear methods miss?",options:{color:INK}}]}});

// SLIDE 4 — Correlation is not causation
twoPanel({kicker:"WHY CAUSALITY",num:"04",title:"Correlation is not causation",footer:FP,pager:"04 / 30",
  L:{h:"The trap",body:"Ice-cream sales and drownings rise together — both driven by summer heat. Strong correlation, zero causation. corr(A,B) = corr(B,A) carries no arrow."},
  R:{h:"What direction needs",body:"A real cause must precede its effect in time, and the link must survive once the target's own history and shared drivers are accounted for."},
  key:{kicker:"IN A COUPLED SYSTEM",runs:[{text:"In turbulence or a floating turbine, dozens of channels move together. Eyeballing what drives what is hopeless — we need a directed, model-free measure.",options:{color:INK}}]}});

// SLIDE 5 — Information theory
twoPanel({kicker:"INFORMATION THEORY",num:"05",title:"The building blocks: entropy and information",footer:FP,pager:"05 / 30",
  L:{h:"Shannon entropy",body:[{text:"H(X) = −Σ p(x) log p(x)\n",options:{color:ACCENT,fontFace:F_SB,breakLine:true}},{text:"Average uncertainty — the “surprise” in a signal. Zero when the outcome is certain, maximal when all outcomes are equally likely.",options:{color:INK}}]},
  R:{h:"Mutual information",body:[{text:"I(X;Y) = H(X) + H(Y) − H(X,Y)\n",options:{color:ACCENT,fontFace:F_SB,breakLine:true}},{text:"The information shared between X and Y — how much knowing one reduces uncertainty about the other.",options:{color:INK}}]},
  key:{kicker:"THE CATCH",runs:[{text:"Mutual information is symmetric: I(X;Y) = I(Y;X). It cannot say which variable drives which — the gap that transfer entropy is built to close.",options:{color:INK}}]}});

// SLIDE 6 — TE defined
twoPanel({kicker:"TRANSFER ENTROPY",num:"06",title:"Transfer entropy, defined",footer:FP,pager:"06 / 30",
  L:{h:"The definition",body:[{text:"TE(X→Y) = H(Y_f | Y_p) − H(Y_f | Y_p, X_p)\n",options:{color:ACCENT,fontFace:F_SB,breakLine:true}},{text:"Y_f = target's future · Y_p = target's past · X_p = source's past. How much the source's past sharpens the prediction of the target's next step, beyond its own history.",options:{color:INK}}]},
  R:{h:"The conditioning trick",body:"Conditioning on Y's own past removes self-prediction and shared history — only genuinely new information from X survives. That is what makes TE directed: TE(X→Y) ≠ TE(Y→X)."},
  key:{kicker:"KEY PROPERTIES",runs:[{text:"TE ≥ 0 always, and TE = 0 means no transfer. Asymmetric by design — and for linear-Gaussian signals reduces exactly to Granger causality (Barnett et al. 2009). Definition: Schreiber (2000).",options:{color:INK}}]}});

// SLIDE 7 — Estimation
twoPanel({kicker:"ESTIMATION",num:"07",title:"Estimating TE without binning",footer:FP,pager:"07 / 30",
  L:{h:"Nearest neighbours, not bins",body:"TE is a conditional mutual information. The Kraskov–Stögbauer–Grassberger (KSG) estimator counts k nearest neighbours (k = 4) in the joint space — no histogram, and no bin count to choose."},
  R:{h:"Why it suits our data",body:"Adaptive resolution on continuous signals; captures nonlinear dependence that Gaussian methods miss. Reported in nats (natural log), not bits — the same quantity. Kraskov et al. (2004)."},
  key:{kicker:"IN THE PIPELINE",runs:[{text:"We run KSG with k = 4 and a non-uniform embedding (max_lag = 150 ≈ one slow-drift cycle), GPU-accelerated through IDTxl (Wollstadt et al. 2019).",options:{color:INK}}]}});

// SLIDE 8 — Embedding
twoPanel({kicker:"EMBEDDING",num:"08",title:"Time delay τ and the embedding window",footer:FP,pager:"08 / 30",
  L:{h:"Delay vectors",body:"TE represents the recent past as a delay vector: Y_past = [ y(t−τ), y(t−2τ), …, y(t−max_lag) ]. The delay τ sets the spacing between lags; max_lag sets how far back the test looks."},
  R:{h:"Our settings",body:"max_lag = 150 samples ≈ 30 s at 5 Hz — one full platform slow-drift cycle. τ = 1 keeps every lag and a greedy search picks the few that matter; τ = 5 thins ~150 candidates to ~30."},
  key:{kicker:"WHY BOTH MATTER",runs:[{text:"Too short a window misses the slow-drift dynamics; too fine a lag grid makes the greedy search explode. Together τ and max_lag decide which lags the causal test can even see.",options:{color:INK}}]}});

// SLIDE 9 — tau not a free knob
twoPanel({kicker:"EMBEDDING",num:"09",title:"τ is not a free knob",footer:FP,pager:"09 / 30",
  L:{h:"A tempting shortcut",body:"A common heuristic sets τ from the first minimum of a signal's self-mutual-information (the AIS-optimal delay). It preserves self-predictability (AIS) well."},
  R:{h:"…that breaks TE",body:[{text:"But a self-MI τ = 10 ",options:{color:INK}},{text:"zeroed",options:{color:ACCENT,fontFace:F_SB}},{text:" the strongest Wave→PtfmPitch edge. Directed couplings live at specific lags that self-prediction heuristics miss — optimal for AIS is not optimal for transfer.",options:{color:INK}}]},
  key:{kicker:"TWO ROLES FOR τ",runs:[{text:"τ is both a modelling choice (which lags the test sees) and a compute lever — the slow-drift platform channels only finish at τ = 5. We validate any τ > 1 against the τ = 1 baseline.",options:{color:INK}}]}});

// SLIDE 10 — Significance
twoPanel({kicker:"SIGNIFICANCE",num:"10",title:"Is the transfer real? Surrogate testing",footer:FP,pager:"10 / 30",
  L:{h:"The null hypothesis",body:"KSG TE is never exactly zero — finite-sample noise leaves a small positive value. So we ask: is the measured TE larger than chance, if there were no coupling?"},
  R:{h:"Circular-shift surrogates",body:"Rotate the source in time (n = 200), destroying its timing with the target while keeping its spectrum. p = fraction of surrogates beating the real TE; keep edges with p < 0.05."},
  key:{kicker:"WHY CIRCULAR",runs:[{text:"A circular shift keeps the source's own spectrum and amplitude intact and removes only the X→Y timing — a strict, honest null that avoids false positives.",options:{color:INK}}]}});

// SLIDE 11 — Toy example
twoPanel({kicker:"INTUITION",num:"11",title:"A toy example: who drives whom?",footer:FP,pager:"11 / 30",
  L:{h:"Setup",body:[{text:"X[i] = 0.5·X[i−1] + noise (autonomous).\nY[i] = 0.5·X[i−1] + noise (responds to X's past).\n",options:{color:ACCENT,fontFace:F_SB,breakLine:true}},{text:"Both look like random noise to the eye.",options:{color:INK}}]},
  R:{h:"What TE recovers",body:[{text:"TE(X→Y) ≫ TE(Y→X).",options:{color:ACCENT,fontFace:F_SB}},{text:" The asymmetry correctly flags X as the driver — something a symmetric correlation could never reveal.",options:{color:INK}}]},
  key:{kicker:"THE TAKEAWAY",runs:[{text:"Direction emerges from the conditioning, not from the raw signals — exactly the test we run on wind, wave and structural channels.",options:{color:INK}}]}});

// SLIDE 12 — Three ways
threeCol({kicker:"FROM CORRELATION TO CAUSATION",num:"12",title:"Three ways to measure dependence",footer:FP,pager:"12 / 30",
  cols:[
   {h:"Correlation",body:[{text:"Strength of linear association. corr(X,Y) = corr(Y,X) — symmetric.\n\n",options:{color:INK,breakLine:true}},{text:"Directional ✗     Nonlinear ✗",options:{color:MUTED,fontFace:F_SB}}]},
   {h:"Granger causality",body:[{text:"Does X's past improve a linear forecast of Y? Directed, but assumes a linear (VAR) model. Granger 1969 · Nobel 2003.\n",options:{color:INK,breakLine:true}},{text:"Directional ✓     Nonlinear ✗",options:{color:MUTED,fontFace:F_SB}}]},
   {h:"Transfer entropy",body:[{text:"Does X's past reduce uncertainty about Y's future? Model-free, no distributional assumption. Schreiber 2000.\n",options:{color:INK,breakLine:true}},{text:"Directional ✓     Nonlinear ✓",options:{color:ACCENT,fontFace:F_SB}}]}],
  key:{kicker:"KEY INSIGHT",runs:[{text:"Transfer entropy is the only one that is both directed and nonlinear. For linear-Gaussian processes it reduces exactly to Granger causality (Barnett et al. 2009) — so it earns its keep precisely where the dynamics are nonlinear or non-Gaussian.",options:{color:INK}}]}});

// SLIDE 13 — TE vs Granger
twoPanel({kicker:"TE vs GRANGER",num:"13",title:"Transfer entropy and Granger causality",footer:FP,pager:"13 / 30",
  L:{h:"Granger causality",body:"Linear autoregressive (VAR) model. Fast and well-understood, but assumes linearity and (often) Gaussian statistics — misses nonlinear coupling."},
  R:{h:"Transfer entropy",body:"Model-free, no distributional assumption, captures any nonlinearity. Costlier (k-NN estimation) and hungrier for data."},
  key:{kicker:"WHEN THEY AGREE",runs:[{text:"For linear-Gaussian processes the two are exactly equivalent (Barnett et al. 2009). TE earns its keep only where the dynamics are nonlinear or non-Gaussian — which is why we run both.",options:{color:INK}}]}});

// SLIDE 14 — When to use TE
threeCol({kicker:"WHEN TO USE TE",num:"14",title:"When does transfer entropy pay off?",footer:FP,pager:"14 / 30",
  cols:[
   {h:"Linear / Gaussian",body:"TE = Granger causality exactly (Barnett 2009). No added value — use the simpler method."},
   {h:"Nonlinear / non-Gaussian",body:[{text:"TE captures directed structure that linear methods cannot see. ",options:{color:INK}},{text:"This is its sweet spot.",options:{color:ACCENT,fontFace:F_SB}}]},
   {h:"Very high-dimensional",body:"Many coupled modes degrade the k-NN estimate — curse of dimensionality, data starvation."}],
  key:{kicker:"KEY INSIGHT",runs:[{text:"A floating turbine in irregular waves with a nonlinear ROSCO controller sits squarely in the middle regime — nonlinear and non-Gaussian — where transfer entropy adds the most.",options:{color:INK}}]}});

// SLIDE 15 — System hero (divider)
(function(){
  const s=pres.addSlide(); s.background={color:PAPER};
  tick(s,ML,0.92);
  s.addText("THE SYSTEM",{x:ML+0.24,y:0.8,w:8,h:0.34,fontFace:F_SB,fontSize:11.5,color:ACCENT,charSpacing:3,valign:"middle",margin:0});
  s.addText(autonum(),{x:RIGHT-2.4,y:0.55,w:2.4,h:1.2,fontFace:F_LIGHT,fontSize:30,color:FAINT,align:"right",valign:"middle",margin:0});
  s.addText("A coupled wind–wave–\nstructure–mooring system",{x:ML,y:2.7,w:6.0,h:1.8,fontFace:F_DISP,fontSize:34,color:INK,lineSpacingMultiple:1.08,valign:"top",margin:0});
  s.addShape(pres.shapes.RECTANGLE,{x:ML,y:4.55,w:1.35,h:0.045,fill:{color:ACCENT},line:{type:"none"}});
  s.addText("Every channel — aerodynamic, hydrodynamic, servo and elastic — moves together. Which couplings are causal?",{x:ML,y:4.85,w:5.6,h:1.2,fontFace:F_LIGHT,fontSize:16,color:INK2,lineSpacingMultiple:1.2,valign:"top",margin:0});
  // image plate right (s15-hero ar 1.103, small/low-res — modest size)
  const iw=4.0, ih=iw/1.103, ix=RIGHT-iw-0.1, iy=2.5;
  s.addShape(pres.shapes.RECTANGLE,{x:ix-0.15,y:iy-0.15,w:iw+0.3,h:ih+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"s15-hero.png",x:ix,y:iy,w:iw,h:ih});
})();

// SLIDE 16 — System & Data (figure + 3 facts)
(function(){
  const s=pres.addSlide(); chromeAuto(s,"SYSTEM & DATA",FD);
  H1(s,"IEA-15MW FOWT, simulated in OpenFAST");
  const figW=5.6, ar=1.632, figH=figW/ar, matY=2.3;
  s.addShape(pres.shapes.RECTANGLE,{x:ML,y:matY,w:figW+0.3,h:figH+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"openfast.png",x:ML+0.15,y:matY+0.15,w:figW,h:figH});
  s.addText("OpenFAST — coupled aero-hydro-servo-elastic modules",{x:ML,y:matY+figH+0.4,w:figW+0.3,h:0.3,fontFace:F_BODY,fontSize:9.5,italic:true,color:MUTED,margin:0});
  const rx=ML+figW+0.9, rw=RIGHT-(ML+figW+0.9); let ry=2.35;
  [["Platform","IEA-15-240-RWT on the UMaine VolturnUS-S semisubmersible; coupled aero-hydro-servo-elastic OpenFAST model."],
   ["Signals","3600 s simulation · drop 600 s transient · decimate to 5 Hz."],
   ["Channels","2 sources — Wind1VelX, Wave1Elev → 9 responses: RootMyc1, RootMxc1, TwrBsMyt, PtfmHeave / Surge / Pitch, FAIRTEN1 / 2 / 3."]
  ].forEach(([h,b],i)=>{ if(i>0)hair(s,rx,ry-0.12,rw); kickerLine(s,rx,ry,rw,h.toUpperCase()); s.addText(b,{x:rx,y:ry+0.34,w:rw,h:1.1,fontFace:F_BODY,fontSize:13,color:INK,lineSpacingMultiple:1.2,valign:"top",margin:0}); ry+=1.45; });
})();

// SLIDE 17 — DLC matrix (full plate)
(function(){
  const s=pres.addSlide(); chromeAuto(s,"DESIGN LOAD CASES",FC);
  H1(s,"The simulation campaign");
  const ar=1.852, figW=7.0, figH=figW/ar, ix=(W-figW)/2, iy=2.2;
  s.addShape(pres.shapes.RECTANGLE,{x:ix-0.15,y:iy-0.15,w:figW+0.3,h:figH+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"dlc-matrix.png",x:ix,y:iy,w:figW,h:figH});
  s.addText("DLC-A / DLC-B / DLC-1.6 across the operating-point sweep",{x:ix,y:iy+figH+0.32,w:figW,h:0.3,fontFace:F_BODY,fontSize:10,italic:true,color:MUTED,align:"center",margin:0});
})();

// SLIDE 18 — Environmental conditions
twoPanel({kicker:"ENVIRONMENTAL CONDITIONS",num:"18",title:"Wind and wave inputs",footer:FC,pager:"18 / 30",
  L:{h:"Wind — TurbSim",body:"IEC Kaimal (IECKAI) spectrum, Normal Turbulence Model, class B, power-law shear, referenced at hub height. URef = 8 / 11 / 15 / 20 m/s."},
  R:{h:"Waves — JONSWAP",body:"Irregular JONSWAP sea (SeaState module). Hs / Tp scale with wind: (3.5 m, 9 s) → (8.0 m, 13 s). DLC-1.6 severe sea: Hs = 8.3 m, Tp = 12.95 s."},
  key:{kicker:"ON THE RANDOM SEEDS",runs:[{text:"DLC-A / DLC-1.6 reuse the wind seed for the wave generator; DLC-B draws an independent one. In OpenFAST, wind (TurbSim) and waves (HydroDyn) are generated separately, so the seed fixes reproducibility — not wind–wave correlation.",options:{color:INK}}]}});

// SLIDE 19 — Preprocessing
twoPanel({kicker:"PREPROCESSING",num:"19",title:"Why 5 Hz is enough",footer:FD,pager:"19 / 30",bodySize:12,
  L:{h:"Environment & platform",body:"Slow-drift platform motion — 0.01–0.1 Hz\nWave first-order band — 0.05–0.3 Hz (JONSWAP peak 0.077 Hz)\nPlatform eigenmodes — pitch 0.0345, heave 0.05, surge 0.01 Hz\nWind low-frequency turbulent eddies — 0.01–1 Hz"},
  R:{h:"Rotor & structure",body:"1P / 3P rotor harmonics — ~0.15 / 0.45 Hz\nTower fore-aft natural mode — ~0.5 Hz\nBlade-flap natural mode — ~0.6 Hz"},
  key:{kicker:"BOTTOM LINE",runs:[{text:"We down-sample 40 Hz → 5 Hz (×8). Nyquist = 2.5 Hz sits well above the highest band (~0.6 Hz), so every causal signal is preserved while the KSG sweep drops ~8×.",options:{color:INK}}]}});

// SLIDE 20 — Method: directed transfer (4 numbered steps + pipeline figure)
(function(){
  const s=pres.addSlide(); chromeAuto(s,"METHOD",FD);
  H1(s,"Directed transfer, with linear baselines");
  const steps=[
   ["1","KSG transfer entropy","Kraskov estimator (k = 4), non-uniform embedding, max_lag = 150 (30 s — one slow-drift cycle)."],
   ["2","Significance & effect size","Circular-shift surrogates ×200, p < 0.05 (max-stat). Normalized: te_frac = TE / (H(Y) − AIS(Y))."],
   ["3","Linear baselines, same pipeline","Gaussian / Granger (estimator swap) + magnitude-squared coherence γ²(f)."],
   ["4","Compute","OpenCL on 2× A100; GPU validated vs CPU (AIS RootMyc1 1.50 vs 1.49)."]];
  let y=2.4;
  steps.forEach(([n,h,b])=>{
    s.addText(n,{x:ML,y:y-0.04,w:0.6,h:0.6,fontFace:F_LIGHT,fontSize:30,color:ACCENT,valign:"top",margin:0});
    s.addText(h,{x:ML+0.7,y:y,w:5.0,h:0.34,fontFace:F_SB,fontSize:14.5,color:INK,margin:0});
    s.addText(b,{x:ML+0.7,y:y+0.36,w:5.1,h:0.6,fontFace:F_BODY,fontSize:12,color:INK,lineSpacingMultiple:1.15,valign:"top",margin:0});
    y+=1.08;
  });
  // pipeline figure right
  const ar=1.759, figW=5.2, figH=figW/ar, ix=ML+6.4, iy=2.7;
  s.addShape(pres.shapes.RECTANGLE,{x:ix-0.15,y:iy-0.15,w:figW+0.3,h:figH+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"pipeline.png",x:ix,y:iy,w:figW,h:figH});
  s.addText("the TE pipeline",{x:ix,y:iy+figH+0.32,w:figW,h:0.3,fontFace:F_BODY,fontSize:9.5,italic:true,color:MUTED,align:"center",margin:0});
})();

// SLIDE 21 — What TE measures (concept figure)
(function(){
  const s=pres.addSlide(); chromeAuto(s,"METHOD",FD);
  H1(s,"What transfer entropy measures");
  const ar=2.043, figW=6.0, figH=figW/ar, ix=(W-figW)/2, iy=2.3;
  s.addShape(pres.shapes.RECTANGLE,{x:ix-0.15,y:iy-0.15,w:figW+0.3,h:figH+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"concept.png",x:ix,y:iy,w:figW,h:figH});
  hair(s,ML,5.65,CW);
  s.addText([
    {text:"In one line — ",options:{color:ACCENT,fontFace:F_SB}},
    {text:"if the source's past sharpens the prediction of the target beyond the target's own history, information flows source → target. Directed (X→Y ≠ Y→X) and nonlinear — what correlation and coherence cannot see.",options:{color:INK}}
  ],{x:ML,y:5.85,w:CW,h:0.8,fontFace:F_BODY,fontSize:14.5,lineSpacingMultiple:1.18,valign:"top",margin:0});
})();

// SLIDE 22 — Wave-dominated graph (te-network)
figureRail({kicker:"RESULT",num:"22",title:"A wave-dominated causal graph",footer:FC,pager:"22 / 30",
  img:A+"te-network.png",ar:1.517,figW:6.0,
  caption:"TE causal network · bivariate KSG, edge weight = mean te_frac across all 54 DLC cases",
  railHead:"READING",
  railBody:[{text:"Wave elevation drives every significant response",options:{fontFace:F_SB,color:INK}},{text:" — pitch, heave, surge, tower base and mooring. Wind shows no significant directed transfer to the structure.",options:{color:INK}}],
  railBodyH:1.4,
  stats:[{big:"7 / 7",color:INK,label:"significant edges — every one originates from wave"},{big:"0",label:"significant wind → structure edges"}]});

// SLIDE 23 — Significant edges (windwave bars)
figureRail({kicker:"RESULT",num:"23",title:"The significant edges — 7 of 18",footer:FC,pager:"23 / 30",
  img:A+"conf-windwave-bars.png",ar:2.165,figW:6.6,matY:2.6,
  caption:"Significant directed transfer (nats) — wave only, mean across 54 cases",
  railHead:"WAVE DRIVES THE STRUCTURE",
  railBody:[{text:"The five strongest edges — pitch, heave, the forward fairleads and surge — cluster at 0.11–0.12 nats. ",options:{color:INK}},{text:"No wind → structure edge is significant",options:{fontFace:F_SB,color:INK}},{text:" anywhere in the campaign.",options:{color:INK}}],
  railBodyH:2.0,
  stats:[{big:"0 / 18",color:INK,label:"significant wind → structure edges — wave drives all seven"}]});

// SLIDE 24 — Triangulation
threeCol({kicker:"TRIANGULATION",num:"24",title:"TE vs. coherence vs. Granger",footer:FD,pager:"24 / 30",
  cols:[
   {h:"Coherence γ²(f)",body:"Undirected spectral ceiling. Shared power, no direction."},
   {h:"Gaussian / Granger",body:"Directional but linear. Over-detects under correlated wind–wave."},
   {h:"Transfer entropy",body:[{text:"Directed AND nonlinear. ",options:{color:ACCENT,fontFace:F_SB}},{text:"Catches couplings the others miss.",options:{color:INK}}]}],
  key:{kicker:"READING THE TRIANGLE",runs:[{text:"Where TE is significant but the linear baselines are not = nonlinear directed coupling unique to TE (e.g. the wave 2nd-order difference-frequency forcing of pitch). Where all three agree, the embedding is validated.",options:{color:INK}}]}});

// SLIDE 25 — Wind paradox
(function(){
  const s=pres.addSlide(); chromeAuto(s,"OPEN QUESTION",FD);
  H1(s,"The wind paradox");
  const y=2.45, lw=5.15, rx=ML+6.0, rw=5.3;
  vhair(s,ML+5.55,y,1.7);
  kickerLine(s,ML,y,lw,"THE PUZZLE");
  s.addText([{text:"Wind → structure ≈ 0 across 8–20 m/s",options:{fontFace:F_SB,color:INK}},{text:" — yet wind is what drives the turbine. Counter-intuitive, and it holds at every operating point.",options:{color:INK}}],{x:ML,y:y+0.4,w:lw,h:1.1,fontFace:F_BODY,fontSize:14.5,lineSpacingMultiple:1.2,valign:"top",margin:0});
  kickerLine(s,rx,y,rw,"NOT AN ARTIFACT");
  s.addText("Wind decorrelates at ~11.6 s — well inside the 30 s embedding window. The wind signal is sampled; it simply isn't transferring information to the structure.",{x:rx,y:y+0.4,w:rw,h:1.3,fontFace:F_BODY,fontSize:14.5,lineSpacingMultiple:1.2,valign:"top",margin:0});
  insight(s,4.75,"HYPOTHESIS — A CONTROLLER “FIREWALL”",[{text:"The blade-pitch controller (ROSCO) regulates rotor thrust so tightly that wind fluctuations are rejected before they reach the platform. The controller acts as a causal firewall — wind energizes the rotor, not the structure.",options:{color:INK}}]);
})();

// SLIDE 26 — Firewall ablation
figureRail({kicker:"OPEN QUESTION",num:"26",title:"Testing the firewall — controller-off ablation",footer:FD,pager:"26 / 30",
  img:A+"conf-ablation.png",ar:2.323,figW:7.0,matY:2.55,
  caption:"Re-ran the same case with blade-pitch control frozen (open-loop)",
  railHead:"VERDICT",
  railBody:[{text:"Suggestive but inconclusive. ",options:{fontFace:F_SB,color:ACCENT}},{text:"The wind→heave edge appears, but open-loop overspeed inflates AIS and masks wind in bivariate TE.",options:{color:INK}}],
  railBodyH:1.9,
  stats:[{big:"next",color:INK,label:"conditional TE  TE(wind→Y | wave)  +  a non-overspeeding ablation"}]});

// SLIDE 27 — Methods lessons
(function(){
  const s=pres.addSlide(); chromeAuto(s,"METHODS LESSONS",FD);
  H1(s,"What made it work — and what nearly broke it");
  const y=2.5, lw=5.15, rx=ML+6.0, rw=5.3;
  vhair(s,ML+5.55,y,3.2);
  kickerLine(s,ML,y,lw,"GPU MADE THE SWEEP TRACTABLE");
  s.addText("~35 h",{x:ML,y:y+0.35,w:lw,h:0.9,fontFace:F_LIGHT,fontSize:48,color:ACCENT,margin:0,valign:"middle"});
  s.addText("per case on a single A100-batched run. The OpenCL KSG estimator (validated vs CPU) is what brings the full DLC sweep into reach.",{x:ML,y:y+1.35,w:lw,h:1.2,fontFace:F_BODY,fontSize:13.5,color:INK,lineSpacingMultiple:1.2,valign:"top",margin:0});
  kickerLine(s,rx,y,rw,"CAUTION — EMBEDDING DELAY MATTERS");
  s.addText("0.12 → 0",{x:rx,y:y+0.35,w:rw,h:0.9,fontFace:F_LIGHT,fontSize:44,color:INK,margin:0,valign:"middle"});
  s.addText("A data-driven τ from self-MI preserved AIS but collapsed the TE edges (τ = 10 zeroed the strongest Wave→PtfmPitch edge). Directed couplings live at specific lags — AIS heuristics don't transfer to TE.",{x:rx,y:y+1.35,w:rw,h:1.4,fontFace:F_BODY,fontSize:13.5,color:INK,lineSpacingMultiple:1.2,valign:"top",margin:0});
})();

// SLIDE 28 — Hybrid TE + Sobol
(function(){
  const s=pres.addSlide(); chromeAuto(s,"OUTLOOK  ·  HYBRID METHOD","Hybrid TE + Sobol · RAFT Saltelli ensemble (Sobol) + IDTxl (TE)");
  H1(s,"Closing the loop: TE + Sobol → data-driven weights");
  // combined figure (left)
  const cw=5.55, car=1.570, ch=cw/car, cy=2.12;
  s.addShape(pres.shapes.RECTANGLE,{x:ML,y:cy,w:cw+0.3,h:ch+0.3,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"combined.png",x:ML+0.15,y:cy+0.15,w:cw,h:ch});
  kickerLine(s,ML+0.02,cy+ch+0.42,cw,"COMBINED GRAPH — TE + SOBOL");
  // sobol figure (right-top)
  const rx=ML+cw+0.72, rw=RIGHT-(ML+cw+0.72), sar=2.209, sw=rw, sh=sw/sar, sy=2.12;
  s.addShape(pres.shapes.RECTANGLE,{x:rx,y:sy,w:sw,h:sh+0.26,fill:{color:"FFFFFF"},line:{color:HAIR,width:1}});
  s.addImage({path:A+"sobol.png",x:rx+0.1,y:sy+0.13,w:sw-0.2,h:(sw-0.2)/sar});
  kickerLine(s,rx+0.02,sy+sh+0.4,rw,"SOBOL Sₜ — DESIGN SENSITIVITY");
  s.addText([
    {text:"Mooring length (L_u) and stiffness (EA)",options:{fontFace:F_SB,color:INK}},{text:" dominate fairlead tensions and several motions. ",options:{color:INK}},
    {text:"Column geometry (D_OCol, R_MO)",options:{fontFace:F_SB,color:INK}},{text:" drives surge, sway and heave.",options:{color:INK}}
  ],{x:rx,y:sy+sh+0.72,w:rw,h:1.2,fontFace:F_BODY,fontSize:12,color:INK,lineSpacingMultiple:1.2,valign:"top",margin:0});
  // full-width synthesis at bottom
  hair(s,ML,6.18,CW);
  s.addText([
    {text:"Two directed importance maps in one graph — ",options:{color:INK}},
    {text:"TE for environment-driven dynamics, Sobol for design sensitivity",options:{fontFace:F_SB,color:ACCENT}},
    {text:" — a data-driven basis for the optimization weights (proposed next step).",options:{color:INK}}
  ],{x:ML,y:6.3,w:CW,h:0.6,fontFace:F_BODY,fontSize:13.5,color:INK,lineSpacingMultiple:1.15,valign:"top",margin:0});
})();

// SLIDE 29 — Limitations & Future
(function(){
  const s=pres.addSlide(); chromeAuto(s,"LIMITATIONS & FUTURE",FD);
  H1(s,"Where this goes next");
  const y=2.5, lw=5.15, rx=ML+6.0, rw=5.3;
  vhair(s,ML+5.55,y,3.4);
  kickerLine(s,ML,y,lw,"LIMITATIONS");
  dashList(s,ML,y+0.45,lw,[
    {text:"Single platform (UMaine VolturnUS-S), simulation-only — no field validation."},
    {text:"max_lag = 150 (30 s) may be short for PtfmSurge (decorrelates ~24.6 s)."},
    {text:"Firewall mechanism (controller) is preliminary and confounded — the wind decoupling is shown, its cause is not."}],13.5);
  kickerLine(s,rx,y,rw,"NEXT STEPS");
  dashList(s,rx,y+0.45,rw,[
    {text:"Conditional TE — TE(wind→Y | wave) — to test the firewall beyond the bivariate estimate."},
    {text:"A non-overspeeding controller-off ablation to settle the firewall mechanism."},
    {text:"Hybrid graph: add Sobol design-parameter sensitivity."},
    {lead:"Feed the ranked TE driver→load pathways",text:"into structural/fatigue load weighting for design optimization."}],13);
})();

// SLIDE 30 — Conclusion (statement)
(function(){
  const s=pres.addSlide(); s.background={color:PAPER};
  tick(s,ML,0.92);
  s.addText("CONCLUSION",{x:ML+0.24,y:0.8,w:8,h:0.34,fontFace:F_SB,fontSize:11.5,color:ACCENT,charSpacing:3,valign:"middle",margin:0});
  s.addText(autonum(),{x:RIGHT-2.4,y:0.55,w:2.4,h:1.2,fontFace:F_LIGHT,fontSize:30,color:FAINT,align:"right",valign:"middle",margin:0});
  s.addText([
    {text:"Transfer entropy reveals a ",options:{color:INK}},
    {text:"wave-dominated causal structure",options:{color:ACCENT}},
    {text:" in FOWT response that linear methods only partially capture.",options:{color:INK}}
  ],{x:ML,y:1.9,w:11.2,h:1.7,fontFace:F_DISP,fontSize:34,lineSpacingMultiple:1.1,valign:"top",margin:0});
  hair(s,ML,4.05,CW);
  dashList(s,ML,4.3,CW,[
    {text:"Wave drives platform pitch, heave, surge, tower base and mooring; no wind → structure edge is significant across the 54-case campaign."},
    {text:"The wind decoupling is robust and non-obvious — holding across 8–20 m/s — yet whether the controller causes it is an open, testable question."},
    {text:"Conditional TE and a non-overspeeding controller-off ablation are the path to settle it."},
    {lead:"Next:",text:"pair this ranking with Sobol design sensitivities to set data-driven weights for design optimization."}],14);
  hair(s,ML,6.85,CW);
  s.addText("IEA-15MW · UMaine VolturnUS-S · OpenFAST + IDTxl   ·   github.com/sinahdme/fowt-te-causal",{x:ML,y:6.92,w:CW,h:0.3,fontFace:F_BODY,fontSize:10,color:MUTED,valign:"middle",margin:0});
})();

pres.writeFile({ fileName: "te-conference-talk-v2.pptx" }).then(f=>console.log("wrote",f));
