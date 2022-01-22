#
# test_models.py
#

# import app.api
import app
from app.api.models import *
from app.api.models import *



# {'x': (0.16499818112915432, 0.21999757483887245, 0.27499696854859057, 0.3299963622583087, 0.38499575596802676, 0.4399951496777449, 0.494994543387463, 0.5499939370971811, 0.6049933308068992, 0.6599927245166173, 0.7149921182263353, 0.7699915119360535, 0.8249909056457716, 0.8799902993554898, 0.9349896930652078, 0.9899890867749259, 1.044988480484644, 1.0999878741943623, 1.1549872679040805, 1.2099866616137984, 1.2649860553235166, 1.3199854490332348, 1.3749848427429527, 1.429984236452671, 1.484983630162389, 1.5399830238721073, 1.5949824175818252, 1.6499818112915434, 1.7049812050012616, 1.7599805987109796, 1.8149799924206977, 1.869979386130416, 1.9249787798401339, 1.979978173549852, 2.03497756725957, 2.089976960969288, 2.1449763546790064, 2.1999757483887246),
#  'y': (12.912515880728177, 19.45343904564521, 32.12647074134198, 53.013664937540476, 83.31495300123542, 123.67964944268913, 175.49621222887464, 240.19132213905047, 319.1999168689312, 413.95492397302746, 525.8878375169154, 656.4319695994517, 807.0276489658172, 979.0957080145427, 1174.0676374001425, 1393.3749279239394, 1638.449070527133, 1910.7215562728404, 2211.628099178302, 2542.6116481449676, 2905.0880134032686, 3300.488686407197, 3730.2451586434754, 4195.788921624284, 4698.551466881734, 5239.964285963664, 5821.458870430374, 6444.466711852103, 7110.41930180706, 7820.775293156087, 8576.945273414734, 9380.354476553095, 10232.434394225167, 11134.61651807939, 12088.332339759538, 13095.013350905463, 14156.091043153674, 15272.996908137862),
#  'xunit': 'littleh / Mpc', 'yunit': 'mK2', 'title': '1D cut', 'plottype': 'line', 'xlabel': 'k [h/Mpc]', 'ylabel': '$\\delta \\Delta^2_{21}$', 'xscale': 'log', 'yscale': 'log'}
def test_one_d_cut():
    input_json_str = """{
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
    input_json = json.loads(input_json_str)
    return_json = one_d_cut(input_json)
    print(return_json)
    assert return_json['x'][0] == 0.16499818112915432
    assert return_json['y'][0] == 12.912515880728177
    for k in ('xunit', 'yunit', 'title', 'plottype', 'xlabel', 'ylabel', 'xscale', 'yscale'):
        assert k in return_json

# should get same result from same input
def test_repeatable_hash():
    input_json_str1 = """{
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
    input_json_str2 = """{
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

    input_json1 = json.loads(input_json_str1)
    input_json2 = json.loads(input_json_str2)

    testapp = app.create_app('default')

    with testapp.test_request_context('/21cm/schema'):

        return_json1 = calculate(input_json1)
        return_json2 = calculate(input_json2)

        assert return_json1.get_json() == return_json2.get_json()


# change dl from 12.02 to 12.03
def test_hash_variance():
    input_json_str1 = """{
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
    input_json_str2 = """{
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

    input_json1 = json.loads(input_json_str1)
    input_json2 = json.loads(input_json_str2)

    testapp = app.create_app('default')

    with testapp.test_request_context('/21cm/schema'):

        return_json1=calculate(input_json1)
        return_json2=calculate(input_json2)
        assert not return_json1 == return_json2


# "antenna" group is missing "schema" keyword
def test_missing_value():
    input_json_str = """{
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
    input_json = json.loads(input_json_str)
    # return_json = one_d_cut(input_json)
    assert True


# "antenna" group is missing "hex_num" keyword
def test_missing_value_2():
    input_json_str = """{
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
    input_json = json.loads(input_json_str)
    # return_json = one_d_cut(input_json)
    assert True


# "antenna" group is completely missing
def test_missing_group():
    input_json_str = """{
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
    input_json = json.loads(input_json_str)
    # return_json = one_d_cut(input_json)
    assert True
