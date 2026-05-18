# General

<div class="toctree" maxdepth="1">

fast_to_openfast.rst api_change.rst input_file_overview.rst

</div>

Workshop material, legacy documentation, and other resources are listed below.

- [Overview of OpenFAST at NAWEA WindTech 2023](https://forums.nrel.gov/t/modeling-workshops/523/27)
- [Overview of OpenFAST at NAWEA WindTech 2022](https://drive.google.com/file/d/1bD5a6rRg6cCKht9Ar8AFJQ8YrI4-wsFe/view)
- [Practical Guide to OpenFAST at NAWEA WindTech 2022](https://drive.google.com/file/d/1FHovo6btDStPBh1Kv2swA09hIQRcZGZf/view)
- [Overview of OpenFAST at NAWEA WindTech 2019](https://drive.google.com/file/d/1wagMTOV_CLxSKzS2EEPFp2CExUo3JLpQ/view)
- [Workshop Presentations](https://drive.google.com/drive/folders/1BDDfcnIyvmZCwf7eFo0ISI7aF_FMAOvt)
- `Old FAST v6 User's Guide <../../OtherSupporting/Old_FAST6_UsersGuide.pdf>`
- `FAST v8 README <../../OtherSupporting/FAST8_README.pdf>`
- [Implementation of Substructure Flexibility and Member-Level Load Capabilities for Floating Offshore Wind Turbines in OpenFAST](https://www.nrel.gov/docs/fy20osti/76822.pdf)
- [FAST modularization framework for wind turbine simulation: full-system linearization](https://www.nrel.gov/docs/fy17osti/67015.pdf)
- [Full-System Linearization for Floating Offshore Wind Turbines in OpenFAST](https://www.nrel.gov/docs/fy19osti/71865.pdf)
- `FAST with Labview <../../OtherSupporting/UsingFAST4Labview.pdf>`
- `OutListParameters.xlsx <../../OtherSupporting/OutListParameters.xlsx>` - Contains the full list of outputs for each module.

## Modularization Framework

Information specific to the modularization framework of OpenFAST is provided here. These are a collection of publications, presentations, and past studies on the subject.

- [The New Modularization Framework for the FAST Wind Turbine CAE Tool](https://www.nrel.gov/docs/fy13osti/57228.pdf)
- `Example Module Implementation Plans <../../OtherSupporting/ModulePlan_GasmiPaperExamples.doc>`
- `Module and Mesh-Mapping Linearization Implementation Plan <../../OtherSupporting/LinearizationOfMeshMapping_Rev18_Rev2.doc>`
- `Interpolation of DCMs <../../OtherSupporting/DCM_Interpolation/DCM_Interpolation.pdf>` - A summary of the mathematics used in the interpolation of DCM (direction cosine matrices) using logarithmic mapping and matrix exponentials.
- `Set-point Linearization Development Plan <../../OtherSupporting/DevelopmentPlan-SetPoint-Linearization.pdf>`
- `OpenFAST Tight-Coupling Solver <../../OtherSupporting/TightCoupling_Rev4.doc>`

## Glue Code and Mesh Mapping

For current documentation on the glue code structure, module variable API, solver, and linearization see `glue-code`.

- [FAST Modular Wind Turbine CAE Tool: Nonmatching Spatial and Temporal Meshes](https://www.nrel.gov/docs/fy14osti/60742.pdf)
- [FAST Modular Framework for Wind Turbine Simulation: New Algorithms and Numerical Examples](https://dx.doi.org/10.2514/6.2015-1461)
- `Predictor-Corrector Approach <../../OtherSupporting/ProposedPCApproach_Rev4.docx>`
