#
# models.py
#
import functools
import pickle
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


class GaussianBeamDispatcher(Dispatcher):
    """
    Makes a py21cmSense library call to the GaussianBeam class
    """

    def get(self):
        # TODO - extract units from JSON
        return GaussianBeam(frequency=self.data_json['frequency'] * units.Unit("MHz"),
                            dish_size=self.data_json['dish_size'] * units.Unit("m"))


class LatitudeDispatcher(Dispatcher):
    """Handles latitude

    """

    def get(self):
        return self.data_json['location']['latitude']


class HeraAntennaDispatcher(Dispatcher):
    """makes a py21cmSense call to the hera antenna class
    """

    def get(self):
        j = self.data_json

        # TODO - extract units from JSON
        return hera(hex_num=j['hex_num'], separation=j['separation'] * units.Unit("m"),
                    dl=j['separation'] * units.Unit("m"))


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
        self.add('Latitude', LatitudeDispatcher)


class BeamFactory(FactoryManager):
    def __init__(self):
        super().__init__("beam")
        self.add('GaussianBeam', GaussianBeamDispatcher).add('FakeBeam', GaussianBeamDispatcher)


class AntennaFactory(FactoryManager):
    def __init__(self):
        super().__init__("antenna")
        self.add('hera', HeraAntennaDispatcher)


class Factory:
    def get_antenna_type(self, thejson):
        return thejson['schema']

    def get_beam_type(self, thejson):
        return thejson['data']['beam']['class']

    def go(self, thejson):
        #        beamtype=
        #        beam=BeamFactory()
        print("in go, processing the following JSON: ", thejson)
        print("got json: ", thejson['schema'])
        for fld in ('antenna', 'beam', 'location'):
            print("%s data: " % fld, thejson['data'][fld])
            print("%s units: " % fld, thejson['units'][fld])
            print("antenna type: ", self.get_antenna_type(thejson))
            print("beam type: ", self.get_beam_type(thejson))

        antenna_obj = AntennaFactory().get(self.get_antenna_type(thejson))
        beam_obj = BeamFactory().get(self.get_beam_type(thejson))
        print("antenna obj=", antenna_obj)
        print("beam_obj=", beam_obj)

        calculation_obj = CalculationFactory().get(self.get_cal)

        antenna = antenna_obj(thejson['data']['antenna'], thejson['units']['antenna'])
        beam = beam_obj(thejson['data']['beam'], thejson['units']['beam'])

        sensitivity = PowerSpectrum(
            observation=Observation(
                observatory=Observatory(
                    antpos=antenna.get(), beam=beam.get(),
                    # antpos=hera(hex_num=7, separation=14, dl=12.12, units="m"),
                    # beam=GaussianBeam(frequency=135.0, dish_size=14),
                    # latitude=38 * np.pi / 180.0
                    latitude=thejson['data']['location']['latitude']
                )
            )
        )

        return sensitivity
