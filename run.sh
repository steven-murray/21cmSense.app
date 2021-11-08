#!/bin/bash

python3 -m venv env
. env/bin/activate

for arg in "$@"
do
  case $arg in
    "--install")
      python3 -m pip install -r requirements.txt;;
    "--test" )
      python -m pytest;;
    "--dev" )
      redis-server
      export FLASK_APP=app
      export FLASK_ENV=development
      flask run;;
    "--prod" )
      redis-server
      export FLASK_APP=app
      export FLASK_ENV=production
      flask run;;
  esac
done
