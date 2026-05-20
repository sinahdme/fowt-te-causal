// Build 2026-05-20 status report as .docx
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageBreak, TabStopType, TabStopPosition,
} = require("docx");

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const cellBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
const cellMargins = { top: 100, bottom: 100, left: 140, right: 140 };

const p = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: 120 },
    ...opts,
    children: opts.children || [new TextRun({ text, ...opts.run })],
  });

const h1 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 180 },
    children: [new TextRun({ text })],
  });

const h2 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text })],
  });

const h3 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 180, after: 100 },
    children: [new TextRun({ text })],
  });

const bullet = (text, children) =>
  new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: children || [new TextRun({ text })],
  });

const numbered = (text, children) =>
  new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { after: 80 },
    children: children || [new TextRun({ text })],
  });

const code = (text) =>
  new Paragraph({
    spacing: { after: 60 },
    children: [new TextRun({ text, font: "Consolas", size: 18 })],
  });

const td = (text, opts = {}) =>
  new TableCell({
    borders: cellBorders,
    margins: cellMargins,
    width: { size: opts.width, type: WidthType.DXA },
    shading: opts.header ? { fill: "2E75B6", type: ShadingType.CLEAR } : undefined,
    children: [
      new Paragraph({
        children: [
          new TextRun({
            text,
            bold: opts.header || opts.bold,
            color: opts.header ? "FFFFFF" : "000000",
            size: opts.small ? 18 : 20,
          }),
        ],
      }),
    ],
  });

// --- Tables ---

const hypothesesTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [720, 6480, 2160],
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        td("#", { header: true, width: 720 }),
        td("Prediction", { header: true, width: 6480 }),
        td("Test method", { header: true, width: 2160 }),
      ],
    }),
    new TableRow({ children: [
      td("H1", { width: 720, bold: true }),
      td("TE(wind → pitch) significant in DLC-A and DLC-B; TE(pitch → wind) ≈ 0 (back-action sanity).", { width: 6480, small: true }),
      td("Phase 4 KSG-TE", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H2", { width: 720, bold: true }),
      td("TE(wave → heave) significant + dominant in 0.1–0.3 Hz wave band; coherence γ²(f) agrees at the peak.", { width: 6480, small: true }),
      td("Phase 4 + scipy.coherence", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H3", { width: 720, bold: true }),
      td("Conditional TE(wind → pitch | wave) ≈ bivariate TE in DLC-B (decoupled seeds) but < 80 % of bivariate in DLC-A (correlated). Demonstrates conditional TE is doing real work.", { width: 6480, small: true }),
      td("DLC-A vs DLC-B contrast", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H4", { width: 720, bold: true }),
      td("ST(EA | std(PtfmSurge)) > 0.5 AND ST(L_u | std(PtfmSurge)) > 0.2; geometry combined contribution < 0.3.", { width: 6480, small: true }),
      td("Phase 5 Sobol", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H5", { width: 720, bold: true }),
      td("Fairlead-tension trade-off is wave-driven, not wind-driven: ST(EA | std(FAIRTEN1)) > ST(geometry); conditional TE(wave → FAIRTEN1 | wind) > 2 × TE(wind → FAIRTEN1 | wave).", { width: 6480, small: true }),
      td("Phase 5 + Phase 4", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H6", { width: 720, bold: true }),
      td("TE local-in-time PSD peak at platform pitch eigenfrequency (~0.0345 Hz).", { width: 6480, small: true }),
      td("Phase 4 spectral", { width: 2160, small: true }),
    ] }),
  ],
});

const openQuestionsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [720, 5040, 3600],
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        td("#", { header: true, width: 720 }),
        td("Topic", { header: true, width: 5040 }),
        td("Status", { header: true, width: 3600 }),
      ],
    }),
    new TableRow({ children: [
      td("Q1", { width: 720, bold: true }),
      td("Response channels", { width: 5040, small: true }),
      td("RESOLVED — 9 channels locked", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q2", { width: 720, bold: true }),
      td("Sweep parameters", { width: 5040, small: true }),
      td("RESOLVED — 9 vars, ±20 % LHS", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q3", { width: 720, bold: true }),
      td("Response summary statistics", { width: 5040, small: true }),
      td("PARTIAL — 4-stat locked, band powers pending", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q4", { width: 720, bold: true }),
      td("IDTxl embedding strategy", { width: 5040, small: true }),
      td("OPEN — revisit during Phase 4 calibration", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q5", { width: 720, bold: true }),
      td("Multi-platform comparison", { width: 5040, small: true }),
      td("IEA-22 locked; deferred to v2 paper", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q6", { width: 720, bold: true }),
      td("Wind-wave correlation", { width: 5040, small: true }),
      td("Handled by DLC-A vs DLC-B contrast", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q7", { width: 720, bold: true }),
      td("Publication venue", { width: 5040, small: true }),
      td("OPEN — workshop vs Wind Energy Science", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q8", { width: 720, bold: true }),
      td("Pre-registered hypotheses H1–H6", { width: 5040, small: true }),
      td("RESOLVED 2026-05-13", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q9", { width: 720, bold: true }),
      td("Concrete design-decision case study", { width: 5040, small: true }),
      td("LEAD: Jeon-2025 Case_03 fairlead-tension", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q10", { width: 720, bold: true }),
      td("Ensemble TE refactor (Wollstadt 2014)", { width: 5040, small: true }),
      td("FILED 2026-05-19 — adopt if needed", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Q11", { width: 720, bold: true }),
      td("Controller-off comparison (ROSCO ΔTE)", { width: 5040, small: true }),
      td("FILED 2026-05-20 — supplementary DLC", { width: 3600, small: true }),
    ] }),
  ],
});

const tradeoffsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2520, 1080, 4320, 1440],
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        td("Option", { header: true, width: 2520 }),
        td("Speedup", { header: true, width: 1080 }),
        td("Effect on results", { header: true, width: 4320 }),
        td("Wall time", { header: true, width: 1440 }),
      ],
    }),
    new TableRow({ children: [
      td("A. Cut surrogates 200 → 50", { width: 2520, small: true }),
      td("4×", { width: 1080, small: true }),
      td("p-value resolution drops from 0.005 to 0.02; alpha=0.05 still defensible", { width: 4320, small: true }),
      td("~7 days", { width: 1440, small: true }),
    ] }),
    new TableRow({ children: [
      td("B. Bivariate-only first pass", { width: 2520, small: true }),
      td("3×", { width: 1080, small: true }),
      td("Skips conditional + Granger initially; loses DLC-A vs DLC-B H3 contrast", { width: 4320, small: true }),
      td("~9 days", { width: 1440, small: true }),
    ] }),
    new TableRow({ children: [
      td("C. Ensemble TE (Q10)", { width: 2520, small: true }),
      td("6×", { width: 1080, small: true }),
      td("Pool 6 seeds per DLC bin; strongest methodology framing, sharper significance", { width: 4320, small: true }),
      td("~5 days", { width: 1440, small: true }),
    ] }),
    new TableRow({ children: [
      td("A + C combined (recommended)", { width: 2520, small: true, bold: true }),
      td("~20×", { width: 1080, small: true, bold: true }),
      td("Best science + best speed", { width: 4320, small: true, bold: true }),
      td("~24–36 h", { width: 1440, small: true, bold: true }),
    ] }),
  ],
});

const tierTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [3240, 2520, 3600],
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        td("Venue tier", { header: true, width: 3240 }),
        td("Reachability", { header: true, width: 2520 }),
        td("What's needed", { header: true, width: 3600 }),
      ],
    }),
    new TableRow({ children: [
      td("Workshop (TORQUE, EERA DeepWind, OMAE)", { width: 3240, small: true }),
      td("≥ 90 % — current scope sufficient", { width: 2520, small: true }),
      td("Nothing additional", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Wind Energy Science", { width: 3240, small: true }),
      td("50–60 % with strengthening moves", { width: 2520, small: true }),
      td("Adopt ensemble TE (Q10) + ≥ 4 of 6 hypotheses confirmed + Q9 takeaway", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Marine Structures / Ocean Eng.", { width: 3240, small: true }),
      td("~40 %", { width: 2520, small: true }),
      td("Frame around mooring/platform causal story (Q9 lead)", { width: 3600, small: true }),
    ] }),
    new TableRow({ children: [
      td("Top-tier (Wind Energy, Appl. Energy)", { width: 3240, small: true }),
      td("Stretch", { width: 2520, small: true }),
      td("OC6 experimental anchor OR IEA-22 multi-platform", { width: 3600, small: true }),
    ] }),
  ],
});

// --- Build document ---

const children = [
  // Title block
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({
      text: "Comprehensive Project Report",
      bold: true,
      size: 36,
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 240 },
    children: [new TextRun({
      text: "Causal Effect on FOWT via Transfer Entropy",
      bold: true,
      size: 28,
      color: "2E75B6",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [
      new TextRun({ text: "Student: ", bold: true }),
      new TextRun({ text: "Sina" }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [
      new TextRun({ text: "Period: ", bold: true }),
      new TextRun({ text: "2026-05-12 to 2026-05-20 (Day 1–9)" }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [
      new TextRun({ text: "Repository: ", bold: true }),
      new TextRun({ text: "github.com/sinahdme/fowt-te-causal", font: "Consolas", size: 20 }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 360 },
    children: [
      new TextRun({ text: "Latest commit: ", bold: true }),
      new TextRun({ text: "d5ed1d2", font: "Consolas", size: 20 }),
    ],
  }),

  // 1. Research Context
  h1("1. Research Context"),
  p("This project quantifies the causal effect of environmental excitation (wind, waves) and structural design parameters (substructure geometry, mooring) on the dynamic response of a floating offshore wind turbine (FOWT), using Transfer Entropy (TE) as the primary causal-inference tool — combined with Sobol sensitivity analysis for the constants-per-run design parameters."),
  p("The reference platform is the IEA-15 MW reference turbine on the UMaine VolturnUS-S semisubmersible (deep-water site, active ROSCO controller). A secondary platform — the IEA-22 MW Semi — is locked-in for a multi-platform comparison in a v2 paper."),
  p("The work extends the recent RL-optimisation study by Jeon et al. (2025) by replacing the purely sensitivity-based ranking with a hybrid TE + Sobol causal graph that disentangles wave-driven, wind-driven, and controller-mediated paths to platform/mooring response."),

  // 2. Pre-registered hypotheses
  h1("2. Pre-registered Hypotheses (locked 2026-05-13 before any campaign sims)"),
  p("These predictions were committed before the Phase 2 campaign launched. Pre-registration prevents post-hoc p-hacking accusations; confirmed and not-confirmed results will be reported with equal prominence."),
  hypothesesTable,

  // 3. Full plan
  h1("3. Full Plan: Six Phases"),
  code("Phase 1  Knowledge base       OpenFAST repo + docs in Obsidian vault"),
  code("Phase 2  Simulation           OpenFAST DLC matrix (54 cases)"),
  code("Phase 3  Data pipeline        Parse .outb, align, preprocess"),
  code("Phase 4  TE: env -> response  IDTxl bivariate + conditional KSG"),
  code("Phase 5  Param causality      Sobol + MI ensemble (RAFT surrogate)"),
  code("Phase 6  Reporting            Combined causal graph + figures"),
  p(""),
  p("Hybrid hydro-evaluation pipeline (locked 2026-05-13): RAFT (frequency-domain) drives the Phase 5 9-variable Saltelli ensemble of 704 evaluations; OpenFAST (time-domain) drives the Phase 2 DLC campaign that feeds Phase 4 TE."),
  p("Compute target: a 65-core Linux server (production). Local Windows machine for development, smoke tests, narrative log authoring, and post-rsync analysis."),

  // 4. What's done
  h1("4. What's Done (Phase by Phase)"),

  h2("4.1 Phase 1 — Knowledge Base — COMPLETE"),
  bullet("48-page Obsidian vault (three-layer structure: raw/, pages/, SCHEMA.md) with backlinked entity/concept/equation/validation-case pages."),
  bullet("Seven reference repositories vendored: openfast, r-test, IEA-15-240-RWT, ROSCO, WEIS, openfast_toolbox, MoorPy."),
  bullet("Three Tier-1 ingest sources (Schreiber 2000, Kraskov 2004, Wollstadt 2019) processed into deep analytical pages."),
  bullet("Predecessor work (Jeon 2025 KSME) ingested and integrated."),

  h2("4.2 Phase 2 — OpenFAST DLC Campaign — COMPLETE"),
  p("54 cases × 1-hour simulated time × 80 Hz output; 268 MB .outb per case; ~14 GB total raw output."),
  bullet("DLC-1.6: 6 cases (V=11 m/s, SSS, Hs=8.3 m, Tp=12.95 s) — predecessor cross-comparability."),
  bullet("DLC-A: 24 cases (NTM at V=8/11/15/20 m/s × 6 seeds, JONSWAP correlated wave) — primary H1/H2 test."),
  bullet("DLC-B: 24 cases (same wind/seeds as DLC-A, decoupled wave seeds via XOR mask) — conditional-TE validation (H3)."),
  bullet("Active ROSCO controller (CompServo=1) engaged throughout."),
  bullet("9 response channels logged per Q1 lockdown: 3 structural loads, 3 platform motions, 3 mooring tensions."),
  p("Five infrastructure bugs identified and patched along the way:"),
  numbered("OpenFAST v4.1.2 → v4.2.1 upgrade (ElastoDyn format incompatibility with IEA-15 deck)."),
  numbered("run_campaign.py: WaveSeed(1) regex false-positive on re-runs."),
  numbered("run_campaign.py: 0-byte wind.bts skip-bug after a killed previous run."),
  numbered("BLAS oversubscription: 24 concurrent TurbSim processes each spawning multi-threaded BLAS calls inflated load average to 168 on a 65-core machine. Fixed by OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1; load dropped to ~24, expected behavior."),
  numbered("IDTxl estimators_opencl.py: calls sys.exit() when pyopencl is missing, silently killing the whole script. Fixed by installing pyopencl + pocl via conda-forge."),

  h2("4.3 Phase 3 — Preprocessing — EMBEDDED IN Phase 4"),
  bullet("analysis/load_runs.py parses .outb via openfast_toolbox.io.FASTOutputFile to pandas DataFrame."),
  bullet("analysis/te_pipeline.py performs drop-transient (600 s), decimate (40 Hz → 5 Hz), jitter (1e-10 Gaussian per Kraskov 2004 §III.A), and z-score normalisation."),

  h2("4.4 Phase 4 — TE Pipeline — VALIDATED, SCOPE DECISION PENDING"),
  bullet("End-to-end IDTxl pipeline operational: Bivariate KSG-TE, Conditional Multivariate-TE, Gaussian-Granger baseline (same IDTxl framework with swapped estimator — apples-to-apples per Wollstadt 2019), Active Information Storage (effect-size denominator), and scipy coherence baseline."),
  bullet("Circular-shift surrogates per the 2026-05-15 methodology reconciliation (preserves spectrum and amplitude, destroys directed coupling)."),
  bullet("Smoke test on dlc16_v11ms_s00 succeeded: AIS(PtfmPitch) = 4.1026 nats, p = 0.002 (highly significant self-prediction). TE(Wind1VelX → PtfmPitch) = 0.0000, p = 1.0 — null result at DLC-1.6."),
  bullet("Production-scale wall-time problem: ~27 days at originally-scoped settings (18 pairs × 200 surrogates × 54 cases). JIDT is multi-threaded internally so naïve parallelization risks the same oversubscription problem we hit in Phase 2."),

  h2("4.5 Phase 5 — Sobol + MI Sensitivity — N=64 PRELIMINARY, N=256 PENDING"),
  bullet("Nine design variables locked at IEA-15 baselines ±20 %: substructure geometry (D_MCol, D_OCol, R_MO, D_Pt, H_Pt, H_FB, H_Draft) + mooring (EA, L_u)."),
  bullet("N=64 Saltelli sample → 704 RAFT evaluations, 313/704 feasible (44 %). The remainder violate the geometric constraints D_OCol > D_Pt and H_Pt > 0.5·D_Pt from Jeon-2025."),
  bullet("Preliminary finding: mooring line length L_u is the dominant Sobol-ST driver across most response statistics. Pre-registered H4 prediction ST(EA | std(PtfmSurge)) > 0.5 not confirmed at N=64 (observed: 0.09 ± 0.08). Production N=256 (~5 minutes on server) is queued."),
  bullet("Files: data/raft_lhs_v2-N64.parquet (704 rows), data/raft_lhs_v2-N64_sobol.json."),

  // 5. Key findings + open questions
  h1("5. Key Methodological Findings"),

  h2("5.1 H1 null on DLC-1.6 is consistent with theory, not a failure"),
  p("The null TE(wind → pitch) at DLC-1.6 reflects two effects acting in concert:"),
  numbered("Wave dominance at SSS: Hs = 8.3 m severe sea state drives the dominant share of platform pitch variance; wind's contribution is masked in the marginal predictability budget."),
  numbered("ROSCO disturbance rejection: an effective controller, by design, removes the wind→pitch causal signature. This is a known TE/closed-loop phenomenon (Schreiber 2000 was open-loop; Massey 1990 / Lizier 2014 handle feedback systems)."),
  p("H1 will properly be tested on DLC-A (NTM, no SSS, four wind speeds), where wind-driven pitch should dominate."),

  h2("5.2 Two new methodology-level open questions logged"),
  bullet("Q10 — Ensemble TE (Wollstadt 2014): pooling the 6 seeds per DLC bin as one estimator reduces 54 cases to 9 effective ensembles, sharpens significance, and reframes the paper as \"extending the Wollstadt-2014 ensemble approach from neuroscience multi-trial designs to FOWT seed ensembles.\""),
  bullet("Q11 — Controller-off comparison: a single supplementary DLC bin with CompServo=0 quantifies ROSCO's contribution to the wind→response causal graph as ΔTE_ctrl = TE_ctrl-off − TE_ctrl-on. Methodological novelty for FOWT TE literature. Cost: ~95 min server compute."),

  h2("5.3 Open methodological questions logged"),
  openQuestionsTable,

  // 6. Future work
  h1("6. Future Work"),

  h2("6.1 Immediate (next 1–3 days, blocking)"),
  bullet("Decision on Phase 4 scope (see table below)."),
  tradeoffsTable,
  p(""),
  p("Recommendation: combine A + C. Wall time drops from ~27 days to ~24–36 hours. Strongest publication framing."),
  bullet("Refactor analysis/te_pipeline.py for ensemble TE (~1 day of work). Stack 6 seeds per DLC bin along IDTxl's replications axis."),
  bullet("Launch Phase 4 (~24–36 h wall on server with the refactor)."),
  bullet("Launch Phase 5 N=256 in parallel (~5 minutes; queued only because the box was saturated)."),

  h2("6.2 Short-term (next 1 week)"),
  bullet("Phase 6 reporting + figures: build the combined causal graph (TE + Sobol), write analysis/plots.py for the publication figures (causal-graph diagram, per-pair TE heatmap, DLC-A vs DLC-B conditional-TE contrast, TE-vs-coherence and TE-vs-Granger comparison tables, Sobol-ST bar charts)."),
  bullet("Evaluate hypotheses H1–H6 against actual data, mark each as confirmed / partial / not-confirmed per the pre-registered thresholds."),
  bullet("Write the narrative for the Q9 engineering takeaway: did the causal graph change a design decision that Sobol-only could not?"),

  h2("6.3 Medium-term (next 2–4 weeks)"),
  bullet("Q11 controller-off comparison (1 DLC bin × 6 seeds with CompServo=0) — adopt only if H5's controller-mediated path is inconclusive. ~95 min server compute."),
  bullet("Pick publication venue (Q7): workshop (TORQUE 2026, EERA DeepWind, ASME OMAE) — low bar, current scope sufficient. Wind Energy Science — reachable with ensemble TE + baseline comparison + design takeaway. Marine Structures — if mooring/platform causal story leads."),
  bullet("Manuscript draft: Methods section first, then Results from confirmed hypotheses, then Discussion / Conclusion."),

  h2("6.4 Stretch / v2 paper"),
  bullet("IEA-22 MW Semi multi-platform comparison (Q5) — adds the \"does causal structure scale?\" figure. Requires re-running Phase 2 + Phase 4 + Phase 5 for the second platform. ~1 week of compute."),
  bullet("OC6 experimental anchor — compare TE results against published model-test data. Adds external validation."),
  bullet("Frequency-band-resolved TE (Q3 extension): low-freq vs wave-freq vs 1P/3P band powers as separate response statistics. More informative for fatigue."),

  // 7. Publication strategy
  h1("7. Publication Strategy (locked 2026-05-12)"),
  p("Honest tier assessment based on current data and planned strengthening moves:"),
  tierTable,
  p(""),
  p("Strengthening moves already in plan:"),
  numbered("Mandatory linear baselines (coherence + Granger via IDTxl-Gaussian) — apples-to-apples per Wollstadt 2019."),
  numbered("Pre-registered H1–H6 (locked before campaign launch — defensible against p-hacking accusations)."),
  numbered("Concrete engineering takeaway via Q9 Case_03 case study."),
  numbered("Open code + reproducible OpenFAST decks in a public repo (this one)."),

  // 8. Headline result
  h1("8. Headline Quotable Result"),
  new Paragraph({
    spacing: { before: 120, after: 120 },
    indent: { left: 720, right: 720 },
    border: {
      left: { style: BorderStyle.SINGLE, size: 24, color: "2E75B6", space: 12 },
    },
    children: [new TextRun({
      text: "A 54-case OpenFAST campaign on the IEA-15 UMaineSemi has been completed (1 hour simulated time per case, 268 MB output, 14 GB total). The transfer-entropy pipeline runs end-to-end on the resulting data. The first smoke test reveals that under severe sea state with active ROSCO control, TE(wind → pitch) = 0 — consistent with both wave-driven platform dynamics dominating the SSS regime and the controller's role in actively rejecting the wind disturbance. Full DLC-A results (where wind-driven pitch should be unambiguous and the controller-rejection story is cleaner) are the next test of pre-registered hypothesis H1. A methodological pivot toward ensemble TE (Wollstadt 2014) is under consideration to reduce the full-campaign wall time from ~27 days to ~24 hours and to give the paper a stronger Wind Energy Science framing.",
      italics: true,
    })],
  }),

  // Footer note
  new Paragraph({
    spacing: { before: 360 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 6, color: "BFBFBF", space: 6 },
    },
    children: [new TextRun({
      text: "Generated 2026-05-20 from PLAN.md, pages/log.md, pages/open-questions.md, and Phase 2 / Phase 4 / Phase 5 results in data/ and reports/.",
      size: 18,
      color: "808080",
      italics: true,
    })],
  }),
];

const doc = new Document({
  creator: "Sina (with Claude Opus 4.7)",
  title: "Causal Effect on FOWT via Transfer Entropy — Comprehensive Project Report",
  description: "Status report covering Phases 1–5, methodology, pre-registered hypotheses, open questions, and future work.",
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 22 } },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Calibri", color: "1F3864" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: "2E75B6" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Calibri", color: "2E75B6" },
        paragraph: { spacing: { before: 180, after: 100 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      ] },
      { reference: "numbers", levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      ] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children: children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(__dirname, "2026-05-20-status-report.docx");
  fs.writeFileSync(out, buf);
  console.log("Wrote", out, "(" + buf.length + " bytes)");
});
