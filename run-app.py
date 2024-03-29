"""run-app.py."""

import argparse
import ipaddress

from app import create_app

parser = argparse.ArgumentParser(
    description="Web interface for py21cmSense astronomy software"
)
parser.add_argument("--port", default=8080, type=int)
parser.add_argument(
    "--bind-address",
    dest="bind_address_raw",
    default="0.0.0.0",
    type=ipaddress.IPv4Address,
)

# flask run passes us the run argument.
parser.add_argument("flask_run", help=argparse.SUPPRESS)
args = parser.parse_args()

bind_address = args.bind_address_raw.exploded
print("Binding to interface ", bind_address)
print("Starting app on port ", args.port)

if __name__ == "__main__":
    app = create_app()
    app.run(host=bind_address, port=args.port, debug=True)
else:
    print("Note: WSGI application should be started with 'wsgi.py'")
