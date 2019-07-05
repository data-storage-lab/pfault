#!/usr/bin/env bash
#Please ~/pfault/pf_virtual_device_manager/virtual_device_manager.sh before runing this script.

#ssh mds_0_user@mds_0_ip
#mdt_0_disk_symbol
#mds_0_tmp_dir

<< EOF

dd if=mdt_n_disk_symbol of=mds_0_tmp_dir/mdt_0_name

EOF


dd if=$PFAULT_DIRECTOR/workload_example/data/FileOne of=$CLIENT_LUSTRE_MOUNTPOINT/FileOne bs=1M count=300 oflag=sync

#to do
#ssh mds_0_user@mds_0_ip
#mdt_0_disk_symbol
#mds_0_tmp_dir

<< EOF

dd if=mds_0_tmp_dir/mdt_0_name of=mdt_n_disk_symbol

EOF


dd if=$PFAULT_DIRECTOR/workload_example/data/FileTwo of=$CLIENT_LUSTRE_MOUNTPOINT/FileTwo bs=1M count=150 oflag=sync


