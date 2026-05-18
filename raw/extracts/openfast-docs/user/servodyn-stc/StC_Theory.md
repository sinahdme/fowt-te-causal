# Theory Manual for the Tuned Mass Damper Module in OpenFAST

Author  
William La Cava & Matthew A. Lackner Department of Mechanical and Industrial Engineering University of Massachusetts Amherst Amherst, MA 01003 `wlacava@umass.edu`, `lackner@ecs.umass.edu`

This document was edited by Jason M. Jonkman of NREL to include an independent vertically oriented TMD in OpenFAST. `jason.jonkman@nrel.gov`

This manual describes updated functionality in OpenFAST that simulates the addition of tuned mass dampers (TMDs) for structural control. The dampers can be added to the blades, nacelle, tower, or substructure. For application studies of these systems, refer to stc-lackner_passive_2011,stc-lackner_structural_2011,stc-namik_active_2013,stc-stewart_effect_2011,stc-stewart_impact_2014,stc-stewart_optimization_2013. The TMDs are three independent, 1 DOF, linear mass spring damping elements that act in the local $`x`$, $`y`$, and $`z`$ coordinate systems of each component. The other functionality of the structural control (StC) module, including an omnidirectional TMD and TLCD are not documented herein. We first present the theoretical background and then describe the code changes.

## Theoretical Background

### Definitions

<div id="tab:defs" class="container">

| Variable | Description |
|----|----|
| $`O`$ | origin point of global inertial reference frame |
| $`P`$ | origin point of non-inertial reference frame fixed to component (blade, nacelle, tower, substructure) where TMDs are at rest |
| $`TMD`$ | location point of a TMD |
| $`G`$ | axis orientation of global reference frame |
| $`N`$ | axis orientation of local component reference frame with unit vectors $`\hat{\imath}, \hat{\jmath}, \hat{k}`$ |
| $`\vec{r}_{_{_{TMD/O_G}}} = \left[ \begin{array}{c} x \\ y\\ z \end{array} \right]_{_{TMD/O_G}}`$ | position of a TMD with respect to (w.r.t.) $`O`$ with orientation $`G`$ |
| $`\vec{r}_{_{_{TMD/P_N}}} = \left[ \begin{array}{c} x \\ y\\ z \end{array} \right]_{_{TMD/P_N}}`$ | position of a TMD w.r.t. $`P_N`$ |
| $`\vec{r}_{_{_{TMD_X}}}`$ | position vector for $`TMD_X`$ |
| $`\vec{r}_{_{_{TMD_Y}}}`$ | position vector for $`TMD_Y`$ |
| $`\vec{r}_{_{_{TMD_Z}}}`$ | position vector for $`TMD_Z`$ |
| $`\vec{r}_{_{P/O_G}} =\left[ \begin{array}{c} x \\ y\\ z \end{array} \right]_{_{P/O_G}}`$ | position vector of component w.r.t. $`O_G`$ |
| $`R_{_{N/G}}`$ | 3 x 3 rotation matrix transforming orientation $`G`$ to $`N`$ |
| $`R_{_{G/N}} = R_{_{N/G}}^T`$ | transformation from $`N`$ to $`G`$ |
| $`\vec{\omega}_{_{N/O_N}} = \dot{\left[ \begin{array}{c} \theta \\ \phi \\ \psi \end{array} \right]}_{_{N/O_N}}`$ | angular velocity of component in orientation $`N`$; defined likewise for $`G`$ |
| $`\dot{\vec{\omega}}_{_{N/O_N}} = \vec{\alpha}_{_{N/O_N}}`$ | angular acceleration of component |
| $`\vec{a}_{G/O_G} = \left[ \begin{array}{c}0 \\ 0\\ -g \end{array} \right]_{/O_G}`$ | gravitational acceleration in global coordinates |
| $`\vec{a}_{G/O_N} = R_{_{N/G}} \vec{a}_{G/O_G} = \left[ \begin{array}{c}a_{_{G_X}} \\ a_{_{G_Y}}\\ a_{_{G_Z}} \end{array} \right]_{/O_N}`$ | gravity w.r.t. $`O_N`$ |

Definitions

</div>

### Equations of motion

The position vectors of the TMDs in the two reference frames $`O`$ and $`P`$ are related by

``` math
\vec{r}_{_{TMD/O_G}} =  \vec{r}_{_{P/O_G}} +  \vec{r}_{_{TMD/P_G}}
```

Expressed in orientation $`N`$,

``` math
\vec{r}_{_{TMD/O_N}} =  \vec{r}_{_{P/O_N}} +  \vec{r}_{_{TMD/P_N}}
```

``` math
\Rightarrow \vec{r}_{_{TMD/P_N}} =  \vec{r}_{_{TMD/O_N}} -  \vec{r}_{_{P/O_N}}
```

Differentiating,[^1]

``` math
\dot{\vec{r}}_{_{TMD/P_N}}= \dot{\vec{r}}_{_{TMD/O_N}} 
- \dot{\vec{r}}_{_{P/O_N}} 
- \vec{\omega}_{_{N/O_N}} \times \vec{r}_{_{TMD/P_N}}
```

differentiating again gives the acceleration of the TMD w.r.t. $`P`$ (the nacelle position), oriented with $`N`$:

<span label="accel">
``` math
\begin{aligned}
\begin{array}{cc}
\ddot{\vec{r}}_{_{TMD/P_N}} =
&  \ddot{\vec{r}}_{_{TMD/O_N}}
- \ddot{\vec{r}}_{_{P/O_N}} - \vec{\omega}_{_{N/O_N}} 
\times (\vec{\omega}_{_{N/O_N}} \times \vec{r}_{_{TMD/P_N}}) \\[1.1em] 
&- \vec{\alpha}_{_{N/O_N}} \times \vec{r}_{_{TMD/P_N}} 
- 2 \vec{\omega}_{_{N/O_N}} \times \dot{\vec{r}}_{_{TMD/P_N}}
\end{array}
\end{aligned}
```
</span>

The right-hand side contains the following terms:

<div id="tab:" class="container">

|  |  |
|----|----|
| $`\ddot{\vec{r}}_{_{TMD/O_N}}`$ | acceleration of the TMD in the *inertial* frame $`O_N`$ |
| $`\ddot{\vec{r}}_{_{P/O_N}} = R_{_{N/G}} \ddot{\vec{r}}_{_{P/O_G}}`$ | acceleration of the Nacelle origin $`P`$ w.r.t. $`O_N`$ |
| $`\vec{\omega}_{_{N/O_N}} = R_{_{N/G}} \vec{\omega}_{_{N/O_G}}`$ | angular velocity of nacelle w.r.t. $`O_N`$ |
| $`\vec{\omega}_{_{N/O_N}} \times (\vec{\omega}_{_{N/O_N}} \times \vec{r}_{_{TMD/P_N}})`$ | Centripetal acceleration |
| $`\vec{\alpha}_{_{N/O_N}} \times \vec{r}_{_{TMD/P_N}}`$ | Tangential acceleration |
| $`2\vec{\omega}_{_{N/O_N}} \times \dot{\vec{r}}_{_{TMD/P_N}}`$ | Coriolis acceleration |

RHS terms

</div>

The acceleration in the inertial frame $`\ddot{\vec{r}}_{_{TMD/O_N}}`$ can be replaced with a force balance

``` math
\begin{aligned}
\begin{aligned}
\ddot{\vec{r}}_{_{TMD/O_N}} = \left[ 
\begin{array}{c} \ddot{x} \\
\ddot{y} \\
\ddot{z}
\end{array}
\right]_{_{TMD/O_N}} = \frac{1}{m} \left[ 
\begin{array}{c} 
\sum{F_X} \\
\sum{F_Y} \\
\sum{F_Z} 
\end{array}
\right]_{_{TMD/O_N}} = \frac{1}{m} \vec{F}_{_{TMD/O_N}}
\end{aligned}
\end{aligned}
```

Substituting the force balance into Equation `accel` gives the general equation of motion for a TMD:

<span label="EOM">
``` math
\begin{aligned}
\begin{array}{cc}
\ddot{\vec{r}}_{_{TMD/P_N}} = & \frac{1}{m} \vec{F}_{_{TMD/O_N}}
- \ddot{\vec{r}}_{_{P/O_N}}
- \vec{\omega}_{_{N/O_N}} \times (\vec{\omega}_{_{N/O_N}}
\times \vec{r}_{_{TMD/P_N}}) \\[1.1em]
& - \vec{\alpha}_{_{N/O_N}} \times \vec{r}_{_{TMD/P_N}}
- 2 \vec{\omega}_{_{N/O_N}} \times \dot{\vec{r}}_{_{TMD/P_N}}
\end{array}
\end{aligned}
```
</span>

We will now solve the equations of motion for $`TMD_X`$, $`TMD_Y`$, and $`TMD_Z`$.

#### TMD_X :

The external forces $`\vec{F}_{_{TMD_X/O_N}}`$ are given by

``` math
\begin{aligned}
\vec{F}_{_{TMD_X/O_N}} = \left[
\begin{array}{c}
- c_x \dot{x}_{_{TMD_X/P_N}}
- k_x x_{_{TMD_X/P_N}}
+ m_x a_{_{G_X/O_N}}
+ F_{ext_x}
+ F_{StopFrc_{X}} \\
F_{Y_{_{TMD_X/O_N}}}
+ m_x a_{_{G_Y/O_N}}  \\
F_{Z_{_{TMD_X/O_N}}}
+ m_x a_{_{G_Z/O_N}}
\end{array}
\right]
\end{aligned}
```

$`TMD_X`$ is fixed to frame $`N`$ in the $`y`$ and $`z`$ directions so that

``` math
\begin{aligned}
{r}_{_{TMD_X/P_N}} = \left[
\begin{array}{c}
x_{_{TMD_X/P_N}} \\
0 \\
0 
\end{array}
\right]
\end{aligned}
```

The other components of Eqn. `EOM` are:

``` math
\begin{aligned}
\vec{\omega}_{_{N/O_N}} \times (\vec{\omega}_{_{N/O_N}} \times \vec{r}_{_{TMD_X/P_N}})
= x_{_{TMD_X/P_N}} \left[
\begin{array}{c}
- (\dot{\phi}_{_{N/O_N}}^2 + \dot{\psi}_{_{N/O_N}}^2) \\
\dot{\theta}_{_{N/O_N}}\dot{\phi}_{_{N/O_N}} \\
\dot{\theta}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}}
\end{array}
\right]
\end{aligned}
```

``` math
\begin{aligned}
2\vec{\omega}_{_{N/O_N}} \times \dot{\vec{r}}_{_{TMD_X/P_N}}
= \dot{x}_{_{TMD_X/P_N}} \left[
\begin{array}{c} 0 \\
2\dot{\psi}_{_{N/O_N}} \\
-2\dot{\phi}_{_{N/O_N}}
\end{array}
\right]
\end{aligned}
```

``` math
\begin{aligned}
\vec{\alpha}_{_{N/O_N}} \times \vec{r}_{_{TMD_X/P_N}} = x_{_{TMD_X/P_N}} \left[ \begin{array}{c} 0 \\ \ddot{\psi}_{_{N/O_N}} \\ -\ddot{\phi}_{_{N/O_N}}\end{array} \right]
\end{aligned}
```

Therefore $`\ddot{x}_{_{TMD_X/P_N}}`$ is governed by the equations

<span label="EOM_Xx">
``` math
\begin{aligned}
\begin{aligned}
\ddot{x}_{_{TMD_X/P_N}} =& (\dot{\phi}_{_{N/O_N}}^2 
+ \dot{\psi}_{_{N/O_N}}^2-\frac{k_x}{m_x}) x_{_{TMD_X/P_N}}
- (\frac{c_x}{m_x}) \dot{x}_{_{TMD_X/P_N}} 
-\ddot{x}_{_{P/O_N}}+a_{_{G_X/O_N}} \\ 
&+ \frac{1}{m_x} ( F_{ext_X} + F_{StopFrc_{X}})
\end{aligned}
\end{aligned}
```
</span>

The forces $`F_{Y_{_{TMD_X/O_N}}}`$ and $`F_{Z_{_{TMD_X/O_N}}}`$ are solved noting $`\ddot{y}_{_{TMD_X/P_N}} = \ddot{z}_{_{TMD_X/P_N}} = 0`$:

<span label="EOM_Xy">
``` math
F_{Y_{_{TMD_X/O_N}}} = m_x \left( - a_{_{G_Y/O_N}} +\ddot{y}_{_{P/O_N}} 
+ (\ddot{\psi}_{_{N/O_N}}
+ \dot{\theta}_{_{N/O_N}}\dot{\phi}_{_{N/O_N}} ) x_{_{TMD_X/P_N}}
+ 2\dot{\psi}_{_{N/O_N}} \dot{x}_{_{TMD_X/P_N}} \right)
```
</span>

<span label="EOM_Xz">
``` math
F_{Z_{_{TMD_X/O_N}}} = m_x \left( - a_{_{G_Z/O_N}} +\ddot{z}_{_{P/O_N}}
- (\ddot{\phi}_{_{N/O_N}}
- \dot{\theta}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}} ) x_{_{TMD_X/P_N}}
- 2\dot{\phi}_{_{N/O_N}} \dot{x}_{_{TMD_X/P_N}} \right)
```
</span>

#### TMD_Y:

The external forces $`\vec{F}_{_{TMD_Y/P_N}}`$ on $`TMD_Y`$ are given by

``` math
\begin{aligned}
\vec{F}_{_{TMD_Y/P_N}} =  \left[
\begin{array}{c}
F_{X_{_{TMD_Y/O_N}}} + m_y a_{_{G_X/O_N}}\\
- c_y \dot{y}_{_{TMD_Y/P_N}} - k_y y_{_{TMD_Y/P_N}}
+ m_y a_{_{G_Y/O_N}} + F_{ext_y} + F_{StopFrc_{Y}} \\
F_{Z_{_{TMD_Y/O_N}}}+ m_y a_{_{G_Z/O_N}}
\end{array}
\right]
\end{aligned}
```

$`TMD_Y`$ is fixed to frame $`N`$ in the $`x`$ and $`z`$ directions so that

``` math
\begin{aligned}
{r}_{_{TMDYX/P_N}} = \left[
\begin{array}{c}
0 \\
y_{_{TMD_Y/P_N}} \\
0
\end{array}
\right]
\end{aligned}
```

The other components of Eqn. `EOM` are:

``` math
\begin{aligned}
\vec{\omega}_{_{N/O_N}} \times (\vec{\omega}_{_{N/O_N}}
\times \vec{r}_{_{TMD_Y/P_N}})
= y_{_{TMD_Y/P_N}}
\left[
\begin{array}{c}
\dot{\theta}_{_{N/O_N}}\dot{\phi}_{_{N/O_N}} \\
-(\dot{\theta}_{_{N/O_N}}^2 + \dot{\psi}_{_{N/O_N}}^2)  \\
\dot{\phi}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}}
\end{array}
\right]
\end{aligned}
```

``` math
\begin{aligned}
2\vec{\omega}_{_{N/O_N}} \times \dot{\vec{r}}_{_{TMD_Y/P_N}}
= \dot{y}_{_{TMD_Y/P_N}} \left[
\begin{array}{c}
- 2 \dot{\psi}_{_{N/O_N}} \\
0 \\
2 \dot{\theta}_{_{N/O_N}}
\end{array}
\right]
\end{aligned}
```

``` math
\begin{aligned}
\vec{\alpha}_{_{N/O_N}} \times \vec{r}_{_{TMD_Y/P_N}}
= y_{_{TMD_Y/P_N}} \left[
\begin{array}{c}
- \ddot{\psi}_{_{N/O_N}} \\
0 \\
\ddot{\theta}_{_{N/O_N}}
\end{array}
\right]
\end{aligned}
```

Therefore $`\ddot{y}_{_{TMD_Y/P_N}}`$ is governed by the equations

<span label="EOM_Yy">
``` math
\begin{aligned}
\begin{aligned}
\ddot{y}_{_{TMD_Y/P_N}}
= & (\dot{\theta}_{_{N/O_N}}^2
+ \dot{\psi}_{_{N/O_N}}^2-\frac{k_y}{m_y}) y_{_{TMD_Y/P_N}}
- (\frac{c_y}{m_y}) \dot{y}_{_{TMD_Y/P_N}} 
-\ddot{y}_{_{P/O_N}} + a_{_{G_Y/O_N}}\\ 
&+ \frac{1}{m_y} (F_{ext_Y} + F_{StopFrc_{Y}})
\end{aligned}
\end{aligned}
```
</span>

The forces $`F_{X_{_{TMD_Y/O_N}}}`$ and $`F_{Z_{_{TMD_Y/O_N}}}`$ are solved noting $`\ddot{x}_{_{TMD_Y/P_N}} = \ddot{z}_{_{TMD_Y/P_N}} = 0`$:

<span label="EOM_Yx">
``` math
F_{X_{_{TMD_Y/O_N}}} = m_y \left( - a_{_{G_X/O_N}} + \ddot{x}_{_{P/O_N}}
- (\ddot{\psi}_{_{N/O_N}}
- \dot{\theta}_{_{N/O_N}}\dot{\phi}_{_{N/O_N}}) y_{_{TMD_Y/P_N}}
- 2\dot{\psi}_{_{N/O_N}} \dot{y}_{_{TMD_Y/P_N}} \right)
```
</span>

<span label="EOM_Yz">
``` math
F_{Z_{_{TMD_Y/O_N}}} = m_y \left( - a_{_{G_Z/O_N}} + \ddot{z}_{_{P/O_N}}
+ (\ddot{\theta}_{_{N/O_N}}
+ \dot{\phi}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}}) y_{_{TMD_Y/P_N}}
+ 2\dot{\theta}_{_{N/O_N}} \dot{y}_{_{TMD_Y/P_N}} \right)
```
</span>

#### TMD_Z :

The external forces $`\vec{F}_{_{TMD_Z/O_N}}`$ are given by

``` math
\begin{aligned}
\vec{F}_{_{TMD_Z/O_N}} = \left[
\begin{array}{c}
F_{X_{_{TMD_Z/O_N}}} + m_z a_{_{G_X/O_N}} \\
F_{Y_{_{TMD_Z/O_N}}} + m_z a_{_{G_Y/O_N}} \\
- c_z \dot{z}_{_{TMD_Z/P_N}} - k_z z_{_{TMD_Z/P_N}}
+ m_z a_{_{G_Z/O_N}} + F_{ext_z} + F_{StopFrc_{Z}} + F_{Z_{PreLoad}}
\end{array}
\right]
\end{aligned}
```

where $`F_{Z_{PreLoad}}`$ is a spring pre-load to shift the neutral position when gravity acts upon the mass for the $`TMD_Z`$. $`TMD_Z`$ is fixed to frame $`N`$ in the $`x`$ and $`y`$ directions so that

``` math
\begin{aligned}
{r}_{_{TMD_Z/P_N}} = \left[
\begin{array}{c}
0 \\
0 \\
z_{_{TMD_Z/P_N}}
\end{array}
\right]
\end{aligned}
```

The other components of Eqn. `EOM` are:

``` math
\begin{aligned}
\vec{\omega}_{_{N/O_N}} \times (\vec{\omega}_{_{N/O_N}} \times \vec{r}_{_{TMD_Z/P_N}})
= z_{_{TMD_Z/P_N}} \left[
\begin{array}{c}
\dot{\theta}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}} \\
\dot{\phi}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}} \\
-(\dot{\theta}_{_{N/O_N}}^2 + \dot{\phi}_{_{N/O_N}}^2)
\end{array}
\right]
\end{aligned}
```

``` math
\begin{aligned}
2\vec{\omega}_{_{N/O_N}} \times \dot{\vec{r}}_{_{TMD_Z/P_N}}
= \dot{z}_{_{TMD_Z/P_N}} \left[
\begin{array}{c}
2\dot{\phi}_{_{N/O_N}} \\
-2\dot{\theta}_{_{N/O_N}} \\
0
\end{array}
\right]
\end{aligned}
```

``` math
\begin{aligned}
\vec{\alpha}_{_{N/O_N}} \times \vec{r}_{_{TMD_Z/P_N}}
= z_{_{TMD_Z/P_N}} \left[
\begin{array}{c}
\ddot{\phi}_{_{N/O_N}} \\
-\ddot{\theta}_{_{N/O_N}} \\
0
\end{array}
\right]
\end{aligned}
```

Therefore $`\ddot{z}_{_{TMD_Z/P_N}}`$ is governed by the equations

<span label="EOM_Zz">
``` math
\begin{aligned}
\begin{aligned}
\ddot{z}_{_{TMD_Z/P_N}}
= & (\dot{\theta}_{_{N/O_N}}^2
+ \dot{\phi}_{_{N/O_N}}^2-\frac{k_z}{m_z}) z_{_{TMD_Z/P_N}}
- (\frac{c_z}{m_z}) \dot{z}_{_{TMD_Z/P_N}} 
-\ddot{z}_{_{P/O_N}} + a_{_{G_Z/O_N}}\\
&+ \frac{1}{m_z} (F_{ext_Z} + F_{StopFrc_{Z}} + F_{Z_{PreLoad}})
\end{aligned}
\end{aligned}
```
</span>

The forces $`F_{X_{_{TMD_Z/O_N}}}`$ and $`F_{Y_{_{TMD_Z/O_N}}}`$ are solved noting $`\ddot{x}_{_{TMD_Z/P_N}} = \ddot{y}_{_{TMD_Z/P_N}} = 0`$:

<span label="EOM_Zx">
``` math
F_{X_{_{TMD_Z/O_N}}} = m_z \left( - a_{_{G_X/O_N}} + \ddot{x}_{_{P/O_N}}
+ (\ddot{\phi}_{_{N/O_N}}
+ \dot{\theta}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}}) z_{_{TMD_Z/P_N}}
+ 2\dot{\phi}_{_{N/O_N}} \dot{z}_{_{TMD_Z/P_N}} \right)
```
</span>

<span label="EOM_Zy">
``` math
F_{Y_{_{TMD_Z/O_N}}} = m_z \left( - a_{_{G_Y/O_N}} + \ddot{y}_{_{P/O_N}}
- (\ddot{\theta}_{_{N/O_N}}
- \dot{\phi}_{_{N/O_N}}\dot{\psi}_{_{N/O_N}}) z_{_{TMD_Z/P_N}}
- 2\dot{\theta}_{_{N/O_N}} \dot{z}_{_{TMD_Z/P_N}} \right)
```
</span>

### State Equations

#### Inputs:

The inputs are the component linear acceleration and angular position, velocity and acceleration:

``` math
\begin{aligned}
\vec{u} = \left[
\begin{array}{c}
\ddot{\vec{r}}_{_{P/O_G}} \\
\vec{R}_{_{N/G}} \\
\vec{\omega}_{_{N/O_G}} \\
\vec{\alpha}_{_{N/O_G}}
\end{array}
\right]
\Rightarrow \left[
\begin{array}{c}
\ddot{\vec{r}}_{_{P/O_N}} \\
\vec{\omega}_{_{N/O_N}} \\
\vec{\alpha}_{_{N/O_N}}
\end{array}
\right]
= \left[
\begin{array}{c}
\vec{R}_{_{N/G}} \ddot{\vec{r}}_{_{P/O_G}} \\
\vec{R}_{_{N/G}} \vec{\omega}_{_{N/O_G}} \\
\vec{R}_{_{N/G}} \vec{\alpha}_{_{N/O_G}
}\end{array}
\right]
\end{aligned}
```

#### States:

The states are the position and velocity of the TMDs along their respective DOFs in the component reference frame:

``` math
\begin{aligned}
\vec{R}_{_{TMD/P_N}} = \left[
\begin{array}{c}
x \\
\dot{x} \\
y \\
\dot{y} \\
z \\
\dot{z}
\end{array}
\right]_{_{TMD/P_N}} 
= \left[
\begin{array}{c}
{x}_{_{TMD_X/P_N}} \\
\dot{x}_{_{TMD_X/P_N}} \\
{y}_{_{TMD_Y/P_N}} \\
\dot{y}_{_{TMD_Y/P_N}} \\
{z}_{_{TMD_Z/P_N}} \\
\dot{z}_{_{TMD_Z/P_N}}
\end{array}
\right]
\end{aligned}
```

The equations of motion can be re-written as a system of non-linear first-order equations of the form

``` math
\dot{\vec{R}}_{_{TMD}} = A \vec{R}_{_{TMD}} + B
```

where

``` math
\begin{aligned}
A(\vec{u}) = \left[
\begin{array}{cccccc}
0& 1 &0&0&0&0 \\
(\dot{\phi}_{_{N/O_N}}^2 + \dot{\psi}_{_{N/O_N}}^2-\frac{k_x}{m_x}) & - (\frac{c_x}{m_x}) &0&0&0&0 \\
0&0&0& 1 &0&0 \\
0&0& (\dot{\theta}_{_{N/O_N}}^2 + \dot{\psi}_{_{N/O_N}}^2-\frac{k_y}{m_y}) & - (\frac{c_y}{m_y}) &0&0 \\
0&0&0&0&0& 1 \\
0&0&0&0& (\dot{\theta}_{_{N/O_N}}^2 + \dot{\phi}_{_{N/O_N}}^2-\frac{k_z}{m_z}) & - (\frac{c_z}{m_z}) \\ 
\end{array} \right]
\end{aligned}
```

and

<span label="Bu">
``` math
\begin{aligned}
B(\vec{u}) = \left[
\begin{array}{l}
0 \\
-\ddot{x}_{_{P/O_N}}+a_{_{G_X/O_N}} + \frac{1}{m_x} ( F_{ext_X} + F_{StopFrc_{X}}) \\
0 \\
-\ddot{y}_{_{P/O_N}}+a_{_{G_Y/O_N}} + \frac{1}{m_y} (F_{ext_Y}+ F_{StopFrc_{Y}}) \\
0 \\
-\ddot{z}_{_{P/O_N}}+a_{_{G_Z/O_N}} + \frac{1}{m_z} (F_{ext_Z}+ F_{StopFrc_{Z}} + F_{Z_{PreLoad}})
\end{array}
\right]
\end{aligned}
```
</span>

The inputs are coupled to the state variables, resulting in A and B as $`f(\vec{u})`$.

### Outputs

The output vector $`\vec{Y}`$ is

``` math
\begin{aligned}
\vec{Y} = \left[
\begin{array}{c}
\vec{F}_{_{P_G}} \\
\vec{M}_{_{P_G}}
\end{array}
\right]
\end{aligned}
```

The output includes reaction forces corresponding to $`F_{Y_{_{TMD_X/O_N}}}`$, $`F_{Z_{_{TMD_X/O_N}}}`$, $`F_{X_{_{TMD_Y/O_N}}}`$, $`F_{Z_{_{TMD_Y/O_N}}}`$, $`F_{X_{_{TMD_Z/O_N}}}`$, and $`F_{Y_{_{TMD_Z/O_N}}}`$ from Eqns. `EOM_Xy`, `EOM_Xz`, `EOM_Yx`, `EOM_Yz`, `EOM_Zx`, and `EOM_Zy`. The resulting forces $`\vec{F}_{_{P_G}}`$ and moments $`\vec{M}_{_{P_G}}`$ acting on the component are

<span label="OutputForces">
``` math
\begin{aligned}
\begin{aligned}
\vec{F}_{_{P_G}} = R^T_{_{N/G}} & \left[
\begin{array}{l}
k_x {x}_{_{TMD_X/P_N}} + c_x \dot{x}_{_{TMD_X/P_N}} - F_{StopFrc_{X}} - F_{ext_x} - F_{X_{_{TMD_Y/O_N}}} - F_{X_{_{TMD_Z/O_N}}} \\ 
k_y {y}_{_{TMD_Y/P_N}} + c_y \dot{y}_{_{TMD_Y/P_N}} - F_{StopFrc_{Y}} - F_{ext_y} - F_{Y_{_{TMD_X/O_N}}} - F_{Y_{_{TMD_Z/O_N}}} \\ 
k_z {z}_{_{TMD_Z/P_N}} + c_z \dot{z}_{_{TMD_Z/P_N}} - F_{StopFrc_{Z}} - F_{ext_z} - F_{Z_{_{TMD_X/O_N}}} - F_{Z_{_{TMD_Y/O_N}}} - F_{Z_{PreLoad}}
\end{array}
\right]
\end{aligned}
\end{aligned}
```
</span>

and

``` math
\begin{aligned}
\vec{M}_{_{P_G}} = R^T_{_{N/G}} \left[
\begin{array}{c}
M_{_X} \\
M_{_Y} \\
M_{_Z}
\end{array}
\right]_{_{N/N}} = R^T_{_{N/G}} \left[
\begin{array}{c}
-(F_{Z_{_{TMD_Y/O_N}}}) y_{_{TMD/P_N}} + (F_{Y_{_{TMD_Z/O_N}}} ) z_{_{TMD/P_N}} \\
(F_{Z_{_{TMD_X/O_N}}}) x_{_{TMD/P_N}} - (F_{X_{_{TMD_Z/O_N}}} ) z_{_{TMD/P_N}} \\
-(F_{Y_{_{TMD_X/O_N}}}) x_{_{TMD/P_N}} + ( F_{X_{_{TMD_Y/O_N}}}) y_{_{TMD/P_N}}
\end{array}
\right]
\end{aligned}
```

#### Stop Forces

The extra forces $`F_{StopFrc_{X}}`$, $`F_{StopFrc_{Y}}`$, and $`F_{StopFrc_{Z}}`$ are added to output forces in the case that the movement of TMD_X, TMD_Y, or TMD_Z exceeds the maximum track length for the mass. Otherwise, they equal zero. The track length has limits on the positive and negative ends in the TMD direction (X_PSP and X_NSP, Y_PSP and Y_NSP, and Z_PSP and Z_NSP). If we define a general maximum and minimum displacements as $`x_{max}`$ and $`x_{min}`$, respectively, the stop forces have the form

``` math
\begin{aligned}
F_{StopFrc} = -\left\{
\begin{array}{lr}
\begin{aligned}
k_S \Delta x  & \quad : ( x > x_{max} \wedge \dot{x}<=0) \vee ( x < x_{min} \wedge \dot{x}>=0)\\
k_S \Delta x + c_S \dot{x} & \quad : ( x > x_{max} \wedge \dot{x}>0) \vee ( x < x_{min} \wedge \dot{x}<0)\\
0 & \quad : \text{otherwise}
\end{aligned}
\end{array}
\right.
\end{aligned}
```

where $`\Delta x`$ is the distance the mass has traveled beyond the stop position and $`k_S`$ and $`c_S`$ are large stiffness and damping constants.

#### Pre-Load Forces

The extra force $`F_{Z_{PreLoad}}`$ is added to the output forces as a method to shift the at rest position of the TMD_Z when gravity is acting on it. This is particularly useful for substructure mounted StCs when very large masses with soft spring constants are used. This appears in the term $`\vec{F}_{_{TMD_Z/O_N}}`$ and in eq equations of motion given by `Bu` and resulting forces in `OutputForces`.

## Code Modifications

The Structural Control (StC) function is a submodule linked into ServoDyn. In addition to references in ServoDyn.f90 and ServoDyn.txt, new files that contain the StC module are listed below.

### New Files

- StrucCtrl.f90 : the structural control module
- StrucCtrl.txt : registry file include files, inputs, states, parameters, and outputs shown in Tables [1](#tbl2) and [2](#tbl1)
- StrucCtrl_Types.f90: automatically generated

### Variables

<div id="tbl2" class="container">

<table>
<caption>Summary of field definitions in the StC registry. Note that state vector <span class="math inline">$\vec{tmd_x}$</span> corresponds to <span class="math inline"><em>R⃗</em><sub><sub><em>T</em><em>M</em><em>D</em>/<em>P</em><sub><em>N</em></sub></sub></sub></span>, and that the outputs <span class="math inline"><em>F⃗</em><sub><sub><em>P</em><sub><em>G</em></sub></sub></sub></span> and <span class="math inline"><em>M⃗</em><sub><sub><em>P</em><sub><em>G</em></sub></sub></sub></span> are contained in the MeshType object (y.Mesh). <span class="math inline"><em>X</em><sub><em>D</em><em>S</em><em>P</em></sub></span>, <span class="math inline"><em>Y</em><sub><em>D</em><em>S</em><em>P</em></sub></span>, and <span class="math inline"><em>Z</em><sub><em>D</em><em>S</em><em>P</em></sub></span> are initial displacements of the TMDs.</caption>
<colgroup>
<col style="width: 22%" />
<col style="width: 77%" />
</colgroup>
<thead>
<tr>
<th rowspan="2">DataType</th>
<th rowspan="2">Variable name</th>
</tr>
<tr>
</tr>
</thead>
<tbody>
<tr>
<td><strong>InitInput</strong></td>
<td></td>
</tr>
<tr>
<td></td>
<td>InputFile</td>
</tr>
<tr>
<td></td>
<td>Gravity</td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>r⃗</em><sub><sub><em>N</em>/<em>O</em><sub><em>G</em></sub></sub></sub></span></td>
</tr>
<tr>
<td><strong>Input u</strong></td>
<td></td>
</tr>
<tr>
<td></td>
<td><span class="math inline">$\ddot{\vec{r}}_{_{P/O_G}}$</span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>R⃗</em><sub><sub><em>N</em>/<em>O</em><sub><em>G</em></sub></sub></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>ω⃗</em><sub><sub><em>N</em>/<em>O</em><sub><em>G</em></sub></sub></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>α⃗</em><sub><sub><em>N</em>/<em>O</em><sub><em>G</em></sub></sub></sub></span></td>
</tr>
<tr>
<td><strong>Parameter p</strong></td>
<td></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>m</em><sub><em>x</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>c</em><sub><em>x</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>k</em><sub><em>x</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>m</em><sub><em>y</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>c</em><sub><em>y</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>k</em><sub><em>y</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>m</em><sub><em>z</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>c</em><sub><em>z</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>k</em><sub><em>z</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>K</em><sub><em>S</em></sub> = [<em>k</em><sub><em>S</em><em>X</em></sub>  <em>k</em><sub><em>S</em><em>Y</em></sub>  <em>k</em><sub><em>S</em><em>Z</em></sub>]</span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>C</em><sub><em>S</em></sub> = [<em>c</em><sub><em>S</em><em>X</em></sub>  <em>c</em><sub><em>S</em><em>Y</em></sub>  <em>c</em><sub><em>S</em><em>Z</em></sub>]</span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>P</em><sub><em>S</em><em>P</em></sub> = [<em>X</em><sub><em>P</em><em>S</em><em>P</em></sub>  <em>Y</em><sub><em>P</em><em>S</em><em>P</em></sub>  <em>Z</em><sub><em>P</em><em>S</em><em>P</em></sub>]</span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>P</em><sub><em>S</em><em>P</em></sub> = [<em>X</em><sub><em>N</em><em>S</em><em>P</em></sub>  <em>Y</em><sub><em>N</em><em>S</em><em>P</em></sub>  <em>Z</em><sub><em>N</em><em>S</em><em>P</em></sub>]</span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>F</em><em>e</em><em>x</em><em>t</em></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>G</em><em>r</em><em>a</em><em>v</em><em>i</em><em>t</em><em>y</em></span></td>
</tr>
<tr>
<td></td>
<td>TMDX_DOF</td>
</tr>
<tr>
<td></td>
<td>TMDY_DOF</td>
</tr>
<tr>
<td></td>
<td>TMDZ_DOF</td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>X</em><sub><em>D</em><em>S</em><em>P</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>Y</em><sub><em>D</em><em>S</em><em>P</em></sub></span></td>
</tr>
<tr>
<td></td>
<td><span class="math inline"><em>Z</em><sub><em>D</em><em>S</em><em>P</em></sub></span></td>
</tr>
<tr>
<td><strong>State x</strong></td>
<td></td>
</tr>
<tr>
<td></td>
<td><span class="math inline">$\vec{tmd_x}$</span></td>
</tr>
<tr>
<td><strong>Output y</strong></td>
<td></td>
</tr>
<tr>
<td></td>
<td>Mesh</td>
</tr>
</tbody>
</table>

</div>

The input, parameter, state and output definitions are summarized in Table [1](#tbl2). The inputs from file are listed in Table [2](#tbl1).

<div id="tbl1" class="container">

| Field Name | Field Type | Description                                          |
|------------|------------|------------------------------------------------------|
| TMD_CMODE  | int        | Control Mode (1:passive, 2:active)                   |
| TMD_X_DOF  | logical    | DOF on or off                                        |
| TMD_Y_DOF  | logical    | DOF on or off                                        |
| TMD_Z_DOF  | logical    | DOF on or off                                        |
| TMD_X_DSP  | real       | TMD_X initial displacement                           |
| TMD_Y_DSP  | real       | TMD_Y initial displacement                           |
| TMD_Z_DSP  | real       | TMD_Z initial displacement                           |
| TMD_X_M    | real       | TMD mass                                             |
| TMD_X_K    | real       | TMD stiffness                                        |
| TMD_X_C    | real       | TMD damping                                          |
| TMD_Y_M    | real       | TMD mass                                             |
| TMD_Y_K    | real       | TMD stiffness                                        |
| TMD_Y_C    | real       | TMD damping                                          |
| TMD_Z_M    | real       | TMD mass                                             |
| TMD_Z_K    | real       | TMD stiffness                                        |
| TMD_Z_C    | real       | TMD damping                                          |
| TMD_X_PSP  | real       | positive stop position (maximum X mass displacement) |
| TMD_X_NSP  | real       | negative stop position (minimum X mass displacement) |
| TMD_X_K_SX | real       | stop spring stiffness                                |
| TMD_X_C_SX | real       | stop spring damping                                  |
| TMD_Y_PSP  | real       | positive stop position (maximum Y mass displacement) |
| TMD_Y_NSP  | real       | negative stop position (minimum Y mass displacement) |
| TMD_Y_K_S  | real       | stop spring stiffness                                |
| TMD_Y_C_S  | real       | stop spring damping                                  |
| TMD_Z_PSP  | real       | positive stop position (maximum Z mass displacement) |
| TMD_Z_NSP  | real       | negative stop position (minimum Z mass displacement) |
| TMD_Z_K_S  | real       | stop spring stiffness                                |
| TMD_Z_C_S  | real       | stop spring damping                                  |
| TMD_P_X    | real       | x origin of P in nacelle coordinate system           |
| TMD_P_Y    | real       | y origin of P in nacelle coordinate system           |
| TMD_P_Z    | real       | z origin of P in nacelle coordinate system           |

Data read in from TMDInputFile.

</div>

## Acknowledgements

The authors would like to thank Dr. Jason Jonkman for reviewing this manual.

[^1]: Note that $`( R a ) \times ( Rb ) = R( a \times b )`$.
