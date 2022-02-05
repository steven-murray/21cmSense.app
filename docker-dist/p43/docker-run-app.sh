#!/bin/bash

# start nginx
service nginx start

# start wsgi app
exec gunicorn --bind=unix:/tmp/gunicorn.sock --workers=4 'app:create_app()'

