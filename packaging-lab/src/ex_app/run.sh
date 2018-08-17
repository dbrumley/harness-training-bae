#!/bin/sh
cd "`dirname "$0"`"

export USER=`whoami`
cd app_dir
./ex_app config
