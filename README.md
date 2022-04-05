# SER401-Project43

[![GitHub Actions Workflow](label=Build&Deploy)](https://github.com/bpape1usa/SER401-Project43/actions/workflows/github-actions.yml)

[![Netlify Workflow](label=Netlify)](https://app.netlify.com/sites/21cmsense/deploys)

[![execute remote ssh to pull updates from master](https://github.com/bpape1usa/SER401-Project43/actions/workflows/backend-deploy.yml/badge.svg)](https://github.com/bpape1usa/SER401-Project43/actions/workflows/backend-deploy.yml)

[![.github/workflows/github-actions.yml](https://github.com/bpape1usa/SER401-Project43/actions/workflows/github-actions.yml/badge.svg)](https://github.com/bpape1usa/SER401-Project43/actions/workflows/github-actions.yml)

**Summary**
	Project 43 is a web application targeted to the scientific and educational communities of radio astronomers and radio astronomer educators.  
The Project 43 sponsors wish to provide a more user-friendly interface to existing scientific code, 21cmSense - proven Python code that generates 
estimates of the sensitivity of different radio telescope configurations to signals coming from the very early Universe -  to broaden the potential 
audience for the software.  Project 43's web-based interface will run on commodity hosting platforms and/or ASU servers and will provide a pipeline 
with a user-friendly interface on the front end and API-driven integration with legacy code on the back end.

## Resources

**GitHub Repos**
		https://github.com/bpape1usa/SER401-Project43.git
		
**TravisCI**
		https://app.travis-ci.com/github/bpape1usa/SER401-Project43
		
**Taiga Board**
		https://tree.taiga.io/project/lclindbe-team43/backlog
		
## Pre-requisite

** clone repo**
git clone git@github.com:bpape1usa/SER401-Project43.git

**python-3.10**

**venv virtual environment**
python3 -m venv venv
source venv/bin/activate

**21cmSense**
		proven Python code that generates estimates of the sensitivity of different radio telescope configurations to signals coming from the very early Universe.
		
```
git clone https://github.com/steven-murray/21cmSense
cd 21cmSense
pip install .
```


## Post-requisite

## Running the Python/Flask back end application

### Standalone (non-production) mode
```text
cd SER401-Project43
source venv/bin/activate
python project43.py
```


Usage:
```text
usage: project43.py [-h] [--port PORT] [--bind-address BIND_ADDRESS_RAW]

Web interface for py21cmSense astronomy software

optional arguments:
  -h, --help            show this help message and exit
  --port PORT
  --bind-address BIND_ADDRESS_RAW
```


### Production mode (docker container)

`docker run -d -p8081:80 p43:latest`

# Notes
use of the port publish parameter:
[local bind addr:]local_port:container_port[/protocol]

So to bind port 80 of the container (where nginx is listening) to port 8081 on the local machine,
listening on 0.0.0.0 (all interfaces), use `-p 8081:80/tcp`.

-d detaches the container after run


To build a docker container for running the application, using `nginx` as a webserver utilizing the `wsgi` interface to the python code, please see the README.md file in the docker-dist directory.


## How to run the Web application 

Repos Path : \repos\SER401-Project43

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.


### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

