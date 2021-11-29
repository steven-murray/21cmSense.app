# import app.api
# import app
from app.api.models import *



def test_get_schema_descriptions():
    # a=app.context()
    # get_schema_descriptions('calculation')
    assert True

def test_one_d_cut():
    input_json="""{
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
}"""
    return_json=one_d_cut(input_json)
    assert True

def test_repeatable_hash():
    input_json = """{
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
    }"""
    return_json = one_d_cut(input_json)
    assert True

# change dl from 12.02 to 12.03
def test_hash_variance():
    input_json = """{
      "calculation": "1D-cut-of-2D-sensitivity",
      "data":{
        "antenna":{
          "schema": "hera",
          "hex_num": 7,
          "separation": 14,
          "dl": 12.03
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
    }"""
    return_json = one_d_cut(input_json)
    assert True


# "antenna" group is missing "schema" keyword
def test_missing_value():
    input_json = """{
      "calculation": "1D-cut-of-2D-sensitivity",
      "data":{
        "antenna":{
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
    }"""
    return_json = one_d_cut(input_json)
    assert True

# "antenna" group is missing "hex_num" keyword
def test_missing_value_2():
    input_json = """{
      "calculation": "1D-cut-of-2D-sensitivity",
      "data":{
        "antenna":{
          "schema": "hera",
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
    }"""
    return_json = one_d_cut(input_json)
    assert True

# "antenna" group is completely missing
def test_missing_group():
    input_json = """{
      "calculation": "1D-cut-of-2D-sensitivity",
      "data":{
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
    }"""
    return_json = one_d_cut(input_json)
    assert True

