#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Usage: $0 <symbol> <interval>"
	exit 1
fi

SYMBOL="$1"
INTERVAL="$2"

python3 src ${SYMBOL} ${INTERVAL}
