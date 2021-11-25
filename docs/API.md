# API

## schema

### Get a list of schema groups

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

### Get a list of schemas in a group

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

### Get descriptions for all schemas in a group

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

### Get the required elements groups for a calculation

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


### Get a specific schema from a group

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

```json
{
  "x": [
    0.05499939370971811,
    0.10999878741943622,
    0.16499818112915432,
    0.21999757483887245,
    0.27499696854859057,
    0.3299963622583087,
    0.38499575596802676,
    0.4399951496777449,
    0.494994543387463,
    0.5499939370971811,
    0.6049933308068992,
    0.6599927245166173,
    0.7149921182263353,
    0.7699915119360535,
    0.8249909056457716,
    0.8799902993554898,
    0.9349896930652078,
    0.9899890867749259,
    1.044988480484644,
    1.0999878741943623,
    1.1549872679040805,
    1.2099866616137984,
    1.2649860553235166,
    1.3199854490332348,
    1.3749848427429527,
    1.429984236452671,
    1.484983630162389,
    1.5399830238721073,
    1.5949824175818252,
    1.6499818112915434,
    1.7049812050012616,
    1.7599805987109796,
    1.8149799924206977,
    1.869979386130416,
    1.9249787798401339,
    1.979978173549852,
    2.03497756725957,
    2.089976960969288,
    2.1449763546790064,
    2.1999757483887246,
    2.2549751420984427,
    2.309974535808161,
    2.3649739295178787,
    2.419973323227597,
    2.474972716937315,
    2.529972110647033,
    2.5849715043567514,
    2.6399708980664696,
    2.6949702917761873,
    2.7499696854859055,
    2.8049690791956237,
    2.859968472905342,
    2.91496786661506,
    2.969967260324778,
    3.0249666540344964,
    3.079966047744214,
    3.1349654414539323,
    3.1899648351636505
  ],
  "xlabel": "k [h/Mpc]",
  "xscale": "log",
  "xunit": "littleh / Mpc",
  "y": [
    Infinity, 
    Infinity,
    12.912515880728177,
    19.45343904564521,
    32.12647074134198,
    53.013664937540476,
    83.31495300123542,
    123.67964944268913,
    175.49621222887464,
    240.19132213905047,
    319.1999168689312,
    413.95492397302746,
    525.8878375169154,
    656.4319695994517,
    807.0276489658172,
    979.0957080145427,
    1174.0676374001425,
    1393.3749279239394,
    1638.449070527133,
    1910.7215562728404,
    2211.628099178302,
    2542.6116481449676,
    2905.0880134032686,
    3300.488686407197,
    3730.2451586434754,
    4195.788921624284,
    4698.551466881734,
    5239.964285963664,
    5821.458870430374,
    6444.466711852103,
    7110.41930180706,
    7820.775293156087,
    8576.945273414734,
    9380.354476553095,
    10232.434394225167,
    11134.61651807939,
    12088.332339759538,
    13095.013350905463,
    14156.091043153674,
    15272.996908137862, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity, 
    Infinity
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