# API

# Users

## Create a new User ID
**POST** `/users`

Body:
```json
{ "username":"the username" }
```

Response: 
``201 Created``

Return:
```json
{
  "uid": "unique uid",
  "username": "user name"
}
```

## Get username for a user ID
**GET** `/users/<userid>/username`

Response:
``200 OK``

Return:
```json
{
  "uid": "unique uid",
  "username": "user name"
}
```


## Delete a user
**DELETE** `/users/<userid>`

Response:
``204 No Content``



# Models

## Create a model ID
**POST** `/models/<userid>/models`

Body:
```json
{
  "modelname": "model name"
}
```

Response:
``201 Created``

Return:
```json
{
  "uid": "unique uid",
  "username": "user name"
  "modelid": "model id",
  "modelname": "model name"
}
```

## Get (retrieve) a model
**GET** `/models/<userid>/models/<modelid>`

Response:
``200 OK``

Return:
```
{
  JSON Schema that was previously stored
}
```

## Update or create a model
**PUT** `/models/<userid>/models/<modelid>`

Body:
```
{
  JSON schema to store
}
```

Response:
``201 OK`` (if model was stored for first time)

``204 No Content`` (if model was updated)

## Delete a model
**DELETE** `/models/<userid>/models/<modelid>`

Response:
``204 No Content``


# schema

## Get a list of schema groups

**GET** `/api-1.0/schema`

Example:

`http://localhost:5000/api-1.0/schema`

Response:
``200 OK``

Return:

```json
[
    "location",
    "calculation",
    "beam",
    "antenna"
]
```

## Get a list of schemas in a group

**GET** `/api-1.0/schema/{group}`

Example:
`http://localhost:5000/api-1.0/schema/antenna`

Response:
``200 OK``

Return:
```json
[
    "hera"
]
```

## Get descriptions for all schemas in a group

**GET** `http://localhost:5000/api-1.0/schema/{group}/descriptions`

Example: `http://localhost:5000/api-1.0/schema/calculation/descriptions`

Response:
``200 OK``

Return:

```json
{
    "1D-cut-of-2D-sensitivity": "1D cut of 2D sensitivity",
    "1D-noise-cut-of-2D-sensitivity": "1D noise of 2D sensitivity",
    "1D-sample-variance-cut-of-2D-sensitivity": "1D sample variance cut of 2D sensitivity",
    "2D-sensitivity": "2D Sensitivity",
    "2D-sensitivity-vs-k": "2D Sensitivity vs k",
    "2D-sensitivity-vs-z": "2D Sensitivity vs z",
    "antenna-positions": "Antenna Positions",
    "baselines-distributions": "Baselines Distributions",
    "calculations": "1D noise cut of 2D sensitivity",
    "k-vs-redshift-plot": "k vs Redshift plot"
}
```


``http://localhost:5000/api-1.0/schema
``

## Get the required elements groups for a calculation

**GET** /api-1.0/schema/calculation/get/baselines-distributions

```json
{
  "schema": "baselines-distributions",
  "group": "calculations",
  "description": "Baselines Distributions",
  "required": [
    "antenna",
    "beam",
    "location"
  ]
}
```


## Get a specific schema from a group

**GET** `/api-1.0/schema/{group}/get/{schema_name}`

Example: `http://localhost:5000/api-1.0/schema/antenna/get/hera`

Response:
``200 OK``

Return:

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

## get an acknowledgement from server

**GET** `/api-1.0/ping`

Response:
``200 OK``

Return:

```json
{
    "pong": ""
}
```


# PUT

# Data Groups

`/api-1.0/calculate`

```
{
  "schema": "schema_name",
  "antenna": {
    "hex_num : int
    "separation" : float
    "separation_units": string
    "dl" : float
    "dl_units": string
    # since we will not pass a Quantity, need separate units for separation and dl (default is the same)
    # "units" : string code for astropy.units.Unit
  },
  "beam": {
    "class": string # ("GaussianBeam", )
    "frequency": float # (units: MHz)
    "dish_size": float # (units: m)
  },
  "latitude": float (units: none (radians): northern hemisphere=positive)
}
```

# Schemas

- default
    - the default and only schema we have right now
    - default is assumed if no schema is supplied in /api-1.0/schema request

# Data fields

## Antenna

```
{
	"antenna": {
		"hex_num : int
		"separation" : float
		"separation_units": string
		"dl" : float
		"dl_units": string
		# since we will not pass a Quantity, need separate units for separation and dl (default is the same)
		# "units" : string code for astropy.units.Unit 
  }
}
```

## Beam

```
{
  "beam": {
  	"class": string ("GaussianBeam", )
	"frequency": float (units: MHz)
	"dish_size": float (units: m)
  }
}
```

## Latitude

```
{
  "latitude": float (units: none (radians): northern hemisphere=positive)
}
```

## Observatory

## Observation

# Example API call

## HTTP POST to http://backend.server/api-1.0/21cm

```json
{
  "calculation": "1D-cut-of-2D-sensitivity",
  "data":{
    "antenna":{
      "schema": "hera",
      "hex_num": 7,
      "separation": 14,
      "dl": 12.02
    },
    "beam":{
      "schema":"GaussianBeam",
      "frequency": 100,
      "dish_size": 14
    },
    "location":{
      "schema": "latitude",
      "latitude": 1.382
    }
  },
  "units":{
    "antenna":{
      "hex_num": "m",
      "separation": "m",
      "dl": "m"
    },
    "beam":{
      "frequency": "MHz",
      "dish_size": "m"
    },
    "location":{
      "latitude": "deg"
    }
  }
}
```

## Returned data

(Series truncated for readability)
Note that Infinity is filtered out

Plot types:
- lines
- scatter
- ...

```json
{
  "title": "2D cut",
  "plottype": "line",,
  "x": [
    0.16499818112915432,
    3.079966047744214,
    3.1349654414539323,
    3.1899648351636505
  ],
  "xlabel": "k [h/Mpc]",
  "xscale": "log",
  "xunit": "littleh / Mpc",
  "y": [
    12.912515880728177,
    19.45343904564521,
    32.12647074134198,
    53.013664937540476
  ],
  "ylabel": "$\\delta \\Delta^2_{21}$",
  "yscale": "log",
  "yunit": "mK2"
}
```

# Schema with separate data and units that validates against previous call

```json
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
        "latitude": {
          "type": "number"
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
              "type": {
                "enum": [
                  "Hz",
                  "Mhz"
                ]
              }
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
              "type": {
                "enum": [
                  "deg",
                  "rad"
                ]
              }
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


```