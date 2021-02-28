#!/bin/bash


DOWN_TIME=$((10 + $RANDOM % 20))
echo "MDS sleep!"
ifconfig enp0s3 down
echo "$DOWN_TIME"
sleep $DOWN_TIME
ifconfig enp0s3 up
echo "MDS wake up!"
