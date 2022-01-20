from flask import jsonify

def json_error(errorcode, msg):
    return jsonify({errorcode: msg})

#def json_complex_error(errorcode, msg, **kwargs):
