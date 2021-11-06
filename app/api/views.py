from flask import current_app
from flask import jsonify
from flask import request
import json
import numpy as np
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera
from . import models
from . import api
from flask import current_app
from flask import jsonify

from .models import CalculationFactory, handle_output, get_schema_descriptions_json
from .models import *
from . import errors
from .json_util import json_error


@api.route('/')
def welcome():  # put application's code here
    return 'Welcome to Project 43!'


@api.route('/ping')
def ping():
    return {
        "pong": "",
    }


@api.route('/schemaj')
def api_all_schema():
    models.get_schema_groups()
    return jsonify({'list': 'here'})


@api.route('/schema/<schemagroup>/descriptions')
def schema_descriptions(schemagroup):
    return get_schema_descriptions_json(schemagroup)


@api.route('/customschema', methods=['POST'])
def api_return():
    if request.method == 'POST':
        lst = models.get_schema_groups()

        # we should be posted something like:
        # { "location": "location.json", "beam": "GaussianBeam.json", "antenna": "hera.json" }

        if request.is_json and request.json:
            req = request.get_json()
            for schema_group in lst:
                if schema_group in req:
                    print("json return for component %s=" % schema_group, req[schema_group]);
            return build_composite_schema(req)
        # return jsonify("blah")
        # return current_app.send_static_file('schema/an


@api.route('/schema/<schemagroup>/get/<schemaname>')
def get_schema(schemagroup, schemaname):
    # the schema we want
    return current_app.send_static_file('schema/' + schemagroup + '/' + schemaname + '.json')


@api.route('/schema/<schemagroup>')
def get_schema_group(schemagroup):
    lst = models.get_schema_names(schemagroup)
    return jsonify(lst)


@api.route('/schema', methods=['GET'])
def list_all_schema():
    lst = models.get_schema_groups()
    return jsonify(lst)


@api.route("/test", methods=['GET', 'POST'])
def testtest():
    if request.is_json:
        if request.json:
            thisjson = request.get_data()

            # req = request.get_json()

            schema = """
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "properties": {
    "schema": {
      "type": "string"
    },
    "data": {
      "type": "object",
      "properties": {
        "antenna": {
          "type": "object",
          "properties": {
            "hex_num": {
              "type": "integer"
            },
            "separation": {
              "type": "number"
            },
            "dl": {
              "type": "number"
            }
          },
          "required": [
            "dl",
            "hex_num",
            "separation"
          ]
        },
        "beam": {
          "type": "object",
          "properties": {
            "class": {
              "type": "string"
            },
            "frequency": {
              "type": "number"
            },
            "dish_size": {
              "type": "number"
            }
          },
          "required": [
            "class",
            "dish_size",
            "frequency"
          ]
        },
        "location": {
            "type": "object",
            "properties": {
                "latitude": {
                  "type": "number"
                }
            }
        }
      },
      "required": [
        "antenna",
        "beam",
        "latitude"
      ]
    },
    "units": {
      "type": "object",
      "properties": {
        "antenna": {
          "type": "object",
          "properties": {
            "separation": {
              "type": "string"
            },
            "dl": {
              "type": "string"
            }
          },
          "required": [
            "dl",
            "separation"
          ]
        },
        "beam": {
          "type": "object",
          "properties": {
            "frequency": {
              "type": "string",
              "enum": [ "Hz", "Mhz" ]
            }
          },
          "required": [
            "frequency"
          ]
        },
        "location": {
          "type": "object",
          "properties": {
            "latitude": {
              "type": "string", 
              "enum": [ "deg", "rad" ]
            }
          },
          "required": [
            "latitude"
          ]
        }
      },
      "required": [
        "antenna",
        "beam",
        "location"
      ]
    }
  },
  "required": [
    "data",
    "schema",
    "units"
  ]
}
    """
            # print("type of schema=",type(schema))
            # ss='{"hello":"there"}'
            # sch=json.loads(ss)
            sch = json.loads(schema)
            v = models.Validator()
            req_json = request.get_json()
            if v.validate(sch, req_json):
                print("json validated")
            else:
                print("json failed validation")

            fact = models.Factory()
            sensitivity = fact.go(req_json)
            power_std = sensitivity.calculate_sensitivity_1d()

            for v in sensitivity.k1d:
                print("v.value=", v.value, ", type(v.value)=", type(v.value))
            for v in power_std:
                print("v.value=", v.value, ", type(v.value)=", type(v.value))
            z = zip([v.value for v in sensitivity.k1d], [v.value for v in power_std])
            print(z)
            d = dict(z)
            print("dict=", d)
            print(json.dumps(d))
            return json.dumps(d)

    return jsonify("nothing")


@api.route("/21cm", methods=['POST'])
def call_21cm():

    if request.is_json and request.json:
        req = request.get_json()
        return calculate(req)

    # if request.is_json and request.json:
    #     req = request.get_json()
    #     return build_composite_schema(req)
    # if 'calculation' not in req:
    #     return json_error("error", "no calculation key found in json")
    # else:
    # key = req['calculation']
    # calculation_factory = CalculationFactory()
    # if calculation_factory.knows(key):
    #     calc = calculation_factory.get(key)
    #     return_json = handle_output(calc)
    #     return return_json
    # else:
    #     return json_error("error", "unknown calculation type: " + key)


@api.route("/21cm_default", methods=['GET', 'POST'])
def to_cm_if():
    sensitivity = PowerSpectrum(
        observation=Observation(
            observatory=Observatory(
                antpos=hera(hex_num=7, separation=14, dl=12.12, units="m"),
                beam=GaussianBeam(frequency=135.0, dish_size=14),
                latitude=38 * np.pi / 180.0
            )
        )
    )
    power_std = sensitivity.calculate_sensitivity_1d()
    sens = [v.value for v in sensitivity.k1d]
    powr = [v.value.tostring() for v in power_std]
    for v in power_std:
        print("v=", v.value, " and type=", type(v.value))
    print('sens=', sens)
    print('powr=', powr)
    z = zip([v.value for v in sensitivity.k1d], [v.value for v in power_std])
    print(z)
    print(json.dumps(z))
    return json.dumps(dict(z))
