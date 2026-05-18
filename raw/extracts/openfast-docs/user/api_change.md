# API changes between versions

This page lists the main changes in the OpenFAST API (input files) between different versions.

The changes are tabulated according to the module input file, line number, and flag name. The line number corresponds to the resulting line number after all changes are implemented. Thus, be sure to implement each in order so that subsequent line numbers are correct.

## OpenFAST v4.2.x to OpenFAST v5.0.0

Added mass and fluid inertia loads were added to the rotor blades and tower in AeroDyn. This results in new columns in the AeroDyn blade input file and new columns in the "Tower Influence and Aerodynamics" section of the AeroDyn primary input file. Given the addition of these loads, the Buoyancy flag was also removed, and the buoyancy, added mass, and inertia loads can all be turned off by setting the appropriate coefficients to zero rather than via a separate flag for each.

Superposition of wave and current velocities between InflowWind and SeaState was enabled, which requires a "SeaState Data" section in the AeroDyn driver input file.

Changes to the OpenFAST input file support multiple rotors in one turbine. Line 16, NRotors, is required to specify the number of rotors in the turbine. Lines 50-56 specify the ElastoDyn, BeamDyn, and ServoDyn input files for the second rotor; all other modules use the input files specified in the first section. The <span class="title-ref">MirrorRotor</span> line sets a flag to reverse the direction the rotor is spinning. The first rotor always spins in the typical direction. These lines are specified only if NRotors is greater than 1 and are repeated for subsequent rotors.

| Added in OpenFAST <span class="title-ref">5.0.0</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | --------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| OpenFAST | 8 | ModCoupling | 3 ModCoupling - Module coupling method (switch) {1=loose; 2=tight with fixed Jacobian updates (DT_UJac); 3=tight with automatic Jacobian updates} |
| OpenFAST | 11 | RhoInf | 1.0 RhoInf - Numerical damping parameter for tight coupling generalized-alpha integrator (-) \[0.0 to 1.0\] |
| OpenFAST | 12 | ConvTol | 1e-4 ConvTol - Convergence iteration error tolerance for tight coupling generalized alpha integrator (-) |
| OpenFAST | 13 | MaxConvIter | 6 MaxConvIter - Maximum number of convergence iterations for tight coupling generalized alpha integrator (-) |
| OpenFAST | 17 | NRotors | 2 NRotors - Number of rotors in turbine (-) |
| OpenFAST | 20 | CompSoil | 0 CompSoil - Compute soil-structural dynamics (switch) {0=None; 1=SoilDyn} |
| OpenFAST | 29 | MirrorRotor | F MirrorRotor - Flag to reverse rotor rotation direction \[1 to NRotors\] {F=Normal, T=Mirror} |
| OpenFAST | 53 | SoilFile | "SoilDyn.dat" SoilFile - Name of the file containing the SoilDyn input parameters (quoted string) |
| OpenFAST | 54 |  | ---------------------- INPUT FILES Rotor 2 ------------------------------------- |
| OpenFAST | 55 | EDFile | "ElastoDyn.dat" EDFile - Name of file containing ElastoDyn input parameters (quoted string) |
| OpenFAST | 56 | BDBldFile(1) | "BeamDyn.dat" BDBldFile(1) - Name of file containing BeamDyn input parameters for blade 1 (quoted string) |
| OpenFAST | 57 | BDBldFile(2) | "BeamDyn.dat" BDBldFile(2) - Name of file containing BeamDyn input parameters for blade 2 (quoted string) |
| OpenFAST | 58 | BDBldFile(3) | "BeamDyn.dat" BDBldFile(3) - Name of file containing BeamDyn input parameters for blade 3 (quoted string) |
| OpenFAST | 59 | ServoFile | "ServoDyn_R2.dat" ServoFile - Name of file containing control and electrical-drive input parameters (quoted string) |
| AeroDyn blade file |  | t_c | 0.8651 \[additional column in *Blade Properties* table\] |
| AeroDyn blade file |  | BlCpn | 1.0 \[additional column in *Blade Properties* table\] |
| AeroDyn blade file |  | BlCpt | 1.0 \[additional column in *Blade Properties* table\] |
| AeroDyn blade file |  | BlCan | 6.8459E+00 \[additional column in *Blade Properties* table\] |
| AeroDyn blade file |  | BlCat | 5.4605E-01 \[additional column in *Blade Properties* table\] |
| AeroDyn blade file |  | BlCam | 5.5180E-02 \[additional column in *Blade Properties* table\] |
| AeroDyn driver | 23 |  | ----- SeaState Data \[used only when MHK = 1 or 2\] --------------------------------------- |
| AeroDyn driver | 24 | CompSeaSt | 1 CompSeaSt - Compute wave velocities (switch) {0=No Waves; 1=SeaState} |
| AeroDyn driver | 25 | SeaStFile | "MHK_RM1_Fixed_SeaState.dat" SeaStFile - Name of the SeaState input file \[used only when CompSeaSt=1\] |
| AeroDyn | \* | TwrCp | 1.0 \[additional column in *Tower Influence and Aerodynamics* table\] |
| AeroDyn | \* | TwrCa | 1.0 \[additional column in *Tower Influence and Aerodynamics* table\] |
| SeaState | 18 | WvCrntMod | 0 WvCrntMod - Combined wave-current modeling option {0: simple superposition, 1: include Doppler effect, 2: include both Doppler effect and wave amplitude/spectrum scaling} (switch) |
| ElastoDyn | 11 | PitchDOF | False PitchDOF - Blade pitch DOF (flag) |
| ElastoDyn | 70 | PtfmRefxt | 0 PtfmRefxt - Downwind distance from the ground level \[onshore\], MSL \[offshore wind or floating MHK\], or seabed \[fixed MHK\] to the platform reference point (meters) |
| ElastoDyn | 71 | PtfmRefyt | 0 PtfmRefyt - Lateral distance from the ground level \[onshore\], MSL \[offshore wind or floating MHK\], or seabed \[fixed MHK\] to the platform reference point (meters) |
| ElastoDyn | 77 | PBrIner(1) | 200 PBrIner(1) - Pitch bearing/actuator inertia, blade 1 (kg m^2) |
| ElastoDyn | 78 | PBrIner(2) | 200 PBrIner(2) - Pitch bearing/actuator inertia, blade 2 (kg m^2) |
| ElastoDyn | 79 | PBrIner(3) | 200 PBrIner(3) - Pitch bearing/actuator inertia, blade 3 (kg m^2) \[unused for 2 blades\] |
| ElastoDyn | 80 | BlPIner(1) | 28578 BlPIner(1) - Pitch inertia of an undeflected blade, blade 1 (kg m^2) |
| ElastoDyn | 81 | BlPIner(2) | 28578 BlPIner(2) - Pitch inertia of an undeflected blade, blade 2 (kg m^2) |
| ElastoDyn | 82 | BlPIner(3) | 28578 BlPIner(3) - Pitch inertia of an undeflected blade, blade 3 (kg m^2) \[unused for 2 blades\] |
| BeamDyn blade file | 10 |  | ------ Modal Damping \[used only if damp_type=2\] -------------------------------- |
| BeamDyn blade file | 11 | n_modes | 3 n_modes - Number of modal damping coefficients (-) |
| BeamDyn blade file | 12 | zeta | 0.1, 0.2, 0.3 zeta - Damping coefficients for mode 1 through n_modes |
| ServoDyn | 9 | PitNeut(1) | 0 PitNeut(1) - Blade 1 neutral pitch position--pitch spring moment is zero at this position *\[unused when* **PCMode\>0** and **t\>=TPCOn** *\]* |
| ServoDyn | 10 | PitNeut(2) | 0 PitNeut(2) - Blade 2 neutral pitch position--pitch spring moment is zero at this position *\[unused when* **PCMode\>0** and **t\>=TPCOn** *\]* |
| ServoDyn | 11 | PitNeut(3) | 0 PitNeut(3) - Blade 3 neutral pitch position--pitch spring moment is zero at this position *\[unused when* **PCMode\>0** and **t\>=TPCOn** *\]* *\[unused for 2 blades\]* |
| ServoDyn | 12 | PitSpr(1) | 3.6E7 PitSpr(1) - Blade 1 pitch spring constant |
| ServoDyn | 13 | PitSpr(2) | 3.6E7 PitSpr(2) - Blade 2 pitch spring constant |
| ServoDyn | 14 | PitSpr(3) | 3.6E7 PitSpr(3) - Blade 3 pitch spring constant *\[unused for 2 blades\]* |
| ServoDyn | 15 | PitDamp(1) | 1.4E6 PitDamp(1) - Blade 1 pitch damping constant |
| ServoDyn | 16 | PitDamp(2) | 1.4E6 PitDamp(2) - Blade 2 pitch damping constant |
| ServoDyn | 17 | PitDamp(3) | 1.4E6 PitDamp(3) - Blade 3 pitch damping constant *\[unused for 2 blades\]* |
| HydroDyn | \* | HstMod | 1 HstMod - Method of computing hydrostatic loads. (0: Up to the still water level. 1: Up to the instantaneous free surface) *\[overwrite to 0 when WaveStMod = 0 in SeaState\]* |
| FAST.Farm | 35 |  | --- AMBIENT WIND: AMReX MODULE --- \[used only for Mod_AmbWind=4\] |
| FAST.Farm | 36 | WindDirPrefix | "inflow/ffboxes" WindDirPrefix - Directory prefix of AMReX wind sub-volumes {0=low-res, 1+=high-res} (quoted string) |
| FAST.Farm | 37 | DirStartIndex | 00110 DirStartIndex - AMReX sub-volume directory suffix to consider as time=0 (quoted string) |
| FAST.Farm | 38 | DT_Low-AMReX | 2.0 DT_Low-AMReX - Time step for low-resolution wind data interpolation; will be used as the global FAST.Farm time step (s) \[\>0.0\] |
| FAST.Farm | 39 | DT_High-AMReX | 1.0 DT_High-AMReX - Time step for high-resolution wind data interpolation (s) \[\>0.0\] |
| FAST.Farm | 50 | NumDFull | DEFAULT NumDFull - Distance of full wake propagation, expressed as a multiple of RotorDiamRef \[\>0.0\] or DEFAULT \[DEFAULT=15\] |
| FAST.Farm | 51 | NumDBuff | DEFAULT NumDBuff - Length of wake propagation buffer region, expressed as a multiple of RotorDiamRef \[\>=0.0\] or DEFAULT \[DEFAULT=5\] |
| SoilDyn | all |  | New module |

<table>
<thead>
<tr>
<th>Modified in OpenFAST <span class="title-ref">5.0.0</span></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>---------</th>
<th>---------------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>AeroDyn blade file</td>
<td>5</td>
<td></td>
<td>BlSpn BlCrvAC BlSwpAC BlCrvAng BlTwist BlChord BlAFID t_c BlCb BlCenBn BlCenBt BlCpn BlCpt BlCan BlCat BlCam</td>
</tr>
<tr>
<td>AeroDyn blade file</td>
<td>6</td>
<td></td>
<td><ol start="13" type="a">
<li><ol start="13" type="a">
<li><ol start="13" type="a">
<li>(deg) (deg) (m) (-) (-) (-) (m) (m) (-) (-) (-) (-) (-)</li>
</ol></li>
</ol></li>
</ol></td>
</tr>
<tr>
<td>AeroDyn</td>
<td>*</td>
<td></td>
<td>====== Hub Properties ============================================================================== [used only when MHK=1 or 2]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>*</td>
<td></td>
<td>====== Nacelle Properties ========================================================================== [used only when MHK=1 or 2 or when NacelleDrag=True]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>*</td>
<td></td>
<td>====== Tower Influence and Aerodynamics ============================================================ [used only when TwrPotent/=0, TwrShadow/=0, TwrAero=True, or MHK=1 or 2]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>*</td>
<td>NumTwrNds</td>
<td>5 NumTwrNds - Number of tower nodes used in the analysis (-) [used only when TwrPotent/=0, TwrShadow/=0, TwrAero=True, or MHK=1 or 2]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>*</td>
<td></td>
<td>TwrElev TwrDiam TwrCd TwrTI TwrCb TwrCp TwrCa !TwrTI used only with TwrShadow=2, TwrCb/TwrCp/TwrCa used only with MHK=1 or 2</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>*</td>
<td></td>
<td><ol start="13" type="a">
<li><ol start="13" type="a">
<li>(-) (-) (-) (-) (-)</li>
</ol></li>
</ol></td>
</tr>
</tbody>
</table>

| Removed in OpenFAST <span class="title-ref">5.0.0</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | --------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| AeroDyn | 11 | Buoyancy | False Buoyancy - Include buoyancy effects? (flag) |
| BeamDyn | \* |  | ---------------------- PITCH ACTUATOR PARAMETERS ------------------------------- |
| BeamDyn | \* | UsePitchAct | False UsePitchAct - Whether a pitch actuator should be used (flag) |
| BeamDyn | \* | PitchJ | 200 PitchJ - Pitch actuator inertia (kg-m^2) \[used only when UsePitchAct is true\] |
| BeamDyn | \* | PitchK | 20000000 PitchK - Pitch actuator stiffness (kg-m^2/s^2) \[used only when UsePitchAct is true\] |
| BeamDyn | \* | PitchC | 500000 PitchC - Pitch actuator damping (kg-m^2/s) \[used only when UsePitchAct is true\] |
| ElastoDyn Blade Input File | \* |  | The PitchAxis column has been removed from the DISTRIBUTED BLADE PROPERTIES table. The table should now only have 5 columns: BlFract, StrcTwst, BMassDen, FlpStff, and EdgStff |
| FAST.Farm | 50 | NumPlanes | 140 NumPlanes - Number of wake planes (-) \[\>=2\] |

### New Modules in v5.0.0

- SoilDyn -- a soil interaction module specifically designed to work with the RedWin DLL from NGI for soil interaction. Documentation for this module is limited.

## OpenFAST v4.2.0 to OpenFAST v4.2.1

No input file changes were made.

## OpenFAST v4.1.x to OpenFAST v4.2.0

<table>
<thead>
<tr>
<th>Modified in OpenFAST <span class="title-ref">v4.2.0</span></th>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>-------------------</th>
<th>------------------------------------------------------------------</th>
<th>-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Change</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>FAST.Farm.fstf</td>
<td>72</td>
<td>WAT_ScaleBox</td>
<td>default changed from <span class="title-ref">false</span> to <span class="title-ref">true</span></td>
<td>default WAT_ScaleBox - Flag to scale the input turbulence box to zero mean and unit standard deviation at every node [DEFAULT=True] (flag)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td>Members section</td>
<td>Added optional <span class="title-ref">FDMod</span> <span class="title-ref">VnCOffA</span> <span class="title-ref">VnCOffB</span> <span class="title-ref">FDLoFScA</span> <span class="title-ref">FDLoFScB</span></td>
<td><p>.. code-block:</p>
<pre><code>-------------------- MEMBERS -------------------------------------------------
   2            NMembers       - Number of members (-)
MemberID  MJointID1  MJointID2  MPropSetID1  MPropSetID2  MSecGeom    MSpinOrient   MDivSize   MCoefMod  MHstLMod   PropPot   FDMod    VnCOffA  VnCOffB  FDLoFScA FDLoFScB   [MCoefMod=1: use simple coeff table, 2: use depth-based coeff table, 3: use member-based coeff table]
  (-)        (-)        (-)         (-)          (-)      (switch)       (deg)        (m)      (switch)  (switch)   (flag)   (switch)   (Hz)     (Hz)       (-)      (-)</code></pre></td>
</tr>
</tbody>
</table>

| Added in OpenFAST <span class="title-ref">v4.2.0</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| ElastoDyn | 72 | HubIner_Teeter | 0 HubIner_Teeter - Hub inertia about teeter axis (2-blades) (kg m^2) |

## OpenFAST v4.1.1 to OpenFAST v4.1.2

No input file changes were made.

## OpenFAST v4.1.0 to OpenFAST v4.1.1

No input file changes were made.

## OpenFAST v4.0.5 to OpenFAST v4.1.0

Supercontroller module has been removed from FAST.Farm.

| Removed in OpenFAST <span class="title-ref">v4.1.0</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| FAST.Farm | 7 | UseSC | False UseSC - Use a super controller? (flag) |
| FAST.Farm | 11 | na | --- SUPER CONTROLLER --- \[used only for UseSC=True\] |
| FAST.Farm | 12 | SC_FileName | "SC_DLL.dll" SC_FileName Name/location of the dynamic library {.dll \[Windows\] or .so \[Linux\]} containing the Super Controller algorithms (quoted string) |

Line numbers are not provided in the table below because the line numbers can change depending on the number of entries in the input files. Please refer to the User Documentation on the input files for examples.

<table>
<thead>
<tr>
<th>Added/Modified in OpenFAST <span class="title-ref">v4.1.0</span></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>----------</th>
<th>-------------------</th>
<th>---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Change</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>na</td>
<td>---------------- CYLINDRICAL MEMBER CROSS-SECTION PROPERTIES -------------------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>NPropSetsCyl</td>
<td>1 NPropSetsCyl - Number of cylindrical member property sets (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>---------------- RECTANGULAR MEMBER CROSS-SECTION PROPERTIES -------------------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>NPropSetsRec</td>
<td>1 NPropSetsRec - Number of rectangular member property sets (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>PropSetID PropA PropB PropThck</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td><blockquote>
<p>(-) (m) (m) (m)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>na</td>
<td>-------- SIMPLE CYLINDRICAL-MEMBER HYDRODYNAMIC COEFFICIENTS (model 1) ---------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>-------- SIMPLE RECTANGULAR-MEMBER HYDRODYNAMIC COEFFICIENTS (model 1) ---------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>SimplCdA SimplCdAMG SimplCdB SimplCdBMG SimplCaA SimplCaAMG SimplCaB SimplCaBMG SimplCp SimplCpMG SimplAxCd SimplAxCdMG SimplAxCa SimplAxCaMG SimplAxCp SimplAxCpMG SimplCb SimplCbMG</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td><blockquote>
<p>(-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>na</td>
<td>------ DEPTH-BASED CYLINDRICAL-MEMBER HYDRODYNAMIC COEFFICIENTS (model 2) -------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>NCoefDpthCyl</td>
<td>0 NCoefDpthCyl - Number of depth-dependent cylindrical member coefficients (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>------ DEPTH-BASED RECTANGULAR-MEMBER HYDRODYNAMIC COEFFICIENTS (model 2) -------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>NCoefDpthRec</td>
<td>0 NCoefDpthRec - Number of depth-dependent rectangular member coefficients (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>Dpth DpthCdA DpthCdAMG DpthCdB DpthCdBMG DpthCaA DpthCaAMG DpthCaB DpthCaBMG DpthCp DpthCpMG DpthAxCd DpthAxCdMG DpthAxCa DpthAxCaMG DpthAxCp DpthAxCpMG DpthCb DpthCbMG</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td><blockquote>
<p><span class="title-ref">(m)</span> (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>na</td>
<td>------ MEMBER-BASED CYLINDRICAL-MEMBER HYDRODYNAMIC COEFFICIENTS (model 3) ------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>NCoefMembersCyl</td>
<td>0 NCoefMembersCyl - Number of member-based cylindrical member coefficients (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>------ MEMBER-BASED RECTANGULAR-MEMBER HYDRODYNAMIC COEFFICIENTS (model 3) ------</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>NCoefMembersRec</td>
<td>0 NCoefMembersRec - Number of member-based rectangular member coefficients (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>MemberID MemberCdA1 MemberCdA2 MemberCdAMG1 MemberCdAMG2 MemberCdB1 MemberCdB2 MemberCdBMG1 MemberCdBMG2 MemberCaA1 MemberCaA2 MemberCaAMG1 MemberCaAMG2 MemberCaB1 MemberCaB2 MemberCaBMG1 MemberCaBMG2 MemberCp1 MemberCp2 MemberCpMG1 MemberCpMG2 MemberAxCd1 MemberAxCd2 MemberAxCdMG1 MemberAxCdMG2 MemberAxCa1 MemberAxCa2 MemberAxCaMG1 MemberAxCaMG2 MemberAxCp1 MemberAxCp2 MemberAxCpMG1 MemberAxCpMG2 MemberCb1 MemberCb2 MemberCbMG1 MemberCbMG2</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Added</td>
<td>na</td>
<td>(-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-)</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>na</td>
<td>MemberID MJointID1 MJointID2 MPropSetID1 MPropSetID2 MSecGeom MSpinOrient MDivSize MCoefMod MHstLMod PropPot [MCoefMod=1: use simple coeff table, 2: use depth-based coeff table, 3: use member-based coeff table] [PropPot/=0 if member is modeled with potential-flow theory]</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>Modified</td>
<td>na</td>
<td>(-) (-) (-) (-) (-) (switch) (deg) (m) (switch) (switch) (flag)</td>
</tr>
<tr>
<td>MoorDyn</td>
<td>Optional</td>
<td>na</td>
<td>&lt;Several new optional sections have been added. See note below&gt;</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Modified</td>
<td>na</td>
<td>MemberID MJointID1 MJointID2 MPropSetID1 MPropSetID2 MType MSpin/COSMID ![MType={1c:beam circ., 1r:beam rect., 2:cable, 3:rigid, 4:beam arb., 5:spring}. COMSID={-1:none}]</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Modified</td>
<td>na</td>
<td>(-) (-) (-) (-) (-) (-) (deg/-)</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Added</td>
<td>na</td>
<td>----------------- RECTANGULAR BEAM CROSS-SECTION PROPERTIES ---------------------------</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Added</td>
<td>na</td>
<td>0 NPropSets - Number of structurally unique cross-sections (if 0 the following table is ignored)</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Added</td>
<td>na</td>
<td>PropSetID YoungE ShearG MatDens XsecSa XsecSb XsecT</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Added</td>
<td>na</td>
<td>(-) (N/m2) (N/m2) (kg/m3) (m) (m) (m)</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Modified</td>
<td>na</td>
<td>PropSetID YoungE ShearG MatDens XsecA XsecAsx XsecAsy XsecJxx XsecJyy XsecJ0 XsecJt</td>
</tr>
<tr>
<td>SubDyn</td>
<td>Modified</td>
<td>na</td>
<td>(-) (N/m2) (N/m2) (kg/m3) (m2) (m2) (m2) (m4) (m4) (m4) (m4)</td>
</tr>
</tbody>
</table>

### MoorDyn changes

The *MoorDyn* input file now includes additional optional inputs, but is fully backwards compatible. For further information on the new inputs:

- coupling with the *SeaState* module for wave information, see example files:

  > - <https://github.com/OpenFAST/r-test/tree/main/modules/moordyn/md_waterkin3> - full wave information from *SeaState* module
  > - <https://github.com/OpenFAST/r-test/tree/main/modules/moordyn/md_waterkin2> - hybrid wave kinematics coupling with *SeaState* module

- vortex-induced vibration (VIV) - see <https://moordyn.readthedocs.io/en/latest/inputs.html#id2>

## OpenFAST v4.0.4 to OpenFAST v4.0.5

No input file changes were made.

## OpenFAST v4.0.3 to OpenFAST v4.0.4

No input file changes were made.

## OpenFAST v4.0.2 to OpenFAST v4.0.3

No input file changes were made.

## OpenFAST v4.0.1 to OpenFAST v4.0.2

No input file changes were made.

## OpenFAST v4.0.0 to OpenFAST v4.0.1

No input file changes are required. MoorDyn can contain an option section for <span class="title-ref">External Loads</span> (see the MoorDyn documentation for details [here](https://moordyn.readthedocs.io/en/latest/inputs.html#the-v2-input-file)).

| Modified in OpenFAST <span class="title-ref">v4.0.1</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | --------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| MoorDyn | \* |  | New optional sections for <span class="title-ref">EXTERNAL LOADS</span> (freeform file). See MoorDyn documentation for details ([here](https://moordyn.readthedocs.io/en/latest/inputs.html#the-v2-input-file)) |

\*Exact line number depends on number and size of preceeding sections.

## OpenFAST v3.5.5 to OpenFAST 4.0.0

The HydroDyn module was split into HydroDyn and SeaState. This results in a completely new input file for SeaState, and complete revision of the HydroDyn input file. See examples in the regression tests for the new formats.

New modules AeroDisk (see `ADsk`), Simplified-ElastoDyn (see `SED`), and SeaState (see `SeaSt`) were added. See documentation on those modules for exmple input files.

<table>
<thead>
<tr>
<th>Modified in OpenFAST <span class="title-ref">v4.0.0</span></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>---------</th>
<th>---------------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>OpenFAST</td>
<td>13</td>
<td>CompElast</td>
<td>3 CompElast - Compute structural dynamics (switch) {1=ElastoDyn; 2=ElastoDyn + BeamDyn for blades; 3=Simplified ElastoDyn}</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>15</td>
<td>CompAero**</td>
<td>2 CompAero - Compute aerodynamic loads (switch) {0=None; 1=AeroDisk; 2=AeroDyn; 3=ExtLoads}</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>17</td>
<td>CompSeaSt</td>
<td>0 CompSeaSt - Compute sea state information (switch) {0=None; 1=SeaState}</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>41</td>
<td>SeaStFile</td>
<td>"unused" SeaStFile - Name of file containing sea state input parameters (quoted string)</td>
</tr>
<tr>
<td>AeroDyn</td>
<td><blockquote>
<p>all</p>
</blockquote></td>
<td></td>
<td>Complete restructuring of input file (see notes below)</td>
</tr>
<tr>
<td>AeroDyn Aeroacoustics</td>
<td>11*</td>
<td>TI</td>
<td>0.1 TI - Rotor-incident wind turbulence intensity (-) [Only used if TiCalcMeth == 1]</td>
</tr>
<tr>
<td>AeroDyn Aeroacoustics</td>
<td>12*</td>
<td>avgV</td>
<td>8 avgV - Average wind speed used to compute the section-incident turbulence intensity (m/s) [Only used if TiCalcMeth == 1]</td>
</tr>
<tr>
<td>HydroDyn</td>
<td><blockquote>
<p>all</p>
</blockquote></td>
<td></td>
<td>Complete restructuring of input file</td>
</tr>
<tr>
<td>SeaState</td>
<td><blockquote>
<p>all</p>
</blockquote></td>
<td></td>
<td>New module (split from HydroDyn, so contains some inputs previously found in HydroDyn)</td>
</tr>
<tr>
<td>AeroDisk</td>
<td><blockquote>
<p>all</p>
</blockquote></td>
<td></td>
<td>New module</td>
</tr>
<tr>
<td>Simplified-ElastoDyn</td>
<td><blockquote>
<p>all</p>
</blockquote></td>
<td></td>
<td>New module</td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>84</td>
<td>PtfmXYIner</td>
<td>0 PtfmXYIner - Platform xy moment of inertia about the platform CM (=-int(xydm)) (kg m^2)</td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>84</td>
<td>PtfmYZIner</td>
<td>0 PtfmYZIner - Platform yz moment of inertia about the platform CM (=-int(yzdm)) (kg m^2)</td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>84</td>
<td>PtfmXZIner</td>
<td>0 PtfmXZIner - Platform xz moment of inertia about the platform CM (=-int(xzdm)) (kg m^2)</td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>101</td>
<td></td>
<td>---------------------- YAW-FRICTION --------------------------------------------</td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>102</td>
<td>YawFrctMod</td>
<td><blockquote>
<p>0 YawFrctMod - Yaw-friction model {0: none, 1: friction independent of yaw-bearing force and bending moment, 2: friction with Coulomb terms depending on yaw-bearing force and bending moment...</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>103</td>
<td>M_CSmax</td>
<td>300 M_CSmax - Maximum static Coulomb friction torque (N-m) [M_CSmax when YawFrctMod=1; abs(Fz)*M_CSmax when YawFrctMod=2 and Fz&lt;0]</td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>104</td>
<td>M_FCSmax</td>
<td><blockquote>
<p>0 M_FCSmax - Maximum static Coulomb friction torque proportional to yaw bearing shear force (N-m) [sqrt(Fx^2+Fy^2)*M_FCSmax; only used when YawFrctMod=2]</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>105</td>
<td>M_MCSmax</td>
<td><blockquote>
<p>0 M_MCSmax - Maximum static Coulomb friction torque proportional to yaw bearing bending moment (N-m) [sqrt(Mx^2+My^2)*M_MCSmax; only used when YawFrctMod=2]</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>106</td>
<td>M_CD</td>
<td><blockquote>
<p>40 M_CD - Dynamic Coulomb friction moment (N-m) [M_CD when YawFrctMod=1; abs(Fz)*M_CD when YawFrctMod=2 and Fz&lt;0]</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>107</td>
<td>M_FCD</td>
<td><blockquote>
<p>0 M_FCD - Dynamic Coulomb friction moment proportional to yaw bearing shear force (N-m) [sqrt(Fx^2+Fy^2)*M_FCD; only used when YawFrctMod=2]</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>108</td>
<td>M_MCD</td>
<td><blockquote>
<p>0 M_MCD - Dynamic Coulomb friction moment proportional to yaw bearing bending moment (N-m) [sqrt(Mx^2+My^2)*M_MCD; only used when YawFrctMod=2]</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>109</td>
<td>sig_v</td>
<td><blockquote>
<p>0 sig_v - Linear viscous friction coefficient (N-m/(rad/s))</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>110</td>
<td>sig_v2</td>
<td><blockquote>
<p>0 sig_v2 - Quadratic viscous friction coefficient (N-m/(rad/s)^2)</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn</td>
<td>111</td>
<td>OmgCut</td>
<td><blockquote>
<p>0 OmgCut - Yaw angular velocity cutoff below which viscous friction is linearized (rad/s)</p>
</blockquote></td>
</tr>
<tr>
<td>ElastoDyn blade file</td>
<td>15</td>
<td></td>
<td>Removal of the <span class="title-ref">PitchAxis</span> input column</td>
</tr>
<tr>
<td>InflowWind driver</td>
<td>27</td>
<td></td>
<td>---- Output VTK slices ------------------------------------------------------</td>
</tr>
<tr>
<td>InflowWind driver</td>
<td>28</td>
<td>NOutWindXY</td>
<td>0 NOutWindXY -- Number of XY planes for output &lt;RootName&gt;.XY&lt;loc&gt;.t&lt;n&gt;.vtk (-) [0 to 9]</td>
</tr>
<tr>
<td>InflowWind driver</td>
<td>29</td>
<td>OutWindZ</td>
<td>90 OutWindZ -- Z coordinates of XY planes for output (m) [1 to NOutWindXY] [unused for NOutWindXY=0]</td>
</tr>
<tr>
<td>MoorDyn</td>
<td>--</td>
<td></td>
<td>New optional sections (freeform file). See MoorDyn documentation for details (<a href="https://moordyn.readthedocs.io/en/latest/inputs.html#the-v2-input-file">here</a>)</td>
</tr>
<tr>
<td>SubDyn</td>
<td>8</td>
<td><blockquote>
<dl>
<dt><code>--removed--</code></dt>
<dd>
&#10;</dd>
</dl>
</blockquote></td>
<td>removed: GuyanLoadCorrection</td>
</tr>
<tr>
<td>SubDyn</td>
<td>12</td>
<td><blockquote>
<dl>
<dt><code>--removed--</code></dt>
<dd>
&#10;</dd>
</dl>
</blockquote></td>
<td>removed: CBMod</td>
</tr>
<tr>
<td>SubDyn</td>
<td>56*</td>
<td></td>
<td><blockquote>
<p>----------------------- SPRING ELEMENT PROPERTIES -------------------------------------</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>57*</td>
<td>NSpringPropSets 0</td>
<td><blockquote>
<ul>
<li>Number of spring properties</li>
</ul>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>58*</td>
<td></td>
<td><blockquote>
<p>PropSetID k11 k12 k13 k14 k15 k16 k22 k23 k24 k25 k26 k33 k34 k35 k36 k44 k45 k46 k55 k56 k66</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>59*</td>
<td></td>
<td><blockquote>
<p>(-) (N/m) (N/m) (N/m) (N/rad) (N/rad) (N/rad) (N/m) (N/m) (N/rad) (N/rad) (N/rad) (N/m) (N/rad) (N/rad) (N/rad) (Nm/rad) (Nm/rad) (Nm/rad) (Nm/rad) (Nm/rad) (Nm/rad)</p>
</blockquote></td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>16</td>
<td>WrMooringVis</td>
<td>true WrMooringVis - Write shared mooring visualization, at DT_Mooring timestep (-) [only used for Mod_SharedMooring=3]</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>48*</td>
<td>RotorDiamRef</td>
<td>125 RotorDiamRef - Reference turbine rotor diameter for wake calculations (m) [&gt;0.0]</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>53*</td>
<td>k_vAmb</td>
<td>DEFAULT k_vAmb - Calibrated parameters for the influence of the ambient turbulence in the eddy viscosity (set of 5 parameters: k, FMin, DMin, DMax, Exp) (-) [&gt;=0.0, &gt;=0.0 and &lt;=1.0, &gt;=0.0, &gt;DMin, &gt;0.0] or DEFAULT [DEFAULT=0.05, 1.0, 0.0, 1.0, 0.01]</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>54*</td>
<td>kvShr</td>
<td>DEFAULT k_vShr - Calibrated parameters for the influence of the shear layer in the eddy viscosity (set of 5 parameters: k, FMin, DMin, DMax, Exp) (-) [&gt;=0.0, &gt;=0.0 and &lt;=1.0, &gt;=0.0, &gt;DMin, &gt;0.0] or DEFAULT [DEFAULT=0.016, 0.2, 3.0, 25.0, 0.1]</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>55-62*</td>
<td><dl>
<dt><code>--removed--</code></dt>
<dd>
&#10;</dd>
</dl></td>
<td></td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>69*</td>
<td></td>
<td>--- WAKE-ADDED TURBULENCE ---</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>70*</td>
<td><blockquote>
<p>WAT</p>
</blockquote></td>
<td>2 WAT - Switch between wake-added turbulence box options {0: no wake added turbulence, 1: predefined turbulence box, 2: user defined turbulence box} (switch)</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>71*</td>
<td><blockquote>
<p>WAT_BoxFile</p>
</blockquote></td>
<td>"../WAT_MannBoxDB/FFDB_D100_512x512x64.u" WAT_BoxFile - Filepath to the file containing the u-component of the turbulence box (either predefined or user-defined) (quoted string)</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>72*</td>
<td><blockquote>
<p>WAT_NxNyNz</p>
</blockquote></td>
<td>512, 512, 64 WAT_NxNyNz - Number of points in the x, y, and z directions of the WAT_BoxFile [used only if WAT=2, derived value if WAT=1] (-)</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>73*</td>
<td><blockquote>
<p>WAT_DxDyDz</p>
</blockquote></td>
<td>5.0, 5.0, 5.0 WAT_DxDyDz - Distance (in meters) between points in the x, y, and z directions of the WAT_BoxFile [used only if WAT=2, derived value if WAT=1] (m)</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>74*</td>
<td><blockquote>
<p>WAT_ScaleBox</p>
</blockquote></td>
<td>default WAT_ScaleBox - Flag to scale the input turbulence box to zero mean and unit standard deviation at every node [DEFAULT=False] (flag)</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>75*</td>
<td><blockquote>
<p>WAT_k_Def</p>
</blockquote></td>
<td>default WAT_k_Def - Calibrated parameters for the influence of the maximum wake deficit on wake-added turbulence (set of 5 parameters: k_Def, FMin, DMin, DMax, Exp) (-) [&gt;=0.0, &gt;=0.0 and &lt;=1.0, &gt;=0.0, &gt;DMin, &gt;0.0] or DEFAULT [DEFAULT=[0.6, 0.0, 0.0, 2.0, 1.0 ]]</td>
</tr>
<tr>
<td>FAST.Farm</td>
<td>76*</td>
<td><blockquote>
<p>WAT_k_Grad</p>
</blockquote></td>
<td>default WAT_k_Grad - Calibrated parameters for the influence of the radial velocity gradient of the wake deficit on wake-added turbulence (set of 5 parameters: k_Grad, FMin, DMin, DMax, Exp) (-) [&gt;=0.0, &gt;=0.0 and &lt;=1.0, &gt;=0.0, &gt;DMin, &gt;0.0] or DEFAULT [DEFAULT=[3.0, 0.0, 0.0, 12.0, 0.65]</td>
</tr>
</tbody>
</table>

\*Exact line number depends on number of entries in various preceeding tables.

\*\* The AeroDyn 14 module has been removed and replaced with AeroDisk. AeroDyn15 renamed to AeroDyn

### New Modules

- AeroDisk -- reduced order actuator disk model (see `ADsk`)
- Simplified ElastoDyn -- a reduced order structural model with only yaw and rotor speed degrees of freedom (see `SED`)
- SeaState -- wave dynamics calculations (previously part of HydroDyn)

## AeroDyn changes starting from v4.x

The table below shows how to convert from the Old AeroDyn inputs to the new AeroDyn inputs. Additional ressources:

- The AeroDyn input file description (`ad_input`) for more details on the new inputs.
- The [discussion](https://github.com/OpenFAST/openfast/discussions/1895) that led to these new inputs.
- An example of AeroDyn input file at it's latest format: `Example <aerodyn/examples/ad_primary_example.dat>`:
- A directory with a working example: [here](https://github.com/OpenFAST/r-test/blob/dev/modules/aerodyn/ad_BAR_OLAF/OpenFAST_BAR_00_AeroDyn.dat)
- An example python converter (v3.5.x to 4.x): [here](https://github.com/OpenFAST/openfast_toolbox/blob/dev/openfast_toolbox/converters/examples/Main_AD30_AD40.py)

| Old inputs | Corresponding new inputs |
|----|----|
| <span class="title-ref">WakeMod=0</span> | <span class="title-ref">Wake_Mod=0</span> |
| <span class="title-ref">WakeMod=1</span> ("BEM") | <span class="title-ref">Wake_Mod=1</span> and <span class="title-ref">DBEMT_Mod=0</span> and <span class="title-ref">BEM_Mod=1</span> |
| <span class="title-ref">WakeMod=2</span> ("DBEMT") | <span class="title-ref">Wake_Mod=1</span> and <span class="title-ref">DBEMT_Mod={1,2,3}</span> |
| <span class="title-ref">WakeMod=3</span> ("OLAF") | <span class="title-ref">Wake_Mod=3</span> |
| <span class="title-ref">AFAeroMod=1</span> | <span class="title-ref">UA_Mod=0</span> and <span class="title-ref">AoA34=False</span> |
| <span class="title-ref">AFAeroMod=2</span> | <span class="title-ref">UA_Mod\>0</span> and <span class="title-ref">AoA34=True</span> and <span class="title-ref">UA_Mod=UAMod</span> |
| <span class="title-ref">FrozenWake=True</span> | <span class="title-ref">DBEMT_Mod=-1</span> |
| <span class="title-ref">FrozenWake=False</span> | <span class="title-ref">DBEMT_Mod=0</span> (quasi-steady) or <span class="title-ref">DBEMT_Mod\>0</span> (dynamic) |
| <span class="title-ref">SkewMod=2</span> (Glauert) | <span class="title-ref">Skew_Mod=1</span> and <span class="title-ref">SkewRedistr_Mod=1</span> |
| <span class="title-ref">SkewMod=0</span> (Orthogonal) | <span class="title-ref">Skew_Mod=-1</span> |
| <span class="title-ref">SkewModFactor</span> | <span class="title-ref">SkewRedistrFactor</span> |
| <span class="title-ref">UAMod={2-7}</span> | <span class="title-ref">UA_Mod={2-7}</span> and <span class="title-ref">AoA34=True</span> |

## OpenFAST v3.5.4 to OpenFAST v3.5.5

No input file changes were made.

## OpenFAST v3.5.3 to OpenFAST v3.5.4

No input file changes were made.

## OpenFAST v3.5.2 to OpenFAST v3.5.3

No input file changes were made.

## OpenFAST v3.5.1 to OpenFAST v3.5.2

No input file changes were made.

## OpenFAST v3.5.0 to OpenFAST v3.5.1

No input file changes were made. Some input files now include additional output channels: AeroDyn nodal outputs for another coordinate system, new MoorDyn output names (Connect changed to Point).

## OpenFAST v3.4.0 to OpenFAST v3.5.0

Updated the CMake build system. Now requires CMake v3.12 or higher.

<table>
<thead>
<tr>
<th>Modified in OpenFAST <span class="title-ref">3.5.0</span></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>---------------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>ServoDyn-StructCtrl</td>
<td><blockquote>
<p>6</p>
</blockquote></td>
<td>StC_DOF_MODE</td>
<td>2 StC_DOF_MODE - DOF mode (switch) {0: No StC or TLCD DOF; 1: StC_X_DOF, StC_Y_DOF, and/or StC_Z_DOF (three independent StC DOFs); 2: StC_XY_DOF (Omni-Directional StC); 3: TLCD; 4: Prescribed force/moment time series; 5: Force determined by external DLL}</td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td>VelInterpCubic</td>
<td><blockquote>
<p>true VelInterpCubic - Use cubic interpolation for velocity in time (false=linear, true=cubic) [Used with WindType=2,3,4,5,7]</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>51</p>
</blockquote></td>
<td></td>
<td>================== LIDAR Parameters ===========================================================================</td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>52</p>
</blockquote></td>
<td>SensorType</td>
<td><blockquote>
<p>0 SensorType - Switch for lidar configuration (0 = None, 1 = Single Point Beam(s), 2 = Continuous, 3 = Pulsed)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>53</p>
</blockquote></td>
<td>NumPulseGate</td>
<td><blockquote>
<p>0 NumPulseGate - Number of lidar measurement gates (used when SensorType = 3)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>54</p>
</blockquote></td>
<td>PulseSpacing</td>
<td><blockquote>
<p>30 PulseSpacing - Distance between range gates (m) (used when SensorType = 3)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>55</p>
</blockquote></td>
<td>NumBeam</td>
<td><blockquote>
<p>0 NumBeam - Number of lidar measurement beams (0-5)(used when SensorType = 1)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>56</p>
</blockquote></td>
<td>FocalDistanceX</td>
<td><blockquote>
<p>-200 FocalDistanceX - Focal distance co-ordinates of the lidar beam in the x direction (relative to hub height) (only first coordinate used for SensorType 2 and 3) (m)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>57</p>
</blockquote></td>
<td>FocalDistanceY</td>
<td><blockquote>
<p>0 FocalDistanceY - Focal distance co-ordinates of the lidar beam in the y direction (relative to hub height) (only first coordinate used for SensorType 2 and 3) (m)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>58</p>
</blockquote></td>
<td>FocalDistanceZ</td>
<td><blockquote>
<p>0 FocalDistanceZ - Focal distance co-ordinates of the lidar beam in the z direction (relative to hub height) (only first coordinate used for SensorType 2 and 3) (m)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>59</p>
</blockquote></td>
<td>RotorApexOffsetPos</td>
<td>0.0 0.0 0.0 RotorApexOffsetPos - Offset of the lidar from hub height (m)</td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>60</p>
</blockquote></td>
<td>URefLid</td>
<td><blockquote>
<p>17 URefLid - Reference average wind speed for the lidar[m/s]</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>61</p>
</blockquote></td>
<td>MeasurementInterval</td>
<td><blockquote>
<p>0.25 MeasurementInterval - Time between each measurement [s]</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>62</p>
</blockquote></td>
<td>LidRadialVel</td>
<td><blockquote>
<p>False LidRadialVel - TRUE =&gt; return radial component, FALSE =&gt; return 'x' direction estimate</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>63</p>
</blockquote></td>
<td>ConsiderHubMotion</td>
<td><blockquote>
<p>1 ConsiderHubMotion - Flag whether to consider the hub motion's impact on Lidar measurements</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v3.4.0 to OpenFAST v3.4.1

Restored the AeroDyn channel names with <span class="title-ref">Aero</span> in the name. These had be changed to <span class="title-ref">Fld</span> in v3.4.0 which caused headaches for users. The <span class="title-ref">Fld</span> names are now aliases to the <span class="title-ref">Aero</span> names.

## OpenFAST v3.4.0 to OpenFAST dev

AeroDyn14 has been removed!

<table>
<thead>
<tr>
<th>Changed in OpenFAST <span class="title-ref">dev</span></th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>------------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>OpenFAST</td>
<td>15</td>
<td>CompAero</td>
<td><blockquote>
<p>2 CompAero - Compute aerodynamic loads (switch) {0=None; 2=AeroDyn v15}</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v3.3.0 to OpenFAST v3.4.0

| Added in OpenFAST <span class="title-ref">3.4.0</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| FAST.Farm | 42\* | ModWake | 1 Mod_Wake - Switch between wake formulations {1:Polar, 2:Curl, 3:Cartesian} (-) (switch) |
| FAST.Farm | 67 | CurlSection | --- CURLED-WAKE PARAMETERS \[only used if Mod_Wake=2 or 3\] --- |
| FAST.Farm | 68 | Swirl | DEFAULT Swirl - Switch to include swirl velocities in wake (-) (switch) \[DEFAULT=True\] |
| FAST.Farm | 69 | k_VortexDecay | DEFAULT k_VortexDecay - Vortex decay constant for curl (-) \[DEFAULT=0.01\] \[only used if Mod_Wake=2\] |
| FAST.Farm | 70 | NumVortices | DEFAULT NumVortices - The number of vortices in the curled wake model (-) \[DEFAULT=100\] \[only used if Mod_Wake=2\] |
| FAST.Farm | 71 | sigma_D | DEFAULT sigma_D - The width of the vortices in the curled wake model non-dimensionalized by rotor diameter (-) \[DEFAULT=0.2\] \[only used if Mod_Wake=2\] |
| FAST.Farm | 72 | FilterInit | DEFAULT FilterInit - Switch to filter the initial wake plane deficit and select the number of grid points for the filter {0: no filter, 1: filter of size 1} or DEFAULT \[DEFAULT=1\] (switch) |
| FAST.Farm | 73 | k_vCurl | DEFAULT k_vCurl - Calibrated parameter for scaling the eddy viscosity in the curled-wake model (-) \[\>=0\] or DEFAULT \[DEFAULT=2.0 \] |
| FAST.Farm | 74 | Mod_Projection | DEFAULT Mod_Projection - Switch to select how the wake plane velocity is projected in AWAE {1: keep all components, 2: project against plane normal} or DEFAULT \[DEFAULT=1: if Mod_Wake is 1 or 3, or DEFAULT=2: if Mod_Wake is 2\] (switch) |
| FAST.Farm | 91 | OutAllPlanes | DEFAULT OutAllPlanes - Output all wake planes at all time steps. \[DEFAULT=False\] |
| AeroDyn 15 | 13 | Buoyancy | True Buoyancy - Include buoyancy effects? (flag) |
| AeroDyn 15 | 65 | HubPropsSection | ====== Hub Properties ============================================================================== \[used only when Buoyancy=True\] |
| AeroDyn 15 | 66 | VolHub | 7.0 VolHub - Hub volume (m^3) |
| AeroDyn 15 | 67 | HubCenBx | 0.5 HubCenBx - Hub center of buoyancy x direction offset (m) |
| AeroDyn 15 | 68 | NacPropsSection | ====== Nacelle Properties ========================================================================== \[used only when Buoyancy=True\] |
| AeroDyn 15 | 69 | VolNac | 32.0 VolNac - Nacelle volume (m^3) |
| AeroDyn 15 | 70 | NacCenB | 0.4,0,0 NacCenB - Position of nacelle center of buoyancy from yaw bearing in nacelle coordinates (m) |
| AeroDyn 15 | 71 | TFinPropsSection | ====== Tail fin Aerodynamics ======================================================================== |
| AeroDyn 15 | 72 | TFinAero | True TFinAero - Calculate tail fin aerodynamics model (flag) |
| AeroDyn 15 | 73 | TFinFile\$ | "AD_Fin.dat" TFinFile - Input file for tail fin aerodynamics \[used only when TFinAero=True\] |
| AeroDyn 15 |  | TwrCb | 1.0 \[additional column in *Tower Influence and Aerodynamics* table\] |
| AeroDyn blade |  | BlCb | 0.187 \[additional column in *Blade Properties* table\] |
| AeroDyn blade |  | BlCenBn | 0.3 \[additional column in *Blade Properties* table\] |
| AeroDyn blade |  | BlCenBt | 0.1 \[additional column in *Blade Properties* table\] |
| OLAF | 18 | nNWPanelFree | 180 nNWPanelFree - Number of free near-wake panels (-) {default: nNWPanels} |
| OLAF | 19 | nFWPanels | 900 nFWPanels - Number of far-wake panels (-) {default: 0} |
| OLAF | 20 | nFWPanelsFree | 0 nFWPanelsFree - Number of free far-wake panels (-) {default: nFWPanels} |

\*Exact line number depends on number of entries in various preceeding tables.

\$ The content of the tail fin input file is described in `TF_tf_input-file`.

**New Default Values**: The following default value were changed

- OLAF *VelocityMethod* is now 2 (particle tree), previous value 1 (n^2 BiotSavart law on segments).
- OLAF *WakeRegMethod* is now 3 (increasing with wake age), previous value was 1 (constant).
- OLAF *nVTKBlades* is now 0 (no wake panels output), previous value was 1 (wake panels output for blade 1)

| Removed in OpenFAST v3.4.0 |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| OLAF | 18 | WakeLength | 900 WakeLength Total wake distance \[integer\] (number of time steps) |
| OLAF | 19 | FreeWakeLength | 0 FreeWakeLength Wake length that is free \[integer\] (number of time steps) {default: WakeLength} |

## OpenFAST v3.2.0 to OpenFAST v3.3.0

| Added in OpenFAST <span class="title-ref">3.3.0</span> |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| FAST.Farm | 9 | ModWaveField | 2 Mod_WaveField - Wave field handling (-) (switch) {1: use individual HydroDyn inputs without adjustment, 2: adjust wave phases based on turbine offsets from farm origin} |
| FAST.Farm | 10 | Mod_SharedMooring | 0 Mod_SharedMooring - Shared mooring system model (switch) {0: None, 3=MoorDyn}} |
| FAST.Farm | 13 | na | ------ SHARED MOORING SYSTEM ------ \[used only for Mod_SharedMoor\>0\] |
| FAST.Farm | 14 | SharedMoorFile | "" SharedMoorFile - Name of file containing shared mooring system input parameters (quoted string) \[used only when Mod_SharedMooring \> 0\] |
| FAST.Farm | 15 | DT_Mooring | 0.04 DT_Mooring - Time step for farm-level mooring coupling with each turbine (s) \[used only when Mod_SharedMooring \> 0\] |
| AeroDyn driver | 54\* | WrVTK_Type | 1 WrVTK_Type - VTK visualization data type: (switch) {1=surfaces; 2=lines; 3=both} |

<table>
<thead>
<tr>
<th>Modified in OpenFAST v3.3.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>MoorDyn&amp;</td>
<td>5</td>
<td>na</td>
<td><blockquote>
<p>Name Diam MassDen EA BA/-zeta EI Cd Ca CdAx CaAx</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>6</td>
<td>na</td>
<td><blockquote>
<p>(-) (m) (kg/m) (N) (N-s/-) (-) (-) (-) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>7</td>
<td>na</td>
<td><blockquote>
<p>main 0.0766 113.35 7.536E8 -1.0 0 2.0 0.8 0.4 0.25</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>8*</td>
<td>na</td>
<td><blockquote>
<p>---------------------- POINTS --------------------------------</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>9*</td>
<td>na</td>
<td><blockquote>
<p>ID Attachment X Y Z M V CdA CA</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>10*</td>
<td>na</td>
<td><blockquote>
<p>(-) (-) (m) (m) (m) (kg) (m^3) (m^2) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>11*</td>
<td>na</td>
<td><blockquote>
<p>1 Fixed 418.8 725.383 -200.0 0 0 0 0</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>17*</td>
<td>na</td>
<td><blockquote>
<p>---------------------- LINES --------------------------------------</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>18*</td>
<td>na</td>
<td><blockquote>
<p>ID LineType AttachA AttachB UnstrLen NumSegs Outputs</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>19*</td>
<td>na</td>
<td><blockquote>
<p>(-) (-) (-) (-) (m) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>20*</td>
<td>na</td>
<td><blockquote>
<p>1 main 1 4 835.35 20 -</p>
</blockquote></td>
</tr>
</tbody>
</table>

&MoorDyn has undergone an extensive revision that leaves few lines unchanged. We recommend looking at a sample input file for the 5MW_OC4Semi_WSt_WavesWN regression test for reference rather than line by line changes in the above tables.

<table>
<thead>
<tr>
<th>Removed in OpenFAST v3.3.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>MoorDyn&amp;</td>
<td>5</td>
<td>NTypes</td>
<td><blockquote>
<p>1 NTypes - number of LineTypes</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>10*</td>
<td>NConnects</td>
<td><blockquote>
<p>6 NConnects - number of connections including anchors and fairleads</p>
</blockquote></td>
</tr>
<tr>
<td>MoorDyn&amp;</td>
<td>20*</td>
<td>NLines</td>
<td><blockquote>
<p>3 NLines - number of line objects</p>
</blockquote></td>
</tr>
</tbody>
</table>

\*Exact line number depends on number of entries in various preceeding tables.

&MoorDyn has undergone an extensive revision that leaves few lines unchanged. We recommend looking at a sample input file for the 5MW_OC4Semi_WSt_WavesWN regression test for reference rather than line by line changes in the above tables.

## OpenFAST v3.1.0 to OpenFAST v3.2.0

<table>
<thead>
<tr>
<th>Added in OpenFAST v3.2.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>TurbSim</td>
<td>13</td>
<td>WrHAWCFF</td>
<td><blockquote>
<p>False WrHAWCFF - Output full-field time-series data in HAWC form? (Generates RootName-u.bin, RootName-v.bin, RootName-w.bin, RootName.hawc)</p>
</blockquote></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Removed in OpenFAST v3.2.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>TurbSim</td>
<td>14</td>
<td>Clockwise</td>
<td><blockquote>
<p>True Clockwise - Clockwise rotation looking downwind? (used only for full-field binary files - not necessary for AeroDyn)</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v3.0.0 to OpenFAST v3.1.0

<table>
<thead>
<tr>
<th>Added in OpenFAST v3.1.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>ServoDyn</td>
<td>60</td>
<td>AeroControlSec</td>
<td>---------------------- AERODYNAMIC FLOW CONTROL --------------------------------</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>61</td>
<td>AfCmode</td>
<td>0 AfCmode - Airfoil control mode {0: none, 1: cosine wave cycle, 4: user-defined from Simulink/Labview, 5: user-defined from Bladed-style DLL} (switch)</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>62</td>
<td>AfC_Mean</td>
<td>0 AfC_Mean - Mean level for cosine cycling or steady value (-) [used only with AfCmode==1]</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>63</td>
<td>AfC_Amp</td>
<td>0 AfC_Amp - Amplitude for cosine cycling of flap signal (-) [used only with AfCmode==1]</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>64</td>
<td>AfC_Phase</td>
<td>0 AfC_Phase - Phase relative to the blade azimuth (0 is vertical) for cosine cycling of flap signal (deg) [used only with AfCmode==1]</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>74</td>
<td>CablesSection</td>
<td>---------------------- CABLE CONTROL -------------------------------------------</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>75</td>
<td>CCmode</td>
<td>0 CCmode - Cable control mode {0: none, 4: user-defined from Simulink/Labview, 5: user-defined from Bladed-style DLL} (switch)</td>
</tr>
<tr>
<td>HydroDyn driver</td>
<td>6</td>
<td>WtrDens</td>
<td>1025 WtrDens - Water density (kg/m^3)</td>
</tr>
<tr>
<td>HydroDyn driver</td>
<td>7</td>
<td>WtrDpth</td>
<td>200 WtrDpth - Water depth (m)</td>
</tr>
<tr>
<td>HydroDyn driver</td>
<td>8</td>
<td>MSL2SWL</td>
<td>0 MSL2SWL - Offset between still-water level and mean sea level (m) [positive upward]</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>21</td>
<td>MHK</td>
<td>0 MHK - MHK turbine type (switch) {0=Not an MHK turbine; 1=Fixed MHK turbine; 2=Floating MHK turbine}</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>22</td>
<td>EnvCondSection</td>
<td>---------------------- ENVIRONMENTAL CONDITIONS --------------------------------</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>23</td>
<td>Gravity</td>
<td>9.80665 Gravity - Gravitational acceleration (m/s^2)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>24</td>
<td>AirDens</td>
<td>1.225 AirDens - Air density (kg/m^3)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>25</td>
<td>WtrDens</td>
<td>1025 WtrDens - Water density (kg/m^3)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>26</td>
<td>KinVisc</td>
<td>1.464E-05 KinVisc - Kinematic viscosity of working fluid (m^2/s)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>27</td>
<td>SpdSound</td>
<td>335 SpdSound - Speed of sound in air (m/s)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>28</td>
<td>Patm</td>
<td>103500 Patm - Atmospheric pressure (Pa) [used only for an MHK turbine cavitation check]</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>29</td>
<td>Pvap</td>
<td>1700 Pvap - Vapour pressure of working fluid (Pa) [used only for an MHK turbine cavitation check]</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>30</td>
<td>WtrDpth</td>
<td>50 WtrDpth - Water depth (m)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>31</td>
<td>MSL2SWL</td>
<td>0 MSL2SWL - Offset between still-water level and mean sea level (m) [positive upward]</td>
</tr>
<tr>
<td>AeroDyn 15</td>
<td>39</td>
<td>UAStartRad</td>
<td>0.25 UAStartRad - Starting radius for dynamic stall (fraction of rotor radius) [used only when AFAeroMod=2; if line is missing UAStartRad=0]</td>
</tr>
<tr>
<td>AeroDyn 15</td>
<td>40</td>
<td>UAEndRad</td>
<td>0.95 UAEndRad - Ending radius for dynamic stall (fraction of rotor radius) [used only when AFAeroMod=2; if line is missing UAEndRad=1]</td>
</tr>
<tr>
<td>AeroDyn driver</td>
<td>34</td>
<td>Twr2Shft</td>
<td>3.09343 Twr2Shft - Vertical distance from the tower-top to the rotor shaft (m)</td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>12*</td>
<td>alphaUpper</td>
<td>5.0 alphaUpper ! Angle of attack at upper boundary of fully-attached region. (deg) [used only when UAMod=5] ! THIS IS AN OPTIONAL LINE; if omitted, it will be calculated from the polar data</td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>13*</td>
<td>alphaLower</td>
<td>-3.0 alphaLower ! Angle of attack at lower boundary of fully-attached region. (deg) [used only when UAMod=5] ! THIS IS AN OPTIONAL LINE; if omitted, it will be calculated from the polar data</td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>42*</td>
<td>UACutout_delta</td>
<td>"DEFAULT" UACutout_delta ! Delta angle of attack below UACutout where unsteady aerodynamics begin to turn off (blend with steady solution) (deg) [Specifying the string "Default" sets UACutout_delta to 5 degrees] ! THIS IS AN OPTIONAL LINE; if omitted, it will be set to its default value</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>28</td>
<td>Mod_Wake</td>
<td>1 Mod_Wake - Switch between wake formulations {1:Polar, 2:Curl, 3:Cartesian} (-) (switch)</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>62</td>
<td>Swirl</td>
<td>False Swirl - Switch to include swirl velocities in wake [only used if Mod_Wake=2 or Mod_Wake=3] (-) (switch)</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>63</td>
<td>k_VortexDecay</td>
<td><ol start="0" type="1">
<li>k_VortexDecay - Vortex decay constant for curl (-)</li>
</ol></td>
</tr>
<tr>
<td>FASTFarm</td>
<td>64</td>
<td>NumVortices</td>
<td>DEFAULT NumVortices - The number of vortices in the curled wake model (-) [DEFAULT=100]</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>65</td>
<td>sigma_D</td>
<td>DEFAULT sigma_D - The width of the vortices in the curled wake model non-dimesionalized by rotor diameter (-) [DEFAULT=0.2]</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>66</td>
<td>FilterInit</td>
<td>DEFAULT FilterInit - Switch to filter the initial wake plane deficit and select the number of grid points for the filter {0: no filter, 1: filter of size 1} or DEFAULT [DEFAULT=1] [unused for Mod_Wake=1] (switch)</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>67</td>
<td>k_vCurl</td>
<td>20 k_vCurl - Calibrated parameter for scaling the eddy viscosity in the curled-wake model (-) [only used if Mod_Wake=2 or Mod_Wake=3] [&gt;=0] or DEFAULT [DEFAULT=2.0 ]</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>68</td>
<td>Mod_Projection</td>
<td>DEFAULT Mod_Projection - Switch to select how the wake plane velocity is project</td>
</tr>
<tr>
<td>FASTFarm</td>
<td>85</td>
<td>OutAllPlanes</td>
<td>True OutAllPlanes - Output all wake planes at all time steps. [DEFAULT=False]</td>
</tr>
</tbody>
</table>

\*non-comment line count, excluding lines contained if NumCoords is not 0, and including all OPTIONAL lines in the UA coefficients table.

| Modified in OpenFAST v3.1.0 |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| AeroDyn | 16 | AirDens | "default" AirDens - Air density (kg/m^3) |
| AeroDyn | 17 | KinVisc | "default" KinVisc - Kinematic viscosity of working fluid (m^2/s) |
| AeroDyn | 18 | SpdSound | "default" SpdSound - Speed of sound in air (m/s) |
| AeroDyn | 19 | Patm | "default" Patm - Atmospheric pressure (Pa) \[used only when CavitCheck=True\] |
| AeroDyn | 20 | Pvap | "default" Pvap - Vapour pressure of working fluid (Pa) \[used only when CavitCheck=True\] |
| HydroDyn | 5 | WtrDens | "default" WtrDens - Water density (kg/m^3) |
| HydroDyn | 6 | WtrDpth | "default" WtrDpth - Water depth (meters) |
| HydroDyn | 7 | MSL2SWL | "default" MSL2SWL - Offset between still-water level and mean sea level (meters) \[positive upward; unused when WaveMod = 6; must be zero if PotMod=1 or 2\] |

| Removed in OpenFAST v3.1.0 |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| AeroDyn | 21 | FluidDepth | 0.5 FluidDepth - Water depth above mid-hub height (m) \[used only when CavitCheck=True\] |
| ElastoDyn | 7 | EnvCondSection | ---------------------- ENVIRONMENTAL CONDITION --------------------------------- |
| ElastoDyn | 8 | Gravity | 9.80665 Gravity - Gravitational acceleration (m/s^2) |

- The AeroDyn driver input file was completely rewritten. You may consult the following examples for a `single rotor <./aerodyn/examples/ad_driver_example.dvr>` and `multiple rotors <./aerodyn/examples/ad_driver_multiple.dvr>` in addition to the `AeroDyn driver documentation<ad_driver>`.
- SubDyn
  - SubDyn Driver, applied loads input:

<table>
<thead>
<tr>
<th>Added</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>---------------</th>
<th>-----</th>
<th>-------------------</th>
<th>-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>SubDyn driver</td>
<td><blockquote>
<p>21</p>
</blockquote></td>
<td>[separator line]</td>
<td>---------------------- LOADS --------------------------------------------------------------------</td>
</tr>
<tr>
<td>SubDyn driver</td>
<td><blockquote>
<p>22</p>
</blockquote></td>
<td>nAppliedLoads</td>
<td><blockquote>
<p>1 nAppliedLoads - Number of applied loads at given nodes false</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn driver</td>
<td><blockquote>
<p>23</p>
</blockquote></td>
<td>ALTableHeader</td>
<td>ALJointID Fx Fy Fz Mx My Mz UnsteadyFile</td>
</tr>
<tr>
<td>SubDyn driver</td>
<td><blockquote>
<p>24</p>
</blockquote></td>
<td>ALTableUnit</td>
<td><blockquote>
<p>(-) (N) (N) (N) (Nm) (Nm) (Nm) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn driver</td>
<td><blockquote>
<p>25</p>
</blockquote></td>
<td>ALTableLine1</td>
<td><blockquote>
<p>10 0.0 0.0 0.0 0.0 0.0 0.0 ""</p>
</blockquote></td>
</tr>
</tbody>
</table>

> - SubDyn: the lines at n+1 and n+2 below were inserted after line n.

<table>
<thead>
<tr>
<th>Added</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>---------------</th>
<th>-----</th>
<th>-------------------</th>
<th>-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>SubDyn</td>
<td><blockquote>
<p>n</p>
</blockquote></td>
<td>OutCOSM</td>
<td>Output cosine matrices with the selected output member forces (flag)</td>
</tr>
<tr>
<td>SubDyn</td>
<td>n+1</td>
<td>OutCBModes</td>
<td>Output Guyan and Craig-Bampton modes {0: No output, 1: JSON output}, (flag)</td>
</tr>
<tr>
<td>SubDyn</td>
<td>n+2</td>
<td>OutFEMModes</td>
<td>Output first 30 FEM modes {0: No output, 1: JSON output} (flag)</td>
</tr>
</tbody>
</table>

## OpenFAST v2.6.0 to OpenFAST v3.0.0

**ServoDyn Changes**

- The input file parser is updated to a keyword/value pair based input. Each entry must have a corresponding keyword with the same spelling as expected.
- The TMD submodule of ServoDyn is replaced by an updated Structural Control module (StC) with updated capabilities and input file.

| Removed in OpenFAST v3.0.0 |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| ServoDyn | 60 | na | ---------------------- TUNED MASS DAMPER --------------------------------------- |
| ServoDyn | 61 | CompNTMD | False CompNTMD - Compute nacelle tuned mass damper {true/false} (flag) |
| ServoDyn | 62 | NTMDfile | "NRELOffshrBsline5MW_ServoDyn_TMD.dat" NTMDfile - Name of the file for nacelle tuned mass damper (quoted string) \[unused when CompNTMD is false\] |
| ServoDyn | 63 | CompTTMD | False CompTTMD - Compute tower tuned mass damper {true/false} (flag) |
| ServoDyn | 64 | TTMDfile | "NRELOffshrBsline5MW_ServoDyn_TMD.dat" TTMDfile - Name of the file for tower tuned mass damper (quoted string) \[unused when CompTTMD is false\] |

<table>
<thead>
<tr>
<th>Added in OpenFAST v3.0.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>ServoDyn</td>
<td>60</td>
<td>na</td>
<td>---------------------- STRUCTURAL CONTROL --------------------------------------</td>
</tr>
<tr>
<td>ServoDyn</td>
<td>61</td>
<td>NumBStC</td>
<td><blockquote>
<p>0 NumBStC - Number of blade structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>62</td>
<td>BStCfiles</td>
<td><blockquote>
<p>"unused" BStCfiles - Name of the files for blade structural controllers (quoted strings) [unused when NumBStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>63</td>
<td>NumNStC</td>
<td><blockquote>
<p>0 NumNStC - Number of nacelle structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>64</td>
<td>NStCfiles</td>
<td><blockquote>
<p>"unused" NStCfiles - Name of the files for nacelle structural controllers (quoted strings) [unused when NumNStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>65</td>
<td>NumTStC</td>
<td><blockquote>
<p>0 NumTStC - Number of tower structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>66</td>
<td>TStCfiles</td>
<td><blockquote>
<p>"unused" TStCfiles - Name of the files for tower structural controllers (quoted strings) [unused when NumTStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>67</td>
<td>NumSStC</td>
<td><blockquote>
<p>0 NumSStC - Number of substructure structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>68</td>
<td>SStCfiles</td>
<td><blockquote>
<p>"unused" SStCfiles - Name of the files for substructure structural controllers (quoted strings) [unused when NumSStC==0]</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v2.5.0 to OpenFAST v2.6.0

Many changes were applied to SubDyn input file format. You may consult the following example: `(SubDyn's Input File) <./subdyn/examples/OC4_Jacket_SD_Input.dat>`: and the online SubDyn documentation.

<table>
<thead>
<tr>
<th>Added in OpenFAST v2.6.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>AeroDyn 15</td>
<td></td>
<td>TwrTi</td>
<td><blockquote>
<p>0.0000000E+00 6.0000000E+00 1.0000000E+00 1.0000000E-01 [additional column in <em>Tower Influence and Aerodynamics</em> table]</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td><blockquote>
<p>8</p>
</blockquote></td>
<td>GuyanLoadCorr.</td>
<td><blockquote>
<p>False GuyanLoadCorection - Include extra moment from lever arm at interface and rotate FEM for floating</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>15</td>
<td>GuyanDampMod</td>
<td><blockquote>
<p>0 GuyanDampMod - Guyan damping {0=none, 1=Rayleigh Damping, 2=user specified 6x6 matrix}</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>16</td>
<td>RayleighDamp</td>
<td><blockquote>
<p>0.001, 0.003 RayleighDamp - Mass and stiffness proportional damping coefficients (Rayleigh Damping) [only if GuyanDampMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>17</td>
<td>GuyanDampSize</td>
<td><blockquote>
<p>6 GuyanDampSize - Guyan damping matrix size (square, 6x6) [only if GuyanDampMod=2]</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>18</td>
<td>GuyanDampMat</td>
<td><blockquote>
<p>0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>-23</td>
<td>GuyanDampMat</td>
<td><blockquote>
<p>0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>CablesSection</td>
<td><blockquote>
<p>-------------------------- CABLE PROPERTIES -------------------------------------</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>CablesSection</td>
<td><blockquote>
<p>0 NCablePropSets - Number of cable cable properties</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>CablesSection</td>
<td><blockquote>
<p>PropSetID EA MatDens T0</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>CablesSection</td>
<td><blockquote>
<p>(-) (N) (kg/m) (N)</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>RigidSection</td>
<td><blockquote>
<p>---------------------- RIGID LINK PROPERTIES ------------------------------------</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>RigidSection</td>
<td><blockquote>
<p>0 NRigidPropSets - Number of rigid link properties</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>RigidSection</td>
<td><blockquote>
<p>PropSetID MatDens</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>RigidSection</td>
<td><blockquote>
<p>(-) (kg/m)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>52</td>
<td>NBody</td>
<td><blockquote>
<p>1 NBody - Number of WAMIT bodies to be used (-) [&gt;=1; only used when PotMod=1. If NBodyMod=1, the WAMIT data contains a vector of size 6*NBody x 1 and matrices of size 6*NBody x 6*NBody; if NBodyMod&gt;1, there are NBody sets of WAMIT data each with a vector of size 6 x 1 and matrices of size 6 x 6]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>53</td>
<td>NBodyMod</td>
<td><blockquote>
<p>1 NBodyMod - Body coupling model {1: include coupling terms between each body and NBody in HydroDyn equals NBODY in WAMIT, 2: neglect coupling terms between each body and NBODY=1 with XBODY=0 in WAMIT, 3: Neglect coupling terms between each body and NBODY=1 with XBODY=/0 in WAMIT} (switch) [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>61</td>
<td>NumBStC</td>
<td><blockquote>
<p>0 NumBStC - Number of blade structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>62</td>
<td>BStCfiles</td>
<td><blockquote>
<p>"unused" BStCfiles - Name of the files for blade structural controllers (quoted strings) [unused when NumBStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>63</td>
<td>NumNStC</td>
<td><blockquote>
<p>0 NumNStC - Number of nacelle structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>64</td>
<td>NStCfiles</td>
<td><blockquote>
<p>"unused" NStCfiles - Name of the files for nacelle structural controllers (quoted strings) [unused when NumNStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>65</td>
<td>NumTStC</td>
<td><blockquote>
<p>0 NumTStC - Number of tower structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>66</td>
<td>TStCfiles</td>
<td><blockquote>
<p>"unused" TStCfiles - Name of the files for tower structural controllers (quoted strings) [unused when NumTStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>67</td>
<td>NumSStC</td>
<td><blockquote>
<p>0 NumSStC - Number of substructure structural controllers (integer)</p>
</blockquote></td>
</tr>
<tr>
<td>ServoDyn</td>
<td>68</td>
<td>SStCfiles</td>
<td><blockquote>
<p>"unused" SStCfiles - Name of the files for substructure structural controllers (quoted strings) [unused when NumSStC==0]</p>
</blockquote></td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>12*</td>
<td>alphaUpper</td>
<td><blockquote>
<p>5.0 alphaUpper ! Angle of attack at upper boundary of fully-attached region. (deg) [used only when UAMod=5] ! THIS IS AN OPTIONAL LINE; if omitted, it will be calculated from the polar data</p>
</blockquote></td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>13*</td>
<td>alphaLower</td>
<td><blockquote>
<p>-3.0 alphaLower ! Angle of attack at lower boundary of fully-attached region. (deg) [used only when UAMod=5] ! THIS IS AN OPTIONAL LINE; if omitted, it will be calculated from the polar data</p>
</blockquote></td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>42*</td>
<td>UACutout_delta</td>
<td><blockquote>
<p>"DEFAULT" UACutout_delta ! Delta angle of attack below UACutout where unsteady aerodynamics begin to turn off (blend with steady solution) (deg) [Specifying the string "Default" sets UACutout_delta to 5 degrees] ! THIS IS AN OPTIONAL LINE; if omitted, it will be set to its default value</p>
</blockquote></td>
</tr>
</tbody>
</table>

\*non-comment line count, excluding lines contained if NumCoords is not 0, and including all OPTIONAL lines in the UA coefficients table.

<table>
<thead>
<tr>
<th>Modified in OpenFAST v2.6.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-------</th>
<th>----------------</th>
<th>------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>AeroDyn 15</td>
<td>9</td>
<td>TwrShadow</td>
<td><blockquote>
<p>0 TwrShadow - Calculate tower influence on wind based on downstream tower shadow (switch) {0=none, 1=Powles model, 2=Eames model}</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>26</td>
<td>Joints</td>
<td><blockquote>
<p>JointID JointXss JointYss JointZss JointType JointDirX JointDirY JointDirZ JointStiff</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>27</td>
<td>Joints</td>
<td><blockquote>
<p>(-) (m) (m) (m) (-) (-) (-) (-) (Nm/rad)</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>Members</td>
<td><blockquote>
<p>MemberID MJointID1 MJointID2 MPropSetID1 MPropSetID2 MType COSMID</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>Members</td>
<td><blockquote>
<p>(-) (-) (-) (-) (-) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>ConcentratedM</td>
<td><blockquote>
<p>CMJointID JMass JMXX JMYY JMZZ JMXY JMXZ JMYZ MCGX MCGY MCGZ</p>
</blockquote></td>
</tr>
<tr>
<td>SubDyn</td>
<td>na</td>
<td>ConcentratedM</td>
<td><blockquote>
<p>(-) (kg) (kg*m^2) (kg*m^2) (kg*m^2) (kg*m^2) (kg*m^2) (kg*m^2) (m) (m) (m)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>48</td>
<td>ExtnMod</td>
<td><blockquote>
<p>1 ExctnMod - Wave-excitation model {0: no wave-excitation calculation, 1: DFT, 2: state-space} (switch) [only used when PotMod=1; STATE-SPACE REQUIRES *.ssexctn INPUT FILE]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>49</td>
<td>RdtnMod</td>
<td><blockquote>
<p>2 RdtnMod - Radiation memory-effect model {0: no memory-effect calculation, 1: convolution, 2: state-space} (switch) [only used when PotMod=1; STATE-SPACE REQUIRES *.ss INPUT FILE]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>50</td>
<td>RdtnTMax</td>
<td><blockquote>
<p>60 RdtnTMax - Analysis time for wave radiation kernel calculations (sec) [only used when PotMod=1 and RdtnMod&gt;0; determines RdtnDOmega=Pi/RdtnTMax in the cosine transform; MAKE SURE THIS IS LONG ENOUGH FOR THE RADIATION IMPULSE RESPONSE FUNCTIONS TO DECAY TO NEAR-ZERO FOR THE GIVEN PLATFORM!]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>51</td>
<td>RdtnDT</td>
<td>0.0125 RdtnDT - Time step for wave radiation kernel calculations (sec) [only used when PotMod=1 and ExctnMod&gt;0 or RdtnMod&gt;0; DT&lt;=RdtnDT&lt;=0.1 recommended; determines RdtnOmegaMax=Pi/RdtnDT in the cosine transform]</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>54</td>
<td>PotFile</td>
<td>"Barge" PotFile - Root name of potential-flow model data; WAMIT output files containing the linear, nondimensionalized, hydrostatic restoring matrix (.hst), frequency-dependent hydrodynamic added mass matrix and damping matrix (.1), and frequency- and direction-dependent wave excitation force vector per unit wave amplitude (.3) (quoted string) [1 to NBody if NBodyMod&gt;1] [MAKE SURE THE FREQUENCIES INHERENT IN THESE WAMIT FILES SPAN THE PHYSICALLY-SIGNIFICANT RANGE OF FREQUENCIES FOR THE GIVEN PLATFORM; THEY MUST CONTAIN THE ZERO- AND INFINITE-FREQUENCY LIMITS!]</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>55</td>
<td>WAMITULEN</td>
<td><blockquote>
<p>1 WAMITULEN - Characteristic body length scale used to redimensionalize WAMIT output (meters) [1 to NBody if NBodyMod&gt;1] [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>56</td>
<td>PtfmRefxt</td>
<td><blockquote>
<p>0.0 PtfmRefxt - The xt offset of the body reference point(s) from (0,0,0) (meters) [1 to NBody] [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>57</td>
<td>PtfmRefyt</td>
<td><blockquote>
<p>0.0 PtfmRefyt - The yt offset of the body reference point(s) from (0,0,0) (meters) [1 to NBody] [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>58</td>
<td>PtfmRefzt</td>
<td><blockquote>
<p>0.0 PtfmRefzt - The zt offset of the body reference point(s) from (0,0,0) (meters) [1 to NBody] [only used when PotMod=1. If NBodyMod=2,PtfmRefzt=0.0]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>59</td>
<td>PtfmRefztRot</td>
<td><blockquote>
<p>0.0 PtfmRefztRot - The rotation about zt of the body reference frame(s) from xt/yt (degrees) [1 to NBody] [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>60</td>
<td>PtfmVol0</td>
<td><blockquote>
<p>6000 PtfmVol0 - Displaced volume of water when the body is in its undisplaced position (m^3) [1 to NBody] [only used when PotMod=1; USE THE SAME VALUE COMPUTED BY WAMIT AS OUTPUT IN THE .OUT FILE!]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>61</td>
<td>PtfmCOBxt</td>
<td><blockquote>
<p>0.0 PtfmCOBxt - The xt offset of the center of buoyancy (COB) from (0,0) (meters) [1 to NBody] [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>62</td>
<td>PtfmCOByt</td>
<td><blockquote>
<p>0.0 PtfmCOByt - The yt offset of the center of buoyancy (COB) from (0,0) (meters) [1 to NBody] [only used when PotMod=1]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>69-74</td>
<td>AddF0</td>
<td><blockquote>
<p>0 AddF0 - Additional preload (N, N-m) [If NBodyMod=1, one size 6*NBody x 1 vector; if NBodyMod&gt;1, NBody size 6 x 1 vectors]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>75-80</td>
<td>AddCLin</td>
<td><blockquote>
<p>0 0 0 0 0 0 AddCLin - Additional linear stiffness (N/m, N/rad, N-m/m, N-m/rad) [If NBodyMod=1, one size 6*NBody x 6*NBody matrix; if NBodyMod&gt;1, NBody size 6 x 6 matrices]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>81-86</td>
<td>AddBLin</td>
<td><blockquote>
<p>0 0 0 0 0 0 AddBLin - Additional linear damping(N/(m/s), N/(rad/s), N-m/(m/s), N-m/(rad/s)) [If NBodyMod=1, one size 6*NBody x 6*NBody matrix; if NBodyMod&gt;1, NBody size 6 x 6 matrices]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>87-92</td>
<td>AddBQuad</td>
<td><blockquote>
<p>0 0 0 0 0 0 AddBQuad - Additional quadratic drag(N/(m/s)^2, N/(rad/s)^2, N-m(m/s)^2, N-m/(rad/s)^2) [If NBodyMod=1, one size 6*NBody x 6*NBody matrix; if NBodyMod&gt;1, NBody size 6 x 6 matrices]</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td>Simple Coef Tab</td>
<td><blockquote>
<p>SimplCd SimplCdMG SimplCa SimplCaMG SimplCp SimplCpMG SimplAxCa SimplAxCaMG SimplAxCa SimplAxCaMG SimplAxCp SimplAxCpMG</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td></td>
<td><blockquote>
<p>(-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td>Depth Coef Tab</td>
<td><blockquote>
<p>Dpth DpthCd DpthCdMG DpthCa DpthCaMG DpthCp DpthCpMG DpthAxCa DpthAxCaMG DpthAxCa DpthAxCaMG DpthAxCp DpthAxCpMG</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td></td>
<td><blockquote>
<ol start="13" type="a">
<li>(-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-)</li>
</ol>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td>Member Coef Tab</td>
<td><blockquote>
<p>MemberID MemberCd1 MemberCd2 MemberCdMG1 MemberCdMG2 MemberCa1 MemberCa2 MemberCaMG1 MemberCaMG2 MemberCp1 MemberCp2 MemberCpMG1 MemberCpMG2 MemberAxCd1 MemberAxCd2 MemberAxCdMG1 MemberAxCdMG2 MemberAxCa1 MemberAxCa2 MemberAxCaMG1 MemberAxCaMG2 MemberAxCp1 MemberAxCp2 MemberAxCpMG1 MemberAxCpMG2</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td></td>
<td><blockquote>
<p>(-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>na</td>
<td>OutList names</td>
<td><blockquote>
<p><em>see OutlistParameters.xlsx for new and revised output channel names</em></p>
</blockquote></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Removed in OpenFAST v2.6.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>HydroDyn</td>
<td>68</td>
<td>na</td>
<td>---------------------- FLOATING PLATFORM FORCE FLAGS -------------------------- [unused with WaveMod=6]</td>
</tr>
<tr>
<td>HydroDyn</td>
<td>69</td>
<td>PtfmSgF</td>
<td><blockquote>
<p>True PtfmSgF - Platform horizontal surge translation force (flag) or DEFAULT</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>70</td>
<td>PtfmSwF</td>
<td><blockquote>
<p>True PtfmSwF - Platform horizontal sway translation force (flag) or DEFAULT</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>71</td>
<td>PtfmHvF</td>
<td><blockquote>
<p>True PtfmHvF - Platform vertical heave translation force (flag) or DEFAULT</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>72</td>
<td>PtfmRF</td>
<td><blockquote>
<p>True PtfmRF - Platform roll tilt rotation force (flag) or DEFAULT</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>73</td>
<td>PtfmPF</td>
<td><blockquote>
<p>True PtfmPF - Platform pitch tilt rotation force (flag) or DEFAULT</p>
</blockquote></td>
</tr>
<tr>
<td>HydroDyn</td>
<td>74</td>
<td>PtfmYF</td>
<td><blockquote>
<p>True PtfmYF - Platform yaw rotation force (flag) or DEFAULT</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v2.4.0 to OpenFAST v2.5.0

- InflowWind
  - The input file parser is updated to a keyword/value pair based input. Each entry must have a corresponding keyword with the same spelling as expected. See `input_file_overview` for an overview.
  - Driver code includes ability to convert between wind types

<table>
<thead>
<tr>
<th>Added in OpenFA</th>
<th>ST v2</th>
<th>.5.0</th>
<th></th>
</tr>
<tr>
<th>---------------</th>
<th>-----</th>
<th>-------------------</th>
<th>-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>IfW driver</td>
<td>6</td>
<td>[separator line]</td>
<td>===================== File Conversion Options =================================</td>
</tr>
<tr>
<td>IfW driver</td>
<td>7</td>
<td>WrHAWC</td>
<td><blockquote>
<p>false WrHAWC - Convert all data to HAWC2 format? (flag)</p>
</blockquote></td>
</tr>
<tr>
<td>IfW driver</td>
<td>8</td>
<td>WrBladed</td>
<td><blockquote>
<p>false WrBladed - Convert all data to Bladed format? (flag)</p>
</blockquote></td>
</tr>
<tr>
<td>IfW driver</td>
<td>9</td>
<td>WrVTK</td>
<td><blockquote>
<p>false WrVTK - Convert all data to VTK format? (flag)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td>7</td>
<td>VFlowAng</td>
<td><blockquote>
<p>0 VFlowAng - Upflow angle (degrees) (not used for native Bladed format WindType=7)</p>
</blockquote></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Modified in OpenFAST v2.5.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>-----------------------------</th>
<th>-------</th>
<th>-------------------------------------------------</th>
<th>------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name / section</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>MoorDyn</td>
<td><blockquote>
<p>na</p>
</blockquote></td>
<td><blockquote>
<p>added CtrlChan column in LINE PROPERTIES table</p>
</blockquote></td>
<td></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Renamed in Open</th>
<th>FAST v2</th>
<th>.5.0</th>
<th></th>
<th></th>
</tr>
<tr>
<th>---------------</th>
<th>-------</th>
<th>----------------</th>
<th>---------------</th>
<th>-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Previous Name</th>
<th>New Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>17</p>
</blockquote></td>
<td>Filename</td>
<td><blockquote>
<p>FileName_Uni</p>
</blockquote></td>
<td><blockquote>
<p>"Shr11_30.wnd" FileName_Uni - Filename of time series data for uniform wind field. (-)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>18</p>
</blockquote></td>
<td>RefHt</td>
<td><blockquote>
<p>RefHt_Uni</p>
</blockquote></td>
<td><blockquote>
<p>90 RefHt_Uni - Reference height for horizontal wind speed (m)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>21</p>
</blockquote></td>
<td>Filename</td>
<td><blockquote>
<p>FileName_BTS</p>
</blockquote></td>
<td><blockquote>
<p>"unused" FileName_BTS - Name of the Full field wind file to use (.bts) (-)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>23</p>
</blockquote></td>
<td>Filename</td>
<td><blockquote>
<p>FileNameRoot</p>
</blockquote></td>
<td><blockquote>
<p>"unused" FileNameRoot - WindType=4: Rootname of the full-field wind file to use (.wnd, .sum); WindType=7: name of the intermediate file with wind scaling values</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>35</p>
</blockquote></td>
<td>RefHt</td>
<td><blockquote>
<p>RefHt_Hawc</p>
</blockquote></td>
<td><blockquote>
<p>90 RefHt_Hawc - reference height; the height (in meters) of the vertical center of the grid (m)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>47</p>
</blockquote></td>
<td>PLExp</td>
<td><blockquote>
<p>PLExp_Hawc</p>
</blockquote></td>
<td><blockquote>
<p>0.2 PLExp_Hawc - Power law exponent (-) (used for PL wind profile type only)</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td><blockquote>
<p>49</p>
</blockquote></td>
<td>InitPosition(x)</td>
<td><blockquote>
<p>XOffset</p>
</blockquote></td>
<td><blockquote>
<p>0 XOffset - Initial offset in +x direction (shift of wind box)</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v2.3.0 to OpenFAST v2.4.0

Additional nodal output channels added for `AeroDyn<AD-Nodal-Outputs>`, `BeamDyn<BD-Nodal-Outputs>`, and `ElastoDyn<ED-Nodal-Outputs>`.

<table>
<thead>
<tr>
<th>Added in OpenFA</th>
<th>ST v2</th>
<th>.4.0</th>
<th></th>
</tr>
<tr>
<th>---------------</th>
<th>-----</th>
<th>-------------------</th>
<th>-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>HydroDyn</td>
<td>53</td>
<td>ExctnMod</td>
<td><blockquote>
<p>0 ExctnMod - Wave Excitation model {0: None, 1: DFT, 2: state-space} (-)</p>
</blockquote></td>
</tr>
<tr>
<td>OpenFAST</td>
<td>44</td>
<td>CalcSteady</td>
<td>true CalcSteady - Calculate a steady-state periodic operating point before linearization? [unused if Linearize=False] (flag)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>45</td>
<td>TrimCase</td>
<td><blockquote>
<p>3 TrimCase - Controller parameter to be trimmed {1:yaw; 2:torque; 3:pitch} [used only if CalcSteady=True] (-)</p>
</blockquote></td>
</tr>
<tr>
<td>OpenFAST</td>
<td>46</td>
<td>TrimTol</td>
<td>0.0001 TrimTol - Tolerance for the rotational speed convergence [used only if CalcSteady=True] (-)</td>
</tr>
<tr>
<td>OpenFAST</td>
<td>47</td>
<td>TrimGain</td>
<td><blockquote>
<p>0.001 TrimGain - Proportional gain for the rotational speed error (&gt;0) [used only if CalcSteady=True] (rad/(rad/s) for yaw or pitch; Nm/(rad/s) for torque)</p>
</blockquote></td>
</tr>
<tr>
<td>OpenFAST</td>
<td>48</td>
<td>Twr_Kdmp</td>
<td><blockquote>
<p>0 Twr_Kdmp - Damping factor for the tower [used only if CalcSteady=True] (N/(m/s))</p>
</blockquote></td>
</tr>
<tr>
<td>OpenFAST</td>
<td>49</td>
<td>Bld_Kdmp</td>
<td><blockquote>
<p>0 Bld_Kdmp - Damping factor for the blades [used only if CalcSteady=True] (N/(m/s))</p>
</blockquote></td>
</tr>
<tr>
<td>InflowWind</td>
<td>48</td>
<td>InitPosition(x)</td>
<td><blockquote>
<p>0.0 InitPosition(x) - Initial offset in +x direction (shift of wind box) [Only used with WindType = 5] (m)</p>
</blockquote></td>
</tr>
<tr>
<td>AeroDyn</td>
<td>13</td>
<td>CompAA</td>
<td>False CompAA - Flag to compute AeroAcoustics calculation [only used when WakeMod=1 or 2]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>14</td>
<td>AA_InputFile</td>
<td>"unused" AA_InputFile - Aeroacoustics input file</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>35</td>
<td>[separator line]</td>
<td>====== OLAF cOnvecting LAgrangian Filaments (Free Vortex Wake) Theory Options ================== [used only when WakeMod=3]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>36</td>
<td>OLAFInputFileName</td>
<td>"Elliptic_OLAF.dat" OLAFInputFileName - Input file for OLAF [used only when WakeMod=3]</td>
</tr>
<tr>
<td>AirFoilTables</td>
<td>4*</td>
<td>BL_file</td>
<td>"unused" BL_file - The file name including the boundary layer characteristics of the profile. Ignored if the aeroacoustic module is not called.</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Modified in Ope</th>
<th>nFAST</th>
<th>v2.4.0</th>
<th></th>
<th></th>
</tr>
<tr>
<th>---------------</th>
<th>-----</th>
<th>-------------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------</th>
<th>-------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>New Flag Name</th>
<th>Example Value</th>
<th>Previous Flag Name/Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>AirFoilTables</td>
<td>40*</td>
<td>filtCutOff</td>
<td>"DEFAULT" filtCutOff - Reduced frequency cut-off for low-pass filtering the AoA input to UA, as well as the 1st and 2nd deriv (-) [default = 0.5]</td>
<td><blockquote>
<p>[default = 20]</p>
</blockquote></td>
</tr>
</tbody>
</table>

\*non-comment line count, excluding lines contained if NumCoords is not 0.

## OpenFAST v2.2.0 to OpenFAST v2.3.0

| Removed in OpenFAST v2.3.0 |  |  |  |
|----|----|----|----|
| ---------------------------------------------- | ----- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| AeroDyn Airfoil Input File - Airfoil Tables | 2 | Ctrl | 0 Ctrl ! Control setting (must be 0 for current AirfoilInfo) |

<table>
<thead>
<tr>
<th>Added in OpenFAST v2.3.0</th>
<th></th>
<th></th>
<th></th>
</tr>
<tr>
<th>----------------------------------------------</th>
<th>-----</th>
<th>----------------</th>
<th>--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>AeroDyn Airfoil Input File - Airfoil Tables</td>
<td>2</td>
<td>UserProp</td>
<td><blockquote>
<p>0 UserProp ! User property (control) setting</p>
</blockquote></td>
</tr>
<tr>
<td>AeroDyn</td>
<td>37</td>
<td>AFTabMod</td>
<td><blockquote>
<p>1 AFTabMod - Interpolation method for multiple airfoil tables {1=1D interpolation on AoA (first table only); 2=2D interpolation on AoA and Re; 3=2D interpolation on AoA and UserProp} (-)</p>
</blockquote></td>
</tr>
</tbody>
</table>

## OpenFAST v2.1.0 to OpenFAST v2.2.0

No changes required.

## OpenFAST v2.0.0 to OpenFAST v2.1.0

| Added in OpenF | AST v | 2.1.0 |  |
|----|----|----|----|
| --------------- | ----- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| BeamDyn driver | 21 | GlbRotBladeT0 | True GlbRotBladeT0 - Reference orientation for BeamDyn calculations is aligned with initial blade root? |

## OpenFAST v1.0.0 to OpenFAST v2.0.0

<table>
<thead>
<tr>
<th>Removed in</th>
<th>Open</th>
<th>FAST v2.0.0</th>
<th></th>
</tr>
<tr>
<th>----------</th>
<th>-----</th>
<th>-------------------</th>
<th>---------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>BeamDyn</td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td>analysis_type</td>
<td>analysis_type - 1: Static analysis; 2: Dynamic analysis</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Added in O</th>
<th>penFA</th>
<th>ST v2.0.0</th>
<th></th>
</tr>
<tr>
<th>----------</th>
<th>-----</th>
<th>-------------------</th>
<th>---------------------------------------------------------------------------------------------------------------------------------------------------------------------</th>
</tr>
<tr>
<th>Module</th>
<th>Line</th>
<th>Flag Name</th>
<th>Example Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>AeroDyn</td>
<td>22</td>
<td>SkewModFactor</td>
<td>"default" SkewModFactor - Constant used in Pitt/Peters skewed wake model {or "default" is 15/32*pi} (-) [used only when SkewMod=2; unused when WakeMod=0]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>30</td>
<td>Section header</td>
<td>====== Dynamic Blade-Element/Momentum Theory Options ============================================== [used only when WakeMod=2]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>31</td>
<td>DBEMT_Mod</td>
<td>2 DBEMT_Mod - Type of dynamic BEMT (DBEMT) model {1=constant tau1, 2=time-dependent tau1} (-) [used only when WakeMod=2]</td>
</tr>
<tr>
<td>AeroDyn</td>
<td>32</td>
<td>tau1_const</td>
<td>4 tau1_const - Time constant for DBEMT (s) [used only when WakeMod=2 and DBEMT_Mod=1]</td>
</tr>
<tr>
<td>BeamDyn</td>
<td><blockquote>
<p>5</p>
</blockquote></td>
<td>QuasiStaticInit</td>
<td>True QuasiStaticInit - Use quasi-static pre-conditioning with centripetal accelerations in initialization (flag) [dynamic solve only]</td>
</tr>
<tr>
<td>BeamDyn</td>
<td>11</td>
<td>load_retries</td>
<td>DEFAULT load_retries - Number of factored load retries before quitting the simulation</td>
</tr>
<tr>
<td>BeamDyn</td>
<td>14</td>
<td>tngt_stf_fd</td>
<td>DEFAULT tngt_stf_fd - Flag to use finite differenced tangent stiffness matrix (-)</td>
</tr>
<tr>
<td>BeamDyn</td>
<td>15</td>
<td>tngt_stf_comp</td>
<td>DEFAULT tngt_stf_comp - Flag to compare analytical finite differenced tangent stiffness matrix (-)</td>
</tr>
<tr>
<td>BeamDyn</td>
<td>16</td>
<td>tngt_stf_pert</td>
<td>DEFAULT tngt_stf_pert - perturbation size for finite differencing (-)</td>
</tr>
<tr>
<td>BeamDyn</td>
<td>17</td>
<td>tngt_stf_difftol</td>
<td>DEFAULT tngt_stf_difftol - Maximum allowable relative difference between analytical and fd tangent stiffness (-)</td>
</tr>
<tr>
<td>BeamDyn</td>
<td>18</td>
<td>RotStates</td>
<td>True RotStates - Orient states in the rotating frame during linearization? (flag) [used only when linearizing]</td>
</tr>
</tbody>
</table>

## FAST v8.16 to OpenFAST v1.0.0

The transition from FAST v8 to OpenFAST is described in detail at `fast_to_openfast`.

| Removed in | OpenF | AST v1.0.0 |  |
|----|----|----|----|
| ----------- | ----- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| OpenFAST | 18 | CompSub | 0 CompSub - Compute sub-structural dynamics (switch) {0=None; 1=SubDyn} |

| Added in Op | enFAS | T v1.0.0 |  |
|----|----|----|----|
| ----------- | ----- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| Module | Line | Flag Name | Example Value |
| OpenFAST | 18 | CompSub | 0 CompSub - Compute sub-structural dynamics (switch) {0=None; 1=SubDyn; 2=External Platform MCKF} |
| AeroDyn | 12 | CavityCheck | False CavitCheck - Perform cavitation check? (flag) |
| AeroDyn | 17 | Patm | 9999.9 Patm - Atmospheric pressure (Pa) \[used only when CavitCheck=True\] |
| AeroDyn | 18 | Pvap | 9999.9 Pvap - Vapor pressure of fluid (Pa) \[used only when CavitCheck=True\] |
| AeroDyn | 19 | FluidDepth | 9999.9 FluidDepth - Water depth above mid-hub height (m) \[used only when CavitCheck=True\] |
