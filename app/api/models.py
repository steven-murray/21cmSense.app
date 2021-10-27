import numpy as np
import os
from flask import current_app
from flask import jsonify

# from ..ant2.ant2 import ant
# from .. import ant2


# from . import utils

import json
import jsonschema
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera


class Hera:
    pass


class BeamFactoryManager:
    def __init__(self):
        self.d['GaussianBeam'] = GaussianBeamDispatcher

    def get(self, beam_type):
        if beam_type in self.d:
            return self.d[beam_type]
        else:
            return None


class AntennaFactoryManager:
    def __init__(self):
        self.d['hera'] = HeraAntennaDispatcher

    def get(self, antenna_type):
        if antenna_type in self.d:
            return self.d[antenna_type]
        else:
            return None


class BeamDispatcher:
    def __init__(self, beam_json, units_json):
        self.beam_json = beam_json
        self.units_json = units_json


class GaussianBeamDispatcher(BeamDispatcher):
    def __init__(self, beam_json, units_json):
        super().__init__(beam_json, units_json)

    def get(self):
        beam = GaussianBeam(frequency=self.beam_json['frequency'], dish_size=self.beam_json['dish_size'])
        return beam


class AntennaDispatcher:
    def __init__(self, antenna_json, units_json):
        self.antenna_json = antenna_json
        self.units_json = units_json


class HeraAntennaDispatcher(AntennaDispatcher):
    def __init__(self, antenna_json, units_json):
        super().__init__(antenna_json, units_json)

    def get(self):
        j = self.antenna_json
        antpos = hera(hex_num=j['hex_num'], separation=j['separation'], dl=j['separation'], units='m')
        return antpos


class BeamFactory:
    def __init__(self):
        pass

    def get(self, beam_type):
        return BeamFactoryManager().get(beam_type)


class AntennaFactory:
    def __init__(self):
        pass

    def get(self, antenna_type):
        return AntennaFactoryManager().get(antenna_type)


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
                    latitude=38 * np.pi / 180.0
                )
            )
        )

        return sensitivity


def get_schema_names(schemagroup):
    dirs=os.listdir(current_app.root_path+'/static/schema/'+schemagroup)
    # print("schema names")
    schemas=[dir.replace('.json', '') for dir in dirs]
    # for dd in dirs:
    #     dd=dd.replace('.json','')
    #     print(dd)
    # j={}
    # j['required']=list(dirs)
    # return jsonify(j)
    return schemas

def get_schema_groups():
    dirs=os.listdir(current_app.root_path+'/static/schema')
    # print("schema groups")
    # for dd in d:
    #     print(dd)
    return dirs


def get_schema_groups_json():
    d=get_schema_groups()
    j={}
    j['required']=list(d)
    return jsonify(j)

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
