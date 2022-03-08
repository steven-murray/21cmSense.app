#!/bin/bash
docker container rm `docker container list -a | grep Exited|awk '{print $1}'`
