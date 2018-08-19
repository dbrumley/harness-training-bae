#!/bin/bash
set -eou pipefail

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
    cat > $KEYLOC <<- EOM
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA7ETlh3kuV/rQYHmOOeapc0Bwgx93OxnVY2wR1FnbzrZNhX86
4k63OXDnXKZKC1VVxd6mPAGcK8jivLeHSeaO1WCtInCtoLLHuLu+WJ6PdwdIcxz/
g9n89umcGU65EiPN2aj7llcW05C9Jn2N8Ds/6hAUS49K5VfM2Oz5A45isRVWcd6g
nvs/1HSJto3jzbnMLGKtVTyqzA5uYVYpv7yyNJAqJm0IjgnlM1EReT1RKMFSGClp
WnTm3VgiI60OqWnVR1Gm2GUpy1WS6e5K7naEIrat73QluBV3AFfYraiAmn7BzUKA
VwBoCfNcPeOvIar88zXuUdWg2IzGIts003pRiwIDAQABAoIBAQCXmzoBbSPstndh
gH5f7v/KgY3wxY8XcGM50c27ChH+mYIy6Eobj1EI3cbH77hRf2dzeYQHuyy/975u
RAHezL/YcZmHIPB4zl9Tzby9VrlOMnEt1Gys6YLl2U8d+iLNXgYn5cPSW329MgH9
odEjVpGTms+7EG6JrYY3qA+9VW9EmuW/gg5I81/ZAaoiYBfKvASaeqzFATQtmia6
TQLJTpvnsPJ4ziM5tpRw6eQdYs7E7fTlZyD935LgXOCu5u8fqUpG5UAZooMsZGT8
kqbzvqUH7Dof+CrJlQB8gWeUTT0L/sKYK7vTp+i6MJ0NqFb86Drv4lMIJxxvUOSn
/3cLEjOJAoGBAP2yuns5dQNSmcdP8VHQGkD5/TSpNjAvqJR/UtUh4kB0vLwkG3PJ
vKosH8fRekJdLndH2G1w6rli5TIjkfaAjOHONlTkfv13oIcjVI5OaMomedBaX1aO
MH8XhwcmzLBxWfEnwru2pRZuOhtLMfaC8OBYOlZCibH43FUOHlbK3TBnAoGBAO5p
r249gDFQ5TFNvhfrAjVzWuCkrxKcv7nMdvNx8osuadDS4wZa/PcYE8/EwegDUz2n
uv8VeF+BmOYzZuPv21BbGqHb0z+D+mMVbjUk7E6j1St6Pt0RtChvtFWS4fcsqFIn
UHGERsPN3WHCIBQbwHyCEJi4a5QniFZKU2Zwuk89AoGAejWoo0dwWKNntJ2L8A9B
Nl+2W7HPirLKkI4tBsKFzOrvJ+p01vgtTARpYsZEEMf2ZDtVxJKKX7eGFPsRix8t
vnCpt4dCrTL9P1wDlXGsBQU31OhT2MwyDGb3ArjsDWrtGsA+jFJVgFKk5xT4Annd
MxUNNRRkZDkvWkGs175tgq0CgYAHY3ETWoaRgK9Jot4kQZ006NlFIvVl/0OVz3dU
PhDFLXAMD60HcmRqh+19P9y+gvPeckdCRnkPhKWnZKpon/NM/zXJFFXsnvtwfKaI
sRc9rKgbi9NM6JKLukJ9cGreTRz+RsegbPgAc23L7McvuFhzw1geU4DJ+5unCPCi
uRWdBQKBgQDbQDmQnURTRr5TDUCc21HjmFa+0h3cBKf4m6pO4tEo4DjEIeKd8FQu
5ptOWLbLuVDw4v5wvgM6Ml+hGj0X4xsfwHFULhCz9Yr0ff6OtOk/neobNqzdu3MU
sYatfdmddtvvlgKWfTm5puf7RjhBq3xyqBvVFlkm4tjs2bhU45M4gA==
-----END RSA PRIVATE KEY-----
EOM
    #echo key > $KEYLOC
    chmod 400 $KEYLOC
fi

# port forward and connect
USER=user
HOST=$1
#INTERNAL_IP=$(ssh -i $KEYLOC $USER@$HOST hostname -I | cut -f 1 -d ' ')
INTERNAL_IP=127.0.0.1
INTERNAL_UI_PORT=$(ssh -i $KEYLOC $USER@$HOST kubectl get svc -o go-template=\'{{range .items}}{{range.spec.ports}}{{if .nodePort}}{{.nodePort}}{{\"\\n\"}}{{end}}{{end}}{{end}}\')

echo [+] Forwarding $INTERNAL_IP:$INTERNAL_UI_PORT
echo [+] Port forwarding done, connect to http://localhost:30001 for the Mayhem web UI
echo [+] SSH-ing into your vm, port forwarding will stay up as long as your session is running
ssh -i $KEYLOC $USER@$HOST -L 30001:$INTERNAL_IP:$INTERNAL_UI_PORT
