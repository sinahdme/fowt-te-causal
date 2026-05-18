# Solver

The OpenFAST tight-coupling solver is implemented in `modules/openfast-library/src/FAST_Solver.f90`. It integrates the continuous states and resolves the input-output coupling between modules using a generalized-alpha scheme with Newton-Raphson convergence iterations.

<div class="contents" local="" depth="2">

</div>

## User input parameters

All solver parameters are set in the main OpenFAST input file (`*.fst`) under the **Feature Switches and Flags** and **Tight-Coupling / Solver** sections.

<table>
<colgroup>
<col style="width: 22%" />
<col style="width: 12%" />
<col style="width: 66%" />
</colgroup>
<thead>
<tr>
<th>Parameter</th>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>DT</code></td>
<td>real</td>
<td>Global (solver) time step in seconds. All module time steps must be equal to or an integer sub-divisor of <code>DT</code>.</td>
</tr>
<tr>
<td><code>ModCoupling</code></td>
<td>integer</td>
<td>Coupling method.
<ul>
<li><code>1</code> – Loose coupling: structural modules (ED/BD/SD) are treated as Option 1 and do <strong>not</strong> participate in the tight Newton loop.</li>
<li><code>2</code> – Tight coupling with fixed Jacobian updates (<code>DT_UJac</code> controls update frequency).</li>
<li><code>3</code> – Tight coupling with adaptive Jacobian updates (the Jacobian is rebuilt whenever the Newton loop fails to converge within the iteration budget).</li>
</ul></td>
</tr>
<tr>
<td><code>RhoInf</code></td>
<td>real</td>
<td>Numerical damping parameter ρ∞ for the generalized-alpha integrator. Range [0, 1]; 1 = no numerical damping (second-order accurate), 0 = maximum damping (first-order accurate). Typical value: <strong>0.9</strong>. Reducing <code>RhoInf</code> below 1 damps high-frequency numerical noise at the cost of slightly reduced accuracy.</td>
</tr>
<tr>
<td><code>MaxConvIter</code></td>
<td>integer</td>
<td>Maximum number of Newton convergence iterations per time step before the solver declares convergence failure. Typical value: <strong>20</strong>. With <code>ModCoupling=2</code> or <code>1</code>, a fatal error is issued on failure; with <code>ModCoupling=3</code> the Jacobian is rebuilt first and the step is retried before a warning is emitted.</td>
</tr>
<tr>
<td><code>ConvTol</code></td>
<td>real</td>
<td>Convergence tolerance. The iteration stops when the average <span class="title-ref">L2</span>-norm of the Newton update vector falls below this value. Typical value: <code>1.0e-4</code>. Tighter tolerances increase computational cost but may be needed for stiff problems.</td>
</tr>
<tr>
<td><code>DT_UJac</code></td>
<td>real</td>
<td>Time interval (seconds) between Jacobian rebuilds when <code>ModCoupling=2</code>.
<ul>
<li>If <code>DT_UJac &lt; DT</code>: the Jacobian is rebuilt at a fraction of the convergence-iteration budget.</li>
<li>If <code>DT_UJac ≥ DT</code>: the Jacobian is rebuilt every <code>CEILING(DT_UJac/DT)</code> time steps.</li>
<li>Setting <code>DT_UJac</code> very large (e.g. <code>9999</code>) freezes the Jacobian for the entire simulation; useful for profiling or when the system is nearly linear and the Jacobian is expensive.</li>
</ul></td>
</tr>
<tr>
<td><code>UJacSclFact</code></td>
<td>real</td>
<td>Conditioning scale factor applied to load rows and columns of the Jacobian. Force and moment variables are divided by this factor before the linear solve and multiplied back afterwards, equalising the magnitude of load entries relative to displacement/velocity entries. Typical value: <strong>1.0e5</strong> for offshore systems; may need adjustment for very large or very small turbines.</td>
</tr>
<tr>
<td><code>CompElast</code></td>
<td>integer</td>
<td>Select the structural dynamics module: <code>1</code> = ElastoDyn, <code>2</code> = BeamDyn (blades only, ElastoDyn still handles the tower/platform), <code>3</code> = Simplified ElastoDyn. The chosen modules become TC members when <code>ModCoupling ≥ 2</code>.</td>
</tr>
<tr>
<td><code>CompSub</code></td>
<td>integer</td>
<td>Sub-structural module: <code>0</code> = none, <code>1</code> = SubDyn, <code>2</code> = ExtPtfm, <code>3</code> = SlD (SoilDyn). SubDyn joins the TC set when <code>ModCoupling ≥ 2</code>.</td>
</tr>
<tr>
<td><code>CompHydro</code></td>
<td>integer</td>
<td><code>0</code> = none, <code>1</code> = HydroDyn. HydroDyn is always Option 1.</td>
</tr>
<tr>
<td><code>CompMooring</code></td>
<td>integer</td>
<td><code>0</code> = none, <code>1</code> = MAP++, <code>2</code> = FEAMooring, <code>3</code> = MoorDyn, <code>4</code> = OrcaFlex. Mooring modules are always Option 1.</td>
</tr>
<tr>
<td><code>CompAero</code></td>
<td>integer</td>
<td>Aerodynamics module: <code>0</code> = none, <code>1</code> = AeroDisk, <code>2</code> = AeroDyn. AeroDyn is Option 2 for land-based turbines and Option 1 for MHK.</td>
</tr>
<tr>
<td><code>CompServo</code></td>
<td>integer</td>
<td>Controller module: <code>0</code> = none, <code>1</code> = ServoDyn. ServoDyn is Post-solve by default but becomes Option 1 when structural controllers (tower, blade, nacelle StC) are active.</td>
</tr>
</tbody>
</table>

## Generalized-alpha integration

The tight-coupling solver integrates second-order ODEs of the form

``` math
\mathbf{M}\,\ddot{\mathbf{q}} + \mathbf{f}(\mathbf{q}, \dot{\mathbf{q}}, t) = 0
```

using the **generalized-alpha method** (Chung & Hulbert, 1993). Given the spectral radius ρ∞ specified by `RhoInf`, the method parameters are:

``` math
\begin{aligned}
\alpha_m &= \frac{2\rho_\infty - 1}{\rho_\infty + 1} \\
\alpha_f &= \frac{\rho_\infty}{\rho_\infty + 1} \\
\gamma   &= \tfrac{1}{2} - \alpha_m + \alpha_f \\
\beta    &= \tfrac{1}{4}(1 - \alpha_m + \alpha_f)^2
\end{aligned}
```

Two derived coefficients used throughout the convergence loop are:

``` math
\begin{aligned}
\beta'   &= h^2 \beta \frac{1 - \alpha_f}{1 - \alpha_m} \\
\gamma'  &= h \gamma  \frac{1 - \alpha_f}{1 - \alpha_m}
\end{aligned}
```

where *h* = `DT`.

**State vector layout** – the solver maintains a per-module *generalized coordinate* (q) vector with four columns:

| Column | Meaning                                                        |
|--------|----------------------------------------------------------------|
| `q`    | Displacement / orientation states (`DerivOrder = 0`)           |
| `v`    | Velocity states (`DerivOrder = 1`)                             |
| `vd`   | Acceleration (physical, from module `CalcContStateDeriv`)      |
| `a`    | Algorithmic acceleration (generalized-alpha internal variable) |

State prediction at the start of each step:

``` math
\begin{aligned}
q_{n+1}^{\rm pred}  &= q_n + h v_n + h^2[(\tfrac{1}{2} - \beta)a_n + \beta\, a_{n+1}] \\
v_{n+1}^{\rm pred}  &= v_n + h[(1-\gamma)a_n + \gamma\, a_{n+1}]
\end{aligned}
```

## Module ordering

During `FAST_SolverInit` each module is categorised based on `ModCoupling` and its own physics type, and assigned to one of the ordered index arrays in the `Glue_TCParam` structure:

| Array | Modules (in order) |
|----|----|
| `iModTC` | ElastoDyn, BeamDyn, SubDyn (when `ModCoupling ≥ 2`) |
| `iModOpt1` | ServoDyn (when StC active), SED, AD (MHK), ExtPtfm, HydroDyn, OrcaFlex, MoorDyn; ED/BD/SD also appear here when `ModCoupling = 1` |
| `iModOpt2` | ServoDyn, SED, ED, BD, SD, InflowWind, SeaState, AeroDyn (land), AeroDisk, ExtLoads, MAP++, FEAMooring, IceDyn, IceFloe, SoilDyn |
| `iModPost` | ServoDyn, ExternalInflow |
| `iModInit` | SED, ED, BD, SD, InflowWind, ExtLoads (Step 0 initialisation only) |

## Jacobian construction

Two separate Jacobians are assembled:

1.  **TC/Option-1 Jacobian** (`BuildJacobianTC`) — for the main time-stepping convergence loop.
2.  **IO Jacobian** (`BuildJacobianIO`) — for the initial and linearization input-output solve.

### Variable selection (`VF_Solve` flag)

During `FAST_SolverInit → SetVarSolveFlags`, the `VF_Solve` flag is set on the variables that must appear in the Jacobian:

- **Continuous states** of all TC modules (automatically).
- **Motion mesh** inputs/outputs of TC-to-TC mappings (all fields).
- **Motion mesh** input accelerations of TC-to-Option1 or Option1-to-TC mappings.
- **Load mesh** inputs and outputs involved in any TC/Option1 mapping.
- **Load mesh** displacement outputs of the destination module when the mapping carries moments (needed for moment-arm Jacobian terms).
- **Variable-to-variable** mapped inputs/outputs of TC/Option1 modules.
- Any variable with `VF_NoLin` is excluded from `VF_Solve`.

### Jacobian structure (TC Jacobian)

The assembled TC Jacobian **J** has size `NumJ × NumJ`, where:

``` math
N_J = \underbrace{N_Q}_{\text{TC states}} +
      \underbrace{N_{U_T}}_{\text{TC inputs}} +
      \underbrace{N_{U_1}}_{\text{Option-1 inputs}}
```

The columns and rows are partitioned as:

``` math
\begin{aligned}
\mathbf{J} = \begin{bmatrix}
  J_{11} & J_{12} \\
  J_{21} & J_{22}
\end{bmatrix}
\end{aligned}
```

where

- **J₁₁** (`NumQ × NumQ`) — derivative of the acceleration residual with respect to TC displacement/velocity states (formed from the module `dXdx` sub-Jacobians plus the generalized-alpha tangent).
- **J₁₂** (`NumQ × NumU_T`) — derivative of the acceleration residual with respect to TC inputs (from `dXdu`).
- **J₂₁** (`NumU_T × NumQ`) — derivative of the input residual with respect to TC states (from `dUdx = dUdy · dydx`).
- **J₂₂** (`NumU × NumU`) — derivative of the input residual with respect to inputs, including load conditioning rows/columns.

The right-hand side (XB) contains the residuals:

- **State residual** (rows `iJX`): difference between the predicted velocity derivative and the module-computed accelerations.
- **Input residual** (rows `iJU`): difference between the inputs computed from mesh mappings (`FAST_InputSolve`) and the current iterate.

The loads portion (rows `iJL`) is pre-divided by `UJacSclFact` before the factorisation to improve conditioning.

### Jacobian update strategy

`ModCoupling = 2` (fixed updates)  
The Jacobian is rebuilt if either of these counters reaches zero:

- `UJacStepsRemain` — steps remaining; initialised to `CEILING(DT_UJac/DT)` each time the Jacobian is rebuilt.
- `UJacIterRemain` — iteration budget; initialised to `CEILING(DT_UJac/DT · MaxConvIter)` when `DT_UJac < DT`.

On convergence failure the solver returns a fatal error immediately.

`ModCoupling = 3` (adaptive updates)  
The Jacobian is rebuilt the first time the convergence loop fails. If the step still does not converge after the forced rebuild, a non-fatal warning is issued and the simulation proceeds.

### Per-module Jacobian contributions

The module-level Jacobian sub-matrices are computed by finite differencing inside `BuildJacobianTC` and `BuildJacobianIO` using the `MV_Perturb` / `MV_ComputeDiff` / `MV_ComputeCentralDiff` utilities from `ModVar`. For each variable flagged `VF_Solve`:

1.  Apply a positive perturbation of magnitude `Var%Perturb` to the working state/input array.
2.  Call `FAST_CalcOutput` (or `FAST_GetContStateDeriv`).
3.  Apply an equal negative perturbation.
4.  Call again.
5.  Compute the central difference: `(y_plus - y_minus) / (2·Perturb)`.

For orientation variables (`FieldOrientation`), perturbations are applied by quaternion composition rather than direct addition (`MV_Perturb`), and differences are extracted as rotation vectors (`MV_ComputeDiff`).

### Linear solve

The LU factorisation of **J** is computed with `LAPACK_getrf` and the system is solved with `LAPACK_getrs` (packed in `NWTC_LAPACK`). The same factored matrix is reused across convergence iterations until the update strategy triggers a rebuild.

### Convergence check

After each Newton step the convergence error is the average <span class="title-ref">L2</span>-norm of the update vector:

``` math
e = \frac{\|\Delta \mathbf{z}\|_2}{N_J}
```

where $`\Delta \mathbf{z}`$ combines state and input updates. The loop exits if `e < ConvTol` (`ErrID_None`) or the iteration count reaches `MaxConvIter` (`ErrID_Fatal` or `ErrID_Warn` depending on `ModCoupling`).

## Output channels from the solver

Three output channels are written to `DriverWriteOutput` each step and appear in the output file when enabled:

| Index | Content                                                |
|-------|--------------------------------------------------------|
| 1     | Total convergence iterations in the step (`TotalIter`) |
| 2     | Final convergence error (`ConvError`)                  |
| 3     | Number of Jacobian rebuilds in the step (`NumUJac`)    |
