#!/bin/sh
cd "`dirname "$0"`"

export EAPP_RESOURCES="`pwd -P`/resources"
export CONFIG_XML=./config.xml
export LD_LIBRARY_PATH="`pwd -P`/libs"

./ex_app run "$@"
