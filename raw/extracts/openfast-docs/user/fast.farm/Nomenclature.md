# Nomenclature

<div id="Tab:FF:Nomenclature" class="container">

|  |  |
|----|----|
| ABLSolver | atmospheric boundary layer solver |
| AWAE | ambient wind and array effects (module) |
| $`a(r)`$ | axial induction factor, distributed radially |
| $`a_K`$ | coherence decrement parameter |
| BEM | blade-element momentum |
| $`b_K`$ | coherence offset parameter |
| $`C^\text{O}_\text{HWkDfl}`$, $`C^\text{OY}_\text{HWkDfl}`$, $`C^\text{x}_\text{HWkDfl}`$, and $`C^\text{xY}_\text{HWkDfl}`$ | calibrated parameters in the horizontal wake-deflection correction |
| $`c_\text{max}`$ | maximum blade chord length |
| $`C_\text{Meander}`$ | calibrated parameter for wake meandering |
| $`C_\text{NearWake}`$ | calibrated parameter in the near-wake correction |
| $`C_\text{WakeDiam}`$ | calibrated parameter in the wake-diameter calculation |
| $`C^\text{DMax}_{\nu \text{Amb}}`$, $`C^\text{DMin}_{\nu \text{Amb}}`$, $`C^\text{Exp}_{\nu Amb}`$, and $`C^\text{FMin}_{\nu Amb}`$ | calibrated parameters in the eddy-viscosity filter function for ambient turbulence |
| $`C^\text{DMax}_{\nu \text{Shr}}`$, $`C^\text{DMin}_{\nu \text{Shr}}`$, $`C^\text{Exp}_{\nu \text{Shr}}`$, and $`C^\text{FMin}_{\nu \text{Shr}}`$ | calibrated parameters in the eddy-viscosity filter function for the wake shear layer |
| $`^\text{AzimAvg}C_t(r)`$ and $`^\text{FiltAzimAvg}C_t(r)`$ | azimuthally averaged thrust-force coefficient (normal to a rotor disk), distributed radially, and its low-pass time-filtered value |
| $`Coh_{i,j}`$ | magnitude of partial coherence between points $`i`$ and $`j`$ |
| DLL | dynamic-link library |
| DWM | dynamic wake meandering |
| $`D_\text{Grid}`$ | Assumed rotor diameter when generating TurbSim inflow |
| $`D^\text{Rotor}`$ and $`^\text{Filt}D_{n_p}^\text{Rotor}`$ | rotor diameter and its low-pass time-filtered value at wake plane $`n_p`$ |
| $`D_{n_p}^\text{Wake}`$ | wake diameter at wake plane $`n_p`$ |
| FLORIS | FLOw Redirection and Induction in Steady state |
| $`f`$ | frequency |
| $`f_c`$ | cutoff (corner) frequency of the low-pass time filter |
| $`\vec{f}_{n_b}(r)`$ | aerodynamic applied loads distributed radially per unit length for blade $`n_b`$ |
| $`f_\text{max}`$ | maximum excitation frequency |
| $`F_{\nu \text{Amb}}(x)`$ | eddy-viscosity filter function associated with ambient turbulence |
| $`F_{\nu \text{Shr}}(x)`$ | eddy-viscosity filter function associated with the wake shear layer |
| HFM | high-fidelity modeling |
| HPC | high-performance computer |
| $`I`$ | three-by-three identify matrix |
| $`K`$ | velocity components $`u`$, $`v`$, and $`w`$ |
| $`k_{\nu \text{Amb}}`$ | calibrated parameter for the influence of ambient turbulence in the eddy viscosity |
| $`k_{\nu \text{Shr}}`$ | calibrated parameter for the influence of the wake shear layer in the eddy viscosity |
| LES | large-eddy simulation |
| MFoR | moving frame of reference |
| MPI | message-passing interface |
| NaN | not a number |
| NREL | National Renewable Energy Laboratory |
| $`N`$ and $`n`$ | number of discrete-time steps and discrete-time-step counter |
| $`N_b`$ and $`n_b`$ | number of rotor blades and blade counter |
| $`N_{n_p}^\text{Polar}`$ and $`n^\text{Polar}`$ | number of points in the polar grid of wake plane $`n_p`$ and point counter |
| $`N^\text{Wake}`$ and $`n^\text{Wake}`$ | number of wakes overlapping a given wind data point in the wind domain and wake counter |
| $`N_P`$ and $`n_P`$ | number of wake planes and wake-plane counter |
| $`N_r`$ and $`n_r`$ | number of radial nodes and radii counter |
| $`N_t`$ and $`n_t`$ | number of wind turbines and turbine counter |
| OF | OpenFAST (module) |
| OpenMP | open multiprocessing |
| $`\vec{p}^\text{Hub}`$ | global position of a rotor center |
| $`\vec{p}^\text{Plane}_{n_p}`$ | global position of the center of wake plane $`n_p`$ |
| RAM | random-access memory |
| RSS | root-sum-squared |
| $`r`$ and $`r^\text{Plane}`$ | radius in the axisymmetric coordinate system |
| $`\hat{r}^\text{Plane}`$ | radial unit vector in the axisymmetric coordinate system |
| SOWFA | Simulator fOr Wind Farm Applications |
| $`t`$ | simulation time |
| $`TI_\text{Amb}`$ and $`^\text{Filt}TI_{\text{Amb}_{n_p}}`$ | ambient turbulence intensity of the wind at a rotor and its low-pass time-filtered value for wake plane $`n_p`$ |
| $`u^d`$ | discrete-time inputs |
| $`V_\text{Advect}`$ | advection speed of the synthetic wind data |
| $`\vec{V}_\text{Amb}^\text{High}`$ | ambient wind across a high-resolution wind domain around a turbine |
| $`\vec{V}_\text{Amb}^\text{Low}`$ | ambient wind across a low-resolution wind domain throughout the wind farm |
| $`\vec{V}_\text{Dist}^\text{High}`$ | disturbed wind across a high-resolution wind domain around a turbine |
| $`\vec{V}_\text{Dist}^\text{Low}`$ | disturbed wind across a low-resolution wind domain throughout the wind farm |
| $`V_\text{Hub}`$ | mean hub-height wind speed |
| $`\vec{V}_{n_p}^\text{Plane}`$ and $`^\text{Filt}\vec{V}_{n_p}^\text{Plane}`$ | advection, deflection, and meandering velocity and its low-pass time-filtered value of wake plane $`n_p`$ |
| $`V_r`$ | radial velocity in the axisymmetric coordinate system |
| $`V_{r_{n_p}}^\text{Wake}(r)`$ | radial wake-velocity deficit at wake plane $`n_p`$, distributed radially |
| VTK | Visualization Toolkit |
| $`^\text{DiskAvg}V_x^\text{Rel}`$ and $`^\text{FiltDiskAvg}V_x^\text{Rel}`$ | rotor-disk-averaged relative wind speed (ambient plus wakes of neighboring turbines plus turbine motion), normal to the disk, and its low-pass time-filtered value |
| $`V_x`$ | axial velocity in the axisymmetric coordinate system |
| $`V_{x_{n_p}}^\text{Wake}(r)`$ | axial wake-velocity deficit at wake plane $`n_p`$, distributed radially |
| $`^\text{DiskAvg}V_x^\text{Wind}`$ and $`^\text{FiltDiskAvg}V_{x_{n_p}}^\text{Wind}`$ | rotor-disk-averaged ambient wind speed, normal to the disk, and its low-pass time-filtered value at wake plane $`n_p`$ |
| $`w_{n^\text{Wind}}`$ | weighting in the spatial averaging for wind data point $`n^\text{Wind}`$ |
| WD | wake dynamics (module) |
| WISDEM | Wind-Plant Integrated System Design & Engineering Model |
| $`x`$ and $`x_{n_p}^\text{Plane}`$ | downwind distance from a rotor to wake plane $`n_p`$ in the axisymmetric coordinate system |
| $`X`$, $`Y`$, and $`Z`$ | inertial-frame coordinates, with Z directed vertically upward, opposite gravity, X directed horizontally nominally downwind (along the zero-degree wind direction), and Y directed horizontally transversely |
| $`\hat{X}`$, $`\hat{Y}`$, and $`\hat{Z}`$ | unit vectors of the inertial-frame coordinate system, parallel to the X, Y, and X coordinates |
| $`X^d(\quad)`$ | discrete-time state functions |
| $`X^d(\quad)`$ | discrete-time state functions |
| $`\hat{x}^\text{Disk}`$ | orientation of a rotor centerline |
| $`\hat{x}_{n_p}^\text{Plane}`$ | orientation of wake plane $`n_p`$ |
| $`Y^d(\quad)`$ | discrete-time output functions |
| $`Y^d(\quad)`$ | discrete-time output functions |
| $`z_\text{bot}`$ | bottom vertical location of synthetic turbulence inflow grid |
| $`\alpha`$ | low-pass time-filter parameter |
| $`\Delta t`$ | discrete time step (increment) |
| $`\gamma^\text{YawErr}`$ and $`^\text{Filt}\gamma_{n_p}^\text{YawErr}`$ | nacelle-yaw error of a rotor and its low-pass time-filtered value at wake plane $`n_p`$ |
| $`\nu_T`$ | eddy viscosity |
| $`\rho`$ | air density |
| 2D | two dimensional |
| 3D | three dimensional |

List of Available FAST.Farm Output Channels

</div>
