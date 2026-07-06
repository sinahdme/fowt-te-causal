# Vendored SURD reference implementation

`surd/vendor/SURD/` is a clone of the official reference code for the SURD
causal decomposition and is **gitignored** (55.9 MB, mostly its bundled
`data/` + `results/` example artifacts). To restore it:

```bash
git clone https://github.com/Computational-Turbulence-Group/SURD surd/vendor/SURD
git -C surd/vendor/SURD checkout 79dbdea85e6754ec2b5457b3e37204c5d53d1815
```

- Pinned commit: `79dbdea85e6754ec2b5457b3e37204c5d53d1815` (2025-04-10,
  validated by `surd/validate_synthetic.py` on 2026-07-06 — gate PASSED,
  see `surd/validation_mediator.{png,json}`)
- Paper: Martínez-Sánchez, Arranz & Lozano-Durán, *Nat. Commun.* 15, 9296
  (2024). DOI: [10.1038/s41467-024-53373-4](https://doi.org/10.1038/s41467-024-53373-4)
- Upstream: <https://github.com/Computational-Turbulence-Group/SURD>

Usage notes discovered in Phase 0:

- Only `utils/{surd,it_tools,analytic_eqs}.py` are needed; they depend on
  numpy/scipy/matplotlib only.
- `utils/surd.py` imports `pymp` (fork-based, POSIX-only) at module level but
  uses it solely in `run_parallel()`. On Windows, stub `sys.modules["pymp"]`
  before import (see `validate_synthetic.py`) instead of installing it.
- The E02 notebook's mediator text says `Q3(n+1)=0.9*Q3(n)+...` but
  `analytic_eqs.mediator` implements `0.5*Q3(n)` — the code is what the
  results reproduce; we validate against the code.
