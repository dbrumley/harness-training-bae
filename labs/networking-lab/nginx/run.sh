#!/bin/sh
LD_LIBRARY_PATH=./root/lib ./root/nginx -p . -c root/nginx.conf
