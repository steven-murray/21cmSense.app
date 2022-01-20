from app import create_app
import sys
import argparse
import ipaddress

# from mod_main import mod_main as main_blueprint
# app.register_blueprint(main_blueprint)

# from . import views, errors

parser = argparse.ArgumentParser(description="Web interface for py21cmSense astronomy software")
parser.add_argument('--port', default=8080, type=int)
parser.add_argument('--bind-address', dest="bind_address", default='0.0.0.0', type=ipaddress.IPv4Address)
args = parser.parse_args()

app = create_app('default')

print("Binding to interface ", args.bind_address)
print("Starting app on port ", args.port)

if __name__ == '__main__':
    app.run(host=args.bind_address, port=args.port, debug=True)
