#!/bin/sh

#input mgt_n_names and/or mdt_n_names and/or ost_n_names 
#ssh mgs/mds/oss_n_user@mgs/mds/oss_n_ip for each
#mgt/mdt/ost_n_disk_symbol
#mgs/mds/oss_n_tmp_dir

<< EOF

cd tmp_space_dir
dd if=mdt_n_disk_symbol of=mdt_n_name

EOF

rollback_workload_n_path

#ssh mgs/mds/oss_n_user@mgs/mds/oss_n_ip for each
#mgt/mdt/ost_n_disk_symbol
#mgs/mds/oss_n_tmp_dir

<< EOF

cd tmp_space_dir
dd if=mdt_n_name of=mdt_n_disk_symbol 

EOF
