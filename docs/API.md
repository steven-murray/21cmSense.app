# GET
## get an acknowledgement from server
`/api-1.0/ping`

## get schema for function with id
`/api-1.0/schema?schema=id`

# PUT
# Data Groups

`/api-1.0/calculate`

```json
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

```json
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

```json
{
  "beam": {
  	"class": string ("GaussianBeam", )
	"frequency": float (units: MHz)
	"dish_size": float (units: m)
  }
}
```

## Latitude

```json
{
  "latitude": float (units: none (radians): northern hemisphere=positive)
}
```



## Observatory
## Observation


