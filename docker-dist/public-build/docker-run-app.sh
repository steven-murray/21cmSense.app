#!/bin/bash

# This script starts nginx and the gunicorn WSGI service in the docker container.
# It utilizes the newer gunicorn functionality of directly calling a method within
# a python file.
#
# It is using a unix socket rather than a tcp socket.

# start nginx
service nginx start

# start wsgi app
exec gunicorn --bind=unix:/tmp/gunicorn.sock --workers=4 'app:create_app()'

