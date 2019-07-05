#!/usr/bin/env bash
#generate IO traffic 

FILE=./node1-mnt/test.ext4.node1

sudo dd if=/dev/zero of=$FILE bs=4K count=10 conv=sync
