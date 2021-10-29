from flask import jsonify

def json_error(errorcode, msg):
    return jsonify({errorcode: msg})
