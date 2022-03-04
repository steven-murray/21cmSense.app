#
# models.py
#
import functools
import pickle
from hashlib import md5

import numpy

from py21cmsense import GaussianBeam, Observation, Observatory, PowerSpectrum, hera
from .calculation import CalculationFactory
from .constants import *
from .factorymanager import FactoryManager
from .schema import *
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
        return GaussianBeam(frequency=self.data_json['frequency'], dish_size=self.data_json['dish_size'])


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
        return hera(hex_num=j['hex_num'], separation=j['separation'], dl=j['separation'], units='m')


# serialize the json to a hashable form for LRU caching
def get_sensitivity(thejson):
    """serialize json to a hashable form for LRU caching and call method that does the actual work

    Parameters
    ----------
    thejson
        json input from application front end
    Returns
    -------
    object
        sensitivity object

    """
    return cached_sensitivity(pickle.dumps(thejson))


@functools.lru_cache
def cached_sensitivity(json_pickle):
    """Use pickled json object to satisfy LRU cache requirements

    unpickle, and calculate sensitivity object

    Parameters
    ----------
    json_pickle
       input json in pickled format

    Returns
    -------
    Sensitivity
        sensitivity object

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
    """calculate antenna data based upon json request from application front end

    Parameters
    ----------
    thejson
        json data

    Returns
    -------
    json
        Calculated output or json-formatted error

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


def filter_infinity(list1: list, list2: list):
    """remove ungraphable infinity values in two parallel lists

        list1[n] is infty OR list2[n] is infty -> list1[n] and list2[n] will both be removed

    Parameters
    ----------
    list1
        first list
    list2
        second list

    Returns
    -------
    tuple
        ( newlist1, newlist2 )

    """
    return zip(*(filter(lambda t: t[0] != numpy.inf and t[1] != numpy.inf, zip(list1, list2))))


def quantity_list_to_scalar(l: list):
    """convert all AstroPy 'quantity' objects to scalars and return new list

    Parameters
    ----------
    l
        input list of Astropy 'quantity' objects

    Returns
    -------
    list
        list of scalars

    """
    newl = []
    for t in l:
        newl.append(t.value)
    return newl


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
