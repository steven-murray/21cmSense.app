#
# calculation.py
#
# Project 43 - Web Application for Radio Astronomy Sensitivity
# Author: Brian Pape
# Revision: 0.1
#
# This module contains routines for all supported calculations

import importlib
import logging
import pickle
from hashlib import md5
from pathlib import Path

import astropy.units as un
import jsonschema
import numpy as np
from flask import jsonify
from py21cmsense import PowerSpectrum

from . import redisfuncs as rd
from .constants import *
from .exceptions import CalculationException, ValidationException
from .factorymanager import FactoryManager
from .schema import Validator
from .sensitivity import get_sensitivity
from .util import filter_infinity, quantity_list_to_scalar

logger = logging.getLogger(__name__)


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


def add_hash(thejson, d: dict) -> dict:
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


def json_to_power_spectrum(json: dict) -> PowerSpectrum:
    """
    Convert a dictionary created by a form into a PowerSpectrum object.

    This is essentially the inverse of creating the schema (create_object_schema.py).
    """
    schema_path = Path(__file__).parent.parent / "static/schema/object-schema.json"
    with open(schema_path) as fl:
        schema = json.load(fl)

    # First validate the json against the schema.
    jsonschema.validate(json, schema)

    def construct_class(schema_dct: dict):
        module = importlib.import_module(
            ".".join(schema_dct["className"].split(".")[:-1])
        )
        cls = getattr(module, schema_dct["className"].split(".")[-1])

        kw = {}
        for k, v in schema_dct["properties"].items():
            if "unit" in v:
                kw[k] = json[k] * un.Unit(v["unit"])
            elif "className" in v:
                kw[k] = construct_class(v)  # recurse into object.
            else:
                kw[k] = v

        return cls(**kw)

    return construct_class(schema)


def update_pspec_from_json(
    old_pspec: PowerSpectrum, json: dict, old_json: dict
) -> PowerSpectrum:
    schema_path = Path(__file__).parent.parent / "static/schema/object-schema.json"
    with open(schema_path) as fl:
        schema = json.load(fl)

    # First validate the json against the schema.
    jsonschema.validate(json, schema)

    def update_obj(obj, schema_dct: dict):
        # module = importlib.import_module('.'.join(schema_dct['className'].split('.')[:-1]))
        # cls = getattr(module, schema_dct['className'].split('.')[-1])

        kw = {}
        objs = {}
        for k, v in schema_dct["properties"].items():
            if "className" in v:
                new_obj = update_obj(getattr(obj, k), v)
                if new_obj != getattr(obj, k):
                    objs[k] = new_obj
            elif not np.all(json[k] == old_json[k]):
                if "unit" in v:
                    kw[k] = json[k] * un.Unit(v["unit"])
                else:
                    kw[k] = v

        if objs or kw:
            return obj.clone(**kw, **objs)
        else:
            return obj

    return update_obj(old_pspec, schema)


def add_calculation_type(thejson, d: dict) -> dict:
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
    d[rd.KW_CALCULATION] = thejson[rd.KW_CALCULATION]
    return d


def add_matplotlib_plot_type(plottype: str, d: dict) -> dict:
    d["matplotlib-plot-type"] = plottype
    return d


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
    try:
        v.valid_groups()
    except ValidationException as e:
        return {"error": "Invalid JSON schema", "errormsg": str(e)}, rd.HTTP_BAD_REQUEST

    try:
        v.valid_sections()
    except ValidationException as e:
        return {"error": "Invalid JSON schema", "errormsg": str(e)}, rd.HTTP_BAD_REQUEST

    logger.info(
        "Going to run calculation " + thejson[rd.KW_CALCULATION] + " on schema ",
        thejson,
    )

    # get proper function for this calculation
    calculator = CalculationFactory().get(thejson[rd.KW_CALCULATION])
    if calculator is None:
        return {
            rd.KW_ERROR: "Unknown calculation",
            rd.KW_CALCULATION: thejson[rd.KW_CALCULATION],
        }, rd.HTTP_UNPROCESSABLE_ENTITY

    try:
        results = calculator(thejson)
    except (CalculationException, Exception) as e:
        return {
            rd.KW_ERROR: str(e),
            rd.KW_CALCULATION: thejson[rd.KW_CALCULATION],
        }, rd.HTTP_UNPROCESSABLE_ENTITY

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
        super().__init__(rd.KW_CALCULATION)
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

        labels = {
            "title": "1D cut",
            "plottype": "line",
            "xlabel": "k [h/Mpc]",
            "ylabel": r"$\delta \Delta^2_{21}$",
            "xscale": "log",
            "yscale": "log",
        }
        sensitivity = get_sensitivity(thejson)
        power_std = sensitivity.calculate_sensitivity_1d()
        (xseries, yseries) = filter_infinity(
            sensitivity.k1d.value.tolist(), power_std.value.tolist()
        )
        d = {
            "x": xseries,
            "y": yseries,
            "xunit": sensitivity.k1d.unit.to_string(),
            "yunit": power_std.unit.to_string(),
        }
        d.update(labels)
        add_matplotlib_plot_type("line", d)
        return d

    def _1D_noise_cut_of_2D_sensitivity(self, thejson):
        """_1D_noise_cut_of_2D_sensitivity includes thermal noise without sample variance

        :param thejson:
        :return:
        """
        labels = {
            "title": "1D thermal var",
            "plottype": "line",
            "xlabel": "k [h/Mpc]",
            "ylabel": r"$\delta \Delta^2_{21}$",
            "xscale": "log",
            "yscale": "log",
        }
        logger.info("in one_d_thermal_var: includes thermal-only variance")
        sensitivity = get_sensitivity(thejson)
        power_std_thermal = sensitivity.calculate_sensitivity_1d(
            thermal=True, sample=False
        )
        (xseries, yseries) = filter_infinity(
            sensitivity.k1d.value.tolist(), power_std_thermal.value.tolist()
        )
        d = {
            "x": xseries,
            "y": yseries,
            "xunit": sensitivity.k1d.unit.to_string(),
            "yunit": power_std_thermal.unit.to_string(),
        }
        d.update(labels)
        add_matplotlib_plot_type("line", d)
        return d

    def _1D_sample_variance_cut_of_2D_sensitivity(self, thejson):
        """_1D_sample_variance_cut_of_2D_sensitivity includes sample-only variance without thermal noise

        :param thejson:
        :return:
        """
        labels = {
            "title": "1D thermal var",
            "plottype": "line",
            "xlabel": "k [h/Mpc]",
            "ylabel": r"$\delta \Delta^2_{21}$",
            "xscale": "log",
            "yscale": "log",
        }
        sensitivity = get_sensitivity(thejson)
        power_std_sample = sensitivity.calculate_sensitivity_1d(
            thermal=False, sample=True
        )
        d = {
            "x": sensitivity.k1d.value.tolist(),
            "y": power_std_sample.value.tolist(),
            "xunit": sensitivity.k1d.unit.to_string(),
            "yunit": power_std_sample.unit.to_string(),
        }
        d.update(labels)
        add_matplotlib_plot_type("line", d)
        return d

    def two_d_sens(self, thejson):
        """Return 2D cylindrical visualization cut of sensitivity

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observation = sensitivity.observation

        # plt.figure(figsize=(7, 5))
        labels = {
            "title": "Number of baselines in group",
            "plottype": "scatter",
            "xlabel": "",
            "ylabel": "",
            "xscale": "log",
            "yscale": "log",
        }
        x = [bl_group[0] for bl_group in observation.baseline_groups]
        y = [bl_group[1] for bl_group in observation.baseline_groups]
        c = [len(bls) for bls in observation.baseline_groups.values()]

        d = {"x": x, "y": y, "c": c, "xunit": "", "yunit": "", "cunit": ""}
        d.update(labels)
        add_matplotlib_plot_type("pcolormesh", d)
        return d

    def _antenna_positions(self, thejson):
        """Antenna position

        :param thejson:
        :return:
        """
        labels = {"xlabel": "m", "ylabel": "m", "xscale": "log", "yscale": "log"}

        sensitivity = get_sensitivity(thejson)
        observatory = sensitivity.observation.observatory

        (xseries, yseries) = filter_infinity(
            observatory.antpos[:, 0], observatory.antpos[:, 1]
        )
        xunit = xseries[0].unit.to_string()
        yunit = yseries[0].unit.to_string()
        xseries = quantity_list_to_scalar(xseries)
        yseries = quantity_list_to_scalar(yseries)

        # suggested plotting
        # plt.scatter(Observatory.antpos[:, 0], Observatory.antpos[:, 1])

        # power_std = sensitivity.calculate_sensitivity_1d()
        # (xseries, yseries) = filter_infinity(sensitivity.k1d.value.tolist(), power_std.value.tolist())
        d = {"x": xseries, "y": yseries, "xunit": xunit, "yunit": yunit}
        d.update(labels)
        add_matplotlib_plot_type("scatter", d)
        return d

    def _baselines_distributions(self, thejson):
        """Baselines distributions

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observatory = sensitivity.observation.observatory
        baselines = observatory.baselines_metres

        labels = {
            "xlabel": "Baseline Length [x, m]",
            "ylabel": r"Baselines Length [y, m]",
            "alpha": 0.1,
        }
        d = {
            "x": baselines[:, :, 0].value.tolist(),
            "y": baselines[:, :, 1].value.tolist(),
            "xunit": baselines.unit.to_string(),
            "yunit": baselines.unit.to_string(),
        }
        d.update(labels)
        add_matplotlib_plot_type("hist", d)
        return d

    def _uv_grid_sampling(self, thejson):
        """Return UV grid sampling data

        :param thejson:
        :return:
        """
        sensitivity = get_sensitivity(thejson)
        observation = sensitivity.observation

        labels = {
            "title": "UV Grid Sampling",
            "plottype": "2DRaster",
            "xlabel": "",
            "xscale": "linear",
        }
        x = observation.uv_coverage.tolist()
        d = {"x": x, "xunit": ""}
        d.update(labels)
        add_matplotlib_plot_type("imshow", d)
        return d
