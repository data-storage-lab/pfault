#!/bin/sh
#ssh mds_1_user@mds_1_ip
#lustre_name-MDT0000
lctl lfsck_start --all --device lustre-MDT0000 --create_ostobj on --create_mdtobj on --orphon
check_workload_n_path
