from json import JSONDecodeError, JSONDecoder

import os
from flask import current_app
from flask import jsonify

from .json_util import json_error
# from app.api.errors import error

import json
import jsonschema
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera


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


class HeraAntennaDispatcher(Dispatcher):
    def get(self):
        j = self.data_json
        return hera(hex_num=j['hex_num'], separation=j['separation'], dl=j['separation'], units='m')


class CalculationDispatcher(Dispatcher):
    pass


def one_d_cut():
    pass
    # antenna_obj = AntennaFactory().get(self.get_antenna_type(thejson))
    # beam_obj = BeamFactory().get(self.get_beam_type(thejson))
    # print("antenna obj=", antenna_obj)
    # print("beam_obj=", beam_obj)
    #
    # antenna = antenna_obj(thejson['data']['antenna'], thejson['units']['antenna'])
    # beam = beam_obj(thejson['data']['beam'], thejson['units']['beam'])
    #
    # sensitivity = PowerSpectrum(
    #     observation=Observation(
    #         observatory=Observatory(
    #             antpos=antenna.get(), beam=beam.get(),
    #             latitude=thejson['data']['location']['latitude']
    #         )
    #     )
    # )
    # plt.plot(sensitivity.k1d, power_std)


def one_d_noise_cut():
    pass


def one_d_sample_var():
    pass


def two_d_sens():
    pass


def two_d_sens_k():
    pass


def two_d_sens_z():
    pass


def ant_pos():
    pass


def baselines_dist():
    pass
    # antenna_obj = AntennaFactory().get(self.get_antenna_type(thejson))
    # beam_obj = BeamFactory().get(self.get_beam_type(thejson))
    # print("antenna obj=", antenna_obj)
    # print("beam_obj=", beam_obj)
    #
    # antenna = antenna_obj(thejson['data']['antenna'], thejson['units']['antenna'])
    # beam = beam_obj(thejson['data']['beam'], thejson['units']['beam'])
    #
    # sensitivity = PowerSpectrum(
    #     observation=Observation(
    #         observatory=Observatory(
    #             antpos=antenna.get(), beam=beam.get(),
    #             latitude=thejson['data']['location']['latitude']
    #         )
    #     )
    # )
    # baseline_group_coords = observatory.baseline_coords_from_groups(red_bl)
    # baseline_group_counts = observatory.baseline_weights_from_groups(red_bl)
    #
    # plt.figure(figsize=(7, 5))
    # plt.scatter(baseline_group_coords[:, 0], baseline_group_coords[:, 1], c=baseline_group_counts)
    # cbar = plt.colorbar();
    # cbar.set_label("Number of baselines in group", fontsize=15)
    # plt.tight_layout();


def calcs():
    pass


def k_vs_redshift():
    pass


def handle_output(calculation):
    return jsonify({"key": "value"})


class CalculationFactory(FactoryManager):
    def __init__(self):
        super().__init__()
        # CalculationFactory.calcs = self.add('1D-cut-of-2D-sensitivity', one_d_cut).add(
        self.add('1D-cut-of-2D-sensitivity', one_d_cut).add(
            '1D-noise-cut-of-2D-sensitivity', one_d_cut).add('1D-sample-variance-cut-of-2D-sensitivity', one_d_cut).add(
            '2D-sensitivity', one_d_cut).add('2D-sensitivity-vs-k', one_d_cut).add('2D-sensitivity-vs-z',
                                                                                   one_d_cut).add('antenna-positions',
                                                                                                  one_d_cut).add(
            'baselines-distributions', one_d_cut).add('calculations', one_d_cut).add('k-vs-redshift-plot', one_d_cut)

        """
        1D-cut-of-2D-sensitivity.json 1D-noise-cut-of-2D-sensitivity.json 1D-sample-variance-cut-of-2D-sensitivity.json 2D-sensitivity.json 2D-sensitivity-vs-k.json 2D-sensitivity-vs-z.json antenna-positions.json baselines-distributions.json calculations.json k-vs-redshift-plot.json
        """


class BeamFactory(FactoryManager):
    def __init__(self):
        super().__init__()
        self.add('GaussianBeam', GaussianBeamDispatcher).add('FakeBeam', GaussianBeamDispatcher)


class AntennaFactory(FactoryManager):
    antennas = None

    def __init__(self):
        super().__init__()
        AntennaFactory.antennas = self.add('hera', HeraAntennaDispatcher)


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


def get_schema_names(schemagroup):
    try:
        dirs = os.listdir(current_app.root_path + '/static/schema/' + schemagroup)
    except FileNotFoundError:
        return None
    schemas = [dir.replace('.json', '') for dir in dirs]
    return schemas


def get_schema_descriptions_json(schemagroup):
    d = {}
    schema_names = get_schema_names(schemagroup)
    if schema_names is None:
        return json_error("error", "schema " + schemagroup + " not found.")

    for schema_name in get_schema_names(schemagroup):
        try:
            f = open("app/static/schema/" + schemagroup + "/" + schema_name + ".json", 'r')
            sch = json.load(f)
            f.close()
            d[schema_name] = sch['description']

        # issue with json.load()
        except JSONDecodeError:
            pass

        # issue with f.open()
        except OSError:
            pass

        # issue with finding 'description' key in json
        except KeyError:
            pass
    return jsonify(d)


def get_schema_groups():
    dirs = os.listdir(current_app.root_path + '/static/schema')
    # print("schema groups")
    # for dd in d:
    #     print(dd)
    return dirs


def get_schema_groups_json():
    d = get_schema_groups()
    j = {}
    j['required'] = list(d)
    return jsonify(j)


def load_schema(schemagroup: str, schemaname: str):
    try:
        f = open("app/static/schema/" + schemagroup + "/" + schemaname + ".json", 'r')
        schema = json.load(f)
        f.close()
    except (JSONDecodeError, IOError):
        return None
    else:
        return schema


# load a validation schema.  It must either have the same name as the schema that is to be validated, or
# be "default"
def load_validation_schema(schemagroup: str, schemaname: str):
    schema = load_schema(schemagroup, schemaname)
    if not schema:
        schema = load_schema(schemagroup, "default")
        if not schema:
            print("DEBUG: Cannot locate schema for %s/%s", (schemagroup, schemaname))
            return None
    print("DEBUG: returning validation schema:", schema)
    return schema


def build_schema_for_validation(data_json, units_json):
    d={}
    d['data']=data_json
    d['units']=units_json
    return d


# pass a dict such as:
# { group: schema, [...] }
# ex: { "beam": "GaussianBeam", "location": "latitude", "antenna": "hera", "calculation": "baselines-distributions" }
# schema should already be a json object
def build_composite_schema(schema: JSONDecoder):
    # get calculation type
    if 'calculation' not in schema:
        return json_error("error", "specified schema missing 'calculation' key")

    calculation_type = schema['calculation']
    print("Going to load schema for calculation ", calculation_type)

    calc_schema = load_schema('calculation', calculation_type)
    if not calc_schema:
        return json_error("error", "Cannot find requested calculation schema " + calculation_type)

    # if not jsonschema.validate(calc_schema, load_validation_schema('calculation', calculation_type)):
    #     return json_error("error", "Schema failed validation")
    for component in calc_schema['required']:
        if component not in schema['data']:
            return json_error("error", "Missing required data component " + component)
        if 'schema' not in schema['data'][component]:
            return json_error("error", "Missing schema identifier in data component " + component)
        else:
            comp_schema_name = schema['data'][component]['schema']

        cs=build_schema_for_validation(schema['data'][component], schema['units'][component])
        print("Going to validate schema: ", cs)
        if not jsonschema.validate(cs, load_validation_schema(component, comp_schema_name)):
            return json_error("error", "Cannot validate schema %s/%s" % (component, comp_schema_name))
        print("Going to load component schema %s/%s" % (component, comp_schema_name))

    return jsonify("nothing", "yet")
    # d[schema_name] = sch['description']


class Validator:

    def __init__(self):
        pass

    # schema must be in JSON and compatible with provided schema rules
    def validate(self, schema, suppliedjson):
        # sch=json.loads(schema)
        # print("Schema=",sch)
        # sch=json.loads(schema)
        #        f = open("app/static/schema/hera-validation.json", 'r')
        f = open("app/static/validation-schema/hera-validation.json", 'r')
        sch = json.load(f)
        print("We got this json:", suppliedjson)
        try:
            jsonschema.validate(instance=suppliedjson, schema=sch)
            return suppliedjson
        except jsonschema.ValidationError as e:
            return None

    def load_schemafile(self, schema_name):

        pass
