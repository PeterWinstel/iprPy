# Standard Python libraries
from pathlib import Path

# iprPy imports
from .. import Calculation

class CrystalSpaceGroup(Calculation):
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
        self.calc = self.script.crystal_space_group
    
    @property
    def files(self):
        """
        iter of str: Path to each file required by the calculation.
        """
        # Fetch universal files from parent
        universalfiles = super().files

        # Specify calculation-specific keys 
        files = [
                ]
        for i in range(len(files)):
            files[i] = Path(self.directory, files[i])
        
        # Join and return
        return universalfiles + files

    @property
    def singularkeys(self):
        """
        list: Calculation keys that can have single values during prepare.
        """        
        # Fetch universal keys from parent
        universalkeys = super().singularkeys
        
        # Specify calculation-specific keys 
        keys = [
                'length_unit',
                'pressure_unit',
                'energy_unit',
                'force_unit',
               ]

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
        keys = [
                   [
                    'load_file',
                    'load_content',
                    'load_style',
                    'family',
                    'load_options',
                    'symbols',
                    'box_parameters',
                   ],
                   [
                    'symmetryprecision',
                    'primitivecell',
                    'idealcell',
                   ],
               ]
        
        # Join and return
        return universalkeys + keys