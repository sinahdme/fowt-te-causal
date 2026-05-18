# Versioning

OpenFAST follows [semantic versioning](https://semver.org). In summary, this means that with a version number as MAJOR.MINOR.PATCH, the components will be incremented as follows:

- MAJOR version when introducing incompatible API changes,
- MINOR version when adding functionality in a backwards-compatible manner, and
- PATCH version when making backwards-compatible bug fixes.

For example, `OpenFAST-v1.0.0-123-gabcd1234-dirty` describes OpenFAST as:

<table>
<thead>
<tr>
<th>Version Component</th>
<th>Explanation</th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p>v1.0.0</p>
</blockquote></td>
<td><blockquote>
<p>MAJOR.MINOR.PATCH numbering system; corresponds to a tagged commit made by NREL (now called NLR after 2025) on GitHub</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p>123-g</p>
</blockquote></td>
<td><blockquote>
<p>Number of additional commits after the most recent tag for a build (the <code>-g</code> is for <code>git</code>)</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p>abcd1234</p>
</blockquote></td>
<td><blockquote>
<p>First 8 characters of the current commit hash</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p>dirty</p>
</blockquote></td>
<td><blockquote>
<p>Denotes that local changes have been made but not committed; omitted if there are no local changes</p>
</blockquote></td>
</tr>
</tbody>
</table>
