#!/bin/bash

ips="1 2 3 4 5"

for itera in $ips; do 
	cmd="gnome-terminal -e \"python3 file_test.py -id ${itera}\""
	echo $cmd
	eval $cmd
done
