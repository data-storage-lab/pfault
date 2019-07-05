#!/bin/bash

export PFAULT_DIR=/pfault
export LUSTRE_NAME=(lustre)
export ROLLBACK_WORKLOAD_CNT=1
export ROLLBACK_WORKLOAD=(/pfault/workload_example/rollback_workload/rollback_workload.sh)
export AGE_WORKLOAD_CNT=2
export AGE_WORKLOAD=(/pfault/workload_example/age_workload/cp_tar_rm.sh /pfault/workload_example/momtage-m101.sh)
export VERIFIABLE_WORKLOAD_CNT=1
export VERIFIABLE_WORKLOAD=(/pfault/workload_example/verifiable_workload/wikiw_init.sh)
export CHECK_WORKLOAD_CNT=1
export CHECK_WORKLOAD=(/pfault/workload_example/check_workload/wikir.sh /pfault/workload_example/check_workload/wikiw-async.sh /pfault/workload_example/check_workload/wikiw-sync.sh)
################## Configure ISCSI ##################
export ISCSI_SERVER_USER=root
export ISCSI_SERVER_IP=192.168.56.102
export ISCSI_DIR=/pfault/pf_virtual_device_manager/iscsi
############## Configure Client ##################
export CLIENT_CNT=1
export CLIENT_USER=(root)
export CLIENT_IP=(192.168.56.101)
export CLIENT_LUSTRE_MNT_PNT=(/lustre)
############## Configure MGT & MGS ################
export MGT_CNT=1
export MGT_SZ=(200)
export MGT_NAME=(mgt0)
export MGT_DISK_LABEL=(/dev/sdb)
export MGT_LUSTRE_MNT_PNT=(/mgt)
export MGT_LDISKFS_MNT_PNT=(/local)
export MGS_CNT=1
export MGS_USER=(root)
export MGS_IP=(192.168.56.111)
export MGS_TMP_DIR=(/lustre_tmp)
export MGS_LNET_POSTFIX=(tcp1)
############## Configure MDT & MDS ################
export MDT_CNT=1
export MDT_SZ=(200)
export MDT_NAME=(mdt0)
export MDT_DISK_LABEL=(/dev/sdb)
export MDT_LUSTRE_MNT_PNT=(/mdt)
export MDT_LDISKFS_MNT_PNT=(/local)
export MDS_CNT=1
export MDS_USER=(root)
export MDS_IP=(192.168.56.110)
export MDS_TMP_DIR=(/lustre_tmp)
############### Configure OST & OSS ###############
export OST_CNT=3
export OST_SZ=(200 200 200)
export OST_NAME=(ost0 ost1 ost2)
export OST_DISK_LABEL=(/dev/sdb /dev/sdb /dev/sdb)
export OST_LUSTRE_MNT_PNT=(/ost /ost /ost)
export OST_LDISKFS_MNT_PNT=(/local /local /local)
export OSS_CNT=3
export OSS_USER=(root root root)
export OSS_IP=(192.168.56.108 192.168.56.109 192.168.56.112)
export OSS_TMP_DIR=(/lustre_tmp /lustre_tmp /lustre_tmp)
