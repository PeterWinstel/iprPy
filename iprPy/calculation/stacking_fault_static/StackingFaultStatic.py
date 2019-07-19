# Standard Python libraries
from pathlib import Path

# iprPy imports
from .. import Calculation
from ...input import subset

class StackingFaultStatic(Calculation):
    """
    Class for handling different calculation styles in the same fashion.  The
    class defines the common methods and attributes, which are then uniquely
    implemented for each style.  The available styles are loaded from the
    iprPy.calculations submodule.
    """
    def __init__(self):
        """
        Initializes a Calculation object for a given style.
        """
        # Call parent constructor
        super().__init__()

        # Define calc shortcut
        self.calc = self.script.stackingfault
    
    @property
    def files(self):
        """
        iter of str: Path to each file required by the calculation.
        """
        # Fetch universal files from parent
        universalfiles = super().files

        # Specify calculation-specific keys 
        files = [
            'sfmin.template',
        ]
        for i in range(len(files)):
            files[i] = Path(self.directory, files[i])
        
        # Join and return
        return universalfiles + files
    
    @property
    def template(self):
        """
        str: The template to use for generating calc.in files.
        """
        # Specify the subsets to include in the template
        subsets = [
            'lammps_commands', 
            'lammps_potential',
            'atomman_systemload',
            'atomman_systemmanipulate',
            'stackingfault',
            'units',
            'lammps_minimize',
        ]
        
        # Specify the calculation-specific run parameters
        runkeys = [
            'stackingfault_shiftfraction1',
            'stackingfault_shiftfraction2', 
        ]
        
        return self._buildtemplate(subsets, runkeys)

    @property
    def singularkeys(self):
        """
        list: Calculation keys that can have single values during prepare.
        """
        # Fetch universal key sets from parent
        universalkeys = super().singularkeys
        
        # Specify calculation-specific key sets 
        keys = (
            subset('lammps_commands').keyset 
            + subset('units').keyset 
            + []
        )
        
        # Join and return
        return universalkeys + keys

    @property
    def multikeys(self):
        """
        list: Calculation key sets that can have multiple values during prepare.
        """
        # Fetch universal key sets from parent
        universalkeys = super().multikeys
        
        # Specify calculation-specific key sets 
        keys =  [
            (
                subset('lammps_potential').keyset 
                + subset('atomman_systemload').keyset
            ),
            (
                [
                    'sizemults',
                ]
            ),
            (
                subset('stackingfault').keyset
                + [
                    'stackingfault_shiftfraction1',
                    'stackingfault_shiftfraction2',
                ],
            ),
            (
                subset('lammps_minimize').keyset
            ),
        ]
               
        # Join and return
        return universalkeys + keys