#!/usr/bin/env bash

#./THISFILE sdb

if (( $# > 0 )); then
    drive=$1
else
    drive=sdb
fi

drive_size=`cat /sys/block/${drive}/size`
drive_model=`cat /sys/block/${drive}/device/model` # | sed s//-/g`

echo "drive: /dev/$drive"
echo "drive_model: $drive_model"
echo "drive_size: $drive_size"
