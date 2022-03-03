#
# models.py
#
import functools
import pickle
from collections import namedtuple
from hashlib import md5

from .factorymanager import FactoryManager

# from app.api.errors import error
import numpy

from functools import cached_property

from .schema import Validator
from .schema import *
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera
from .util import DebugPrint
from .calculation import CalculationFactory
from .constants import *


debug = DebugPrint(0).debug_print


class Hera:
    pass


# This class simplifies the handling of data and unit data
class Dispatcher:
    def __init__(self, data_json, units_json):
        self.data_json = data_json
        self.units_json = units_json


class GaussianBeamDispatcher(Dispatcher):
    """
    Makes a py21cmSense library call to the GaussianBeam class
    """

    def get(self):
        return GaussianBeam(frequency=self.data_json['frequency'], dish_size=self.data_json['dish_size'])


class LatitudeDispatcher(Dispatcher):
    def get(self):
        return self.data_json['location']['latitude']


class HeraAntennaDispatcher(Dispatcher):
    """
    makes a py21cmSense call to the hera antenna class
    """

    def get(self):
        j = self.data_json
        return hera(hex_num=j['hex_num'], separation=j['separation'], dl=j['separation'], units='m')



# serialize the json to a hashable form for LRU caching
def get_sensitivity(thejson):
    """
    serialize json to a hashable form for LRU caching and call method that does the actual work
    :param thejson: json input from application front end
    :return: sensitivity object
    """
    return cached_sensitivity(pickle.dumps(thejson))


@functools.lru_cache
def cached_sensitivity(json_pickle):
    """
    use pickled json object to satisfy LRU cache requirements
    unpickle, and calculate sensitivity object
    :param json_pickle: input json in pickled format
    :return: sensitivity object
    """
    thejson = pickle.loads(json_pickle)
    # get an antenna factory object to calculate antenna parameters based on submitted data
    antenna_obj = AntennaFactory().get(thejson['data']['antenna']['schema'])
    beam_obj = BeamFactory().get(thejson['data']['beam']['schema'])
    # location_obj = Loc
    # print("antenna obj=", antenna_obj)
    # print("beam_obj=", beam_obj)

    # create an antenna object and calculate antenna parameters based on submitted data
    antenna = antenna_obj(thejson['data']['antenna'], thejson['units']['antenna'])
    beam = beam_obj(thejson['data']['beam'], thejson['units']['beam'])

    sensitivity = PowerSpectrum(
        observation=Observation(
            observatory=Observatory(
                antpos=antenna.get(), beam=beam.get(),
                latitude=thejson['data']['location']['latitude']
            )
        )
    )
    return sensitivity


def calculate(thejson):
    """
    calculate antenna data based upon json request from application front end
    :param thejson: json data
    :return: json output or json-formatted error
    """

    v = Validator(thejson)
    if not v.valid_groups():
        return jsonify(error="Invalid JSON schema", errormsg=v.errorMsg)
    else:
        print("JSON SCHEMA VALIDATED")

    if KW_CALCULATION not in thejson:
        return jsonify(error="Calculation type not provided")

    print("Going to run calculation " + thejson[KW_CALCULATION] + " on schema ", thejson)

    # get proper function for this calculation
    calculator = CalculationFactory().get(thejson[KW_CALCULATION])

    if calculator is None:
        return jsonify({KW_ERROR: "Unknown calculation", KW_CALCULATION: thejson[KW_CALCULATION]})

    results = calculator(thejson)

    add_hash(thejson, results)
    add_calculation_type(thejson, results)

    return jsonify(results)


def hash_json(thejson):
    """
    create a unique hash from json for fingerprinting / model identification for front end
    :param thejson: json to hash
    :return: hex-formatted string with digest of input json
    """
    hashfunc = md5()
    hashfunc.update(pickle.dumps(thejson))
    return hashfunc.hexdigest()


def add_hash(thejson, d: dict):
    """
    add hash to the dictionary 'd' (to be jsonified for client return)
    :param thejson: input json to be hashed
    :param d: dictionary containing json being built for client return
    :return: updated dictionary with a modelID k/v pair added.  Format: "modelID": "base64 md5"
    """
    d["modelID"] = hash_json(thejson)


def add_calculation_type(thejson, d: dict):
    """
    Add the calculation type requested (and returned)
    :param thejson:
    :param d:
    :return:
    """
    d[KW_CALCULATION] = thejson[KW_CALCULATION]


def filter_infinity(list1: list, list2: list):
    """
    remove ungraphable infinity values
    :param list1:
    :param list2:
    :return:
    """
    return zip(*(filter(lambda t: t[0] != numpy.inf and t[1] != numpy.inf, zip(list1, list2))))


def quantity_list_to_scalar(l: list):
    """
    convert all AstroPy 'quantity' objects to scalars and return new list
    :param l:
    :return: list of scalars
    """
    newl = []
    for t in l:
        newl.append(t.value)
    return newl


def handle_output(calculation):
    return jsonify({"key": "value"})





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
