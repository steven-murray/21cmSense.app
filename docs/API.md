# GET

## get an acknowledgement from server

`/api-1.0/ping`

## get schema for function with id

**GET** `/api-1.0/schema`

Response:
``200 OK``

``
{ groups: ['group1', 'group2', 'group3'] }
``


**GET** `/api-1.0/schema/group`

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

HTTP POST to http://backend.server/api-1.0/21cm

```json
{
  "schema": "hera",
  "data": {
    "antenna": {
      "hex_num": 7,
      "separation": 1.2,
      "dl": 3
    },
    "beam": {
      "class": "GaussianBeam",
      "frequency": 100,
      "dish_size": 12
    },
    "latitude": 180
  },
  "units": {
    "antenna": {
      "separation": "m",
      "dl": "m"
    },
    "beam": {
      "frequency": "MHz"
    },
    "location": {
      "latitude": "deg"
    }
  }
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