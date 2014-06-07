#!/bin/sh

PAUTH=
#IIURL=http://51t.ru/u/point
IIURL=http://127.0.0.1:62220/u/point

wget -O - $IIURL/$PAUTH/$(cat $1)
