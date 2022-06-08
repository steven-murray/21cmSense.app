#
# models.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains support for keyword-mapped functions and automatic
# on-disk schema mapping to supported calculation methods in the code.


from functools import cache, cached_property
from typing import Callable
from app.api.schema import get_schema_names
import logging

logger = logging.getLogger(__name__)


class FactoryManager:
    """Class to manage methods for callbacks
    """

    def __init__(self, schemagroup):
        self.d = {}
        assert schemagroup, "Factory manager initialized without a schema group name"
        
        self.schema_group = schemagroup

        self.schema_methods = {m.upper(): m for m in dir(self) if hasattr(m, 'schema_method')}
        lookup_list = self.map_schema_to_methods(self.schema_group)

        self.add_all(lookup_list)

    def add_all(self, **kwargs):
        """adds mappings from maplist, which contains (keyword, func) mappings

        Parameters
        ----------
        maplist
            dict with (keyword, func) mappings

        """
        for k, v in kwargs.items():
            self[k] = v

    def __setitem__(self, key, val):
        self.d[key] = val

    def __getitem__(self, key):
        return self.d[key]

    def __contains__(self, key):
        return key in self.d

    def get(self, key):
        """Get function mapped to key

        Parameters
        ----------
        key
            key to check

        Returns
        -------
        function
            function mapped to key or None if no match on key

        """
        return self.d.get(key)

    @cache
    def map_schema_to_methods(self, schemagroup) -> dict[str, Callable]:
        """Map on-disk schema to class methods based on name

        Returns
        -------
        list
            list of ("name", function) tuples for lookups
        """
        lookup_list = {}

        schemas = get_schema_names(schemagroup)

        for s in schemas:
            # transliterate "-" in schema to "_" in method and add leading underscore
            method_name = "_" + s.replace("-", "_").upper()
            try:
                lookup_list[s] = self.schema_methods[method_name]
            except KeyError:
                logger.error("Missing group " + schemagroup + " method for schema " + s)

        return lookup_list
