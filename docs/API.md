# API

# Users

## Create a new User ID
**POST** `/users`

Response:
``201 Created``

Return:
```json
{
  "userid": "unique userid",
}
```

Response:
``400 Bad Request`` (if JSON is invalid)


## Delete a user
**DELETE** `/users/<userid>`

Response:
``204 No Content``

Response:
``404 Not Found`` (if userid does not exist)

NOTE: Deleting a user deletes ALL of their stored models.

# Models

## Create a new model
**POST** `/users/<userid>/models`

Body:
```
{
  "modelname": "model name",
  "data": { json schema }
}
```

Response:
``201 Created`` (if created successfully)

Return:
```json
{
  "userid": "unique userid",
  "modelid": "model id",
  "modelname": "model name"
}
```

Response:
``400 Bad Request`` (if JSON is invalid)

Response:
``404 Not Found`` (if userid does not exist)

Response:
``409 Conflict`` (if model name already exists)

Return:
```json
{"error":"Model name already exists"}
```


## Get a list of models
**GET** `/users/<userid>/models`

Response:
``200 OK`` (if (userid, model) pair exists)

Return:
```json
{
  "uuid": "user's UUID",
  "models": [
    {
      "modelname": "model 1 name",
      "modelid": "model 1 ID"
    },
    {
      "modelname": "model 2 name",
      "modelid": "model 1 ID"
    }
  ]
}
```

Response:
``404 Not Found`` (if userid does not exist)

## Get (retrieve) a model
**GET** `/users/<userid>/models/<modelid>`

Response:
``200 OK`` (if (userid, model) pair exists)

Return:
```json
{
  "modelname": "name of model",
  "data": "JSON Schema that was previously stored"
}
```

Response:
``404 Bad Request`` (if modelID or userID do not exist)

## Update a model
**PUT** `/users/<userid>/models/<modelid>`

Body:
```json
{
  "modelname": "name of model",
  "data": "JSON schema to store"
}
```

Response:
``204 No Content`` (if model was updated)

Response:
``400 Bad Request`` (if JSON is invalid)

Response:
``404 Not Found`` (if userid or modelid does not exist)

ref: [HTTP return code decision tree](https://github.com/for-GET/http-decision-diagram/blob/master/httpdd.graffle.png)


## Delete a model
**DELETE** `/users/<userid>/models/<modelid>`

Response:
``204 No Content`` (in all cases, including for invalid userid or modelid)

## Calculate from a saved model

**POST** `/21cm/model/<modelid>`

Body:
```json
{"calculation":"name-of-calculation"}
```

Returns:

``200 OK`` (if model exists)

Response body contains data or error if appropriate

``404 Not Found`` (if model id does not exist)

# Antenna position data

## Create new antenna position data
**POST** `/users/<userid>/antpos`

Body:
```
{
  "antpos": "antenna position data name",
  "data": { "base64 encoded CSV file" }
}
```

Notes:
The CSV file shall be comma separated, UTF-8 encoded with either
two or three floating point numbers per line.  All lines with two
values will have the third (missing) value replaced with 0.0.


Response:
``201 Created`` (if created successfully)

Return:
```json
{
  "userid": "unique userid",
  "antposid": "antenna position data id",
  "name": "antenna position data name"
}
```

Response:
``400 Bad Request`` (if JSON is invalid)

Response:
``404 Not Found`` (if userid does not exist)

Response:
``409 Conflict`` (if antenna position data name already exists)

Return:
```json
{"error":"Antenna position data name already exists"}
```


## Get a list of stored antenna positions
**GET** `/users/<userid>/antpos`

Response:
``200 OK`` (if (userid, antpos) pair exists)

Return:
```json
{
  "uuid": "user's UUID",
  "antpos": [
    {
      "name": "antpos 1 name",
      "antposid": "antpos 1 ID"
    },
    {
      "name": "antpos 2 name",
      "antposid": "antpos 1 ID"
    }
  ]
}
```

Response:
``404 Not Found`` (if userid does not exist)

## Get (retrieve) antenna position data
**GET** `/users/<userid>/antpos/<antposid>`

Response:
``200 OK`` (if (userid, antposid) pair exists)

Return:
```json
{
  "name": "name of antenna position data",
  "data": "Antenna position data that was previously stored"
}
```

Response:
``404 Bad Request`` (if antposID or userID do not exist)

## Update antenna position data
**PUT** `/users/<userid>/antpos/<modelid>`

Body:
```json
{
  "name": "name of antenna position data",
  "data": "CSV triplet or double to store"
}
```

Response:
``204 No Content`` (if antenna position data was updated)

Response:
``400 Bad Request`` (if JSON is invalid)

Response:
``404 Not Found`` (if userid or antposid does not exist)

ref: [HTTP return code decision tree](https://github.com/for-GET/http-decision-diagram/blob/master/httpdd.graffle.png)


## Delete antenna position data
**DELETE** `/users/<userid>/antpos/<antposid>`

Response:
``204 No Content`` (in all cases, including for invalid userid or antposid)


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

#### Credits

Project 43 - Web Application for Radio Astronomy Sensitivity
Author: Brian Pape
Revision: 0.1
