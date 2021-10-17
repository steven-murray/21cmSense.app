from flask import Flask
from flask import request
from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera
import numpy as np

from . import api


@api.route('/')
def welcome():  # put application's code here
    return 'Welcome to Project 43!'

@api.route('/ping')
def ping():
    return {
        "pong":"",
    }

@api.route("/schema")
def api_return():
    # return a dict as JSON
    # return {"id" : "1", }

    # the schema we want
    return { "id": request.args.get('id'), }


@api.route("/21cm", methods=['GET', 'POST'])
def to_cm_if():
    sensitivity = PowerSpectrum(
        observation=Observation(
            observatory=Observatory(
                antpos=hera(hex_num=7, separation=14, dl=12.12, units="m"),
                beam=GaussianBeam(frequency=135.0, dish_size=14),
                latitude=38 * np.pi / 180.0
            )
        )
    )
    power_std = sensitivity.calculate_sensitivity_1d()
    z = zip([v.value for v in sensitivity.k1d], [v.value for v in power_std])
    return (dict(z))
