# Theory

In this module, the rotor is represented by a rigid disk.

The module has two states $`\psi`$ and $`\dot{\psi}`$, corresponding to the azimuthal angle and the rotor speed. (Note: introducing the azimuthal angle as a state is optional, but convenient for coupling with AeroDyn. Such introduction should not have any influence on the time-step required since both equations are effictively decoupled.). The state-space equations are:

``` math
:label: sed_stateEq
```
``` math
\begin{aligned}
\begin{aligned}
    \dot{\psi}  & = \dot{\psi} \\
    \ddot{\psi} & = \frac{1}{J_\text{DT}}\left( Q_g - Q_a + Q_b\right)
\end{aligned}
\end{aligned}
```

where $`J_{DT}`$ is the total inertia of the drivetrain (blades+hub+generator), $`Q_g`$, $`Q_a`$ and $`Q_b`$ are the generator, aerodynamic and brake torque respectively, all expressed on the low-speed-shaft (LSS) side. The total inertia of the drivetrain is obtained as:

``` math
:label: sed_JDT
```
``` math
J_\text{DT} = J_r + n_g^2 J_{g,HSS}
```

where $`J_r`$ is the inertia of the rotor (blades+hub+"shaft"), $`n_g`$ is the gear ratio of the gearbox and $`J_{g,HSS}`$ is the inertia of the generator on the high-speed-shaft (HSS). It is noted that OpenFAST considers the inertia of the shaft to be included in the "hub" (i.e. rotor). The generator and brake torques on the LSS is obtained from the HSS as follows:

``` math
:label: QgLSS
```
``` math
Q_g = n_g Q_{g,HSS}
,\quad
Q_b = n_g Q_{b,HSS}
```

The initial conditions associated with equation `sed_stateEq` are:

``` math
:label: sed_stateInit
```
``` math
\begin{aligned}
\begin{aligned}
    \psi       & = \psi_0 \\
    \dot{\psi} & = \Omega_0
\end{aligned}
\end{aligned}
```

where $`\psi_0`$ is the initial azimuthal angle in rad and $`\Omega_0`$ is the initial rotor speed in rad/s.

If the generator degrees of freedom is off, then the states are simply determined as follows:

``` math
:label: sed_stateEqGenDOF
```
``` math
\begin{aligned}
\begin{aligned}
    \psi  & = \psi_0 +  \int_{0}^t \dot{\psi} dt = \psi_0  +  \Omega_0 n \Delta t \\
    \dot{\psi} & = \Omega_0
\end{aligned}
\end{aligned}
```

where $`n`$ is the time step index and $`\Delta t`$ is the time step of the module.
