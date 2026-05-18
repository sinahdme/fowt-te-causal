# Tail fin Aerodynamics Theory

## Notations

**Tail fin aerodynamic reference point**

The tail fin aerodynamic reference point, $`\boldsymbol{x}_\text{ref}`$, is the point where the aerodynamic loads are calculated on the tail fin. The structural solver computes the instantenous position, velocity, acceleration, of the reference point at each time step. The initial position of the reference point with respect to the tower top is a user input. Typical choices are the leading edge/apex of the fin or a point close to the center of pressure at zero angle of attack. The other aerodynamic inputs (e.g. aerodynamic moment coefficient) need to be consistent with the choice of the reference point.

**Tail fin coordinate system**

The inertial and tail fin coordinate systems are illustrated in `figTFcoord1`. The transformation matrix from the inertial coordinate system to the tail fin coordinate system is given by $`\boldsymbol{R}_\text{tf,i}`$.

> Coordinate systems and velocity vectors used for the tail fin aerodynamics

The reference orientation (when the structure is un-deflected), the transformation matrix is:

``` math
:label: tfRrfiinit
```
``` math
\boldsymbol{R}_\text{tf,i} = \operatorname{EulerConstruct}(\theta_\text{bank}, \theta_\text{tilt}, \theta_\text{skew})
```

For a common application with a vertical fin, the three angles are zero.

**Velocities**

The following velocity vectors (3D vectors in global coordinates) are defined (see `figTFcoord1`):

- $`\boldsymbol{V}_\text{wind}`$: Undisturbed Wind speed vector at the reference point
- $`\boldsymbol{V}_\text{dist}`$: Disturbed wind speed vector at the reference point (the disturbed wind contains the influence of the tower on the flow). AeroDyn has internal methods to compute $`\boldsymbol{V}_\text{dist}`$ from $`\boldsymbol{V}_\text{wind}`$.
- $`\boldsymbol{V}_\text{elast}`$: Structural translational velocity vector at the reference point
- $`\boldsymbol{V}_\text{ind}`$: Induced velocity from the wake at the reference point (assumed to be zero for now)
- $`\boldsymbol{\omega}`$: Structural rotational velocity of the fin

All velocities (except for $`\boldsymbol{V}_\text{ind}`$ and $`\boldsymbol{V}_\text{dist}`$ which are computed internally by AeroDyn) are provided as input to the aerodynamic solver. The relative wind experienced by the airfoil is given by:

``` math
:label: tfVrel
```
``` math
\boldsymbol{V}_\text{rel} = 
     \boldsymbol{V}_\text{wind} 
    -\boldsymbol{V}_\text{elast} 
    +\boldsymbol{V}_\text{ind}
```

**Angle of attack**

The angle of attack is defined in the $`x_\text{tf}-y_\text{tf}`$ plane of the tail fin coordinate systems as illustrated in `figTFcoord2`.

> Tail fin airfoil coordinate system and definition of angle of attack in the x-y plane

We write $`V_{\text{rel},\perp}`$ the projection of $`\boldsymbol{V}_\text{rel}`$ in this plane. The angle of attack is given by the components of this vector:

``` math
:label: tfalpha
```
``` math
\alpha = \arctan\frac{V_{\text{rel},y_\text{tf}}}{V_{\text{rel},x_\text{tf}}}
```

In this implementation, the function <span class="title-ref">atan2</span> is used to compute the angle of attack.

**Loads**

If the dimensionless coefficients are known, they can be projected in the $`x_\text{tf}-y_\text{tf}`$ plane as follows:

``` math
:label: tfCxCy
```
``` math
C_{x_\text{tf}}(\alpha)  = -C_l(\alpha) \sin\alpha + C_d(\alpha)\cos\alpha
,\quad                                                     
C_{y_\text{tf}}(\alpha)  =  C_l(\alpha) \cos\alpha + C_d(\alpha)\sin\alpha
```

and the loads are therefore given by:

``` math
:label: tffxfymz
```
``` math
f_{x_\text{tf}} = \frac{1}{2}\rho V_{\text{rel},\perp}^2 A  \,C_{x_\text{tf}}(\alpha)
             ,\quad
f_{y_\text{tf}} = \frac{1}{2}\rho V_{\text{rel},\perp}^2 A  \,C_{y_\text{tf}}(\alpha)
             ,\quad
m_{z_\text{tf}} = \frac{1}{2}\rho V_{\text{rel},\perp}^2 Ac \, C_m(\alpha)
```

Once the loads are known in the tail fin coordinate systems, they are transferred to the inertial system as follows:

``` math
:label: tfforcesi
```
``` math
\begin{aligned}
\left.\boldsymbol{f}\right|_{i} = \boldsymbol{R}_\text{tf,i}^t  \left.\boldsymbol{f}\right|_\text{tf} 
 = \boldsymbol{R}_\text{tf,i}^t  
 \begin{bmatrix}
 f_{x_\text{tf}}\\
 f_{y_\text{tf}}\\
 0\\
 \end{bmatrix}
 ,\qquad
\left.\boldsymbol{m}\right|_{i} = \boldsymbol{R}_\text{tf,i}^t  \left.\boldsymbol{m}\right|_\text{tf} 
 = \boldsymbol{R}_\text{tf,i}^t  
 \begin{bmatrix}
 0\\
 0\\
 m_{z_\text{tf}}\\
 \end{bmatrix}
\end{aligned}
```

**Induced velocity**

The induced velocity from the wake at the reference point will affect the relative wind and therefore the angle of attack of the tail fin. Different models are implemented to compute this induced velocity. As a first approximation, this velocity may be set to zero (corresponding to the input <span class="title-ref">TFinIndMod=0</span>):

``` math
:label: TFVindZero
```
``` math
\boldsymbol{V}_\text{ind}=0
```

The rotor-averaged induced velocity can also be used as an estimate (<span class="title-ref">TFinIndMod=1</span>). It is computed as the mean induced velocity over all the blade and aerodynamic nodes

``` math
:label: TFVindRtAvg
```
``` math
\boldsymbol{V}_\text{ind}=\frac{1}{n_B n_r}\sum_{i_b=1..n_B} \sum_{i_r=1..n_r}  \boldsymbol{V}_{\text{ind},\text{blade}}[i_b, i_r]
```

Where $`\boldsymbol{V}_{\text{ind},\text{blade}}[i_b, i_r]`$ is the induced velocity vector for blade $`i_b`$ and at the radial node $`i_r`$.

More advanced models could set the induced velocity to zero when outside of the wake boundary, or include a tower-shadow-like wake model. Such option is not yet available.

## Polar-based model

In the polar-based model, the user provides the aerodynamic coefficients $`C_l, C_d, C_m`$, as tabulated data, functions of the angle of attack. The aerodynamic moment is assumed to be provided at the reference point. A common practice is to use the center of pressure at zero angle of attack for polar data, so the user might want to chose such a point as the reference point of the fin. The tabulated data are provided as part of the list of airfoils given with <span class="title-ref">AFNames</span> in the AeroDyn input file. The user only needs to indicate the index <span class="title-ref">TFinAFIndex</span> within the list <span class="title-ref">AFNames</span> to indicate which polar to use for the tail fin.

## Unsteady slender body model

The unsteady aerodynamics of the tail fin is modeled based on Unsteady Slender Body Theory. The theory is extended to include the effect of high yaw angle ad-hammam_NREL:2023. To simplify the implementation, it is assumed that that arm length of the tail fin is much greater than the chord and the characteristic time (chord/wind speed) is small.

The normal force on the tail fin can be described as the sum of three contributions (potential lift, vortex lift, and drag), weighted by separation functions $`x_i`$ as:

<span label="tfusbforce">
``` math
N = \frac{\rho}{2} A_{tf} \bigg(  K_p x_1 V_{\text{rel},x} V_{\text{rel},y} +  \Big[x_2 K_v+(1- x_3)C_{Dc} \Big] V_{\text{rel},y}\big|V_{\text{rel},y}\big|\bigg)
```
</span>

where $`\rho`$ is the density of air, $`A_{tf}`$ is the tail fin area, $`K_p`$ is the potential lift coefficient and $`K_v`$ is the vortex lift coefficient, and $`C_{Dc}`$ is the drag coefficient. Note that the sign convnetion of OpenFAST is slightly different than used in ad-hammam_NREL:2023. This is reflected in Equation `tfusbforce`.

$`x_i`$ are the separation functions calculated using a quasi-steady approximation as:

``` math
:label: TFUSBxiEquation
```
``` math
x_i = (1+exp{[\sigma_i (|\gamma_{tf}|-\alpha^*_i)]})^{-1}
```

where $`\sigma_i`$ are empirical constants characterizing the decay of separation functions, $`\gamma_{tf}`$ is the yaw angle of the tail fin with respect to the free-stream wind ($`V_{\text{wind}}`$), $`\alpha^*_i`$ are the characteristics angles for separation functions. $`x_i`$ takes on a value between 0 and 1, and are used to activate or deactivate a the contribution of potential lift, vortex lift and drag to the normal force on the tail fin.

The normal force is assumed to act at the user defined reference point on the tail fin and the moment of the normal force is calculated accordingly.
