# Overview
## Adding a new calculation

1. Create a JSON schema with the required data.

Calculation schema are relatively simple and simple refer to the components required to perform the calculation along with a name.

```json
{
  "schema": "2D-sensitivity",
  "group": "calculations",
  "description": "2D Sensitivity",
  "required": [
    "antenna",
    "beam",
    "location"
  ]
}
```

We identify the schema with a unique name (this name will map to a similarly named method),
add a group (which, for calculations, should always be `calculations`), and add a user-friendly textual
description.

The "required" section should include the schema classes required to calculate the desired data. In most
cases, these will always be "antenna", "beam", and "location".

2. In the CalculationFactory class, add a method, prefix with a single underscore, and named the same as the schema name, with all dashes in the schema name transliterated to underscores.
A schema named 2D-sensitivity will map to a method called _2d_sensitivity.  The comparison is case-insensitive.

3. Upon restart, the disk files will be scanned and automatically matched to calculation methods.
