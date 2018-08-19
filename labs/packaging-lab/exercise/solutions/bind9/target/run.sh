#!/bin/bash
LD_LIBRARY_PATH=root/lib/x86_64-linux-gnu:root/usr/lib/x86_64-linux-gnu root/usr/sbin/named -f -d 100 -p 2222 -c root/etc/named/named.conf
