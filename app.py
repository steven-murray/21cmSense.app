from app import create_app
import sys
import argparse
import ipaddress

# from mod_main import mod_main as main_blueprint
# app.register_blueprint(main_blueprint)

# from . import views, errors

parser = argparse.ArgumentParser(description="Web interface for py21cmSense astronomy software")
parser.add_argument('--port', default=8080, type=int)
parser.add_argument('--bind-address', dest="bind_address_raw", default='0.0.0.0', type=ipaddress.IPv4Address)
args = parser.parse_args()

bind_address = args.bind_address_raw.exploded
print("Binding to interface ", bind_address)
print("Starting app on port ", args.port)

app = create_app('default')

if __name__ == '__main__':
    app.run(host=bind_address, port=args.port, debug=True)
