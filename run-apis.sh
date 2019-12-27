#!/bin/bash

ips="127.0.0.2 127.0.0.3 127.0.0.4 127.0.0.5"

for itera in $ips; do 
	cmd="gnome-terminal -e \"python3 rest.py -i ${itera}\""
	echo $cmd
	eval $cmd
done
