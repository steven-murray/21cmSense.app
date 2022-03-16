#
# models.py
#
import pickle
from abc import abstractmethod
from hashlib import md5

from py21cmsense import GaussianBeam, Observation, Observatory, PowerSpectrum, hera
from astropy import units
# from .calculation import CalculationFactory
from .constants import *
from .factorymanager import FactoryManager
from .util import DebugPrint

debug = DebugPrint(0).debug_print


class Hera:
    pass


class Dispatcher:
    """The Dispatcher class simplifies the handling of data and unit data in a json object

    """

    def __init__(self, data_json, units_json):
        self.data_json = data_json
        self.units_json = units_json

    @abstractmethod
    def get(self):
        pass


def hash_json(thejson):
    """create a unique hash from json for fingerprinting / model identification for front end

    Parameters
    ----------
    thejson
       json to hash

    Returns
    -------
    String
        hex-formatted string with digest of input json
    """
    hashfunc = md5()
    hashfunc.update(pickle.dumps(thejson))
    return hashfunc.hexdigest()


def add_hash(thejson, d: dict):
    """add hash of the supplied json to the dictionary 'd' (to be jsonified for client return)

    Parameters
    ----------
    thejson
        input json to be hashed
    d
        dictionary containing json being built for client return

    Returns
    -------
    dict
        updated dictionary with a modelID k/v pair added.

        Format: "modelID": "base64 md5"
    """
    d["modelID"] = hash_json(thejson)
    return d


def add_calculation_type(thejson, d: dict):
    """Add the calculation type requested (and returned)

    Parameters
    ----------
    thejson
        input json containing calculation type
    d
        dictionary to add calculation type to

    Returns
    -------
    dict
        updated dictionary with a calculation k/v pair added.

        Format: "calculation": "name_of_calculation"

    """
    d[KW_CALCULATION] = thejson[KW_CALCULATION]
    return d


class LocationFactory(FactoryManager):
    def __init__(self):
        super().__init__("location")
        # self.add('latitude', LatitudeDispatcher)

    class _latitude(Dispatcher):
        """Handles latitude

        """

        def get(self):
            return self.data_json['latitude'] * units.Unit(self.units_json['latitude'])


class BeamFactory(FactoryManager):
    def __init__(self):
        super().__init__("beam")
        # self.add('GaussianBeam', GaussianBeamDispatcher).add('FakeBeam', GaussianBeamDispatcher)

    class _GaussianBeam(Dispatcher):
        """
        Makes a py21cmSense library call to the GaussianBeam class
        """

        def get(self):
            # TODO - add error checking on units
            # return GaussianBeam(frequency=self.data_json['frequency'] * units.Unit("MHz"),
            #                     dish_size=self.data_json['dish_size'] * units.Unit("m"))
            return GaussianBeam(frequency=self.data_json['frequency'] * units.Unit(self.units_json['frequency']),
                                dish_size=self.data_json['dish_size'] * units.Unit(self.units_json['dish_size']))


class AntennaFactory(FactoryManager):
    def __init__(self):
        super().__init__("antenna")
        # self.add('ahera', HeraAntennaDispatcher)
        # print("ANTENNA DICT=",self.d)

    class _hera(Dispatcher):
        """makes a py21cmSense call to the hera antenna class
        """

        def get(self):
            j = self.data_json
            u = self.units_json

            # TODO - error checking on units
            # return hera(hex_num=j['hex_num'], separation=j['separation'] * units.Unit("m"),
            #             dl=j['separation'] * units.Unit("m"))
            return hera(hex_num=j['hex_num'], separation=j['separation'] * units.Unit(u['separation']),
                        dl=j['dl'] * units.Unit(u['dl']))
