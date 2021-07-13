#!/bin/bash
while true
do
	raspivid -a 12 -t 0 -w 600 -h 480 -ih -fps 30 -l -o tcp://0.0.0.0:8554

done
