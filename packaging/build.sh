#!/bin/sh
set -xe
docker run --rm `docker build -q src` tar -cz ex_app | tar -xz
