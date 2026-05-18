# Installation and Getting Started

HydroDyn is included in the OpenFAST software repository and consists of two major components:

- <span class="title-ref">hydrodyn_driver</span> is the standalone HydroDyn executable
- <span class="title-ref">hydrodynlib</span> is the OpenFAST module library; it is most commonly used when driven through the HydroDyn driver or the OpenFAST glue code

For installation instructions, see `installation`. In sections where an installation target can be specific, use <span class="title-ref">hydrodyn_driver</span>.

## Running the HydroDyn Driver

The HydroDyn Driver has a simple command line interface:

``` bash
hydrodyn_driver <input_file>
```

where <span class="title-ref">input_file</span> is the file described in `hd-driver-input`. Additional input files are required, including the `hd-primary-input`. The time-series output as well as other output from HydroDyn are described in `hd-output`.

## Running HydroDyn coupled to OpenFAST

To run an OpenFAST simulation with the HydroDyn module enabled, the <span class="title-ref">CompHydro</span> flag must be switched on and the `hd-primary-input` path supplied in the OpenFAST primary input file:

``` 
# In the "Feature switches" section
1               CompHydro   - Compute hydrodynamic loads (switch) {0=None; 1=HydroDyn}

# In the "Input files" section
"HydroDyn.dat"  HydroFile   - Name of file containing hydrodynamic input parameters (quoted string)
```

The time-series output as well as other output from HydroDyn are described in `hd-output`.
