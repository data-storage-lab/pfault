#!/usr/bin/env bash
#simple fs worklod

#$MNT is the mount point of the fs to test
#MNT defined in pfe_config.sh


FILE=$MNT/test.node1 
sudo dd if=/dev/zero of=$FILE bs=4K count=20 conv=sync
