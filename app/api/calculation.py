from flask import jsonify

from .factorymanager import FactoryManager
from .constants import *
from .models import add_calculation_type, add_hash
from .schema import Validator
from .sensitivity import get_sensitivity
from .util import filter_infinity, quantity_list_to_scalar


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

    # check for top level groups, e.g., calculation, data, and units.
    if not v.valid_groups():
        return {"error": "Invalid JSON schema", "errormsg": v.errorMsg}, HTTP_BAD_REQUEST
    else:
        print("JSON SCHEMA VALIDATED")

    print("Going to run calculation " + thejson[KW_CALCULATION] + " on schema ", thejson)

    # get proper function for this calculation
    calculator = CalculationFactory().get(thejson[KW_CALCULATION])

    if calculator is None:
        return {KW_ERROR: "Unknown calculation", KW_CALCULATION: thejson[KW_CALCULATION]}, HTTP_UNPROCESSABLE_ENTITY

    results = calculator(thejson)

    add_hash(thejson, results)
    add_calculation_type(thejson, results)

    return jsonify(results)


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

    def _1D_cut_of_2D_sensitivity(self, thejson):
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

    def _1D_noise_cut_of_2D_sensitivity(self, thejson):
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
        return d

    def _1D_sample_variance_cut_of_2D_sensitivity(self, thejson):
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

    def two_d_sens(self, thejson):
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

    def _antenna_positions(self, thejson):
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

    def _baselines_distributions(self, thejson):
        """Baselines distributions

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observatory = sensitivity.observation.observatory
        baselines = observatory.baselines_metres

        labels = {"xlabel": "Baseline Length [x, m]", "ylabel": r"Baselines Length [y, m]", "alpha": 0.1}
        d = {"x": baselines[:, :, 0].value.tolist(), "y": baselines[:, :, 1].value.tolist(),
             "xunit": baselines.unit.to_string(), "yunit": baselines.unit.to_string()}
        d.update(labels)
        return d

    def _uv_grid_sampling(self, thejson):
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
