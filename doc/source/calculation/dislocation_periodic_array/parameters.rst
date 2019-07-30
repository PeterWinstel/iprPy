Input script parameters
-----------------------

This is a list of the input parameter names recognized by the
calculation script.

Command lines for LAMMPS and MPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides the external commands for running LAMMPS and MPI.

-  **lammps_command**: the path to the executable for running LAMMPS on
   your system. Don’t include command line options.

-  **mpi_command**: the path to the MPI executable and any command line
   options to use for calling LAMMPS to run in parallel on your system.
   Default value is None (run LAMMPS as a serial process).

Potential definition and directory containing associated files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides the information associated with an interatomic potential
implemented for LAMMPS.

-  **potential_file**: the path to the potential_LAMMPS data model used
   by atomman to generate the proper LAMMPS commands for an interatomic
   potential.

-  **potential_dir**: the path to the directory containing any potential
   artifacts (eg. eam.alloy setfl files) that are used. If not given,
   then any required files are expected to be in the working directory
   where the calculation is executed.

Initial system configuration to load
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides the information associated with loading an atomic
configuration.

-  **load_file**: the path to the initial configuration file being read
   in.

-  **load_style**: the style/format for the load_file. The style can be
   any file type supported by atomman.load()

-  **load_options**: a list of key-value pairs for the optional
   style-dependent arguments used by atomman.load().

-  **family**: specifies the configuration family to associate with the
   loaded file. This is typically a crystal structure/prototype
   identifier that helps with linking calculations on the same material
   together. If not given and the load_style is system_model, then the
   family will be taken from the file if included. Otherwise, the family
   will be taken as load_file stripped of path and extension.

-  **symbols**: a space-delimited list of the potential’s atom-model
   symbols to associate with the loaded system’s atom types. Required if
   load_file does not contain this information.

-  **box_parameters**: *Note that this parameter has no influence on
   this calculation.* allows for the specification of new box parameters
   to scale the loaded configuration by. This is useful for running
   calculations based on prototype configurations that do not contain
   material-specific dimensions. Can be given either as a list of three
   or six numbers, with an optional unit of length at the end. If the
   unit of length is not given, the specified length_unit (below) will
   be used.

   -  a b c (unit): for orthogonal boxes.

   -  a b c alpha beta gamma (unit): for triclinic boxes. The angles are
      taken in degrees.

System manipulations
~~~~~~~~~~~~~~~~~~~~

Performs simple manipulations on the loaded initial system.

-  **a_uvw, b_uvw, c_uvw**: are crystallographic Miller vectors to
   rotate the system by such that the rotated system’s a, b, c box
   vectors correspond to the specified Miller vectors of the loaded
   configuration. Using crystallographic vectors for rotating ensures
   that if the initial configuration is periodic in all three
   directions, the resulting rotated configuration can be as well with
   no boundary incompatibilities. Default values are ‘1 0 0’, ‘0 1 0’,
   and ‘0 0 1’, respectively (i.e. no rotation). **Calculation-specific
   note**: the appropriate *uvw*\ s for a dislocation depend on the
   dislocation and how the *dislocation_stroh_m*, *dislocation_stroh_n*,
   and *dislocation_lineboxvector* parameters are defined (see below).

-  **atomshift**: a vector positional shift to apply to all atoms. The
   shift is relative to the size of the system after rotating, but
   before sizemults have been applied. This allows for the same relative
   shift regardless of box_parameters and sizemults. Default value is
   ‘0.0 0.0 0.0’ (i.e. no shift). **Calculation-specific note**: a shift
   needs to be applied such that no atom position vectors dotted with
   the *dislocation_stroh_n* vector are zero. For example, if
   *dislocation_stroh_n* = [0, 0, 1], i.e. parallel to the
   :math:`z`-axis, then no atoms can have a :math:`z` coordinate equal
   to 0.

-  **sizemults**: multiplication parameters for making a supercell of
   the loaded system. This may either be a list of three or six integer
   numbers. Default value is ‘0 3 -20 20 -20 20’. **Calculation-specific
   note**: The two box directions not corresponding to
   *dislocation_lineboxvector* should have negative, positive
   *sizemults* of the same magnitude.

   -  ma mb mc: multipliers for each box axis. Values can be positive or
      negative indicating the direction relative to the original box’s
      origin for shifting/multiplying the system.

   -  na pa nb pb nc pc: negative, positive multiplier pairs for each
      box axis. The n terms must be less than or equal to zero, and the
      p terms greater than or equal to zero. This allows for expanding
      the system in both directions relative to the original box’s
      origin.

Defect parameters
~~~~~~~~~~~~~~~~~

Defines the defect system to construct and analyze.

-  **dislocation_file**: the path to a dislocation_monopole record file
   that contains a set of input parameters associated with a specific
   dislocation. In particular, the dislocation_monopole record contains
   values for the *a_uvw, b_uvw, c_uvw, atomshift, dislocation_stroh_m,
   dislocation_stroh_n, dislocation_lineboxvector,* and
   *dislocation_burgersvector* parameters. As such, those parameters
   cannot be specified separately if *pointdefect_model* is given.

-  **dislocation_stroh_m**: three floating point numbers corresponding
   to the :math:`m` unit vector defining one of the two axes used by the
   Stroh method. :math:`m` must be perpendicular to the
   *dislocation_lineboxvector* and within the slip plane. Default value
   is ‘0 1 0’.

-  **dislocation_stroh_n**: three floating point numbers corresponding
   to the :math:`m` unit vector defining one of the two axes used by the
   Stroh method. :math:`n` must be perpendicular to the
   *dislocation_lineboxvector* and normal to the slip plane. Default
   value is ‘0 0 1’.

-  **dislocation_lineboxvector**: ‘a’, ‘b’, or ‘c’ specifying which of
   the three box vectors the dislocation line is made parallel to.
   Default value is ‘a’.

-  **dislocation_burgersvector**: three floating point numbers
   specifying the dislocation’s Burgers vector in Crystallographic uvw
   units relative to the loaded system’s box vectors.

-  **dislocation_boundarywidth**: floating point number specifying the
   minimum thickness of the boundary region. This number is taken
   relative to the loaded system’s :math:`a` box vector magnitude.

-  **dislocation_boundaryshape**: ‘box’ or ‘circle’ specifying the
   resulting shape of the active region after defining the boundary
   atoms. For ‘box’, the boundary width is constant at the two
   non-periodic box edges. For ‘circle’, the active region is a cylinder
   centered around the dislocation line. Default value is ‘circle’.

Elastic constants parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifies the computed elastic constants for the interatomic potential
and crystal structure, relative to the loaded system’s orientation.

-  **elasticconstants_file**: the path to a record containing the
   elastic constants to use. If neither this or the individual Cij
   components (below) are given and *load_style* is ‘system_model’, this
   will be set to *load_file*.

-  **C11, C12, C13, C14, C15, C16, C22, C23, C24, C25, C26, C33, C34,
   C35, C36, C44, C45, C46, C55, C56, C66**: the individual elastic
   constants components in units of pressure. If the loaded system’s
   orientation is the standard setting for the crystal type, then
   missing values will automatically be filled in. Example: if the
   loaded system is a cubic prototype, then only *C11, C12* and *C44*
   need be specified.

Units for input/output values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifies the units for various physical quantities to use when saving
values to the results record file. Also used as the default units for
parameters in this input parameter file.

-  **length_unit**: defines the unit of length for results, and input
   parameters if not directly specified. Default value is ‘angstrom’.

-  **energy_unit**: defines the unit of energy for results, and input
   parameters if not directly specified. Default value is ‘eV’.

-  **pressure_unit**: defines the unit of pressure for results, and
   input parameters if not directly specified. Default value is ‘GPa’.

-  **force_unit**: defines the unit of pressure for results, and input
   parameters if not directly specified. Default value is ‘eV/angstrom’.

Run Parameters
~~~~~~~~~~~~~~

Provides parameters specific to the calculation at hand.

-  **annealtemperature**: specifies the temperature at which to anneal
   the dislocation system. If 0.0, only a static energy/force
   minimization will be performed. Otherwise, 10,000 NVT steps at this
   temperature will be performed prior to the minimization.

-  **energytolerance**: specifies the energy tolerance to use for the
   minimization. This value is unitless and corresponds to the etol term
   for the `LAMMPS minimize
   command. <http://lammps.sandia.gov/doc/minimize.html>`__ Default
   value is 0.

-  **forcetolerance**: specifies the force tolerance to use for the
   minimization. This value is in force units and corresponds to the
   ftol term for the `LAMMPS minimize
   command. <http://lammps.sandia.gov/doc/minimize.html>`__ Default
   value is ‘1.0e-10 eV/angstrom’.

-  **maxiterations**: specifies the maximum number of iterations to use
   for the minimization. This value corresponds to the maxiter term for
   the `LAMMPS minimize
   command. <http://lammps.sandia.gov/doc/minimize.html>`__ Default
   value is 1000.

-  **maxevaluations**: specifies the maximum number of iterations to use
   for the minimization. This value corresponds to the maxeval term for
   the `LAMMPS minimize
   command. <http://lammps.sandia.gov/doc/minimize.html>`__ Default
   value is 10000.

-  **maxatommotion**: specifies the maximum distance that any atom can
   move during a minimization iteration. This value is in units length
   and corresponds to the dmax term for the `LAMMPS min_modify
   command. <http://lammps.sandia.gov/doc/min_modify.html>`__ Default
   value is ‘0.01 angstrom’.

-  **randomseed**: provides a random number seed to generating the
   initial atomic velocities. Default value gives a random number as the
   seed.
