#!/bin/sh
set -xe
rm -Rf ./ex_app
docker run --rm `docker build -q src` tar -cz ex_app | tar -xz
