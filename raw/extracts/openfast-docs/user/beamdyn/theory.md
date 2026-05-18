# BeamDyn Theory

This section focuses on the theory behind the BeamDyn module. The theoretical foundation, numerical tools, and some special handling in the implementation will be introduced. References will be provided in each section detailing the theories and numerical tools.

In this chapter, matrix notation is used to denote vectorial or vectorial-like quantities. For example, an underline denotes a vector $`\underline{u}`$, an over bar denotes unit vector $`\bar{n}`$, and a double underline denotes a tensor $`\underline{\underline{\Delta}}`$. Note that sometimes the underlines only denote the dimension of the corresponding matrix.

## Coordinate Systems

`blade-geometry` (in `bd-input-files`) and `bd-frame` show the coordinate system used in BeamDyn.

<div id="bd-frame">

<figure class="align-center">
<img src="figs/bd_frame.png" style="width:100.0%" alt="figs/bd_frame.png" />
<figcaption>Global, blade reference, and internal coordinate systems in BeamDyn. Illustration by Al Hicks, NLR.</figcaption>
</figure>

</div>

### Global Coordinate System

The global coordinate system is denoted as `X`, `Y`, and `Z` in `bd-frame`. This is an inertial frame and in FAST its origin is usually placed at the bottom of the tower as shown.

### BD Coordinate System

The BD coordinate system is denoted as $`x_1`$, $`x_2`$, and $`x_3`$ respectively in `bd-frame`. This is an inertial frame used internally in BeamDyn (i.e., doesn’t rotate with the rotor) and its origin is placed at the initial position of the blade root point.

### Blade Reference Coordinate System

The blade reference coordinate system is denoted as $`X_{rt}`$, $`Y_{rt}`$, and $`Z_{rt}`$ in `bd-frame` at initialization ($`t = 0`$). The blade reference coordinate system is a floating frame that attaches at the blade root and is rotating with the blade. Its origin is at the blade root and the directions of axes following the IEC standard, i.e., $`Z_r`$ is pointing along the blade axis from root to tip; $`Y_r`$ pointing nominally towards the trailing edge of the blade and parallel with the chord line at the zero-twist blade station; and $`X_r`$ is orthogonal with the $`Y_r`$ and $`Z_r`$ axes, such that they form a right-handed coordinate system (pointing nominally downwind). We note that the initial blade reference coordinate system, denoted by subscript $`r0`$, coincides with the BD coordinate system, which is used internally in BeamDyn and introduced in the previous section. The axis convention relations between the initial blade reference coordinate system and the BD coordinate system can be found in `IECBD`.

<div id="IECBD">

|             |            |            |            |
|-------------|------------|------------|------------|
| Blade Frame | $`X_{r0}`$ | $`Y_{r0}`$ | $`Z_{r0}`$ |
| BD Frame    | $`x_2`$    | $`x_3`$    | $`x_1`$    |

Transformation between blade coordinate system and BD coordinate system.

</div>

### Local blade coordinate system

The local blade coordinate system is used for some input and output quantities, for example, the cross-sectional mass and stiffness matrices and the sectional force and moment resultants. This coordinate system is different from the blade reference coordinate system in that its $`Z_l`$ axis is always tangent to the blade axis as the blade deflects. Note that a subscript $`l`$ denotes the local blade coordinate system.

## Geometrically Exact Beam Theory

The theoretical foundation of BeamDyn is the geometrically exact beam theory. This theory features the capability of beams that are initially curved and twisted and subjected to large displacement and rotations. Along with a proper two-dimensional (2D) cross-sectional analysis, the coupling effects between all six DOFs, including extension, bending, shear, and torsion, can be captured by GEBT as well . The term, “geometrically exact” refer to the fact that there is no approximation made on the geometries, including both initial and deformed geometries, in formulating the equations HodgesBeamBook.

The governing equations of motion for geometrically exact beam theory can be written as Bauchau:2010

<span label="GovernGEBT-1-2">
``` math
\begin{aligned}
\dot{\underline{h}} - \underline{F}^\prime &= \underline{f} \\
\dot{\underline{g}} + \dot{\tilde{u}} \underline{h} - \underline{M}^\prime + (\tilde{x}_0^\prime + \tilde{u}^\prime)^T \underline{F} &= \underline{m}
\end{aligned}
```
</span>

where $`{\underline{h}}`$ and $`{\underline{g}}`$ are the linear and angular momenta resolved in the inertial coordinate system, respectively; $`{\underline{F}}`$ and $`{\underline{M}}`$ are the beam’s sectional force and moment resultants, respectively; $`{\underline{u}}`$ is the one-dimensional (1D) displacement of a point on the reference line; $`{\underline{x}}_0`$ is the position vector of a point along the beam’s reference line; and $`{\underline{f}}`$ and $`{\underline{m}}`$ are the distributed force and moment applied to the beam structure. The notation $`(\bullet)^\prime`$ indicates a derivative with respect to beam axis $`x_1`$ and $`\dot{(\bullet)}`$ indicates a derivative with respect to time. The tilde operator $`({\widetilde{\bullet}})`$ defines a skew-symmetric tensor corresponding to the given vector. In the literature, it is also termed as “cross-product matrix”. For example,

``` math
\begin{aligned}
{\widetilde{n}} =
     \begin{bmatrix}
     0 & -n_3 & n_2 \\
     n_3 & 0 & -n_1 \\
     -n_2 & n_1 & 0\\
     \end{bmatrix}
\end{aligned}
```

The constitutive equations relate the velocities to the momenta and the 1D strain measures to the sectional resultants as

<span label="ConstitutiveMass-Stiff">
``` math
\begin{aligned}
\begin{Bmatrix}
\underline{h} \\
\underline{g}
\end{Bmatrix}
= \underline{\underline{\mathcal{M}}} \begin{Bmatrix}
\dot{\underline{u}} \\
\underline{\omega}
\end{Bmatrix} \\
\end{aligned}
```
``` math
\begin{aligned}
\begin{Bmatrix}
\underline{F} \\
\underline{M}
\end{Bmatrix}
= \underline{\underline{\mathcal{C}}} \begin{Bmatrix}
\underline{\epsilon} \\
\underline{\kappa}
\end{Bmatrix}
\end{aligned}
```
</span>

where $`\underline{\underline{\mathcal{M}}}`$ and $`\underline{\underline{\mathcal{C}}}`$ are the $`6 \times 6`$ sectional mass and stiffness matrices, respectively (note that they are not really tensors); $`\underline{\epsilon}`$ and $`\underline{\kappa}`$ are the 1D strains and curvatures, respectively; and, $`\underline{\omega}`$ is the angular velocity vector that is defined by the rotation tensor $`\underline{\underline{R}}`$ as $`\underline{\omega} =
axial(\dot{\underline{\underline{R}}}~\underline{\underline{R}}^T)`$. The axial vector $`{\underline{a}}`$ associated with a second-order tensor $`{\underline{\underline{A}}}`$ is denoted $`{\underline{a}}=axial({\underline{\underline{A}}})`$ and its components are defined as

<span label="axial">
``` math
\begin{aligned}
{\underline{a}} = axial({\underline{\underline{A}}})=\begin{Bmatrix}
a_1 \\
a_2 \\
a_3
\end{Bmatrix}
=\frac{1}{2}
\begin{Bmatrix}
A_{32}-A_{23} \\
A_{13}-A_{31} \\
A_{21}-A_{12}
\end{Bmatrix}
\end{aligned}
```
</span>

The 1D strain measures are defined as

<span label="1DStrain">
``` math
\begin{aligned}
\begin{Bmatrix}
   {\underline{\epsilon}} \\
   {\underline{\kappa}}
\end{Bmatrix}
=
\begin{Bmatrix}
        {\underline{x}}^\prime_0 + {\underline{u}}^\prime - ({\underline{\underline{R}}} ~{\underline{\underline{R}}}_0) \bar{\imath}_1 \\
        {\underline{k}}
\end{Bmatrix}
\end{aligned}
```
</span>

where $`{\underline{k}} = axial [({\underline{\underline{R R_0}}})^\prime ({\underline{\underline{R R_0}}})^T]`$ is the sectional curvature vector resolved in the inertial basis; $`{\underline{\underline{R}}}_0`$ is the initial rotation tensor; and $`\bar{\imath}_1`$ is the unit vector along $`x_1`$ direction in the inertial basis. These three sets of equations, including equations of motion Eq. `GovernGEBT-1-2`, constitutive equations Eq. `ConstitutiveMass-Stiff`, and kinematical equations Eq. `1DStrain`, provide a full mathematical description of the beam elasticity problems.

## Numerical Implementation with Legendre Spectral Finite Elements

For a displacement-based finite element implementation, there are six degree-of-freedoms at each node: three displacement components and three rotation components. Here we use $`{\underline{q}}`$ to denote the elemental displacement array as $`\underline{q}=\left[
\underline{u}^T~~\underline{c}^T\right]`$ where $`{\underline{u}}`$ is the displacement and $`{\underline{c}}`$ is the rotation-parameter vector. The acceleration array can thus be defined as $`\underline{a}=\left[ \ddot{\underline{u}}^T~~ \dot{\underline{\omega}}^T \right]`$. For nonlinear finite-element analysis, the discretized and incremental forms of displacement, velocity, and acceleration are written as

<span label="Discretized">
``` math
\begin{aligned}
\underline{q} (x_1) &= \underline{\underline{N}} ~\hat{\underline{q}}~~~~\Delta \underline{q}^T = \left[ \Delta \underline{u}^T~~\Delta \underline{c}^T \right] \\
\underline{v}(x_1) &= \underline{\underline{N}}~\hat{\underline{v}}~~~~\Delta \underline{v}^T = \left[\Delta \underline{\dot{u}}^T~~\Delta \underline{\omega}^T \right] \\
\underline{a}(x_1) &= \underline{\underline{N}}~ \hat{\underline{a}}~~~~\Delta \underline{a}^T = \left[ \Delta \ddot{\underline{u}}^T~~\Delta \dot{\underline{\omega}}^T \right]
\end{aligned}
```
</span>

where $`{\underline{\underline{N}}}`$ is the shape function matrix and $`(\hat{\cdot})`$ denotes a column matrix of nodal values.

The displacement fields in an element are approximated as

<span label="InterpolateDisp">
``` math
\begin{aligned}
{\underline{u}}(\xi) &=  h^k(\xi) {\underline{\hat{u}}}^k \\
{\underline{u}}^\prime(\xi) &=  h^{k\prime}(\xi) {\underline{\hat{u}}}^k
\end{aligned}
```
</span>

where $`h^k(\xi)`$, the component of shape function matrix $`{\underline{\underline{N}}}`$, is the $`p^{th}`$-order polynomial Lagrangian-interpolant shape function of node $`k`$, $`k=\{1,2,...,p+1\}`$, $`{\underline{\hat{u}}}^k`$ is the $`k^{th}`$ nodal value, and $`\xi \in \left[-1,1\right]`$ is the element natural coordinate. However, as discussed in Bauchau-etal:2008, the 3D rotation field cannot simply be interpolated as the displacement field in the form of

<span label="InterpolateRot">
``` math
\begin{aligned}
{\underline{c}}(\xi) &= h^k(\xi) {\underline{\hat{c}}}^k \\
{\underline{c}}^\prime(\xi) &= h^{k \prime}(\xi) {\underline{\hat{c}}}^k
\end{aligned}
```
</span>

where $`{\underline{c}}`$ is the rotation field in an element and $`{\underline{\hat{c}}}^k`$ is the nodal value at the $`k^{th}`$ node, for three reasons:

1)  rotations do not form a linear space so that they must be “composed” rather than added;
2)  a rescaling operation is needed to eliminate the singularity existing in the vectorial rotation parameters;
3)  the rotation field lacks objectivity, which, as defined by Crisfield1999, refers to the invariance of strain measures computed through interpolation to the addition of a rigid-bodymotion.

Therefore, we adopt the more robust interpolation approach proposed by Crisfield1999 to deal with the finite rotations. Our approach is described as follows

Step 1:  
Compute the nodal relative rotations, $`{\underline{\hat{r}}}^k`$, by removing the reference rotation, $`{\underline{\hat{c}}}^1`$, from the finite rotation at each node, $`{\underline{\hat{r}}}^k = ({\underline{\hat{c}}}^{1-}) \oplus
{\underline{\hat{c}}}^k`$. It is noted that the minus sign on $`{\underline{\hat{c}}}^1`$ denotes that the relative rotation is calculated by removing the reference rotation from each node. The composition in that equation is an equivalent of $`{\underline{\underline{R}}}({\underline{\hat{r}}}^k) = {\underline{\underline{R}}}^T({\underline{\hat{c}}}^1)~{\underline{\underline{R}}}({\underline{{\underline{c}}}}^k).`$

Step 2:  
Interpolate the relative-rotation field: $`{\underline{r}}(\xi) = h^k(\xi) {\underline{\hat{r}}}^k`$ and $`{\underline{r}}^\prime(\xi) = h^{k \prime}(\xi) {\underline{\hat{r}}}^k`$. Find the curvature field $`{\underline{\kappa}}(\xi) = {\underline{\underline{R}}}({\underline{\hat{c}}}^1) {\underline{\underline{H}}}({\underline{r}}) {\underline{r}}^\prime`$, where $`{\underline{\underline{H}}}`$ is the tangent tensor that relates the curvature vector $`{\underline{k}}`$ and rotation vector $`{\underline{c}}`$ as

<span label="Tensor">
``` math
{\underline{k}} = {\underline{\underline{H}}}~ {\underline{c}}^\prime
```
</span>

Step 3:  
Restore the rigid-body rotation removed in Step 1: $`{\underline{c}}(\xi) = {\underline{\hat{c}}}^1 \oplus {\underline{r}}(\xi)`$.

Note that the relative-rotation field can be computed with respect to any of the nodes of the element; we choose node 1 as the reference node for convenience. In the LSFE approach, shape functions (i.e., those composing $`{\underline{\underline{N}}}`$) are $`p^{th}`$-order Lagrangian interpolants, where nodes are located at the $`p+1`$ Gauss-Lobatto-Legendre (GLL) points in the $`[-1,1]`$ element natural-coordinate domain. `N4_lsfe` shows representative LSFE basis functions for fourth- and eighth-order elements. Note that nodes are clustered near element endpoints. More details on the LSFE and its applications can be found in References Patera:1984,Ronquist:1987,Sprague:2003,Sprague:2004.

<div id="N4_lsfe">

<figure class="align-center">
<img src="figs/n4.png" style="width:47.0%" alt="figs/n4.png" />
<figcaption>Representative <span class="math inline"><em>p</em> + 1</span> Lagrangian-interpolant shape functions in the element natural coordinates for a fourth-order LSFEs, where nodes are located at the Gauss-Lobatto-Legendre points.</figcaption>
</figure>

</div>

<div id="N8_lsfe">

<figure class="align-center">
<img src="figs/n8.png" style="width:47.0%" alt="figs/n8.png" />
<figcaption>Representative <span class="math inline"><em>p</em> + 1</span> Lagrangian-interpolant shape functions in the element natural coordinates for a eighth-order LSFEs, where nodes are located at the Gauss-Lobatto-Legendre points.</figcaption>
</figure>

</div>

## Wiener-Milenković Rotation Parameter

In BeamDyn, the 3D rotations are represented as Wiener-Milenković parameters defined in the following equation:

<span label="WMParameter">
``` math
{\underline{c}} = 4 \tan\left(\frac{\phi}{4} \right) \bar{n}
```
</span>

where $`\phi`$ is the rotation angle and $`\bar{n}`$ is the unit vector of the rotation axis. It can be observed that the valid range for this parameter is $`|\phi| < 2 \pi`$. The singularities existing at integer multiples of $`\pm 2 \pi`$ can be removed by a rescaling operation at $`\pi`$ as:

<span label="RescaledWM">
``` math
\begin{aligned}
{\underline{r}} = \begin{cases}
4(q_0{\underline{p}} + p_0 {\underline{q}} + \tilde{p} {\underline{q}} ) / (\Delta_1 + \Delta_2), & \text{if } \Delta_2 \geq 0 \\
-4(q_0{\underline{p}} + p_0 {\underline{q}} + \tilde{p} {\underline{q}} ) / (\Delta_1 - \Delta_2), & \text{if } \Delta_2 < 0
\end{cases}
\end{aligned}
```
</span>

where $`{\underline{p}}`$, $`{\underline{q}}`$, and $`{\underline{r}}`$ are the vectorial parameterization of three finite rotations such that $`{\underline{\underline{R}}}({\underline{r}}) = {\underline{\underline{R}}}({\underline{p}}) {\underline{\underline{R}}}({\underline{q}})`$, $`p_0 = 2 - {\underline{p}}^T {\underline{p}}/8`$, $`q_0 = 2 - {\underline{q}}^T {\underline{q}}/8`$, $`\Delta_1 = (4-p_0)(4-q_0)`$, and $`\Delta_2 = p_0 q_0 - {\underline{p}}^T {\underline{q}}`$. It is noted that the rescaling operation could cause a discontinuity of the interpolated rotation field; therefore a more robust interpolation algorithm has been introduced in Section `num-imp` where the rescaling-independent relative-rotation field is interpolated.

The rotation tensor expressed in terms of Wiener-Milenković parameters is

<span label="eqn:RotTensorWM">
``` math
\begin{aligned}
{\underline{\underline{R}}} ({\underline{c}}) = \frac{1}{(4-c_0)^2}
\begin{bmatrix}
c_0^2 + c_1^2 - c_2^2 - c_3^2 & 2(c_1 c_2 - c_0 c_3) & 2(c_1 c_3 + c_0 c_2) \\
2(c_1 c_2 + c_0 c_3) & c_0^2 - c_1^2 + c_2^2 - c_3^2 & 2(c_2 c_3 - c_0 c_1) \\
2(c_1 c_3 - c_0 c_2)  & 2(c_2 c_3 + c_0 c_1) & c_0^2 - c_1^2 - c_2^2 + c_3^2 \\
\end{bmatrix}
\end{aligned}
```
</span>

where $`{\underline{c}} = \left[ c_1~~c_2~~c_3\right]^T`$ is the Wiener-Milenković parameter and $`c_0 = 2 - \frac{1}{8}{\underline{c}}^T {\underline{c}}`$. The relation between rotation tensor and direction cosine matrix (DCM) is

<span label="RT2DCM">
``` math
{\underline{\underline{R}}} = ({\underline{\underline{DCM}}})^T
```
</span>

Interested users are referred to Bauchau-etal:2008 and Wang:GEBT2013 for more details on the rotation parameter and its implementation with GEBT.

## Linearization Process

The nonlinear governing equations introduced in the previous section are solved by Newton-Raphson method, where a linearization process is needed. The linearization of each term in the governing equations are presented in this section.

According to Bauchau:2010, the linearized governing equations in Eq.  `GovernGEBT-1-2` are in the form of

<span label="LinearizedEqn">
``` math
\hat{\underline{\underline{M}}} \Delta \hat{\underline{a}} +\hat{\underline{\underline{G}}} \Delta \hat{\underline{v}}+ \hat{\underline{\underline{K}}} \Delta \hat{\underline{q}} = \hat{\underline{F}}^{ext} - \hat{\underline{F}}
```
</span>

where the $`\hat{{\underline{\underline{M}}}}`$, $`\hat{{\underline{\underline{G}}}}`$, and $`\hat{{\underline{\underline{K}}}}`$ are the elemental mass, gyroscopic, and stiffness matrices, respectively; $`\hat{{\underline{F}}}`$ and $`\hat{{\underline{F}}}^{ext}`$ are the elemental forces and externally applied loads, respectively. They are defined for an element of length $`l`$ along $`x_1`$ as follows

<span label="hatMGKFFext">
``` math
\begin{aligned}
\hat{{\underline{\underline{M}}}}&= \int_0^l \underline{\underline{N}}^T \mathcal{\underline{\underline{M}}} ~\underline{\underline{N}} dx_1 \\
\hat{{\underline{\underline{G}}}} &= \int_0^l {\underline{\underline{N}}}^T {\underline{\underline{\mathcal{G}}}}^I~{\underline{\underline{N}}} dx_1\\
\hat{{\underline{\underline{K}}}}&=\int_0^l \left[ {\underline{\underline{N}}}^T ({\underline{\underline{\mathcal{K}}}}^I + \mathcal{{\underline{\underline{Q}}}})~ {\underline{\underline{N}}} + {\underline{\underline{N}}}^T \mathcal{{\underline{\underline{P}}}}~ {\underline{\underline{N}}}^\prime + {\underline{\underline{N}}}^{\prime T} \mathcal{{\underline{\underline{C}}}}~ {\underline{\underline{N}}}^\prime + {\underline{\underline{N}}}^{\prime T} \mathcal{{\underline{\underline{O}}}}~ {\underline{\underline{N}}} \right] d x_1 \\
\hat{{\underline{F}}} &= \int_0^l ({\underline{\underline{N}}}^T {\underline{\mathcal{F}}}^I + {\underline{\underline{N}}}^T \mathcal{{\underline{F}}}^D + {\underline{\underline{N}}}^{\prime T} \mathcal{{\underline{F}}}^C)dx_1 \\
\hat{{\underline{F}}}^{ext}& = \int_0^l {\underline{\underline{N}}}^T \mathcal{{\underline{F}}}^{ext} dx_1
\end{aligned}
```
</span>

where $`\mathcal{{\underline{F}}}^{ext}`$ is the applied load vector. The new matrix notations in Eqs. `hatMGKFFext` to are briefly introduced here. $`\mathcal{{\underline{F}}}^C`$ and $`\mathcal{{\underline{F}}}^D`$ are elastic forces obtained from Eq. `GovernGEBT-1-2` as

<span label="FCD">
``` math
\begin{aligned}
\mathcal{{\underline{F}}}^C &= \begin{Bmatrix}
        {\underline{F}} \\
{\underline{M}}
\end{Bmatrix} = {\underline{\underline{\mathcal{C}}}} \begin{Bmatrix}
{\underline{\epsilon}} \\
{\underline{\kappa}}
\end{Bmatrix} \\
\mathcal{{\underline{F}}}^D & = \begin{bmatrix}
\underline{\underline{0}} & \underline{\underline{0}}\\
(\tilde{x}_0^\prime+\tilde{u}^\prime)^T & \underline{\underline{0}}
\end{bmatrix}
\mathcal{{\underline{F}}}^C \equiv {\underline{\underline{\Upsilon}}}~ \mathcal{{\underline{F}}}^C
\end{aligned}
```
</span>

where $`\underline{\underline{0}}`$ denotes a $`3 \times 3`$ null matrix. The $`{\underline{\underline{\mathcal{G}}}}^I`$, $`{\underline{\underline{\mathcal{K}}}}^I`$, $`\mathcal{{\underline{\underline{O}}}}`$, $`\mathcal{{\underline{\underline{P}}}}`$, $`\mathcal{{\underline{\underline{Q}}}}`$, and $`{\underline{\mathcal{F}}}^I`$ in Eqs. `hatMGKFFext`  are defined as

<span label="mathcalGKOPFI">
``` math
\begin{aligned}
{\underline{\underline{\mathcal{G}}}}^I &= \begin{bmatrix}
{\underline{\underline{0}}} & (\widetilde{\tilde{\omega} m {\underline{\eta}}})^T+\tilde{\omega} m \tilde{\eta}^T  \\
{\underline{\underline{0}}} & \tilde{\omega} {\underline{\underline{\varrho}}}-\widetilde{{\underline{\underline{\varrho}}} {\underline{\omega}}}
\end{bmatrix} \\
{\underline{\underline{\mathcal{K}}}}^I &= \begin{bmatrix}
{\underline{\underline{0}}} & \dot{\tilde{\omega}}m\tilde{\eta}^T + \tilde{\omega} \tilde{\omega}m\tilde{\eta}^T  \\
{\underline{\underline{0}}} & \ddot{\tilde{u}}m\tilde{\eta} + {\underline{\underline{\varrho}}} \dot{\tilde{\omega}}-\widetilde{{\underline{\underline{\varrho}}} {\underline{\dot{\omega}}}}+\tilde{\omega} {\underline{\underline{\varrho}}} \tilde{\omega} - \tilde{\omega}  \widetilde{{\underline{\underline{\varrho}}} {\underline{\omega}}}
\end{bmatrix}\\
\mathcal{{\underline{\underline{O}}}} &= \begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{C}}}_{11} \tilde{E_1} - \tilde{F} \\
{\underline{\underline{0}}}& {\underline{\underline{C}}}_{21} \tilde{E_1} - \tilde{M}
\end{bmatrix} \\
\mathcal{{\underline{\underline{P}}}} &= \begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{0}}} \\
\tilde{F} +  ({\underline{\underline{C}}}_{11} \tilde{E_1})^T & ({\underline{\underline{C}}}_{21} \tilde{E_1})^T
\end{bmatrix}  \\
\mathcal{{\underline{\underline{Q}}}} &= {\underline{\underline{\Upsilon}}}~ \mathcal{{\underline{\underline{O}}}} \\
{\underline{\mathcal{F}}}^I &= \begin{Bmatrix}
m \ddot{{\underline{u}}} + (\dot{\tilde{\omega}} + \tilde{\omega} \tilde{\omega})m {\underline{\eta}} \\
m \tilde{\eta} \ddot{{\underline{u}}} +{\underline{\underline{\varrho}}}\dot{{\underline{\omega}}}+\tilde{\omega}{\underline{\underline{\varrho}}}{\underline{\omega}}
\end{Bmatrix}
\end{aligned}
```
</span>

where $`m`$ is the mass density per unit length, $`{\underline{\eta}}`$ is the location of the sectional center of mass, $`{\underline{\underline{\varrho}}}`$ is the moment of inertia tensor, and the following notations were introduced to simplify the above expressions

<span label="E1-PartC">
``` math
\begin{aligned}
{\underline{E}}_1 &= {\underline{x}}_0^\prime + {\underline{u}}^\prime \\
{\underline{\underline{\mathcal{C}}}} &= \begin{bmatrix}
{\underline{\underline{C}}}_{11} & {\underline{\underline{C}}}_{12} \\
{\underline{\underline{C}}}_{21} & {\underline{\underline{C}}}_{22}
\end{bmatrix}
\end{aligned}
```
</span>

## Damping Forces and Linearization

A viscous damping model has been implemented into BeamDyn to account for the structural damping effect. The damping force is defined as

<span label="Damping">
``` math
\begin{aligned}
{\underline{f}}_d = {\underline{\underline{\mu}}}~ {\underline{\underline{\mathcal{C}}}} \begin{Bmatrix}
\dot{\epsilon} \\
\dot{\kappa}
\end{Bmatrix}
\end{aligned}
```
</span>

where $`{\underline{\underline{\mu}}}`$ is a user-defined damping-coefficient diagonal matrix. The damping force can be recast in two separate parts, like $`{\underline{\mathcal{F}}}^C`$ and $`{\underline{\mathcal{F}}}^D`$ in the elastic force, as

<span label="DampingForce-1-2">
``` math
\begin{aligned}
{\underline{\mathcal{F}}}^C_d &= \begin{Bmatrix}
{\underline{F}}_d \\
{\underline{M}}_d
\end{Bmatrix} \\
{\underline{\mathcal{F}}}^D_d &= \begin{Bmatrix}
 {\underline{0}} \\
 (\tilde{x}^\prime_0 + \tilde{u}^\prime)^T \underline{F}_d
 \end{Bmatrix}
\end{aligned}
```
</span>

The linearization of the structural damping forces are as follows:

<span label="DampingForceLinear-1-2">
``` math
\begin{aligned}
\Delta {\underline{\mathcal{F}}}^C_d &= {\underline{\underline{\mathcal{S}}}}_d \begin{Bmatrix}
\Delta {\underline{u}}^\prime \\
\Delta {\underline{c}}^\prime
\end{Bmatrix} + {\underline{\underline{\mathcal{O}}}}_d \begin{Bmatrix}
\Delta {\underline{u}} \\
\Delta {\underline{c}}
\end{Bmatrix} + {\underline{\underline{\mathcal{G}}}}_d \begin{Bmatrix}
\Delta {\underline{\dot{u}}} \\
\Delta {\underline{\omega}}
\end{Bmatrix}     + {\underline{\underline{\mu}}} ~{\underline{\underline{C}}} \begin{Bmatrix}
\Delta {\underline{\dot{u}}}^\prime \\
\Delta {\underline{\omega}}^\prime
\end{Bmatrix} \\
\Delta {\underline{\mathcal{F}}}^D_d &= {\underline{\underline{\mathcal{P}}}}_d \begin{Bmatrix}
\Delta {\underline{u}}^\prime \\
\Delta {\underline{c}}^\prime
\end{Bmatrix} + {\underline{\underline{\mathcal{Q}}}}_d \begin{Bmatrix}
\Delta {\underline{u}} \\
\Delta {\underline{c}}
\end{Bmatrix} + {\underline{\underline{\mathcal{X}}}}_d \begin{Bmatrix}
\Delta {\underline{\dot{u}}} \\
\Delta {\underline{\omega}}
\end{Bmatrix}     + {\underline{\underline{\mathcal{Y}}}}_d \begin{Bmatrix}
\Delta {\underline{\dot{u}}}^\prime \\
\Delta {\underline{\omega}}^\prime
\end{Bmatrix}
\end{aligned}
```
</span>

where the newly introduced matrices are defined as

<span label="DampingSd-Od-Gd-Pd-Qd-Xd-Yd">
``` math
\begin{aligned}
{\underline{\underline{\mathcal{S}}}}_d &=
{\underline{\underline{\mu}}} {\underline{\underline{\mathcal{C}}}} \begin{bmatrix}
\tilde{\omega}^T & {\underline{\underline{0}}} \\
{\underline{\underline{0}}} & \tilde{\omega}^T
\end{bmatrix} \\
{\underline{\underline{\mathcal{O}}}}_d &=
\begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{\mu}}} {\underline{\underline{C}}}_{11} (\dot{\tilde{u}}^\prime - \tilde{\omega} \tilde{E}_1) - \tilde{F}_d \\
{\underline{\underline{0}}} &{\underline{\underline{\mu}}} {\underline{\underline{C}}}_{21} (\dot{\tilde{u}}^\prime - \tilde{\omega} \tilde{E}_1) - \tilde{M}_d
\end{bmatrix} \\
{\underline{\underline{\mathcal{G}}}}_d &=
\begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{C}}}_{11}^T {\underline{\underline{\mu}}}^T \tilde{E}_1 \\
{\underline{\underline{0}}} & {\underline{\underline{C}}}_{12}^T {\underline{\underline{\mu}}}^T \tilde{E}_1
\end{bmatrix} \\
{\underline{\underline{\mathcal{P}}}}_d &=
\begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{0}}}  \\
\tilde{F}_d + \tilde{E}_1^T {\underline{\underline{\mu}}} {\underline{\underline{C}}}_{11} \tilde{\omega}^T &  \tilde{E}_1^T {\underline{\underline{\mu}}} {\underline{\underline{C}}}_{12} \tilde{\omega}^T
\end{bmatrix} \\
{\underline{\underline{\mathcal{Q}}}}_d &=
\begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{0}}}  \\
{\underline{\underline{0}}} &  \tilde{E}_1^T {\underline{\underline{O}}}_{12}
\end{bmatrix} \\
{\underline{\underline{\mathcal{X}}}}_d &=
\begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{0}}}  \\
 {\underline{\underline{0}}} &  \tilde{E}_1^T {\underline{\underline{G}}}_{12}
\end{bmatrix} \\
{\underline{\underline{\mathcal{Y}}}}_d &=
\begin{bmatrix}
{\underline{\underline{0}}} & {\underline{\underline{0}}}  \\
  \tilde{E}_1^T {\underline{\underline{\mu}}} {\underline{\underline{C}}}_{11} &   \tilde{E}_1^T {\underline{\underline{\mu}}} {\underline{\underline{C}}}_{12}
\end{bmatrix} \\
\end{aligned}
```
</span>

where $`{\underline{\underline{O}}}_{12}`$ and $`{\underline{\underline{G}}}_{12}`$ are the $`3 \times 3`$ sub matrices of $`\mathcal{{\underline{\underline{O}}}}`$ and $`\mathcal{{\underline{\underline{G}}}}`$ as $`{\underline{\underline{C}}}_{12}`$ in Eq. `E1-PartC`. Modal Damping -------------

In addition to the stiffness-proportional viscous damping described above, BeamDyn also supports modal damping. This is currently only supported when run in tight coupling with OpenFAST. When modal damping is selected (`damp_flag = 2`), BeamDyn computes the natural frequencies and mode shapes of the blade and applies damping in the modal coordinates.

The modal damping approach constructs a damping matrix $`{\underline{\underline{C}}}_{modal}`$ based on user-specified modal damping ratios $`\zeta_i`$ for modes $`i = 1, 2, \ldots, n_{modes}`$. Past the user-specified $`n_{modes}`$, BeamDyn assigns $`\zeta_i`$ to grow proportional to the modal natural frequency and match the last prescribed $`\zeta_i`$ value. The modal damping matrix is defined in terms of the modal properties:

<span label="ModalDamping">
``` math
{\underline{\underline{C}}}_{modal} = {\underline{\underline{\Phi}}}^{-T} {\underline{\underline{Z}}} {\underline{\underline{\Phi}}}^{-1} 
= {\underline{\underline{M}}} {\underline{\underline{\Phi}}} {\underline{\underline{Z}}} {\underline{\underline{\Phi}}}^T {\underline{\underline{M}}}
```
</span>

where $`\underline{\underline{Z}}`$ is a diagonal matrix with diagonal entry $`i`$ equal to $`2 \omega_i \zeta_i`$ for natural frequency in rad/s of $`\omega_i`$. Additionally, $`\underline{\underline{\Phi}}`$ is the matrix of mass-normalized mode shapes (each as a column). $`\underline{\underline{M}}`$ is the mass matrix after the quasi-static initialization.

At each time step, a vector of nodal velocities is calculated subtracting off the rigid body motion of the root. This vector of velocities is rotated at each node to be aligned with the beam as initialized. Damping forces at nodes are then simply the product of the damping matrix and the vector of velocities. These forces are then rotated back to the global coordinates with the inverse of the velocity rotation. The extra rotations appear to give better modal damping results than fixing the damping matrix in the root frame.

Modal damping gives the user mode-specific control of damping levels to better match experiments or theoretical damping predictions. Furthermore, modal damping need not grow proportional to frequency (as prescribed by stiffness proportional damping). Rather, more constant damping factors across frequency can be used as have been observed in some experiments and model predictions.

## Convergence Criterion and Generalized-$`\alpha`$ Time Integrator

The system of nonlinear equations in Eqs. `GovernGEBT-1-2` are solved using the Newton-Raphson method with the linearized form in Eq. `LinearizedEqn`. In the present implementation, an energy-like stopping criterion has been chosen, which is calculated as

<span label="StoppingCriterion">
``` math
| \Delta \mathbf{U}^{(i)T} \left( {^{t+\Delta t}} \mathbf{R} -  {^{t+\Delta t}} \mathbf{F}^{(i-1)}  \right) | \leq | \epsilon_E \left( \Delta \mathbf{U}^{(1)T} \left( {^{t+\Delta t}} \mathbf{R} - {^t}\mathbf{F} \right) \right) |
```
</span>

where $`|\cdot|`$ denotes the absolute value, $`\Delta \mathbf{U}`$ is the incremental displacement vector, $`\mathbf{R}`$ is the vector of externally applied nodal point loads, $`\mathbf{F}`$ is the vector of nodal point forces corresponding to the internal element stresses, and $`\epsilon_E`$ is the user-defined energy tolerance. The superscript on the left side of a variable denotes the time-step number (in a dynamic analysis), while the one on the right side denotes the Newton-Raphson iteration number. As pointed out by Bathe-Cimento:1980, this criterion provides a measure of when both the displacements and the forces are near their equilibrium values.

Time integration is performed using the generalized-$`\alpha`$ scheme in BeamDyn, which is an unconditionally stable (for linear systems), second-order accurate algorithm. The scheme allows for users to choose integration parameters that introduce high-frequency numerical dissipation. The amount of numerical dissipation is controlled by the user-specified spectral radius at infinity, $`\rho_{\infty}`$. More details regarding the generalized-$`\alpha`$ method can be found in Chung-Hulbert:1993,Bauchau:2010.

## Calculation of Reaction Loads

Since the root motion of the wind turbine blade, including displacements and rotations, translational and angular velocities, and translational and angular accelerates, are prescribed as inputs to BeamDyn either by the driver (in stand-alone mode) or by FAST glue code (in FAST-coupled mode), the reaction loads at the root are needed to satisfy equality of the governing equations. The reaction loads at the root are also the loads passing from blade to hub in a full turbine analysis.

The governing equations in Eq. `GovernGEBT-1-2` can be recast in a compact form

<span label="CompactGovern">
``` math
{\underline{\mathcal{F}}}^I - {\underline{\mathcal{F}}}^{C\prime} + {\underline{\mathcal{F}}}^D = {\underline{\mathcal{F}}}^{ext}
```
</span>

with all the vectors defined in Section \[sec:LinearProcess\]. At the blade root, the governing equation is revised as

<span label="CompactGovernRoot">
``` math
{\underline{\mathcal{F}}}^I - {\underline{\mathcal{F}}}^{C\prime} + {\underline{\mathcal{F}}}^D = {\underline{\mathcal{F}}}^{ext}+{\underline{\mathcal{F}}}^R
```
</span>

where $`{\underline{\mathcal{F}}}^R = \left[ {\underline{F}}^R~~~{\underline{M}}^R\right]^T`$ is the reaction force vector and it can be solved from Eq. `CompactGovernRoot` given that the motion fields are known at this point.

## Calculation of Blade Loads

BeamDyn can also calculate the blade loads at each finite element node along the blade axis. The governing equation in Eq. `CompactGovern` are recast as

<span label="GovernBF">
``` math
{\underline{\mathcal{F}}}^A + {\underline{\mathcal{F}}}^V - {\underline{\mathcal{F}}}^{C\prime} + {\underline{\mathcal{F}}}^D = {\underline{\mathcal{F}}}^{ext}
```
</span>

where the inertial force vector $`{\underline{\mathcal{F}}}^I`$ is split into $`{\underline{\mathcal{F}}}^A`$ and $`{\underline{\mathcal{F}}}^V`$:

<span label="mathcalFA-FV">
``` math
\begin{aligned}
{\underline{\mathcal{F}}}^A &= \begin{Bmatrix}
m \ddot{{\underline{u}}} + \dot{\tilde{\omega}}m {\underline{\eta}}\\
m \tilde{\eta} \ddot{{\underline{u}}} + {\underline{\underline{\rho}}} \dot{{\underline{\omega}}}
\end{Bmatrix} \\
{\underline{\mathcal{F}}}^V &= \begin{Bmatrix}
\tilde{\omega} \tilde{\omega} m {\underline{\eta}}\\
 \tilde{\omega} {\underline{\underline{\rho}}} {\underline{\omega}}
\end{Bmatrix} \\
\end{aligned}
```
</span>

The blade loads are thus defined as

<span label="BladeForce">
``` math
{\underline{\mathcal{F}}}^{BF} \equiv {\underline{\mathcal{F}}}^V - {\underline{\mathcal{F}}}^{C\prime} + {\underline{\mathcal{F}}}^D
```
</span>

We note that if structural damping is considered in the analysis, the $`{\underline{\mathcal{F}}}^{C}_d`$ and $`{\underline{\mathcal{F}}}^D_d`$ are incorporated into the internal elastic forces, $`{\underline{\mathcal{F}}}^C`$ and $`{\underline{\mathcal{F}}}^D`$, for calculation.
