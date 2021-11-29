#!/bin/bash

python3 -m venv venv
source venv/bin/activate

for arg in "$@"
do
  case $arg in
    "--install")
      python3 -m pip install -r requirements.txt

       # stage 21cmSense code
      git clone https://github.com/steven-murray/21cmSense

      # install py21cmsense library egg into our venv site-packages
      cd 21cmSense && python ./setup.py install && cd ..
      ;;
    "--test" )
      python -m pytest;;
    "--dev" )
      # redis-server
      export FLASK_APP=app
      export FLASK_ENV=development
      flask run;;
    "--prod" )
      # redis-server
      export FLASK_APP=app
      export FLASK_ENV=production
      flask run;;
  esac
done
