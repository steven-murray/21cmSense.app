import json
from pathlib import Path

import attr
import numpy as np
import py21cmsense as sense
from astropy import units as un

# This is the thing we need to create and save in our cache in the end.
TOP_LEVEL_OBJECT = sense.PowerSpectrum

if __name__ == "__main__":
    top_level = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://21cmSense.app/object-schema.json",
        "title": "PowerSpectrum Sensitivity",
        "description": "A PowerSpectrum",
        "type": "object",
        "properties": {},
        "required": [],
    }

    def get_python_type(param):
        # Hard-code some corner cases.
        if param.name == "_antpos":
            return "antpos"
        elif param.name == "frequency":
            return un.MHz
        elif param.name == "obs_duration":
            return "obs_duration"
        elif param.name == "dish_size":
            return un.m

        elif param.default is None:
            return None

        if param.default == attr.NOTHING:
            # Check the validator(s)...
            if param.validator is not None and isinstance(
                param.validator, attr.validators._InstanceOfValidator
            ):
                tp = param.validator.type
            else:
                raise ValueError(f"Dang it, can't deal with this param: {param}")
        elif isinstance(param.default, un.Quantity):
            return param.default.unit
        else:
            tp = type(param.default)

        # Another special case
        if tp == sense.beam.PrimaryBeam:
            return sense.beam.GaussianBeam

        return tp

    def get_type(tp):
        if tp in (int, float) or isinstance(tp, un.UnitBase):
            return "number"
        elif tp == bool:
            return "boolean"
        elif attr.has(tp) or tp == "antpos":
            return "object"
        elif tp is None:
            return "null"
        elif tp == "obs_duration":
            return ["null", "number"]
        elif tp == str:
            return "string"
        else:
            raise ValueError("Don't know how to deal with type: ", tp)

    def fullname(cls):
        module = cls.__module__
        if module is None or module == str.__class__.__module__:
            return cls.__name__
        return module + "." + cls.__name__

    def write_object(dct, cls):
        dct["className"] = fullname(cls)

        for param in attr.fields(cls):
            if isinstance(param.default, np.ndarray):
                continue

            tp = get_python_type(param)
            json_type = get_type(tp)

            dct["properties"][param.name] = {
                "description": param.name,  # OK, this could be better...
                "type": json_type,
            }

            if param.default != attr.NOTHING:
                if isinstance(param.default, un.Quantity):
                    default = param.default.value
                elif isinstance(param.default, attr.Factory):
                    default = None
                else:
                    default = param.default

                dct["properties"][param.name]["default"] = default
            else:
                dct["required"].append(param.name)

            if isinstance(tp, un.UnitBase):
                dct["properties"][param.name]["unit"] = str(tp)

            if tp == "antpos":
                dct["properties"][param.name]["properties"] = {
                    "hex_num": {
                        "description": "Number of antennas on each side of the hex",
                        "default": 7,
                        "type": "number",
                    },
                    "separation": {
                        "description": "Separation between antennas on a side, meters.",
                        "default": 14,
                        "type": "number",
                        "unit": "m",
                    },
                }
            elif json_type == "object":
                dct["properties"][param.name]["properties"] = {}
                dct["properties"][param.name]["required"] = []

                write_object(dct["properties"][param.name], tp)

    write_object(top_level, TOP_LEVEL_OBJECT)

    with open(
        Path(__file__).parent / "app/static/schema/object-schema.json", "w"
    ) as fl:
        json.dump(top_level, fl, indent=4)
