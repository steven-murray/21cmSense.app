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

from app.schema import Validator

debug = DebugPrint(9).debug_print


class Hera:
    pass


class FactoryManager:
    def __init__(self):
        self.d = {}

    def add(self, key, f):
        if key not in self.d:
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


class Dispatcher:
    def __init__(self, data_json, units_json):
        self.data_json = data_json
        self.units_json = units_json


class GaussianBeamDispatcher(Dispatcher):
    def get(self):
        return GaussianBeam(frequency=self.data_json['frequency'], dish_size=self.data_json['dish_size'])


class LatitudeDispatcher(Dispatcher):
    def get(self):
        return self.data_json['location']['latitude']


class HeraAntennaDispatcher(Dispatcher):
    def get(self):
        j = self.data_json
        return hera(hex_num=j['hex_num'], separation=j['separation'], dl=j['separation'], units='m')


class CalculationDispatcher(Dispatcher):
    pass


# serialize the json to a hashable form for LRU caching
def get_sensitivity(thejson):
    return cached_sensitivity(pickle.dumps(thejson))


@functools.lru_cache
def cached_sensitivity(json_pickle):
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
    v = Validator(thejson)
    if not v.valid_groups():
        return jsonify(error="INVALID JSON SCHEMA", errormsg=v.errorMsg)
    else:
        print("JSON SCHEMA VALIDATED")

    if 'calculation' not in thejson:
        return jsonify(error="calculation type not provided")

    print("Going to run calculation " + thejson['calculation'] + " on schema ", thejson)
    calculator = CalculationFactory().get(thejson['calculation'])

    if calculator is None:
        return jsonify({"error": "unknown calculation", "calculation": thejson['calculation']})

    results = calculator(thejson)

    add_hash(thejson, results)
    add_calculation_type(thejson, results)

    return jsonify(results)


def hash_json(thejson):
    hashfunc = md5()
    hashfunc.update(pickle.dumps(thejson))
    return hashfunc.hexdigest()


# hashes the input request json and adds a "modelID": "base64 md5" to the dict prior to jsonification
def add_hash(thejson, d: dict):
    d["modelID"] = hash_json(thejson)


def add_calculation_type(thejson, d: dict):
    d["calculation"] = thejson['calculation']


# remove ungraphable infinity values
def filter_infinity(list1: list, list2: list):
    return zip(*(filter(lambda t: t[0] != numpy.inf and t[1] != numpy.inf, zip(list1, list2))))


# moved to CalculationFactor for now
# def one_d_cut(thejson):
#     """one_d_cut: includes thermal noise and sample variance
#
#     :param thejson:
#     :return:
#     """
#     labels = {"title": "1D cut", "plottype": "line", "xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$",
#               "xscale": "log", "yscale": "log"}
#     sensitivity = get_sensitivity(thejson)
#     power_std = sensitivity.calculate_sensitivity_1d()
#     (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
#     d = {"x": xseries, "y": yseries,
#          "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std.unit.to_string()}
#     d.update(labels)
#     return d

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


def one_d_noise_cut(thejson):
    """1D noise cut

    :param thejson:
    :return:
    """
    sensitivity = get_sensitivity(thejson)


# done
def one_d_thermal_var(thejson):
    """one_d_thermal_var

    :param thejson:
    :return:
    """
    labels = {"title": "1D thermal var", "plottype": "line", "xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$",
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


# done
def one_d_sample_var(thejson):
    """one_d_sample_var: includes sample-only variance

    :param thejson:
    :return:
    """
    labels = {"title": "1D thermal var", "plottype": "line", "xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$",
              "xscale": "log", "yscale": "log"}
    sensitivity = get_sensitivity(thejson)
    power_std_sample = sensitivity.calculate_sensitivity_1d(thermal=False, sample=True)
    d = {"x": sensitivity.k1d.value.tolist(), "y": power_std_sample.value.tolist(),
         "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std_sample.unit.to_string()}
    d.update(labels)
    return d


def two_d_sens(thejson):
    """Return 2D cut of sensitivity

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


def two_d_sens_z(thejson):
    """Return 2D cut of sensitivity -z

    :param thejson:
    :return:
    """
    labels = {"xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$", "xscale": "log", "yscale": "log"}
    sensitivity = get_sensitivity(thejson)
    power_std = sensitivity.calculate_sensitivity_1d()
    (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
    d = {"x": xseries, "y": yseries,
         "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std.unit.to_string()}
    d.update(labels)
    return d


def two_d_sens_k(thejson):
    """Return 2D cut of sensitivity -z

    :param thejson:
    :return:
    """

    sensitivity = get_sensitivity(thejson)
    sense2d = sensitivity.calculate_sensitivity_2d()

    # dict of arrays
    # sensitivity.plot_sense_2d(sense2d)


def ant_pos(thejson):
    """Antenna position

    :param thejson:
    :return:
    """
    labels = {"xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$", "xscale": "log", "yscale": "log"}
    print("in antenna position")
    sensitivity = get_sensitivity(thejson)
    power_std = sensitivity.calculate_sensitivity_1d()
    (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
    d = {"x": xseries, "y": yseries,
         "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std.unit.to_string()}
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

def baselines_distributions(thejson):
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


def k_vs_redshift(thejson):
    """K vs redshift

    :param thejson:
    :return:
    """
    labels = {"xlabel": "k [h/Mpc]", "ylabel": r"$\delta \Delta^2_{21}$", "xscale": "log", "yscale": "log"}
    print("in one_d_cut: includes thermal noise and sample variance")
    sensitivity = get_sensitivity(thejson)
    power_std = sensitivity.calculate_sensitivity_1d()
    (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
    d = {"x": xseries, "y": yseries,
         "xunit": sensitivity.k1d.unit.to_string(), "yunit": power_std.unit.to_string()}
    d.update(labels)


def handle_output(calculation):
    return jsonify({"key": "value"})


def one_d_cut(thejson):
    pass


# note that the keys below, e.g., '1D-cut-of-2D-sensitivity', must match the NAME prefix of a .json file in the
# schema directories.  ex: static/schema/calculation/1D-cut-of-2D-sensitivity.json
class CalculationFactory(FactoryManager):
    def __init__(self):
        super().__init__()
        # CalculationFactory.calcs = self.add('1D-cut-of-2D-sensitivity', one_d_cut).add(

        #
        calculation_schemas = get_schema_names('calculation')
        for c in calculation_schemas:
            print("Got schema=", c)

        # now check the directory
        # for f in getattr(globals()):
        #     print(f)

        allmethods = []
        for m in dir(CalculationFactory):
            if not m.startswith('__'):
                print("Got method=", m)
                allmethods.append(m)

        lookfor = ["one_d_cut", "two_d_cut"]
        for s in lookfor:
            try:
                method = getattr(CalculationFactory, s)
                if method in allmethods:
                    allmethods.remove(method)

            # this function does not exist
            except AttributeError as e:
                print("Missing method for schema " + s)
                pass

        for m in allmethods:
            print("Missing schema for method " + m)

        #        self.add('1D-cut-of-2D-sensitivity', one_d_cut).\
        self.add('1D-cut-of-2D-sensitivity', method).add(
            '1D-noise-cut-of-2D-sensitivity', one_d_thermal_var).add(
            '1D-sample-variance-cut-of-2D-sensitivity', one_d_sample_var).add(
            '2D-sensitivity', one_d_cut).add('2D-sensitivity-vs-k', one_d_cut).add(
            '2D-sensitivity-vs-z', one_d_cut).add('antenna-positions', one_d_cut).add(
            'calculations', one_d_cut).add('k-vs-redshift-plot', one_d_cut).add('baselines-distributions',
                                                                                baselines_distributions)

        """
        1D-cut-of-2D-sensitivity.json 1D-noise-cut-of-2D-sensitivity.json 1D-sample-variance-cut-of-2D-sensitivity.json 2D-sensitivity.json 2D-sensitivity-vs-k.json 2D-sensitivity-vs-z.json antenna-positions.json baselines-distributions.json calculations.json k-vs-redshift-plot.json
        """

    def one_d_cut(thejson):

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


class LocationFactory(FactoryManager):
    def __init__(self):
        super().__init__()
        self.add('Latitude', LatitudeDispatcher)


class BeamFactory(FactoryManager):
    def __init__(self):
        super().__init__()
        self.add('GaussianBeam', GaussianBeamDispatcher).add('FakeBeam', GaussianBeamDispatcher)


class AntennaFactory(FactoryManager):
    def __init__(self):
        super().__init__()
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
