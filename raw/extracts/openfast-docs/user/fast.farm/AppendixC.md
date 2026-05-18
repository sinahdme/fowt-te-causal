# List of Output Channels

This is a list of all possible output parameters available within FAST.Farm (except those that are available from OpenFAST, which are specified within the OpenFAST input file(s) and output separately for each turbine). The names are grouped by meaning, but can be ordered in the OUTPUTS section of the FAST.Farm primary input file as you see fit.

T$`\alpha`$ refers to turbine $`\alpha`$, where $`\alpha`$ is a one-digit number in the range \[1,9\], corresponding to row $`\alpha`$ in the wind turbine input table. If **NumTurbines** \> 9, only values for the first 9 turbines can be output. Setting $`\alpha`$ \> **NumTurbines** yields invalid output.

N$`\beta`$ refers to radial output node $`\beta`$, where $`\beta`$ is a two-digit number in the range \[01,20\], corresponding to entry $`\beta`$ in the **OutRadii** list, where node $`\beta`$ is at radius **dr** $`\times`$ **OutRadii**\[$`\beta`$\]. Setting $`\beta`$ \> **NOutRadii** yields invalid output.

W$`\eta`$ refers to wind point $`\eta`$, where $`\eta`$ is a one-digit number in the range \[1,9\], corresponding to entry $`\eta`$in the **WindVelX**, **WindVelY**, and **WindVelZ** lists. Setting $`\eta`$ \> **NWindVel** yields invalid output. Setting **WindVelX**, **WindVelY**, and **WindVelZ** outside the low-resolution wind domain also yields invalid output.

$`\delta`$ refers to the X, Y, or Z coordinate axis.

D$`\gamma`$ refers to downstream distance $`\gamma`$, where $`\gamma`$ is a one-digit number in the range \[1,9\], corresponding to entry $`\gamma`$ in the **OutDist** list. Setting $`\gamma`$ \> **NOutDist** yields invalid output. The output is also invalid if **OutDist** is a distance further downstream than the wake has been calculated or for any distance where the wake from the turbine has overlapped itself.

<div id="Tab:FF:Outputs" class="container">

<table style="width:99%;">
<caption>List of Available FAST.Farm Output Channels</caption>
<colgroup>
<col style="width: 47%" />
<col style="width: 14%" />
<col style="width: 37%" />
</colgroup>
<thead>
<tr>
<th>Channel Name</th>
<th>Units</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3"><em>Wind Turbine and Inflow</em></td>
</tr>
<tr>
<td>RtAxs<span class="math inline"><em>δ</em></span>T<span class="math inline"><em>α</em></span></td>
<td>(-)</td>
<td>Orientation of the rotor centerline for turbine <span class="math inline"><em>α</em></span> in the global coordinate system</td>
</tr>
<tr>
<td>RtPos<span class="math inline"><em>δ</em></span>T<span class="math inline"><em>α</em></span></td>
<td>(m)</td>
<td>Position of the rotor (hub) center for turbine <span class="math inline"><em>α</em></span> in the global coordinate system</td>
</tr>
<tr>
<td>RtDiamT<span class="math inline"><em>α</em></span></td>
<td>(m)</td>
<td>Rotor diameter for turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>YawErrT<span class="math inline"><em>α</em></span></td>
<td>(deg)</td>
<td>Nacelle-yaw error for turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>TIAmbT<span class="math inline"><em>α</em></span></td>
<td>(%)</td>
<td>Ambient turbulence intensity of the wind at the the rotor disk for turbine <span class="math inline"><em>α</em></span>. The ambient turbulence intensity is based on a spatial-average of the three vector components, instead of just the axial component.</td>
</tr>
<tr>
<td>RtVAmbT<span class="math inline"><em>α</em></span></td>
<td>(m/s)</td>
<td>Rotor-disk-averaged ambient wind speed (normal to disk, not including structural motion, local induction or wakes from upstream turbines) for turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>RtVAmbFiltT<span class="math inline"><em>α</em></span></td>
<td>(m/s)</td>
<td><dl>
<dt>Time-filtered value of RtVAmbT<span class="math inline"><em>α</em></span></dt>
<dd>
<p>for turbine <span class="math inline"><em>α</em></span></p>
</dd>
</dl></td>
</tr>
<tr>
<td>AxiSkewT<span class="math inline"><em>α</em></span></td>
<td>(deg)</td>
<td><dl>
<dt>Skew azimuth angle (used in curled-wake model)</dt>
<dd>
<p>for turbine <span class="math inline"><em>α</em></span></p>
</dd>
</dl></td>
</tr>
<tr>
<td>AxiSkewFiltT<span class="math inline"><em>α</em></span></td>
<td>(deg)</td>
<td><dl>
<dt>Time-filtered value of AxiSkewT<span class="math inline"><em>α</em></span></dt>
<dd>
<p>for turbine <span class="math inline"><em>α</em></span></p>
</dd>
</dl></td>
</tr>
<tr>
<td>RtSkewT<span class="math inline"><em>α</em></span></td>
<td>(deg)</td>
<td>Skew angle (used in curled-wake model) for turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>RtSkewFiltT<span class="math inline"><em>α</em></span></td>
<td>(deg)</td>
<td><dl>
<dt>Time-filtered value of RtSkewT<span class="math inline"><em>α</em></span></dt>
<dd>
<p>for turbine <span class="math inline"><em>α</em></span></p>
</dd>
</dl></td>
</tr>
<tr>
<td>RtGamCurlT<span class="math inline"><em>α</em></span></td>
<td>(m^2/s)</td>
<td><dl>
<dt>Rotor circulation (used in curled-wake model)</dt>
<dd>
<p>for turbine <span class="math inline"><em>α</em></span></p>
</dd>
</dl></td>
</tr>
<tr>
<td>RtVRelT<span class="math inline"><em>α</em></span></td>
<td>(m/s)</td>
<td>Rotor-disk-averaged relative wind speed (normal to disk, including structural motion and wakes from upstream turbines, but not including local induction) for turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>RtCtAvgT<span class="math inline"><em>α</em></span></td>
<td>(-)</td>
<td><dl>
<dt>Rotor-disk-averaged thrust coefficient</dt>
<dd>
<p>for turbine <span class="math inline"><em>α</em></span></p>
</dd>
</dl></td>
</tr>
<tr>
<td>CtT<span class="math inline"><em>α</em></span>N<span class="math inline"><em>β</em></span></td>
<td>(-)</td>
<td>Azimuthally averaged thrust force coefficient (normal to disk) for radial output node <span class="math inline"><em>β</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td colspan="3"><em>Wake (for an Individual Rotor)</em></td>
</tr>
<tr>
<td>WkAxs<span class="math inline"><em>δ</em></span>T<span class="math inline"><em>α</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(-)</td>
<td>Orientation of the wake centerline for downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span> in the global coordinate system</td>
</tr>
<tr>
<td>WkPos<span class="math inline"><em>δ</em></span>T<span class="math inline"><em>α</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m)</td>
<td>Center position of the wake centerline for downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span> in the global coordinate system</td>
</tr>
<tr>
<td>WkVel<span class="math inline"><em>δ</em></span>T<span class="math inline"><em>α</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m/s)</td>
<td>Advection, deflection, and meandering velocity (not including the horizontal wake-deflection correction or low-pass time-filtering) of the wake for downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span> in the global coordinate system</td>
</tr>
<tr>
<td>WkDiamT<span class="math inline"><em>α</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m)</td>
<td>Wake diameter for downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>WkDfVxT<span class="math inline"><em>α</em></span>N<span class="math inline"><em>β</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m/s)</td>
<td>Axial wake velocity deficits for radial output node <span class="math inline"><em>β</em></span> and downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>WkDfVrT<span class="math inline"><em>α</em></span>N<span class="math inline"><em>β</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m/s)</td>
<td>Radial wake velocity deficits for radial output node <span class="math inline"><em>β</em></span> and downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>EddVisT<span class="math inline"><em>α</em></span>N<span class="math inline"><em>β</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m<span class="math inline"><sup>2</sup></span>/s)</td>
<td>Total eddy viscosity for radial output node <span class="math inline"><em>β</em></span> and downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>EddAmbT<span class="math inline"><em>α</em></span>N<span class="math inline"><em>β</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m<span class="math inline"><sup>2</sup></span>/s)</td>
<td>Individual contribution to the eddy viscosity from ambient turbulence for radial output node <span class="math inline"><em>β</em></span> and downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td>EddShrT<span class="math inline"><em>α</em></span>N<span class="math inline"><em>β</em></span>D<span class="math inline"><em>γ</em></span></td>
<td>(m<span class="math inline"><sup>2</sup></span>/s)</td>
<td>Individual contributions to the eddy viscosity from the shear layer for radial output node <span class="math inline"><em>β</em></span> and downstream distance <span class="math inline"><em>γ</em></span> of turbine <span class="math inline"><em>α</em></span></td>
</tr>
<tr>
<td colspan="3"><em>Ambient Wind and Array Effects</em></td>
</tr>
<tr>
<td>W<span class="math inline"><em>η</em></span>VAmb<span class="math inline"><em>δ</em></span></td>
<td>(m/s)</td>
<td>Ambient wind velocity (not including wakes) for point <span class="math inline"><em>η</em></span> in the global coordinate system (from the low-resolution domain)</td>
</tr>
<tr>
<td>W<span class="math inline"><em>η</em></span>VDis<span class="math inline"><em>δ</em></span></td>
<td>(m/s)</td>
<td>Disturbed wind velocity (including wakes) for point <span class="math inline"><em>η</em></span> in the global coordinate system (from the low-resolution domain)</td>
</tr>
</tbody>
</table>

</div>
