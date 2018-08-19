#!/bin/sh
set -xe
cd "`dirname "$0"`"
LD_LIBRARY_PATH="`pwd -P`" exec ./example1 "$@"
