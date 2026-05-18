# Appendix D. List of Output Channels

This is a list of all possible output parameters for the SubDyn module. The names are grouped by meaning, but can be ordered in the OUTPUT CHANNELS section of the SubDyn input file as the user sees fit. $`M \alpha N \beta`$, refers to node $`\beta`$ of member $`\alpha`$, where $`\alpha`$ is a number in the range \[1,99\] and corresponds to row $`\alpha`$ in the MEMBER OUTPUT LIST table (see `SD_Member_Output`) and $`\beta`$ is a number in the range \[1,9\] and corresponds to node $`\beta`$ in the **NodeCnt** list of that table entry.

Some outputs are in the SS reference coordinate system (global inertial-frame coordinate system), and end with the suffix <span class="title-ref">ss</span>; others refer to the local (member) reference system and they have suffixes "Xe", "Ye", or "Ze" (see Section 7).

Table C-1. List of Output Channels.

<table style="width:100%;">
<colgroup>
<col style="width: 16%" />
<col style="width: 26%" />
<col style="width: 56%" />
</colgroup>
<thead>
<tr>
<th>Channel Name(s)</th>
<th>Units</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="3"><em>Base and Interface Reaction Loads</em></td>
</tr>
<tr>
<td><p>ReactFXss, ReactFYss, ReactFZss,</p>
<p>ReactMXss, ReactMYss, ReactMZss,</p></td>
<td><p>(N), (N), (N),</p>
<p>(Nm), (Nm), (Nm)</p></td>
<td><p>Total base reaction forces and moments</p>
<p>at the (0.,0.,-<strong>WtrDpth</strong>) location in SS coordinate system</p></td>
</tr>
<tr>
<td><p>Intf?FXss, Intf?FYss, Intf?FZss,</p>
<p>Intf?MXss, Intf?MYss, Intf?MZss,</p></td>
<td><p>(N), (N), (N),</p>
<p>(Nm), (Nm), (Nm)</p></td>
<td>Total interface reaction forces and moments at the TP reference points (platform reference points) in SS coordinate system. ? can be replaced with any number between 1 and 9 to indicate which transition piece to output. Omitting ? defaults to transition piece 1 for backward compatibility.</td>
</tr>
<tr>
<td colspan="3"><em>Interface Kinematics</em></td>
</tr>
<tr>
<td><p>Intf?TDXss, Intf?TDYss, Intf?TDZss,</p>
<p>Intf?RDXss, Intf?RDYss, Intf?RDZss</p></td>
<td><p>(m), (m), (m),</p>
<p>(rad), (rad), (rad)</p></td>
<td>Displacements and rotations of the TP reference points in SS coordinate system. The rotation angles are Tait-Bryan angles following the convention of intrinsic yaw first, pitch second, and roll last. ? can be replaced with any number between 1 and 9 to indicate which transition piece to output. Omitting ? defaults to transition piece 1 for backward compatibility.</td>
</tr>
<tr>
<td><p>Intf?TDXe, Intf?TDYe, Intf?TDZe,</p>
<p>Intf?RDXe, Intf?RDYe, Intf?RDZe</p></td>
<td><p>(m), (m), (m),</p>
<p>(rad), (rad), (rad)</p></td>
<td>Elastic part of the TP reference point displacements and (small angle) rotations in the rigid-body coordinate system. ? can be replaced with any number between 1 and 9 to indicate which transition piece to output. Omitting ? defaults to transition piece 1 for backward compatibility.</td>
</tr>
<tr>
<td><p>Intf?TAXss, Intf?TAYss, Intf?TAZss,</p>
<p>Intf?RAXss, Intf?RAYss, Intf?RAZss</p></td>
<td><p>(<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>),</p>
<p>(<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>)</p></td>
<td>Translational and rotational accelerations of the TP reference points in SS coordinate system. ? can be replaced with any number between 1 and 9 to indicate which transition piece to output. Omitting ? defaults to transition piece 1 for backward compatibility.</td>
</tr>
<tr>
<td colspan="3"><em>Rigid-Body Kinematics (floating only)</em></td>
</tr>
<tr>
<td><p>RBTDXss, RBTDYss, RBTDZss,</p>
<p>RBRDXss, RBRDYss, RBRDZss</p></td>
<td><p>(m), (m), (m),</p>
<p>(rad), (rad), (rad)</p></td>
<td><p>Displacements and rotations of the rigid-body reference point in SS coordinate system.</p>
<p>The rotation angles are Tait-Bryan angles following the convention of intrinsic yaw first, pitch second, and roll last.</p></td>
</tr>
<tr>
<td><p>RBTVXss, RBTVYss, RBTVZss,</p>
<p>RBRVXss, RBRVYss, RBRVZss</p></td>
<td><p>(m/s), (m/s), (m/s),</p>
<p>(rad/s), (rad/s), (rad/s)</p></td>
<td>Translational and rotational velocities of the rigid-body reference point in SS coordinate system.</td>
</tr>
<tr>
<td><p>RBTAXss, RBTAYss, RBTAZss,</p>
<p>RBRAXss, RBRAYss, RBRAZss</p></td>
<td><p>(<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>),</p>
<p>(<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>), (<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>)</p></td>
<td>Translational and rotational accelerations of the rigid-body reference point in SS coordinate system.</td>
</tr>
<tr>
<td colspan="3"><em>Modal Parameters</em></td>
</tr>
<tr>
<td>SSqm01-SSqm99</td>
<td>(-)</td>
<td>C-B modal variables (up to first 99)</td>
</tr>
<tr>
<td>SSqmd01-SSqmd99</td>
<td>(1/s)</td>
<td>First time-derivatives of C-B modal variables (up to first 99)</td>
</tr>
<tr>
<td>SSqmdd01-SSqmdd99</td>
<td>(<span class="math inline">1/<em>s</em><sup>2</sup></span>)</td>
<td>Second time-derivatives of C-B modal variables (up to first 99)</td>
</tr>
<tr>
<td colspan="3"><em>Node Kinematics</em></td>
</tr>
<tr>
<td><p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> TDxss,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> TDyss,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> TDzss,</p></td>
<td>(m)</td>
<td><p>Nodal total translational displacements of <span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span></p>
<p>(up to 81 designated locations) in SS coordinate system</p></td>
</tr>
<tr>
<td><p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> RDxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> RDye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> RDze</p></td>
<td>(rad)</td>
<td><p>Nodal rotational elastic deflection of <span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> relative to the rigid-body configuration</p>
<p>(up to 81 designated locations) in member local coordinate system</p></td>
</tr>
<tr>
<td><p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> TAxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> TAye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> TAze</p></td>
<td>(<span class="math inline"><em>m</em>/<em>s</em><sup>2</sup></span>)</td>
<td><p>Nodal translational accelerations of <span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span></p>
<p>(up to 81 designated locations) in member local coordinate system</p></td>
</tr>
<tr>
<td><p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> RAxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> RAye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> RAze</p></td>
<td>(<span class="math inline"><em>r</em><em>a</em><em>d</em>/<em>s</em><sup>2</sup></span>)</td>
<td><p>Nodal rotational accelerations of <span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span></p>
<p>(up to 81 designated locations) in member local coordinate system</p></td>
</tr>
<tr>
<td colspan="3"><em>Node Forces and Moments</em></td>
</tr>
<tr>
<td><p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> FKxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> FKye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> FKze</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> MKxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> MKye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> MKze</p></td>
<td><p>(N),</p>
<p>(N),</p>
<p>(N),</p>
<p>(Nm),</p>
<p>(Nm),</p>
<p>(Nm)</p></td>
<td><blockquote>
<p>Static (elastic) component of reaction forces and moments</p>
<p>at <span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> along local member coordinate system</p>
</blockquote></td>
</tr>
<tr>
<td><p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> FMxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> FMye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> FMze</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> MMxe,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> MMye,</p>
<p><span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> MMze</p></td>
<td><p>(N),</p>
<p>(N),</p>
<p>(N),</p>
<p>(Nm),</p>
<p>(Nm),</p>
<p>(Nm)</p></td>
<td><blockquote>
<p>Dynamic (inertial) component of reaction forces and moments</p>
<p>at <span class="math inline"><em>M</em><em>α</em><em>N</em><em>β</em></span> along local member coordinate system</p>
</blockquote></td>
</tr>
</tbody>
</table>
