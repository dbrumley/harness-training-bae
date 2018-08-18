#!/bin/sh
cd "`dirname "$0"`"

export EAPP_RESOURCES="`pwd`/resources"
export CONFIG_XML="`pwd`/config.xml"
export LD_LIBRARY_PATH="`pwd`/libs"

./ex_app run "$@"
