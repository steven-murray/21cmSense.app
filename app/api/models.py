#
# models.py
#
import functools
import pickle
from hashlib import md5

# from app.api.errors import error
import numpy

from app.schema import *
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera
from .util import DebugPrint
from ..constants import *

from app.schema import Validator

debug = DebugPrint(0).debug_print


class Hera:
    pass


class FactoryManager:
    def __init__(self, schemagroup):
        self.d = {}
        if not schemagroup:
            assert (schemagroup), "Factory manager initialized without a schema group name"
        else:
            self.schemagroup = schemagroup

        self.map_schema_to_methods()

    def add(self, key, f):
        # if key not in self.d:
        # allow updating/overwriting
        self.d[key] = f
        return self

    def knows(self, key):
        if key in self.d:
            return True
        else:
            return False

    def get(self, key):
        if self.knows(key):
            return self.d[key]
        else:
            return None

    def map_schema_to_methods(self):
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

                method = getattr(CalculationFactory, allmethods[method_name])
                self.add(s, method)
                print("Mapped group " + self.schemagroup + " method " + allmethods[method_name] + " to schema " + s)
                allmethods.pop(method_name)

            else:
                print("Missing group " + self.schemagroup + " method for schema " + s)
                # if method.__name__ in allmethods:
                #     allmethods.remove(method.__name__)

        for m in allmethods:
            print("Missing group " + self.schemagroup + " schema for method " + m)


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


class CalculationDispatcher(Dispatcher):
    pass


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

    # plt.plot(sensitivity.k1d, power_std)


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
        return jsonify(error="calculation type not provided")

    print("Going to run calculation " + thejson[KW_CALCULATION] + " on schema ", thejson)
    calculator = CalculationFactory().get(thejson[KW_CALCULATION])

    if calculator is None:
        return jsonify({KW_ERROR: "unknown calculation", KW_CALCULATION: thejson[KW_CALCULATION]})

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


# note that the keys below, e.g., '1D-cut-of-2D-sensitivity', must match the NAME prefix of a .json file in the
# schema directories.  ex: static/schema/calculation/1D-cut-of-2D-sensitivity.json
#
# '-' characters will be transliterated to "_" when searching for applicable methods
#
class CalculationFactory(FactoryManager):
    def __init__(self):
        super().__init__(KW_CALCULATION)
        # CalculationFactory.calcs = self.add('1D-cut-of-2D-sensitivity', one_d_cut).add(

        #        self.add('1D-cut-of-2D-sensitivity', one_d_cut).\
        # self.add('1D-cut-of-2D-sensitivity', method).add(
        #     '1D-noise-cut-of-2D-sensitivity', one_d_thermal_var).add(
        #     '1D-sample-variance-cut-of-2D-sensitivity', one_d_sample_var).add(
        #     '2D-sensitivity', one_d_cut).add('antenna-positions', one_d_cut).add(
        #     'calculations', one_d_cut).add('k-vs-redshift-plot', one_d_cut).add(
        #     'baselines-distributions', baselines_distributions)

        """
        1D-cut-of-2D-sensitivity.json 1D-noise-cut-of-2D-sensitivity.json 1D-sample-variance-cut-of-2D-sensitivity.json 2D-sensitivity.json antenna-positions.json baselines-distributions.json calculations.json k-vs-redshift-plot.json
        """

    def _1D_cut_of_2D_sensitivity(thejson):
        """one_d_cut: includes thermal noise and sample variance

        :param thejson:
        :return:
        """

        labels = {"title": "1D cut", "plottype": "line", "xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$",
                  "xscale": "log", "yscale": "log"}
        sensitivity = get_sensitivity(thejson)
        power_std = sensitivity.calculate_sensitivity_1d()
        (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
        d = {"x": xseries, "y": yseries,
             "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std.unit.to_string()}
        d.update(labels)
        return d

    # prototype debugging output
    # print(pprint.pprint(d))
    #
    # print("Astropy quantity breakdown:")
    # print("type of k1d=", type(sensitivity.k1d))
    # print("value=", sensitivity.k1d.value)
    # print("unit=", sensitivity.k1d.unit)
    #
    # print("type of power=", type(power_std))
    # print("value=", power_std.value)
    # print("unit=", power_std.unit)

    # add_hash(thejson, d)
    # return jsonify(d)
    # return jsonify({"a": "b"})

    def _1D_noise_cut_of_2D_sensitivity(thejson):
        """_1D_noise_cut_of_2D_sensitivity includes thermal noise without sample variance

        :param thejson:
        :return:
        """
        labels = {"title": "1D thermal var", "plottype": "line", "xlabel": "k [h/Mpc]",
                  "ylabel": r"$\delta \Delta^2_{21}$",
                  "xscale": "log", "yscale": "log"}
        print("in one_d_thermal_var: includes thermal-only variance")
        sensitivity = get_sensitivity(thejson)
        power_std_thermal = sensitivity.calculate_sensitivity_1d(thermal=True, sample=False)
        (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std_thermal.value.tolist())
        d = {"x": xseries, "y": yseries,
             "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std_thermal.unit.to_string()}
        d.update(labels)
        # add_hash(thejson, d)
        # return jsonify(d)
        return d

    def _1D_sample_variance_cut_of_2D_sensitivity(thejson):
        """_1D_sample_variance_cut_of_2D_sensitivity includes sample-only variance without thermal noise

        :param thejson:
        :return:
        """
        labels = {"title": "1D thermal var", "plottype": "line", "xlabel": "k [h/Mpc]",
                  "ylabel": r"$\delta \Delta^2_{21}$",
                  "xscale": "log", "yscale": "log"}
        sensitivity = get_sensitivity(thejson)
        power_std_sample = sensitivity.calculate_sensitivity_1d(thermal=False, sample=True)
        d = {"x": sensitivity.k1d.value.tolist(), "y": power_std_sample.value.tolist(),
             "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std_sample.unit.to_string()}
        d.update(labels)
        return d

    def two_d_sens(thejson):
        """Return 2D cylindrical visualization cut of sensitivity

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observation = sensitivity.observation

        # plt.figure(figsize=(7, 5))
        labels = {"title": "Number of baselines in group", "plottype": "scatter", "xlabel": "", "ylabel": "",
                  "xscale": "log", "yscale": "log"}
        x = [bl_group[0] for bl_group in observation.baseline_groups]
        y = [bl_group[1] for bl_group in observation.baseline_groups]
        c = [len(bls) for bls in observation.baseline_groups.values()]

        d = {"x": x, "y": y, "c": c, "xunit": "", "yunit": "", "cunit": ""}
        d.update(labels)
        return d

        #
        # plt.scatter(x, y, c=c)
        # cbar = plt.colorbar();
        # cbar.set_label("Number of baselines in group", fontsize=15)
        # plt.tight_layout();

    def _antenna_positions(thejson):
        """Antenna position

        :param thejson:
        :return:
        """
        labels = {"xlabel": "m", "ylabel": "m", "xscale": "log", "yscale": "log"}

        sensitivity = get_sensitivity(thejson)
        observatory = sensitivity.observation.observatory

        (xseries, yseries) = filter_infinity(observatory.antpos[:, 0], observatory.antpos[:, 1])
        xunit = xseries[0].unit.to_string()
        yunit = yseries[0].unit.to_string()
        xseries = quantity_list_to_scalar(xseries)
        yseries = quantity_list_to_scalar(yseries)

        # suggested plotting
        # plt.scatter(Observatory.antpos[:, 0], Observatory.antpos[:, 1])

        # power_std = sensitivity.calculate_sensitivity_1d()
        # (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
        d = {"x": xseries, "y": yseries,
             "xunit": xunit, "yunit": yunit}
        d.update(labels)
        return d

    # baselines_distributions= [[[   0.    0.    0.]
    #   [  14.    0.    0.]
    #   [  28.    0.    0.]
    #   ...
    #   [ 112.  -84.    0.]
    #   [ 126.   84.    0.]
    #   [ 126.  -84.    0.]]
    #
    #  [[ -14.    0.    0.]
    #   [   0.    0.    0.]
    #   [  14.    0.    0.]
    #   ...

    # baselines_distributions[:,:,0]= [[   0.   14.   28. ...  112.  126.  126.]
    # [ -14.    0.   14. ...   98.  112.  112.]
    # [ -28.  -14.    0. ...   84.   98.   98.]
    # ...
    # [-112.  -98.  -84. ...    0.   14.   14.]
    # [-126. -112.  -98. ...  -14.    0.    0.]
    # [-126. -112.  -98. ...  -14.    0.    0.]] m

    def _baselines_distributions(thejson):
        """Baselines distributions

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observatory = sensitivity.observation.observatory
        baselines = observatory.baselines_metres

        # print("baselines_distributions=", baselines[:, :, 0])
        # l = baselines[:, :, 0]
        # print("type l=", type(l))
        # print(l)
        # print("l dim=",l.ndim)
        # for q in l:
        #     for qq in q:
        #         print("type=",type(qq))
        # print("value=",l.value)
        # print("value.tolist()=",l.value.tolist())
        # print("l.tolist()=", l.tolist())
        # print("list(l)=",list(l))
        # return jsonify({"none": "none"})

        labels = {"xlabel": "Baseline Length [x, m]", "ylabel": r"Baselines Length [y, m]", "alpha": 0.1}
        d = {"x": baselines[:, :, 0].value.tolist(), "y": baselines[:, :, 1].value.tolist(),
             "xunit": baselines.unit.to_string(), "yunit": baselines.unit.to_string()}
        d.update(labels)
        # add_hash(thejson, d)
        #
        # print("d=", d)

        # return jsonify(d)
        return d
        # baseline_group_coords = observatory.baseline_coords_from_groups(red_bl)
        # baseline_group_counts = observatory.baseline_weights_from_groups(red_bl)
        #
        # plt.figure(figsize=(7, 5))
        # plt.scatter(baseline_group_coords[:, 0], baseline_group_coords[:, 1], c=baseline_group_counts)
        # cbar = plt.colorbar();
        # cbar.set_label("Number of baselines in group", fontsize=15)
        # plt.tight_layout();

    # def baselines_distributions(thejson):
    #     sensitivity = get_sensitivity(thejson)
    #     coherent_grid = observatory.grid_baselines_coherent(
    #         baselines=baseline_group_coords,
    #         weights=baseline_group_counts
    #     )

    def _uv_grid_sampling(thejson):
        """Return UV grid sampling data

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observation = sensitivity.observation

        labels = {"title": "UV Grid Sampling", "plottype": "2DRaster", "xlabel": "", "xscale": "linear"}
        x = observation.uv_coverage.tolist()
        d = {"x": x, "xunit": ""}
        d.update(labels)
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
