from .models import *
from .models import AntennaFactory


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

    a = antenna.get()
    b = beam.get()
    l = thejson['data']['location']['latitude']
    t=400*units.K
    obs = Observatory(antpos=a, beam=b, latitude=l, Trcv=t)

    pass
    pass

    sensitivity = PowerSpectrum(
        observation=Observation(
            observatory=Observatory(
                antpos=antenna.get(), beam=beam.get(),
                latitude=thejson['data']['location']['latitude']
            )
        )
    )
    return sensitivity
