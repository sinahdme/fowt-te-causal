# C++ API Users Guide

<div class="only">

html

This document offers a quick reference guide for the C++ API and glue code. It is intended to be used by the general user in combination with other OpenFAST manuals. The manual will be updated as new releases are issued and as needed to provide further information on advancements or modifications to the software.

</div>

The C++ API provides a high level API to run OpenFAST through a C++ gluecode. The primary purpose of the C++ API is to help interface OpenFAST to external programs like CFD solvers that are typically written in C++. The installation of C++ API is enabled via CMake by turning on the `BUILD_OPENFAST_CPP_API` flag.

A sample glue-code [FAST_Prog.cpp](https://github.com/OpenFAST/openfast/blob/dev/glue-codes/openfast-cpp/src/FAST_Prog.cpp) is provided as a demonstration of the usage of the C++ API. The glue-code allows for the simulation of multiple turbines using OpenFAST in parallel over multiple processors. The glue-code takes a single input file named `cDriver.i` (`download <files/cDriver.i>`).

<div class="literalinclude" language="yaml">

files/cDriver.i

</div>

## Command line invocation

``` bash
mpiexec -np <N> openfastcpp 
```

## Common input file options

<div class="confval">

n_turbines_glob

Total number of turbines in the simulation. The input file must contain a number of turbine specific sections (<span class="title-ref">Turbine0</span>, <span class="title-ref">Turbine1</span>, ..., <span class="title-ref">Turbine(n-1)</span>) that is consistent with <span class="title-ref">nTurbinesGlob</span>.

</div>

<div class="confval">

debug

Enable debug outputs if set to true

</div>

<div class="confval">

dry_run

The simulation will not run if dryRun is set to true. However, the simulation will read the input files, allocate turbines to processors and prepare to run the individual turbine instances. This flag is useful to test the setup of the simulation before running it.

</div>

<div class="confval">

sim_start

Flag indicating whether the simulation starts from scratch or restart. `sim_start` takes on one of three values:

- `init` - Use this option when starting a simulation from <span class="title-ref">t=0s</span>.
- `trueRestart` - While OpenFAST allows for restart of a turbine simulation, external components like the Bladed style controller may not. Use this option when all components of the simulation are known to restart.
- `restartDriverInitFAST` - When the `restartDriverInitFAST` option is selected, the individual turbine models start from <span class="title-ref">t=0s</span> and run up to the specified restart time using the inflow data stored at the actuator nodes from a hdf5 file. The C++ API stores the inflow data at the actuator nodes in a hdf5 file at every OpenFAST time step and then reads it back when using this restart option. This restart option is especially useful when the glue code is a CFD solver.

</div>

<div class="confval">

coupling_mode

Choice of coupling mode. `coupling_mode` takes one of two values: `strong` or `classic`. `strong` coupling mode uses 2 outer iterations for every driver time step while `classic` coupling mode calls the <span class="title-ref">step()</span> function to use the loose coupling mode.

</div>

<div class="confval">

t_start

Start time of the simulation

</div>

<div class="confval">

t_end

End time of the simulation. t_end \<= t_max

</div>

<div class="confval">

t_max

Max time of the simulation

</div>

<div class="confval">

dt_fast

Time step for FAST. All turbines should have the same time step.

</div>

<div class="confval">

n_substeps

Number of sub-timesteps of OpenFAST per time step of the driver program.

</div>

<div class="confval">

n_checkpoint

Restart files will be written every so many time steps

</div>

<div class="confval">

set_exp_law_wind

Boolean value of True/False. When true, set velocity at the Aerodyn nodes using a power law wind profile using an exponent of 0.2 and a reference wind speed of 10 m/s at 90 meters. This option is useful to test the setup for actuator line simulations in individual mode before running massive CFD simulations.

</div>

## Turbine specific input options

<div class="confval">

turbine_base_pos

The position of the turbine base for actuator-line simulations

</div>

<div class="confval">

num_force_pts_blade

The number of actuator points along each blade for actuator-line simulations

</div>

<div class="confval">

num_force_pts_tower

The number of actuator points along the tower for actuator-line simulations.

</div>

<div class="confval">

restart_filename

The checkpoint file for this turbine when restarting a simulation

</div>

<div class="confval">

FAST_input_filename

The FAST input file for this turbine

</div>

<div class="confval">

turb_id

A unique turbine id for each turbine

</div>
