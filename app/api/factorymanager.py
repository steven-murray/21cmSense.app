from functools import cached_property

from app.api.schema import get_schema_names


class FactoryManager:
    """Class to manage methods for callbacks

    Attributes
    ----------
    maplist : dict
        Mapping of names to methods
    """

    def __init__(self, schemagroup):
        self.d = {}
        if not schemagroup:
            assert (schemagroup), "Factory manager initialized without a schema group name"
        else:
            self.schemagroup = schemagroup

        lookup_list = self.map_schema_to_methods
        self.add_all(lookup_list)

    def add_all(self, maplist):
        """adds mappings from maplist, which contains (keyword, func) mappings

        Parameters
        ----------
        maplist
            dict with (keyword, func) mappings

        """
        for t in maplist:
            self.add(t[0], t[1])

    def add(self, key, f):
        """Add single keyword, function mapping

        Parameters
        ----------
        key : string
            key
        f : function
            function to map to

        Returns
        -------
        FactoryManager
            returns a reference to this object as a builder pattern
        """
        # if key not in self.d:
        # allow updating/overwriting
        self.d[key] = f
        return self

    def knows(self, key):
        """Whether this object has a mapping for key

        Parameters
        ----------
        key
            key to check

        Returns
        -------
        bool
            true if mapping exists, false otherwise

        """
        if key in self.d:
            return True
        else:
            return False

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
        if self.knows(key):
            return self.d[key]
        else:
            return None

    @cached_property
    def map_schema_to_methods(self):
        """Map on-disk schema to class methods based on name

        Returns
        -------
        list
            list of ("name", function) tuples for lookups
        """
        lookup_list = []

        schemas = get_schema_names(self.schemagroup)
        for c in schemas:
            print("Got schema=", c)

        # find all of the methods in this class.  Nomenclature is '_name_of_schema_on_disk'
        allmethods = {}
        for m in dir(self):
            if not m.startswith('__') and m.startswith('_'):
                print("Got method=", m)
                allmethods[m.upper()] = m

        # lookfor = ["one_d_cut", "two_d_cut"]
        # a list of schema names; we will look for methods matching these
        lookfor = schemas
        print("Going to look for methods matching these schema:", lookfor)
        for s in lookfor:

            # transliterate "-" in schema to "_" in method and add leading underscore
            method_name = "_" + s.replace("-", "_").upper()
            if method_name in allmethods:

                # method = getattr(CalculationFactory, allmethods[method_name])
                method = getattr(self, allmethods[method_name])
                # self.add(s, method)
                lookup_list.append((s, method))
                print("Mapped group " + self.schemagroup + " method " + allmethods[method_name] + " to schema " + s)
                allmethods.pop(method_name)

            else:
                print("Missing group " + self.schemagroup + " method for schema " + s)
                # if method.__name__ in allmethods:
                #     allmethods.remove(method.__name__)

        for m in allmethods:
            print("Missing group " + self.schemagroup + " schema for method " + m)

        return lookup_list
