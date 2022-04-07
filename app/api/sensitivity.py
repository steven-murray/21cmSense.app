import functools
import pickle

from astropy.units import UnitConversionError

from .models import *
from .models import AntennaFactory
from .observation import ObservationFactory
from .observatory import ObservatoryFactory


# serialize the json to a hashable form for LRU caching
def get_sensitivity(thejson) -> PowerSpectrum:
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
    # TODO - do better with exception
    try:
        return cached_sensitivity(pickle.dumps(thejson))
    except Exception as e:
        pass


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
    location_obj = LocationFactory().get(thejson['data']['location']['schema'])
    # print("antenna obj=", antenna_obj)
    # print("beam_obj=", beam_obj)

    # create an antenna object and calculate antenna parameters based on submitted data
    antenna = antenna_obj(thejson['data']['antenna'], thejson['units']['antenna'])
    beam = beam_obj(thejson['data']['beam'], thejson['units']['beam'])
    dl = thejson['data']['location']
    ul = thejson['units']['location']
    location = location_obj(thejson['data']['location'], thejson['units']['location'])

    # we will build the objects incrementally for better error reporting.
    # TODO handle return on exceptions
    try:
        a = antenna.get()
    except UnitConversionError as e:
        raise TypeError("Invalid units passed to antenna object") from e
    except (ValueError, AssertionError) as e:
        raise ValueError("Out of range value passed to antenna object") from e
    except Exception as e:
        raise Exception("Unknown error on antenna object") from e

    # TODO: check these exceptions
    try:
        b = beam.get()
    except Exception as e:
        pass
    try:
        lat = location.get()
    except Exception as e:
        pass

    # t = 400 * units.K
    # observatory is an optional schema.  If it's not provided, use a default

    # TODO: integrate this
    # observatory_obj=ObservatoryFactory().get(thejson['data']['observatory']['schema'])
    obs = Observatory(antpos=a, beam=b, latitude=lat)

    # TODO: integrate this
    # observation is an optional schema.  If it's not provided, use a default
    # observation_obj=ObservationFactory().get(thejson['data']['observation']['schema'])
    sensitivity = PowerSpectrum(observation=Observation(observatory=obs))

    # sensitivity = PowerSpectrum(
    #     observation=Observation(
    #         observatory=Observatory(
    #             antpos=antenna.get(), beam=beam.get(),
    #             TODO - add in units
    # latitude=thejson['data']['location']['latitude'] * units.rad
    # )
    # )
    # )
    return sensitivity
