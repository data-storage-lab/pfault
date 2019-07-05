#!/bin/bash

dir=`pwd`
echo "$dir"
source $dir/configuration.sh
sz=0
it=0
	while [ $it -lt $MGT_CNT ]
	do

		let "sz=${MGT_SZ[$it]} + 10"
		pv_name=`echo "mgt.pv.$it"`
		sudo dd if=/dev/zero of=$ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name bs=1M count=$sz
		sleep 10
		losetup /dev/loop0 $ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name
		sudo pvcreate /dev/loop0
		vg_name=`echo "mgt.vg.$it"`
		sudo vgcreate $vg_name /dev/loop0
		sudo lvcreate --name /dev/$vg_name/${MGT_NAME[$it]} --size ${MGT_SZ[$it]}M
		sudo dd if=/dev/$vg_name/${MGT_NAME[$it]} of=$ISCSI_DIR/pfe_scripts/multinodes/img/${MGT_NAME[$it]} bs=1M count=${MGT_SZ[$it]}
		sudo lvremove -y /dev/$vg_name/${MGT_NAME[$it]}
		sudo vgremove -y /dev/$vg_name
		sudo pvremove -y /dev/loop0
		losetup -d /dev/loop0
		sudo rm -rf $ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name
		let  "it+=1" 
	done
        sync

sz=0
it=0
	while [ $it -lt $MDT_CNT ]
	do

		let "sz=${MDT_SZ[$it]} + 10"
		pv_name=`echo "mdt.pv.$it"`
		sudo dd if=/dev/zero of=$ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name bs=1M count=$sz
		sleep 10
		losetup /dev/loop0 $ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name
		sudo pvcreate /dev/loop0
		vg_name=`echo "mdt.vg.$it"`
		sudo vgcreate $vg_name /dev/loop0
		sudo lvcreate --name /dev/$vg_name/${MDT_NAME[$it]} --size ${MDT_SZ[$it]}M
		sudo dd if=/dev/$vg_name/${MDT_NAME[$it]} of=$ISCSI_DIR/pfe_scripts/multinodes/img/${MDT_NAME[$it]} bs=1M count=${MDT_SZ[$it]}
		sudo lvremove -y /dev/$vg_name/${MDT_NAME[$it]}
		sudo vgremove -y /dev/$vg_name
		sudo pvremove -y /dev/loop0
		losetup -d /dev/loop0
		sudo rm -rf $ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name
		let  "it+=1" 
	done
        sync

sz=0
it=0
	while [ $it -lt $OST_CNT ]
	do

		let "sz=${OST_SZ[$it]} + 10"
		pv_name=`echo "ost.pv.$it"`
		sudo dd if=/dev/zero of=$ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name bs=1M count=$sz
		sleep 10
		losetup /dev/loop0 $ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name
		sudo pvcreate /dev/loop0
		vg_name=`echo "ost.vg.$it"`
		sudo vgcreate $vg_name /dev/loop0
		sudo lvcreate --name /dev/$vg_name/${OST_NAME[$it]} --size ${OST_SZ[$it]}M
		sudo dd if=/dev/$vg_name/${OST_NAME[$it]} of=$ISCSI_DIR/pfe_scripts/multinodes/img/${OST_NAME[$it]} bs=1M count=${OST_SZ[$it]}
		sudo lvremove -y /dev/$vg_name/${OST_NAME[$it]}
		sudo vgremove -y /dev/$vg_name
		sudo pvremove -y /dev/loop0
		losetup -d /dev/loop0
		sudo rm -rf $ISCSI_DIR/pfe_scripts/multinodes/img/$pv_name
		let  "it+=1" 
	done
        sync
