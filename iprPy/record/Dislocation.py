from copy import deepcopy

import numpy as np


# iprPy imports
from DataModelDict import DataModelDict as DM

from datamodelbase import query

# iprPy imports
from . import Record

modelroot = 'dislocation'

class Dislocation(Record):
    
    @property
    def style(self):
        """str: The record style"""
        return 'dislocation'

    @property
    def xsd_filename(self):
        return ('iprPy.record.xsd', f'{self.style}.xsd')

    @property
    def modelroot(self):
        """str: The root element of the content"""
        return modelroot
    
    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = str(value)
    
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = str(value)

    @property
    def character(self):
        return self.__character

    @character.setter
    def character(self, value):
        self.__character = str(value)

    @property
    def burgers_vector(self):
        return self.__burgers_vector

    @burgers_vector.setter
    def burgers_vector(self, value):
        self.__burgers_vector = str(value)

    @property
    def slip_plane(self):
        return deepcopy(self.__slip_plane)

    @slip_plane.setter
    def slip_plane(self, value):
        value = np.asarray(value, dtype=int)
        assert value.shape == (3,)
        self.__slip_plane = value

    @property
    def line_direction(self):
        return deepcopy(self.__line_direction)

    @line_direction.setter
    def line_direction(self, value):
        value = np.asarray(value, dtype=int)
        assert value.shape == (3,)
        self.__line_direction = value

    @property
    def family(self):
        return self.__family

    @family.setter
    def family(self, value):
        self.__family = str(value)

    @property
    def parameters(self):
        return self.__parameters
    
    def load_model(self, model, name=None):

        super().load_model(model, name=name)
        content = self.model[self.modelroot]

        self.key = content['key']
        self.id = content['id']
        self.character = content['character']
        self.burgers_vector = content['Burgers-vector']
        self.slip_plane = content['slip-plane']
        self.line_direction = content['line-direction']
        self.family = content['system-family']
        self.__parameters = dict(content['calculation-parameter'])

    def build_model(self):
        model = DM()
        model[self.modelroot] = content = DM()

        content['key'] = self.key
        content['id'] = self.id
        content['character'] = self.character
        content['Burgers-vector'] = self.burgers_vector
        content['slip-plane'] = self.slip_plane.tolist()
        content['line-direction'] = self.line_direction.tolist()
        content['system-family'] = self.family
        content['calculation-parameter'] = DM(self.parameters)

        return model

    def metadata(self):
        """
        Converts the structured content to a simpler dictionary.
        
        Parameters
        ----------
        full : bool, optional
            Flag used by the calculation records.  A True value will include
            terms for both the calculation's input and results, while a value
            of False will only include input terms (Default is True).
        flat : bool, optional
            Flag affecting the format of the dictionary terms.  If True, the
            dictionary terms are limited to having only str, int, and float
            values, which is useful for comparisons.  If False, the term
            values can be of any data type, which is convenient for analysis.
            (Default is False).
            
        Returns
        -------
        dict
            A dictionary representation of the record's content.
        """
        meta = {}
        meta['name'] = self.name
        meta['id'] = self.id
        meta['character'] = self.character
        meta['burgers_vector'] = self.burgers_vector
        meta['slip_plane'] = self.slip_plane
        meta['line_direction'] = self.line_direction
        meta['family'] = self.family
        meta['slip_hkl'] = self.parameters['slip_hkl']
        meta['ξ_uvw'] = self.parameters['ξ_uvw']
        meta['burgers'] = self.parameters['burgers']
        meta['m'] = self.parameters['m']
        meta['n'] = self.parameters['n']
        if 'shift' in self.parameters:
            meta['shift'] = self.parameters['shift']
        if 'shiftscale' in self.parameters:
            meta['shiftscale'] = self.parameters['shiftscale']        
        if 'shiftindex' in self.parameters:
            meta['shiftindex'] = self.parameters['shiftindex']
        
        return meta

    @staticmethod
    def pandasfilter(dataframe, name=None, key=None, id=None,
                     character=None, family=None):
        matches = (
            query.str_match.pandas(dataframe, 'name', name)
            &query.str_match.pandas(dataframe, 'key', key)
            &query.str_match.pandas(dataframe, 'id', id)
            &query.str_match.pandas(dataframe, 'character', character)
            &query.str_match.pandas(dataframe, 'family', family)
        )
        return matches

    @staticmethod
    def mongoquery(name=None, key=None, id=None, character=None, family=None):
        mquery = {}
        root = f'content.{modelroot}'

        query.str_match.mongo(mquery, f'name', name)

        query.str_match.mongo(mquery, f'{root}.key', key)
        query.str_match.mongo(mquery, f'{root}.id', id)
        query.str_match.mongo(mquery, f'{root}.character', character)
        query.str_match.mongo(mquery, f'{root}.system-family', family)
        
        
        return mquery

    @staticmethod
    def cdcsquery(key=None, id=None, character=None, family=None):
        mquery = {}
        root = modelroot

        query.str_match.mongo(mquery, f'{root}.key', key)
        query.str_match.mongo(mquery, f'{root}.id', id)
        query.str_match.mongo(mquery, f'{root}.character', character)
        query.str_match.mongo(mquery, f'{root}.system-family', family)

        return mquery