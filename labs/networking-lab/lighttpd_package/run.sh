#!/bin/bash
LD_LIBRARY_PATH=./root/lib/x86_64-linux-gnu:./root/usr/lib/x86_64-linux-gnu ./root/usr/sbin/lighttpd -D -f ./root/etc/lighttpd/lighttpd.conf -m ./root/etc/lighttpd/modules
