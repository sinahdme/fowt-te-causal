// Build 2026-05-20 technical report v2 — topic-structured, with embedded figures
// and trimmed theory pointing to repo documentation.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageBreak, ImageRun, ExternalHyperlink,
  Math, MathRun, MathFraction, MathNumerator, MathDenominator,
  MathSubScript, MathSuperScript, MathSubSuperScript,
  MathSquareBrackets, MathRoundBrackets,
} = require("docx");

// Hyperlink target for any repo file mention.
const REPO_URL = "https://github.com/sinahdme/fowt-te-causal/blob/main";

// ---------- styling helpers ----------

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const cellBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
const cellMargins = { top: 100, bottom: 100, left: 140, right: 140 };

const p = (text, opts = {}) =>
  new Paragraph({
    spacing: { after: 140 },
    alignment: opts.center ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
    ...opts.paragraph,
    children: opts.children || [new TextRun({ text, ...opts.run })],
  });

const para = (children, paragraphOpts = {}) =>
  new Paragraph({
    spacing: { after: 140 },
    alignment: AlignmentType.JUSTIFIED,
    ...paragraphOpts,
    children,
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
    spacing: { before: 280, after: 120 },
    children: [new TextRun({ text })],
  });

const h3 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text })],
  });

const bullet = (children) =>
  new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: typeof children === "string" ? [new TextRun({ text: children })] : children,
  });

const numbered = (children) =>
  new Paragraph({
    numbering: { reference: "numbers", level: 0 },
    spacing: { after: 80 },
    children: typeof children === "string" ? [new TextRun({ text: children })] : children,
  });

const code = (text) =>
  new Paragraph({
    spacing: { after: 60 },
    children: [new TextRun({ text, font: "Consolas", size: 18 })],
  });

const equation = (text) =>
  new Paragraph({
    spacing: { before: 80, after: 120 },
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text, font: "Cambria Math", italics: true, size: 24 })],
  });

const it = (text) => new TextRun({ text, italics: true });
const b = (text) => new TextRun({ text, bold: true });
const t = (text) => new TextRun({ text });
const mono = (text) => new TextRun({ text, font: "Consolas", size: 20 });

// Hyperlinked file path — clickable link to the repo's main branch.
const repoLink = (filePath, opts = {}) => new ExternalHyperlink({
  link: `${REPO_URL}/${filePath}`,
  children: [new TextRun({
    text: filePath,
    font: "Consolas",
    size: opts.small ? 18 : 20,
    color: "2E75B6",
    underline: { type: "single" },
  })],
});

// "Table N. caption text"  paragraph (label is bold + colored, caption italic gray).
const tableCaption = (n, desc) => new Paragraph({
  spacing: { before: 200, after: 80 },
  alignment: AlignmentType.LEFT,
  children: [
    new TextRun({ text: `Table ${n}. `, bold: true, size: 20, color: "1F3864" }),
    new TextRun({ text: desc, italics: true, size: 20, color: "595959" }),
  ],
});

// Math helpers — produce native OMML equations editable in Word's equation editor.
const mrun = (s) => new MathRun(s);
const msub = (base, sub) => new MathSubScript({
  children: [typeof base === "string" ? mrun(base) : base],
  subScript: Array.isArray(sub) ? sub : [typeof sub === "string" ? mrun(sub) : sub],
});

// Wrap a Math object into a centered display equation paragraph.
const displayMath = (mathChildren) => new Paragraph({
  spacing: { before: 100, after: 140 },
  alignment: AlignmentType.CENTER,
  children: [new Math({ children: mathChildren })],
});

const td = (text, opts = {}) =>
  new TableCell({
    borders: cellBorders,
    margins: cellMargins,
    width: { size: opts.width, type: WidthType.DXA },
    shading: opts.header ? { fill: "2E75B6", type: ShadingType.CLEAR } : undefined,
    children: [
      new Paragraph({
        alignment: opts.center ? AlignmentType.CENTER : AlignmentType.LEFT,
        children: [
          new TextRun({
            text,
            bold: opts.header || opts.bold,
            color: opts.header ? "FFFFFF" : "000000",
            size: opts.small ? 18 : 20,
            font: opts.mono ? "Consolas" : undefined,
          }),
        ],
      }),
    ],
  });

// Table cell containing a clickable repo-file hyperlink.
const tdRepoLink = (filePath, opts = {}) =>
  new TableCell({
    borders: cellBorders,
    margins: cellMargins,
    width: { size: opts.width, type: WidthType.DXA },
    children: [
      new Paragraph({
        alignment: AlignmentType.LEFT,
        children: [repoLink(filePath, opts)],
      }),
    ],
  });

// Figure embedding: pass desired width in inches; aspect ratio comes from PNG itself.
function figure(filename, captionText, widthInches, aspectRatio) {
  const buf = fs.readFileSync(path.join(__dirname, "figs", filename));
  const widthPx = globalThis.Math.round(widthInches * 96);
  const heightPx = globalThis.Math.round(widthPx / aspectRatio);
  return [
    new Paragraph({
      spacing: { before: 120, after: 60 },
      alignment: AlignmentType.CENTER,
      children: [new ImageRun({
        type: "png",
        data: buf,
        transformation: { width: widthPx, height: heightPx },
        altText: { title: captionText, description: captionText, name: filename },
      })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 240 },
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: captionText, italics: true, size: 18, color: "595959" })],
    }),
  ];
}

// ---------- tables ----------

const hypothesesTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [720, 6480, 2160],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("ID", { header: true, width: 720, center: true }),
      td("Pre-registered prediction (locked 2026-05-13)", { header: true, width: 6480 }),
      td("Confirms via", { header: true, width: 2160 }),
    ] }),
    new TableRow({ children: [
      td("H1", { width: 720, bold: true, center: true }),
      td("TE(Wind1VelX → PtfmPitch) > 0 and significant at p < 0.05 in DLC-A and DLC-B. Sanity check: TE(PtfmPitch → Wind1VelX) ≈ 0 (no back-action on environment).", { width: 6480, small: true }),
      td("Phase 4 KSG-TE + circular surrogates", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H2", { width: 720, bold: true, center: true }),
      td("TE(Wave1Elev → PtfmHeave) > 0 and significant, with dominant contribution in the 0.1–0.3 Hz wave band. Coherence γ²(f) shows a matching peak.", { width: 6480, small: true }),
      td("Phase 4 + scipy.signal.coherence", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H3", { width: 720, bold: true, center: true }),
      td("Conditional TE(wind → pitch | wave) ≈ bivariate TE in DLC-B (decoupled wind/wave seeds), but < 80 % of bivariate TE in DLC-A (correlated seeds). Demonstrates conditional TE removes spurious coupling.", { width: 6480, small: true }),
      td("DLC-A vs DLC-B contrast", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H4", { width: 720, bold: true, center: true }),
      td("Sobol ST(EA | std(PtfmSurge)) > 0.5 AND ST(L_u | std(PtfmSurge)) > 0.2; aggregate geometry contribution ΣST(D_*, R_MO, H_*) < 0.3.", { width: 6480, small: true }),
      td("Phase 5 Sobol", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H5", { width: 720, bold: true, center: true }),
      td("Fairlead-tension trade-off is wave-driven not wind-driven: ST(EA | std(FAIRTEN1)) > ST(geometry-combined | std(FAIRTEN1)); conditional TE(wave → FAIRTEN1 | wind) > 2 × conditional TE(wind → FAIRTEN1 | wave).", { width: 6480, small: true }),
      td("Phase 5 + Phase 4 conditional", { width: 2160, small: true }),
    ] }),
    new TableRow({ children: [
      td("H6", { width: 720, bold: true, center: true }),
      td("Local-in-time TE(wave → PtfmPitch) shows a PSD peak at the platform pitch natural frequency (~0.0345 Hz for VolturnUS-S).", { width: 6480, small: true }),
      td("Phase 4 spectral decomposition", { width: 2160, small: true }),
    ] }),
  ],
});

// Theory references → repo
const theoryRefsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2880, 3600, 2880],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Concept", { header: true, width: 2880 }),
      td("Repo path (in this project)", { header: true, width: 3600 }),
      td("Primary reference", { header: true, width: 2880 }),
    ] }),
    ...[
      ["Transfer entropy", "pages/concepts/transfer-entropy.md", "Schreiber 2000"],
      ["KSG estimator", "pages/concepts/ksg-estimator.md", "Kraskov et al. 2004"],
      ["Conditional / multivariate TE", "pages/concepts/conditional-transfer-entropy.md", "Lizier 2014; Wollstadt 2019"],
      ["Mutual information", "pages/concepts/mutual-information.md", "Cover & Thomas 2006"],
      ["Surrogate significance", "pages/concepts/surrogate-significance.md", "Schreiber 2000 §IV"],
      ["Sobol sensitivity", "pages/concepts/sobol-sensitivity.md", "Saltelli et al. 2008"],
      ["TE equation", "pages/equations/eq-transfer-entropy.md", "—"],
      ["Sobol first-order index", "pages/equations/eq-sobol-first-order.md", "—"],
      ["Sobol total-order index", "pages/equations/eq-sobol-total.md", "—"],
    ].map(row => new TableRow({ children: [
      td(row[0], { width: 2880, small: true, bold: true }),
      tdRepoLink(row[1], { width: 3600, small: true }),
      td(row[2], { width: 2880, small: true }),
    ] })),
  ],
});

const designVarsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [600, 2160, 1200, 1800, 1800, 1800],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("#", { header: true, width: 600, center: true }),
      td("Variable", { header: true, width: 2160 }),
      td("Symbol", { header: true, width: 1200, center: true }),
      td("Lower (−20 %)", { header: true, width: 1800, center: true }),
      td("Baseline (IEA-15)", { header: true, width: 1800, center: true }),
      td("Upper (+20 %)", { header: true, width: 1800, center: true }),
    ] }),
    ...[
      ["1", "Main column diameter", "D_MCol", "8.00 m", "10.00 m", "12.00 m"],
      ["2", "Offset column diameter", "D_OCol", "10.00 m", "12.50 m", "15.00 m"],
      ["3", "Offset column radius (spacing)", "R_MO", "41.40 m", "51.75 m", "62.10 m"],
      ["4", "Pontoon diameter (equivalent)", "D_Pt", "7.69 m", "9.61 m", "11.54 m"],
      ["5", "Pontoon height", "H_Pt", "5.60 m", "7.00 m", "8.40 m"],
      ["6", "Freeboard", "H_FB", "12.00 m", "15.00 m", "18.00 m"],
      ["7", "Draft", "H_Draft", "16.00 m", "20.00 m", "24.00 m"],
      ["8", "Mooring axial stiffness", "EA", "2.62 × 10⁹ N", "3.27 × 10⁹ N", "3.92 × 10⁹ N"],
      ["9", "Mooring unstretched length", "L_u", "680 m", "850 m", "1020 m"],
    ].map(row => new TableRow({ children: [
      td(row[0], { width: 600, center: true }),
      td(row[1], { width: 2160, small: true }),
      td(row[2], { width: 1200, center: true, mono: true, small: true }),
      td(row[3], { width: 1800, center: true, small: true }),
      td(row[4], { width: 1800, center: true, small: true }),
      td(row[5], { width: 1800, center: true, small: true }),
    ] })),
  ],
});

const channelsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2160, 7200],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Group", { header: true, width: 2160 }),
      td("Channels", { header: true, width: 7200 }),
    ] }),
    new TableRow({ children: [
      td("Structural loads", { width: 2160, bold: true, small: true }),
      td("RootMyc1 (blade-1 root flapwise moment), RootMxc1 (edgewise), TwrBsMyt (tower-base fore-aft moment)", { width: 7200, small: true, mono: true }),
    ] }),
    new TableRow({ children: [
      td("Platform motions", { width: 2160, bold: true, small: true }),
      td("PtfmHeave, PtfmSurge, PtfmPitch", { width: 7200, small: true, mono: true }),
    ] }),
    new TableRow({ children: [
      td("Mooring tensions", { width: 2160, bold: true, small: true }),
      td("FAIRTEN1, FAIRTEN2, FAIRTEN3 (fairlead line tensions)", { width: 7200, small: true, mono: true }),
    ] }),
    new TableRow({ children: [
      td("Environment", { width: 2160, bold: true, small: true }),
      td("Wind1VelX (longitudinal wind at hub), Wave1Elev (sea-surface elevation at platform)", { width: 7200, small: true, mono: true }),
    ] }),
  ],
});

// Detailed per-channel description table.
const channelsDescriptionTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1620, 1440, 3420, 1080, 1800],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Channel", { header: true, width: 1620 }),
      td("Group", { header: true, width: 1440 }),
      td("Physical quantity", { header: true, width: 3420 }),
      td("Units", { header: true, width: 1080, center: true }),
      td("Sign / convention", { header: true, width: 1800 }),
    ] }),
    ...[
      ["Wind1VelX", "Environment", "Longitudinal (along-wind) wind speed at hub height (150 m)", "m/s", "+ x downwind"],
      ["Wave1Elev", "Environment", "Sea-surface elevation η at platform reference point", "m", "+ up from SWL"],
      ["PtfmSurge", "Platform motion", "Platform centre-of-mass longitudinal displacement", "m", "+ x downwind"],
      ["PtfmHeave", "Platform motion", "Platform centre-of-mass vertical displacement", "m", "+ z up"],
      ["PtfmPitch", "Platform motion", "Platform rotation about the transverse (y) axis", "deg", "+ bow up"],
      ["RootMyc1", "Structural load", "Blade-1 root flapwise (out-of-plane) bending moment", "kN·m", "+ pressure side"],
      ["RootMxc1", "Structural load", "Blade-1 root edgewise (in-plane) bending moment", "kN·m", "+ leading edge"],
      ["TwrBsMyt", "Structural load", "Tower-base fore-aft bending moment (about y axis)", "kN·m", "+ downwind tilt"],
      ["FAIRTEN1", "Mooring", "Fairlead line-1 tension (upwind-pointing line 1)", "kN", "+ tensile load"],
      ["FAIRTEN2", "Mooring", "Fairlead line-2 tension (~120° from line 1)", "kN", "+ tensile load"],
      ["FAIRTEN3", "Mooring", "Fairlead line-3 tension (~240° from line 1)", "kN", "+ tensile load"],
    ].map(row => new TableRow({ children: [
      td(row[0], { width: 1620, bold: true, mono: true, small: true }),
      td(row[1], { width: 1440, small: true }),
      td(row[2], { width: 3420, small: true }),
      td(row[3], { width: 1080, center: true, small: true }),
      td(row[4], { width: 1800, small: true }),
    ] })),
  ],
});

const teSettingsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [3000, 3000, 3360],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Parameter", { header: true, width: 3000 }),
      td("Value", { header: true, width: 3000, center: true }),
      td("Justification", { header: true, width: 3360 }),
    ] }),
    ...[
      ["Source sample rate", "40 Hz (OpenFAST DT_Out = 0.025 s)", "Native OpenFAST output"],
      ["Decimated rate", "5 Hz", "KSG O(N²) tractability + TE rate-invariance"],
      ["Transient drop", "600 s of 3600 s run", "OpenFAST startup transient"],
      ["Effective samples per case", "N = 15 001", "(3600 − 600) × 5 + 1"],
      ["Jitter scale", "1 × 10⁻¹⁰", "Kraskov 2004 §III.A — break NN degeneracy"],
      ["KSG k (NN count)", "k = 4", "Kraskov 2004 recommendation k ∈ [2,4]"],
      ["Embedding (max lag)", "150 samples = 30 s window", "Covers one slow-drift cycle (pitch eigenfreq ≈ 0.034 Hz). Raised 2026-05-20 from 30 after the slow-drift physics check (§6.3)."],
      ["Coherence NPERSEG", "4096 samples", "Welch Δf ≈ 0.0012 Hz; resolves pitch eigenfreq from JONSWAP peak"],
      ["Surrogate type", "Circular shift", "Preserves spectrum + amplitude exactly"],
      ["Surrogate count", "200 (planned)", "Resolves p down to ~0.005"],
      ["Significance threshold", "α = 0.05", "Two-sided per pair, max-stat family correction"],
    ].map(row => new TableRow({ children: [
      td(row[0], { width: 3000, small: true }),
      td(row[1], { width: 3000, center: true, small: true }),
      td(row[2], { width: 3360, small: true }),
    ] })),
  ],
});

const phaseStatusTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1080, 2880, 1440, 3960],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Phase", { header: true, width: 1080, center: true }),
      td("Description", { header: true, width: 2880 }),
      td("Status", { header: true, width: 1440, center: true }),
      td("Output / next action", { header: true, width: 3960 }),
    ] }),
    ...[
      ["1", "Knowledge base (Obsidian vault + vendored reference repos)", "Complete",
        [new TextRun({ text: "48 pages, 7 repos, 4 primary references ingested", size: 18 })]],
      ["2", "OpenFAST DLC matrix (DLC-1.6 + DLC-A + DLC-B)", "Complete",
        [new TextRun({ text: "54 cases, 268 MB .outb each, ~14 GB total", size: 18 })]],
      ["3", "Preprocessing (load, decimate, jitter, normalise)", "Embedded",
        [new TextRun({ text: "Implemented as front-end of ", size: 18 }),
         repoLink("analysis/te_pipeline.py", { small: true })]],
      ["4", "TE pipeline (Bivariate, Conditional, Granger, AIS, coherence)", "Validated",
        [new TextRun({ text: "Smoke succeeded; full-campaign scope under decision", size: 18 })]],
      ["5", "RAFT Sobol + KSG-MI on 9 design variables", "Preliminary",
        [new TextRun({ text: "N=64 done (44 % feasible); N=256 production ~5 min", size: 18 })]],
      ["6", "Combined causal graph + figures + manuscript", "Pending",
        [new TextRun({ text: "Awaits Phase 4 results; plots.py to be written", size: 18 })]],
    ].map(row => new TableRow({ children: [
      td(row[0], { width: 1080, center: true, bold: true }),
      td(row[1], { width: 2880, small: true }),
      td(row[2], { width: 1440, center: true, small: true, bold: true }),
      new TableCell({
        borders: cellBorders, margins: cellMargins,
        width: { size: 3960, type: WidthType.DXA },
        children: [new Paragraph({ children: row[3] })],
      }),
    ] })),
  ],
});

const tradeoffsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [2520, 1080, 4320, 1440],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Scope-reduction option", { header: true, width: 2520 }),
      td("Speedup", { header: true, width: 1080, center: true }),
      td("Effect on inference quality", { header: true, width: 4320 }),
      td("Wall time", { header: true, width: 1440, center: true }),
    ] }),
    new TableRow({ children: [
      td("A. Surrogate count 200 → 50", { width: 2520, small: true }),
      td("4×", { width: 1080, center: true, small: true }),
      td("p-value resolution drops from 0.005 to 0.02; α = 0.05 still defensible. Borderline cases (p ≈ 0.04) less certain.", { width: 4320, small: true }),
      td("~7 days", { width: 1440, center: true, small: true }),
    ] }),
    new TableRow({ children: [
      td("B. Bivariate-only first pass", { width: 2520, small: true }),
      td("3×", { width: 1080, center: true, small: true }),
      td("Skips conditional TE + Granger baseline initially; H3 contrast deferred.", { width: 4320, small: true }),
      td("~9 days", { width: 1440, center: true, small: true }),
    ] }),
    new TableRow({ children: [
      td("C. Ensemble TE (Wollstadt 2014, Q10)", { width: 2520, small: true }),
      td("6× effective", { width: 1080, center: true, small: true }),
      td("Pool 6 seeds per DLC bin into one estimator. Sharper significance via N_eff scaling. Reframes paper as methodology contribution.", { width: 4320, small: true }),
      td("~5 days", { width: 1440, center: true, small: true }),
    ] }),
  ],
});

// Repository documentation index (appendix)
const repoDocsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [3000, 6360],
  rows: [
    new TableRow({ tableHeader: true, children: [
      td("Path", { header: true, width: 3000 }),
      td("Purpose", { header: true, width: 6360 }),
    ] }),
    ...[
      ["PLAN.md", "Full project plan, all six phases, publication strategy"],
      ["SCHEMA.md", "Wiki structure, naming conventions, frontmatter spec"],
      ["LLM_Wiki_Pattern.md", "Three-layer wiki methodology"],
      ["SERVER_DEPLOYMENT.md", "65-core Linux server setup instructions"],
      ["PER_ROUND_CHECKLIST.md", "Recurring server round-trip workflow"],
      ["pages/log.md", "Chronological narrative log of all major changes"],
      ["pages/open-questions.md", "All open / resolved questions Q0–Q11"],
      ["pages/index.md", "Top-level wiki index with backlinks"],
      ["pages/concepts/", "Concept pages (TE, KSG, conditional TE, MI, Sobol, surrogates)"],
      ["pages/equations/", "Standalone equation pages with derivations"],
      ["pages/entities/", "Per-module entity pages (OpenFAST-AeroDyn, -ElastoDyn, -HydroDyn, -ServoDyn, …; IDTxl; RAFT; SALib; ROSCO)"],
      ["pages/sources/", "Per-source pages for ingested references (Schreiber 2000, Kraskov 2004, Wollstadt 2019, Jeon 2025)"],
      ["pages/papers/", "Deep analytical reading-notes pages for key references"],
      ["pages/validation/", "Four verification cases (r-test parse, AR1 TE recovery, IEA-15 single-case TE, Sobol 3-pt mooring-EA)"],
      ["pages/cookbook/", "Operational how-to pages (run-one-openfast-case, build-saltelli-ensemble)"],
      ["analysis/te_pipeline.py", "Phase 4 TE production pipeline (Bivariate, Conditional, Granger, AIS, coherence)"],
      ["analysis/load_runs.py", ".outb → pandas DataFrame parser with channel-name resolution"],
      ["sims/run_campaign.py", "Phase 2 DLC matrix driver (templating + parallel OpenFAST)"],
      ["sims/run_raft_lhs.py", "Phase 5 RAFT Saltelli ensemble driver"],
      ["pipeline.py", "Top-level orchestrator with idempotent per-phase skip logic"],
    ].map(row => new TableRow({ children: [
      tdRepoLink(row[0], { width: 3000, small: true }),
      td(row[1], { width: 6360, small: true }),
    ] })),
  ],
});

// ---------- content ----------

const children = [
  // Title block
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 60 },
    children: [new TextRun({ text: "Technical Report", bold: true, size: 36 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({
      text: "Causal Effect Analysis on a Floating Offshore Wind Turbine via Transfer Entropy",
      bold: true, size: 28, color: "2E75B6",
    })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [
      new TextRun({ text: "Reference platform: ", bold: true }),
      new TextRun({ text: "IEA-15 MW on UMaine VolturnUS-S semisubmersible" }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [
      new TextRun({ text: "Methods: ", bold: true }),
      new TextRun({ text: "Bivariate + conditional KSG transfer entropy (IDTxl); Sobol global sensitivity on RAFT" }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [
      new TextRun({ text: "Status: ", bold: true }),
      new TextRun({ text: "Phases 1–2 complete, Phase 4 validated and scope-bounded, Phase 5 preliminary (N=64)" }),
    ],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 360 },
    children: [
      new TextRun({ text: "Project repository (open code + reproducible decks): ", italics: true, size: 18, color: "595959" }),
      new TextRun({ text: "github.com/sinahdme/fowt-te-causal", font: "Consolas", size: 18, color: "595959" }),
    ],
  }),

  // ----- Abstract -----
  h1("Abstract"),
  para([
    t("This report presents the design, current status, and preliminary findings of a methodology that combines "),
    b("Transfer Entropy (TE)"),
    t(" and "),
    b("Sobol global sensitivity analysis"),
    t(" to construct a directed causal graph for the dynamic response of a floating offshore wind turbine (FOWT). The reference platform is the IEA-15 MW reference turbine on the UMaine VolturnUS-S semisubmersible. The two arms of the methodology — TE for time-varying environmental forcing and Sobol for constants-per-run design parameters — are merged into a single weighted causal graph in which edge weight reports the externally-driven fraction of response predictability."),
  ]),
  para([
    t("All 54 OpenFAST runs in the DLC matrix (1 hour simulated each) have completed. The TE pipeline has been validated end-to-end and produces interpretable output. A preliminary Sobol analysis at N = 64 yields a partial-confirmation of pre-registered hypothesis H4: mooring unstretched length L"),
    new TextRun({ text: "u", subScript: true }),
    t(" is the dominant driver of platform-surge variability (ST(L_u | std(PtfmSurge)) = 0.82, above the H4 threshold of 0.2), but mooring axial stiffness EA — predicted by H4 to dominate — yields ST = 0.09, well below its 0.5 threshold. The N = 64 result is qualified by median-imputation bias on the 44 %-feasible subset; the production N = 256 run will sharpen these numbers. The first TE smoke test on a single DLC-1.6 case returned "),
    it("TE(wind → pitch) ≈ 0"),
    t(", interpreted as consistent with wave-driven dynamics dominating the severe sea state plus the ROSCO controller's role in rejecting the wind disturbance. The DLC-A campaign at normal turbulence and four wind speeds will be the proper test of hypothesis H1."),
  ]),
  para([
    t("This document focuses on the methodology, experimental setup, and findings. Theoretical derivations and concept-by-concept explanations are deferred to the project repository (see Appendix A); this preserves brevity here and lets the project documentation serve as the authoritative source for those topics."),
  ]),

  // ----- 1. Introduction -----
  h1("1. Introduction"),

  h2("1.1 Motivation"),
  para([
    t("The dynamic response of a floating offshore wind turbine (FOWT) to its environment is the output of a coupled aero-hydro-servo-elastic system. This work models that system with the standard open-source toolchain. The "),
    b("coupled-physics modules"),
    t(" are: "),
    b("TurbSim"),
    t(" (turbulent inflow generation) feeding "),
    b("AeroDyn 15"),
    t(" (blade-element-momentum aerodynamics with tip-loss and dynamic stall); "),
    b("ElastoDyn"),
    t(" for the rotor, drivetrain, nacelle, tower, and platform structural dynamics (with "),
    b("BeamDyn"),
    t(" available for higher-order blade deformation when needed); "),
    b("HydroDyn"),
    t(" for hydrodynamic forcing (linear potential-flow from WAMIT augmented with Morison strip-theory drag); "),
    b("SeaState"),
    t(" for irregular wave construction (JONSWAP for normal-turbulence DLCs, SSS for the severe-sea bin); "),
    b("MoorDyn"),
    t(" for lumped-mass dynamic catenary moorings (with "),
    b("MoorPy"),
    t(" available for quasi-static cross-checks); and "),
    b("ServoDyn"),
    t(" interfacing with the "),
    b("ROSCO"),
    t(" reference controller library for active blade-pitch and generator-torque control. All modules are orchestrated by "),
    b("OpenFAST"),
    t(" (v4.2.1). Figure 1 shows how they couple — external conditions drive applied loads, which in turn drive the structural / control modules, with ServoDyn closing the loop between platform-pitch motion and rotor actuation."),
  ]),
  para([
    t("Downstream of the simulations, the "),
    b("post-processing and analysis stack"),
    t(" is: "),
    b("openfast_toolbox"),
    t(" for OpenFAST `.outb` parsing; "),
    b("IDTxl"),
    t(" with the "),
    b("JIDT"),
    t(" Java backend for KSG transfer-entropy estimation; "),
    b("SALib"),
    t(" on a "),
    b("RAFT"),
    t(" frequency-domain surrogate for Sobol global sensitivity on the design-variable sweep; and scipy / pandas / NetworkX for preprocessing, the linear baselines, and the final causal-graph assembly."),
  ]),
  ...figure("fig0-openfast-modules.png",
    "Figure 1. OpenFAST coupled aero-hydro-servo-elastic module architecture used in this work. External conditions (TurbSim-generated wind, JONSWAP/SSS waves via SeaState) feed applied-load modules (AeroDyn 15, HydroDyn); the wind-turbine column is grouped by structural / control module (ServoDyn with ROSCO; ElastoDyn with optional BeamDyn; MoorDyn). OpenFAST 4.2.1 orchestrates the coupled time-step integration. Adapted and updated from Jonkman & NREL.",
    6.5, 13 / 9),
  para([
    t("The standard analysis approach for such systems is "),
    b("simulation + sensitivity"),
    t(" — Sobol or Morris indices on response summary statistics across a parameter sweep — supplemented by linear cross-spectral methods (coherence, transfer functions) for frequency-domain interpretation."),
  ]),
  para([
    t("Both approaches have known limitations for causal questions. Sobol indices are "),
    b("undirected"),
    t(" and assess only variance contribution; they say nothing about the response paths a parameter acts through. Linear coherence and Granger causality assume Gaussian dynamics and linear coupling; they miss nonlinear couplings such as wave-induced surge-pitch interaction, controller-mediated rotor-thrust modulation, and threshold-driven mooring tension events. Neither gives a "),
    b("directed, nonlinear, multivariate"),
    t(" view of the causal structure."),
  ]),
  para([
    t("Transfer entropy (Schreiber 2000) is a directed, nonlinear, multivariate information-theoretic measure of directed causal flow between time series, and its KSG estimator (Kraskov et al. 2004) is the standard for continuous variables. The present work is the first systematic application of this machinery to FOWT response analysis, with the practical goal of "),
    b("disentangling wave-driven, wind-driven, and controller-mediated paths"),
    t(" to platform motion, structural loads, and mooring tensions — and of explaining the design-trade-off observed by Jeon et al. (2025) in which mass-only optimisation of an IEA-22 MW semi produced a substantial fairlead-tension penalty that pure sensitivity ranking could not attribute."),
  ]),

  h2("1.2 Why the IEA-15 MW UMaineSemi was selected as the starting platform"),
  para([
    t("Five reasons led to selecting the IEA-15 MW on UMaine VolturnUS-S as the v1 reference platform, ahead of alternative FOWT options (OC4-DeepCWind, OC3-Hywind, IEA-22 MW Semi, real industry geometries):"),
  ]),
  numbered([
    b("Open and fully documented."),
    t(" The IEA Wind Task 37 design (Gaertner et al. 2020) and the UMaine VolturnUS-S definition (Allen et al. 2020) ship with a complete OpenFAST input deck, baseline ROSCO controller (Abbas et al. 2022), WAMIT hydrodynamic coefficients, and a published parameter-by-parameter justification. No proprietary or estimated values are required."),
  ]),
  numbered([
    b("Validation maturity."),
    t(" The IEA-15 / VolturnUS-S combination has been extensively cross-checked through the OC6 verification project, with experimental tank-test anchor data publicly available. Any pre-registered hypothesis (§1.3) can be argued against a validated reference baseline, which strengthens defensibility."),
  ]),
  numbered([
    b("Direct continuity with the predecessor study."),
    t(" Jeon et al. (2025) used the IEA-22 MW Semi, which is geometrically a scale-up of the same UMaine semi family. Phase 5 design-variable sweep and the Q9 fairlead-tension trade-off (the engineering takeaway candidate) port directly between IEA-15 and IEA-22 at the variable-name level. Choosing IEA-15 first preserves the v2 multi-platform extension toward IEA-22 with no methodological discontinuity."),
  ]),
  numbered([
    b("Deep-water site (200 m design depth)."),
    t(" Linear wave theory and HydroDyn's potential-flow + Morison hybrid is appropriate at this depth, removing the need for shallow-water phase-resolved wave models (SWASH, FUNWAVE) that would dramatically expand computational scope. The standard JONSWAP / SSS irregular-wave generator inside HydroDyn is sufficient."),
  ]),
  numbered([
    b("15 MW is the published reference class."),
    t(" Most current floating-wind academic literature uses either the NREL 5 MW (legacy) or the IEA 15 MW (current). The 15 MW choice maximises citation overlap with the existing TE-on-wind-turbine literature and the wind-energy methodology community more broadly. IEA-22 (Q5 stretch) is the v2 extension; IEA-15 is the v1 starting point."),
  ]),

  h2("1.3 Methodology overview, project phases, and pre-registered hypotheses"),
  para([
    t("The methodology consists of two parallel arms — one for time-varying environmental forcing, one for constants-per-run design parameters — combined into a single causal graph. Figure 2 shows the high-level structure."),
  ]),
  ...figure("fig1-methodology-arms.png",
    "Figure 2. Methodology arms. The TE arm operates on OpenFAST time-series output via IDTxl bivariate and conditional KSG estimators with circular surrogates. The Sobol arm operates on RAFT-evaluated design-variable sweeps via SALib first- and total-order indices. Outputs merge into the Phase-6 combined causal graph.",
    6.5, 11 / 8),
  para([
    t("The work is organised into six phases that map onto the methodology arms in Figure 2:"),
  ]),
  code("Phase 1   Knowledge base       Obsidian vault + vendored reference repositories"),
  code("Phase 2   Simulation campaign  OpenFAST DLC matrix (54 cases × 1 hour)"),
  code("Phase 3   Data extraction      Parse .outb, preprocess (transient drop, decimate, jitter, normalise)"),
  code("Phase 4   TE pipeline          IDTxl KSG bivariate + conditional, Granger and coherence baselines"),
  code("Phase 5   Parameter sensitivity   RAFT Saltelli ensemble + SALib Sobol indices + KSG-MI ranking"),
  code("Phase 6   Reporting            Combined causal graph + publication figures + manuscript"),
  para([
    t("Driver scripts: "),
    repoLink("sims/run_campaign.py"),
    t(" (Phase 2), "),
    repoLink("analysis/load_runs.py"),
    t(" + "),
    repoLink("analysis/te_pipeline.py"),
    t(" (Phases 3–4), "),
    repoLink("sims/run_raft_lhs.py"),
    t(" (Phase 5), all coordinated by "),
    repoLink("pipeline.py"),
    t("."),
  ]),
  para([
    t("Phase 1 builds the knowledge base; Phase 2 runs the OpenFAST simulation campaign. Phase 3 is not a standalone phase but the preprocessing front-end embedded in the Phase 4 driver (transient drop, decimation, jitter, normalisation — see §4.3). Phases 4 and 5 are the two analytical arms shown in Figure 2 — they can in principle run in parallel since they consume different inputs (time series vs. summary statistics over a design-variable sweep). Phase 6 merges their outputs into a single weighted directed graph that supports both environmental and design-parameter edges, alongside the publication figures and the narrative discussion."),
  ]),
  para([
    t("Six hypotheses were locked on 2026-05-13, "),
    b("before any simulation runs"),
    t(", to defend against post-hoc statistical fishing. Each is evaluated as confirmed / partially-confirmed / not-confirmed against the explicit numeric thresholds below."),
  ]),
  tableCaption(1, "Pre-registered hypotheses H1–H6 (locked 2026-05-13)."),
  hypothesesTable,
  para([
    t("H1–H3 are the environmental-TE tests; H4–H5 are the parameter-sensitivity tests; H6 is the spectral-decomposition test. Methodologically, H3 (DLC-A vs DLC-B contrast) and H5 (wave-driven fairlead-tension trade-off) are the strongest tests of the combined-method value, because each requires both bivariate and conditional TE, or both TE and Sobol, to reach its conclusion."),
  ]),

  // ----- 2. Theoretical Background (TRIMMED — point to repo) -----
  h1("2. Theoretical Background"),
  para([
    t("This section provides a concise summary of the methods used. Full mathematical derivations, worked examples, and the foundational references are documented as standalone concept and equation pages in the project repository — each concept name below is hyperlinked to its authoritative page. Appendix A contains the complete documentation index. Readers familiar with the IDTxl / Wollstadt-2019 methodology stack may skip ahead to §3."),
  ]),

  h2("2.1 Transfer entropy in one paragraph"),
  para([
    new ExternalHyperlink({
      link: `${REPO_URL}/pages/concepts/transfer-entropy.md`,
      children: [new TextRun({ text: "Transfer entropy", color: "2E75B6", underline: { type: "single" } })],
    }),
    t(" from source X to target Y is the "),
    new ExternalHyperlink({
      link: `${REPO_URL}/pages/concepts/mutual-information.md`,
      children: [new TextRun({ text: "conditional mutual information", color: "2E75B6", underline: { type: "single" } })],
    }),
  ]),
  displayMath([
    mrun("TE(X → Y) = I("),
    msub("Y", "t"),
    mrun(" ; "),
    msub("X", "t−1:t−l"),
    mrun(" | "),
    msub("Y", "t−1:t−k"),
    mrun(")"),
  ]),
  para([
    t("measuring the reduction in uncertainty about Y"),
    new TextRun({ text: "t", subScript: true }),
    t(" gained from X's past, beyond what Y's own past already provides. It is "),
    b("directed"),
    t(", "),
    b("nonlinear"),
    t(", and "),
    b("non-negative"),
    t(". We estimate it with the "),
    new ExternalHyperlink({
      link: `${REPO_URL}/pages/concepts/ksg-estimator.md`,
      children: [new TextRun({ text: "KSG estimator", color: "2E75B6", underline: { type: "single" } })],
    }),
    t(" (Kraskov 2004) via IDTxl's JIDT backend (Lizier 2014; Wollstadt et al. 2019). "),
    new ExternalHyperlink({
      link: `${REPO_URL}/pages/concepts/conditional-transfer-entropy.md`,
      children: [new TextRun({ text: "Conditional TE", bold: true, color: "2E75B6", underline: { type: "single" } })],
    }),
    t(" extends this by adding a third process Z to the conditioning set, removing Z-mediated confounders (the cornerstone of pre-registered hypothesis H3)."),
  ]),

  h2("2.2 Effect-size normalisation and surrogate significance"),
  para([
    t("Raw TE values are normalised by the "),
    b("Active Information Storage"),
    t(" of the target, defined as"),
  ]),
  displayMath([
    mrun("AIS(Y) = I("),
    msub("Y", "t"),
    mrun(" ; "),
    msub("Y", "t−1:t−k"),
    mrun(")"),
  ]),
  para([
    t("giving the normalised effect size"),
  ]),
  displayMath([
    new MathFraction({
      numerator: [mrun("TE(X → Y)")],
      denominator: [mrun("H("), msub("Y", "t"), mrun(") − AIS(Y)")],
    }),
    mrun("  =  "),
    msub("TE", "frac"),
  ]),
  para([
    t("which is the fraction of externally-driven predictability of "),
    new TextRun({ text: "Y", italics: true }),
    new TextRun({ text: "t", italics: true, subScript: true }),
    t(" provided by X. Significance is assessed via "),
    new ExternalHyperlink({
      link: `${REPO_URL}/pages/concepts/surrogate-significance.md`,
      children: [new TextRun({ text: "circular-shift surrogates", bold: true, color: "2E75B6", underline: { type: "single" } })],
    }),
    t(" (the source is shifted by a random amount; spectrum preserved exactly; coupling destroyed), with 200 surrogates resolving p-values down to ~0.005."),
  ]),

  h2("2.3 The closed-loop / controller-mediated case"),
  para([
    t("Schreiber's original TE was open-loop; for a controlled system like an FOWT, the controller observes Y and acts on the path X → Y, suppressing the observed TE without changing the underlying causality (Massey 1990, Lizier 2014). Two practical consequences for this work:"),
  ]),
  bullet([
    b("TE direction is preserved"),
    t(" for an exogenous driver such as wind — wind is not affected by the controller's actions, so TE(pitch → wind) ≈ 0 (the H1 back-action sanity check)."),
  ]),
  bullet([
    b("TE magnitude can be heavily suppressed"),
    t(" by an effective controller: a perfect rejection pushes TE(wind → pitch) toward zero by design. This motivates the controller-off comparison filed as Q11 in the "),
    repoLink("pages/open-questions.md"),
    t("."),
  ]),

  h2("2.4 Sobol global sensitivity for constants-per-run parameters"),
  para([
    t("Transfer entropy does not apply to design parameters that are fixed per OpenFAST run. For these, "),
    new ExternalHyperlink({
      link: `${REPO_URL}/pages/concepts/sobol-sensitivity.md`,
      children: [new TextRun({ text: "Sobol global sensitivity", color: "2E75B6", underline: { type: "single" } })],
    }),
    t(" on a Saltelli sample provides first-order indices S"),
    new TextRun({ text: "1", subScript: true }),
    t(" (variance contribution of one parameter alone) and total-order indices S"),
    new TextRun({ text: "T", subScript: true }),
    t(" (including interactions). To make a 704-evaluation Saltelli sample tractable, we use "),
    b("RAFT"),
    t(" (Hall 2022) — the frequency-domain coupled solver — for the sweep and reserve OpenFAST for the time-domain Phase 4 TE on the validated DLC matrix."),
  ]),

  // §2.5 deleted in this revision — concept pages and equation pages are now
  // hyperlinked directly from the prose and from Appendix A, which removes the
  // need for a dedicated references-to-repo table.

  // ----- 3. System modelling -----
  h1("3. System Modelling"),

  h2("3.1 Reference platform"),
  para([
    t("The reference design is the IEA Wind Task 37 15 MW reference wind turbine (Gaertner et al. 2020) mounted on the UMaine VolturnUS-S semisubmersible (Allen et al. 2020). The selection rationale was given in §1.2."),
  ]),

  h2("3.2 OpenFAST configuration"),
  para([
    t("All simulations use OpenFAST 4.2.1 with the standard module set: AeroDyn 15 (BEM + tip-loss + dynamic stall), ElastoDyn (multibody blade and tower with pitch and torque inputs from ServoDyn), HydroDyn (linear potential-flow from WAMIT in IEA-15-240-RWT/HydroData + strip-theory Morison for viscous drag), SeaState (irregular waves; JONSWAP for DLC-A/B; SSS for DLC-1.6), ServoDyn + ROSCO (open-source reference controller as a shared library libdiscon.so), and MoorDyn (lumped-mass dynamic mooring with three catenary lines)."),
  ]),
  para([
    t("Active ServoDyn ("),
    mono("CompServo = 1"),
    t(") is engaged throughout; ROSCO is the IEA-15-tuned baseline including the platform-pitch feedback term that improves floating-platform stability. The HydroDyn deck has the full difference-frequency second-order QTF enabled ("),
    mono("DiffQTF = 12"),
    t(", using the WAMIT "),
    mono(".12s"),
    t(" file shipped with the IEA-15 deck) — so the simulated platform-pitch slow-drift dynamics at the pitch eigenfrequency are excited by the same second-order wave forcing that drives the real platform. Simulations run for 3600 s of physical time at 40 Hz output (DT_Out = 0.025 s); the first 600 s are discarded as initial transient. TurbSim generates synthetic turbulent wind fields with IEC NTM turbulence class B."),
  ]),

  h2("3.3 Design Load Case matrix"),
  para([
    t("Three DLC bins are simulated. Together they enable both the absolute TE analysis (H1, H2, H6), the conditional-TE validation (H3), and a cross-comparability bin with the predecessor study (Jeon et al. 2025). Figure 3 visualises the matrix structure."),
  ]),
  ...figure("fig2-dlc-matrix.png",
    "Figure 3. Phase 2 DLC matrix. 54 OpenFAST simulations × 1 hour simulated time = ~14 GB of raw .outb output. DLC-1.6 is the predecessor cross-comparability bin (severe sea state, wave-dominated). DLC-A is the primary TE test (NTM + correlated wind-wave seeds). DLC-B mirrors DLC-A's wind seeds but decouples the wave seeds via XOR; the A-vs-B contrast is the conditional-TE validation for H3.",
    6.5, 12 / 7),
  para([
    t("Six wind seeds (deterministic 7-digit primes) per (DLC, wind speed) combination provide the statistical ensemble. The XOR mask "),
    mono("0x5A5A5A5A"),
    t(" decouples DLC-B's wave seeds from its wind seeds while keeping the construction reproducible — DLC-A and DLC-B share marginal wind and wave statistics but differ in their joint dependency, exactly the condition needed to test H3."),
  ]),

  h2("3.4 Output channels"),
  para([
    t("Nine response channels and two environmental channels are logged. The set is locked (Q1, 2026-05-13) and matches Jeon et al. (2025) for direct comparison. Table 2 groups the channels by category; Table 3 provides the physical-quantity description, units, and sign convention for each."),
  ]),
  tableCaption(2, "Output channels grouped by category."),
  channelsTable,
  tableCaption(3, "Per-channel description, units, and sign convention. Channels marked PtfmSurge / PtfmHeave / PtfmPitch / RootMyc1 / RootMxc1 / TwrBsMyt / FAIRTEN1–3 are the nine response channels analysed in the TE pipeline; Wind1VelX and Wave1Elev are the two environmental sources."),
  channelsDescriptionTable,

  // ----- 4. Methodology -----
  h1("4. Methodology"),

  h2("4.1 Pipeline architecture"),
  para([
    t("The overall analysis pipeline is implemented in Python and orchestrated by a single entry point ("),
    repoLink("pipeline.py"),
    t(") with idempotent per-phase skip logic:"),
  ]),
  code("Phase 1  Knowledge base       Obsidian vault + vendored reference repos"),
  para([t("Phase 2  Simulation           OpenFAST DLC matrix — driver: "), repoLink("sims/run_campaign.py")], { spacing: { after: 60 } }),
  para([t("Phase 3  Data extraction      Parse .outb, preprocess — "), repoLink("analysis/load_runs.py")], { spacing: { after: 60 } }),
  para([t("Phase 4  TE pipeline          IDTxl + scipy — "), repoLink("analysis/te_pipeline.py")], { spacing: { after: 60 } }),
  para([t("Phase 5  Parameter Sobol      RAFT + SALib — "), repoLink("sims/run_raft_lhs.py")], { spacing: { after: 60 } }),
  code("Phase 6  Causal graph + plots NetworkX + matplotlib"),
  p(""),

  h2("4.2 TE pipeline (Phase 4) data flow"),
  para([
    t("Figure 4 shows the per-case pipeline applied to every .outb file in the DLC matrix."),
  ]),
  ...figure("fig3-te-pipeline.png",
    "Figure 4. Per-case TE pipeline. .outb files are loaded by openfast_toolbox, preprocessed (drop transient, decimate to 5 Hz, jitter, z-score), then passed to five analyses per (source, target) pair: AIS for effect-size normalisation, KSG bivariate TE with circular surrogates, KSG conditional/multivariate TE with greedy parent-set search, Gaussian-Granger baseline via the same IDTxl pipeline with the estimator swapped, and scipy coherence γ²(f) as the linear-spectrum ceiling. Per-case long-form DataFrames are aggregated to reports/te_table.parquet plus a NetworkX directed-graph pickle.",
    6.5, 14 / 8),

  h2("4.3 Preprocessing details"),
  para([
    t("Each channel undergoes four steps in this order, per Wollstadt et al. (2019) and Kraskov et al. (2004): transient drop (600 s); decimation from 40 Hz to ~5 Hz; jitter of 10⁻¹⁰ Gaussian noise (breaks finite-precision NN degeneracy per Kraskov 2004 §III.A); z-score normalisation. After preprocessing, each case provides N = 15 001 samples per channel at 5 Hz (50 minutes of usable data)."),
  ]),

  h2("4.4 TE estimation settings"),
  tableCaption(4, "TE estimator settings and their justification."),
  teSettingsTable,
  p(""),

  h2("4.5 Per-case TE analyses"),
  para([
    t("For each .outb file the pipeline computes, for every (source, response) pair with source ∈ {Wind1VelX, Wave1Elev} and response ∈ {9 response channels}:"),
  ]),
  bullet("Bivariate KSG transfer entropy (IDTxl BivariateTE with JidtKraskovCMI), with circular surrogates and IDTxl's max-stat embedding;"),
  bullet("Conditional KSG transfer entropy TE(source → response | other-env-source) via IDTxl MultivariateTE with greedy parent-set search over both env sources;"),
  bullet([
    t("Bivariate Gaussian Granger baseline, "),
    b("via the same IDTxl pipeline"),
    t(" with the estimator swapped to JidtGaussianCMI — equivalent to classical conditional-Granger by closed-form Gaussian CMI, but with the same parent-set search and surrogate test as the KSG version. This is the apples-to-apples linear baseline (Wollstadt 2019 §Surprise 1);"),
  ]),
  bullet("Magnitude-squared coherence γ²(f) via scipy.signal.coherence, with peak detected in the 0.01–0.5 Hz band. Establishes the linear-spectrum ceiling and the frequency-domain validation for H6."),
  para([
    t("Per response channel the pipeline additionally computes AIS for use as the effect-size normaliser. Each per-case run produces a long-form pandas DataFrame with one row per (case, source, target, method) combination, written incrementally to "),
    mono("reports/te_table.parquet"),
    t(" via per-case checkpointing so that a mid-campaign crash does not lose prior cases' results."),
  ]),

  h2("4.6 Phase 5: Sobol sensitivity via the RAFT surrogate"),
  para([
    t("Phase 5 uses a SALib Saltelli sample on the nine design variables locked in §5.1. Each sample point is evaluated through the RAFT frequency-domain solver, which produces summary statistics directly; the resulting (parameter, response-statistic) array is fed to SALib's Sobol decomposition. The same parameter sweep is used for KSG mutual-information ranking, providing an information-theoretic companion to Sobol that captures nonlinear contributions Sobol can miss."),
  ]),
  para([
    t("Geometric constraints from Jeon et al. (2025) — `D_OCol > D_Pt`, `H_Pt > 0.5·D_Pt`, `H_Draft > 0.5·D_Pt + H_Pt` — are enforced in the dimensional space before RAFT evaluation. Constraint-violating points are marked infeasible and excluded from the Sobol decomposition; the fraction-infeasible is reported as a diagnostic."),
  ]),

  // ----- 5. Experimental setup -----
  h1("5. Experimental Setup"),

  h2("5.1 Design variable bounds (Phase 5)"),
  para([
    t("Nine design variables, each ±20 % around the IEA-15 VolturnUS-S baseline. The first seven are the predecessor's substructure-geometry decision variables (Jeon et al. 2025); the last two (mooring axial stiffness EA and unstretched length L"),
    new TextRun({ text: "u", subScript: true }),
    t(") are added so the causal graph can disentangle geometry-driven and mooring-driven contributions to the fairlead-tension trade-off."),
  ]),
  tableCaption(5, "Phase 5 design-variable bounds (IEA-15 baseline ±20 %)."),
  designVarsTable,
  p(""),

  h2("5.2 Computational platform"),
  para([
    t("Production simulation and analysis run on a 65-core Linux server. The conda environment "),
    mono("raft-env"),
    t(" provides OpenFAST 4.2.1 + TurbSim + ROSCO (libdiscon.so) + IDTxl + JDK 11 + SALib + scipy + pandas + openfast_toolbox. Local development and analysis use a Windows host with the same Python stack; the two machines synchronise via Git for code and rsync for results. BLAS thread counts are pinned to 1 to avoid oversubscription when running 24 simultaneous OpenFAST/TurbSim processes; see "),
    repoLink("SERVER_DEPLOYMENT.md"),
    t(" for the full deployment notes."),
  ]),

  h2("5.3 Pre-registered hypothesis thresholds"),
  para([
    t("Each H1–H6 prediction in §1.3 is paired with an evaluation criterion — numeric where applicable (H4, H5), procedural where the statistic is a categorical significance call (H1, H2: p < α). A hypothesis is reported as confirmed, partially-confirmed, or not-confirmed against that criterion. "),
    b("Not-confirmed results are reported with equal prominence"),
    t(" to confirmed ones — that is the scientific value of pre-registration."),
  ]),

  // ----- 6. Preliminary Results -----
  h1("6. Preliminary Results"),

  h2("6.1 Phase 2 simulation campaign — complete"),
  para([
    t("All 54 OpenFAST simulations completed (6 cases at DLC-1.6 + 24 at DLC-A + 24 at DLC-B). Each case produced a ~268 MB binary output file; per-case OpenFAST wall time ranged from 1416 to 1706 s (typical ~1450 s). Total output: ~14 GB."),
  ]),

  h2("6.2 Phase 4 TE pipeline — validated"),
  para([
    t("End-to-end Phase 4 was validated on a single DLC-1.6 case in smoke mode (one source-target pair, 50 surrogates):"),
  ]),
  bullet([
    b("AIS(PtfmPitch) = 4.1026 nats (p = 0.0020)"),
    t(" — platform pitch is highly self-predictive, as expected for a low-damped floating mode under continuous excitation."),
  ]),
  bullet([
    b("TE(Wind1VelX → PtfmPitch) = 0.0000 nats (p = 1.0000)"),
    t(" — the null result at DLC-1.6. The unit p-value means the observed TE fell at or below every one of the 50 circular-shift surrogates, consistent with an active controller that rejects the wind disturbance before it reaches the platform-pitch sensor (see §6.3 and §7.4); the value is not an artifact of broken code."),
  ]),
  bullet([
    b("Coherence γ²(Wind1VelX, PtfmPitch) peak in 0.01–0.5 Hz: not significant"),
    t(" at the 0.3 threshold — consistent with the TE null."),
  ]),

  h2("6.3 Interpretation of the DLC-1.6 null"),
  para([
    t("DLC-1.6 prescribes a Severe Sea State with Hs = 8.3 m and Tp = 12.95 s (first-order JONSWAP peak frequency fp ≈ 0.077 Hz). The platform pitch eigenfrequency for VolturnUS-S (~0.0345 Hz) lies in the low-frequency tail of the first-order spectrum, but is strongly excited by "),
    b("second-order difference-frequency (slow-drift) wave forcing"),
    t(", which has substantial energy at the spacings between linear wave components in the SSS spectrum. Under SSS this slow-drift excitation dominates the pitch response. In information-theoretic terms, "),
    it("AIS(PtfmPitch) = 4.10 nats"),
    t(" indicates that platform pitch already carries substantial self-predictability; the wind component (mean-flow energy ~0.02 Hz, dwarfed by the wave forcing) adds negligible additional predictive information above this floor."),
  ]),
  para([
    t("In addition, the ROSCO controller explicitly rejects wind disturbances on the platform-pitch path via its floating-feedback gain (Abbas et al. 2022). This is the closed-loop case discussed in §2.3: even where open-loop physics would produce a wind → pitch causality, the controller actively cancels it before it reaches the pitch sensor. A controller doing its job produces precisely the null TE observed."),
  ]),
  para([
    t("The H1 test is therefore not invalidated by the DLC-1.6 null. H1 is properly tested on DLC-A, where wind speeds span four operating points (8, 11, 15, 20 m/s), turbulence is NTM rather than SSS-dominant, and the rotor-thrust path is clearer. Six seeds × four wind speeds × two DLC variants (A and B) provide 48 cases for the H1 evaluation."),
  ]),

  h2("6.4 Phase 5 Sobol sensitivity (N = 64) — preliminary"),
  para([
    t("A Saltelli sample at base size N = 64 (D = 9, total 704 evaluations, second-order indices disabled) ran on RAFT. The geometric constraints in §4.6 produced 313/704 feasible (44 %). Sobol decomposition on the feasible subset, with median imputation of infeasible Y values:"),
  ]),
  bullet([
    b("Mooring unstretched length L"),
    new TextRun({ text: "u", bold: true, subScript: true }),
    b(" is the dominant driver of platform-motion summary statistics."),
    t(" ST(L_u | surge_avg) = 1.26 ± 0.67, ST(L_u | heave_std) = 1.56 ± 1.21. Indices > 1.0 indicate numerical instability from the median imputation and the relatively small feasible subset."),
  ]),
  bullet([
    b("Pre-registered H4 — partial confirmation."),
    t(" ST(L_u | std(PtfmSurge)) = 0.82 ± 0.44, "),
    b("above"),
    t(" the predicted L_u threshold of 0.2 (the L_u half of H4 is confirmed). ST(EA | std(PtfmSurge)) = 0.09 ± 0.08, "),
    b("well below"),
    t(" the predicted 0.5 threshold (the EA half is not confirmed). H4 is therefore reported as partial-confirmation; the surge-variance signal is mooring-dominated, but length L_u rather than axial stiffness EA is the active variable."),
  ]),
  para([
    t("Two caveats temper the N = 64 result:"),
  ]),
  bullet([
    b("Median imputation biases the Sobol decomposition."),
    t(" Replacing the Y of infeasible X samples with the median compresses the variance of the response and distorts the Sobol indices in a direction that is not predictable a priori. The ST > 1.0 values are the visible symptom; an unknown share of the index magnitudes is also affected. Increasing N alone does not fix this — the production N = 256 run will additionally either (i) apply rejection sampling within the feasible region, or (ii) use a constrained Saltelli scheme — the choice is Q3-extension territory and is logged in [[open-questions]]."),
  ]),
  bullet([
    b("Small feasible subset."),
    t(" 313 feasible points across nine variables is borderline for stable second-moment estimates. The N = 256 run gives ~1100 feasible points (assuming the same 44 % rate), which is the realistic regime for these confidence intervals."),
  ]),
  para([
    t("The unexpected dominance of L"),
    new TextRun({ text: "u", subScript: true }),
    t(" over EA, if it persists once both caveats are addressed, is a non-trivial finding: it suggests that mooring catenary length (which sets the static restoring stiffness via the suspended-line weight) matters more than the line's elastic stiffness in the surge response — counter to the pre-registered EA part of H4. The mechanism is physically plausible: L"),
    new TextRun({ text: "u", subScript: true }),
    t(" sets the surge natural frequency (~0.01 Hz for VolturnUS-S), which lies squarely in the slow-drift band where the dominant excitation lives (see §6.3). EA controls the line elastic stiffness, which matters at higher frequencies where the catenary geometry is approximately taut — a regime our SSS / NTM cases do not strongly excite. The L"),
    new TextRun({ text: "u", subScript: true }),
    t("-mediated surge-natural-frequency mechanism is the same one that makes the §6.3 pitch null physically interpretable."),
  ]),

  h2("6.5 Phase status overview"),
  tableCaption(6, "Status overview of the six project phases."),
  phaseStatusTable,
  p(""),

  // ----- 7. Discussion -----
  h1("7. Discussion"),

  h2("7.1 Computational scope — three options under consideration (no decision yet)"),
  para([
    t("At the originally-scoped TE settings (18 source-target pairs × 200 surrogates × 54 cases, per-pair conditional + Granger + AIS sub-tests) per-case wall time on the production server is approximately 12 hours, giving a full Phase 4 of ~27 days. JIDT is multi-threaded internally, so naive parallel execution across cases risks the thread-oversubscription problem already encountered in Phase 2."),
  ]),
  para([
    t("Three independent scope-reduction options have been identified. No decision has been made on which to adopt; this is an open question awaiting discussion with the project supervisor."),
  ]),
  tableCaption(7, "Scope-reduction options for Phase 4 — under consideration."),
  tradeoffsTable,
  para([
    t("Each option preserves the pre-registered hypotheses' testability. The combinatorial speedup of multiple options is "),
    b("approximately"),
    t(" multiplicative — for instance, A × C ≈ 20–24× — only if the conditional-TE and Granger sub-tests are still computed under C. If C is interpreted as a bivariate-only ensemble (dropping conditional + Granger), then the C-row's 6× already absorbs that reduction and A + C is closer to 4× × the residual ~3× = 12×. The actual speedup is bounded above by the originally-scoped wall time of ~27 days. The choice will be made before the next campaign launch; the decision rationale will be documented in "),
    repoLink("pages/open-questions.md"),
    t("."),
  ]),

  h2("7.2 Methodological refinement: ensemble TE (Wollstadt 2014)"),
  para([
    t("Wollstadt et al. (2014) introduced ensemble TE specifically for multi-trial designs in which the same generative process is observed across independent realisations — exactly the structure of our six seeds per DLC bin. Ensemble TE pools the realisations into a single estimator instead of computing per-seed TE and averaging post-hoc. Benefits:"),
  ]),
  bullet("Effective sample size scales as `seeds × samples` rather than `samples`, sharpening significance;"),
  bullet("Robust to within-run non-stationarity (assumes inter-realisation stationarity, a weaker condition);"),
  bullet("Produces one TE value per (source, target, DLC bin) rather than per seed, simplifying the conditional-TE contrast figure for H3 and the publication baseline tables."),
  para([
    t("Adopting ensemble TE also reframes the publication contribution from \"TE applied to FOWT\" (incremental) to \"TE methodology extended to FOWT seed ensembles\" (a genuine novelty within the wind-energy literature)."),
  ]),

  h2("7.3 Controller-mediated paths and the controller-off comparison (Q11)"),
  para([
    t("The DLC-1.6 null in §6.3 motivates a controller-off comparison run on a single DLC bin (six seeds, ~95 minutes of additional server compute): re-run with "),
    mono("CompServo = 0"),
    t(" and compute the same Phase 4 pipeline. The headline quantity"),
  ]),
  displayMath([
    mrun("Δ"),
    msub("TE", "ctrl"),
    mrun("(X → Y) = "),
    msub("TE", "ctrl-off"),
    mrun("(X → Y) − "),
    msub("TE", "ctrl-on"),
    mrun("(X → Y)"),
  ]),
  para([
    t("is then interpretable as the share of (X → Y) causality the controller absorbs via disturbance rejection. For wind → pitch this is expected to be large (the ROSCO floating-feedback gain is designed for this); for wave → heave it is expected to be near zero. The decision to commit to this run is deferred until the main controller-on campaign indicates whether H5 (controller-mediated fairlead-tension story) needs the additional evidence."),
  ]),

  h2("7.4 On direction reversal"),
  para([
    t("A subtle TE methodology point: an intermediating controller does not reverse the apparent direction of TE for an exogenous driver. Wind is unaffected by the controller's actions, so "),
    it("TE(wind → pitch)"),
    t(" ≥ 0 and "),
    it("TE(pitch → wind)"),
    t(" ≈ 0 (the H1 back-action sanity check). What the controller does change is the "),
    b("magnitude"),
    t(" of TE(wind → pitch) — a perfect controller pushes it toward zero — and it can introduce "),
    b("spurious bidirectional artifacts"),
    t(" if the controller's internal state is a hidden mediator. Conditioning on the controller's pitch-demand signal removes those artifacts."),
  ]),

  h2("7.5 Linear baselines"),
  para([
    t("Every TE result is reported alongside two linear-method baselines per Wollstadt et al. (2019): magnitude-squared coherence γ²(f) (scipy.signal.coherence) — the linear-spectrum ceiling — and bivariate plus conditional Granger causality via IDTxl with JidtGaussianCMI — directional but linear. Both come from the same IDTxl pipeline with only the estimator swapped, so the comparison is apples-to-apples (Wollstadt 2019 §Surprise 1). Cells where KSG-TE is significant and Gaussian-Granger is not are exactly the ones where the nonlinear contribution is genuine; cells where both agree validate the embedding."),
  ]),

  // ----- 8. Conclusions and Future Work -----
  h1("8. Conclusions and Future Work"),

  h2("8.1 Summary"),
  para([
    t("This report describes the design, implementation, and current status of a hybrid TE + Sobol causal-analysis pipeline applied to the IEA-15 MW UMaineSemi FOWT. Phases 1–2 (knowledge base + simulation campaign) are complete; Phase 4 (TE pipeline) is validated end-to-end pending a scope decision; Phase 5 (Sobol sensitivity) is at preliminary N = 64. The framework supports six pre-registered hypotheses, includes the linear baselines needed for apples-to-apples comparison, and produces a directed weighted causal graph as its principal scientific output."),
  ]),

  h2("8.2 Key preliminary findings"),
  bullet("Phase 5 N=64 yields partial-confirmation of H4: the L_u half (ST(L_u | std(PtfmSurge)) = 0.82 > 0.2) is confirmed, but the EA half (ST(EA | std(PtfmSurge)) = 0.09 < 0.5) is not. Median imputation on the 44 %-feasible subset qualifies the result; N=256 with constrained sampling will sharpen."),
  bullet("First TE smoke test returned TE(wind → pitch) = 0 at DLC-1.6. This null is interpreted as the joint signature of wave-driven dominance under severe sea state and ROSCO's disturbance-rejection behaviour. H1 will be tested properly on DLC-A."),
  bullet([
    t("Five infrastructure issues were identified and patched during the campaign — see "),
    repoLink("pages/log.md"),
    t(" for the chronological detail."),
  ]),

  h2("8.3 Immediate next steps"),
  numbered("Decide on the Phase 4 scope-reduction strategy (§7.1) in consultation with the project supervisor."),
  numbered([
    t("Refactor "),
    repoLink("analysis/te_pipeline.py"),
    t(" for the chosen scope; if ensemble TE is adopted, stack the six seeds per DLC bin along IDTxl's replications axis."),
  ]),
  numbered("Launch the full Phase 4 campaign and Phase 5 N = 256 production run."),
  numbered("Write analysis/plots.py to generate publication figures from the resulting parquet tables."),

  h2("8.4 Open questions to resolve before publication"),
  bullet("Q4 (embedding strategy): per-pair vs fixed-global. To be resolved during the first DLC-A post-mortem (once Phase 4 has produced its first round of TE values)."),
  bullet("Q7 (publication venue): workshop versus journal. Contingent on Phase 4 results."),
  bullet("Q10 (ensemble TE): adopt now or defer to v2?"),
  bullet("Q11 (controller-off comparison): adopt only if controller-on H5 evidence is inconclusive."),

  h2("8.5 Stretch / v2 paper"),
  bullet("IEA-22 MW Semi multi-platform comparison to test cross-platform generalisability of the causal-graph structure."),
  bullet("OC6 experimental anchor — compare TE outputs against published model-test data."),
  bullet("Frequency-band-resolved TE: extend Phase 4 to compute TE on band-decomposed signals."),
  bullet("Improved surrogate scheme: IAAFT instead of circular shift for higher methodological defensibility."),

  // ----- Appendix A: Repo documentation index -----
  h1("Appendix A. Repository Documentation Index"),
  para([
    t("This report is deliberately concise on theory, methodology details, and chronology — those are documented in the project repository. The table below maps each topic of likely interest to its authoritative source file. Browse the repository at "),
    new ExternalHyperlink({
      link: "https://github.com/sinahdme/fowt-te-causal",
      children: [new TextRun({ text: "github.com/sinahdme/fowt-te-causal", font: "Consolas", size: 20, color: "2E75B6", underline: { type: "single" } })],
    }),
    t(". Each path in the table below is a clickable link to the corresponding file in the GitHub repository's main branch."),
  ]),
  tableCaption(8, "Repository documentation index — clickable file paths in the main branch of the GitHub repo."),
  repoDocsTable,

  // ----- References -----
  h1("References"),
  bullet("Abbas, N. J., Zalkind, D. S., Pao, L., & Wright, A. (2022). A reference open-source controller for fixed and floating offshore wind turbines. Wind Energy Science, 7, 53–73."),
  bullet("Allen, C., Viselli, A., Dagher, H., et al. (2020). Definition of the UMaine VolturnUS-S reference platform developed for the IEA Wind 15-MW offshore reference wind turbine. NREL/TP-5000-76773."),
  bullet("Gaertner, E., Rinker, J., Sethuraman, L., et al. (2020). IEA Wind TCP Task 37: Definition of the IEA 15-megawatt offshore reference wind turbine. NREL/TP-5000-75698."),
  bullet("Hall, M. (2022). RAFT: Response Amplitudes of Floating Turbines. https://github.com/WISDEM/RAFT"),
  bullet("Jeon, H., et al. (2025). Reinforcement-learning-based floating-platform substructure design optimisation. KSME Annual Conference. (Predecessor study used as the comparison baseline.)"),
  bullet("Kraskov, A., Stögbauer, H., & Grassberger, P. (2004). Estimating mutual information. Physical Review E, 69(6), 066138."),
  bullet("Lizier, J. T. (2014). JIDT: An information-theoretic toolkit for studying the dynamics of complex systems. Frontiers in Robotics and AI, 1, 11."),
  bullet("Massey, J. L. (1990). Causality, feedback and directed information. Proc. Int. Symp. Inf. Theory Applic. (ISITA-90), 303–305."),
  bullet("Saltelli, A., Ratto, M., Andres, T., et al. (2008). Global Sensitivity Analysis: The Primer. Wiley."),
  bullet("Schreiber, T. (2000). Measuring information transfer. Physical Review Letters, 85(2), 461."),
  bullet("Vicente, R., Wibral, M., Lindner, M., & Pipa, G. (2011). Transfer entropy — a model-free measure of effective connectivity for the neurosciences. Journal of Computational Neuroscience, 30(1), 45–67."),
  bullet("Wollstadt, P., Lizier, J. T., Vicente, R., Finn, C., Martínez-Zarzuela, M., Mediano, P., et al. (2019). IDTxl: The Information Dynamics Toolkit xl. Journal of Open Source Software, 4(34), 1081."),
  bullet("Wollstadt, P., Martínez-Zarzuela, M., Vicente, R., Díaz-Pernas, F. J., & Wibral, M. (2014). Efficient transfer entropy analysis of non-stationary neural time series. PLOS ONE, 9(7), e102833."),

  // Footer
  new Paragraph({
    spacing: { before: 360 },
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: "BFBFBF", space: 6 } },
    children: [new TextRun({
      text: "Project repository: github.com/sinahdme/fowt-te-causal. Latest commit at time of writing: d5ed1d2. Concept pages, equation derivations, narrative log, and open-question history are all maintained in the repository — this report stays brief and points there for depth.",
      size: 18, color: "808080", italics: true,
    })],
  }),
];

const doc = new Document({
  creator: "Sina (with Claude Opus 4.7)",
  title: "Causal Effect Analysis on a Floating Offshore Wind Turbine via Transfer Entropy — Technical Report v2",
  description: "Topic-structured technical report with embedded methodology figures and pointers to project documentation.",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Calibri", color: "1F3864" },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: "2E75B6" },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Calibri", color: "2E75B6" },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
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
  const out = path.join(__dirname, "2026-05-20-technical-report-ver05.docx");
  fs.writeFileSync(out, buf);
  console.log("Wrote", out, "(" + buf.length + " bytes)");
});
