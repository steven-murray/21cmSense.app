# Overview
Adding additional JSON schema to support new objects in the 21cmSense library code

Each py21cmSense library call that is made requires some amount of external data that has been
supplied by the user.  In order for the front end to present an appropriate input
form to the user, and for the back end to decode the data and make the appropriate
calls to the library code, controlling JSON schema are used.

In the `static/schema` directory, there are initially four subdirectories containing
schema relating to:
1. calculations
The `calculation` directory contains information for each type of calculation that the
back end is expected to make.  Additional information on calculations can be found in
[add_calculation.md](add_calculation.md).
2. antennas
The `antenna` directory contains schema for different antenna configurations.
Initially, only the `hera` antenna type is supported.
3. beams
The `beam` directory contains schema for different beam configurations.  Initially,
only GaussianBeam beam types are supported.
4. locations
The `location` directory contains schema for different methods of specifying
geographic location.  Currently, only latitude location types are supported.

# File contents
Each JSON file (containing a single JSON object) requires the following top level
keywords:
- `schema`
  - The name of this schema.  This name is used during validation, by the front-end
    code, by calculation schema, etc.
- `description`
  - A user-friendly description of the purpose of this schema.
- `group`
  - The group that this schema belongs to.  Typically the group would be the same
    as the name of the directory in which the file resides.
- `data`
  - The data keyword is a dictionary that contains each of the data fields that the
  user needs to supply in order to satisfy the requirements.
- `units`
  - The units keyword is a dictionary that contains the units for each of the data
  fields (if applicable).  Note that not all data fields have corresponding units
  (they may be dimensionless), and units may contain a `default` field, and must
  contain an `enum` field that lists possible and valid units.

# Example
The following example is for the hera antenna type.

```json
{
  "__comment__": "this is an extension of the JSON schema document and includes 'default' specifier",
  "schema": "hera",
  "description": "Hera-class antenna array",
  "group": "antenna",
  "data": {
    "antenna": {
      "hex_num": {
        "type": "integer",
        "minimum": 3,
        "help": "Number of antennas per side of hexagonal array"
      },
      "separation": {
        "type": "number",
        "minimum": 0,
        "help": "The distance between antennas along a side"
      },
      "dl": {
        "type": "float",
        "minimum": 0,
        "help": "The distance between rows of antennas"
      },
      "required": [
        "hex_num",
        "separation",
        "dl"
      ]
    }
  },
  "units": {
    "antenna": {
      "separation": {
        "type": "string",
        "default": "m",
        "enum": [
          "m",
          "s"
        ]
      },
      "dl": {
        "type": "string",
        "default": "m",
        "enum": [
          "m",
          "s"
        ]
      },
      "required": [
        "separation",
        "dl"
      ]
    }
  }
}
```
