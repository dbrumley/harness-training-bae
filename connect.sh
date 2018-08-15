#!/bin/bash
set -eoux pipefail

if [ "$#" -ne 1 ]; then
    echo "ERROR: Must provide host ip"
    echo
    echo "Usage: ./`basename $0` host"
    exit 0
fi

KEYLOC=~/.ssh/mayhem-training
# create private key
if [ ! -f $KEYLOC ]; then
    echo [+] Creating SSH key
    #TODO: insert key here
    #echo key > $KEYLOC
    sudo chmod 400 $KEYLOC
fi

# port forward and connect
USER=user
HOST=$1
INTERNAL_IP=10.142.0.2
INTERNAL_UI_PORT=31299

echo [+] Port forwarding done, connect to http://localhost:8081 for the Mayhem web UI
echo [+] SSH-ing into your vm, port forwarding will stay up as long as your session is running
ssh $USER@$HOST -L 8081:[::1]:$INTERNAL_UI_PORT 
