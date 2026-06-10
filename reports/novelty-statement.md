# Paper novelty statement (draft)
*2026-06-10. Strong version is contingent on the operating-point sweep (8/11/15/20 m/s) confirming the controller-firewall. Fill bracketed clauses + Granger/TE % from final results.*

---

## Strong version (firewall holds)

The contribution of this work is not the application of transfer entropy to a floating
offshore wind turbine (FOWT) *per se*, but what directed-information analysis reveals
about the role of the control system in shaping environment-to-structure load dynamics.
We show that the directed coupling from environmental excitation to structural response
is **operating-point dependent and controller-mediated**: below rated wind speed, where
blade pitch is largely passive, wind fluctuations transfer information to [**confirm which
responses: tower-base bending, mooring tension, surge**]; at and above rated, where the
pitch controller actively regulates rotor thrust, this wind to structure transfer is
[**suppressed / strongly reduced**] — the controller acts as a causal "firewall." To our
knowledge, this is the first information-theoretic characterization of how the control
regime reorganizes the causal structure of FOWT loads. Crucially, this finding could not
be obtained with conventional linear tools: magnitude-squared coherence is undirected,
and conditional Granger causality over-detects in the strongly correlated wind-wave field
[**Granger flagged X% of edges significant vs Y% for KSG-TE**]; only nonlinear, directed,
*conditional* transfer entropy disentangles wind from correlated wave forcing and resolves
the directional, controller-dependent pathway. The directed-coupling graph is complemented
by a global parameter-sensitivity analysis (Sobol indices on a frequency-domain design
ensemble), yielding a unified causal picture of how both stochastic excitation and design
parameters drive FOWT response.

### Clauses that depend on the sweep
- "suppressed at/above rated" -> needs 15/20 m/s.
- "wind transfers below rated" -> needs 8 m/s n_selected_from_source + 11 m/s conditional.
- Granger X% vs TE Y% -> fill from final sweep.

---

## Fallback version (firewall does NOT hold cleanly)

The contribution is a rigorous, baseline-anchored information-theoretic characterization of
environment-to-structure causal coupling in a FOWT, showing that the response is
wave-dominated and that **wind to structure directed transfer is intrinsically weak across
operating conditions** — a non-obvious result given wind's role as the primary energy input.
We demonstrate that *conditional* transfer entropy is required to separate wind from
correlated wave forcing, that linear directed-causality (Granger) systematically
over-detects in this setting, and that a data-driven embedding heuristic effective for
self-information (AIS) fails for directed transfer — methodological cautions relevant to
anyone applying these tools to coupled offshore-loading data.

---

*Strong = journal-tier (firewall is a finding). Fallback = honest mid-tier (careful
application + methods cautions). The operating-point sweep decides which.*
*Framing rule: lead with the turbine-physics finding, not the entropy method.*
