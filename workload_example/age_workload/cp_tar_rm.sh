#!/usr/bin/env bash
cp $PFAULT_DIRECTOR/workload_example/data/tutorial-initial.tar.gz $CLIENT_LUSTRE_MOUNTPOINT
sleep 60
tar -xzvf $CLIENT_LUSTRE_MOUNTPOINT/tutorial-initial.tar.gz
sleep 60
rm -rf $CLIENT_LUSTRE_MOUNTPOINT/tutorial-initial.tar.gz
