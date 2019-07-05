#!/usr/bin/env bash
#create a new fs on initiator side
#create "device" file in the fs (for workers)
#save the disk image for future record&replay 


. $PFE_SCRIPT_DIR/pfe_helper.sh


echo -e "################ STAGE #1 : CREATE BASE IMAGE\n"
date

sudo cp $PRISTINE_INSTALL_IMG $TGT_IMG




sudo rm -rf $MNT/*
echo "### sudo mount -t $PFE_FS -o loop $TGT_IMG $MNT"
sudo mount -t $PFE_FS -o loop $TGT_IMG $MNT 
sleep 3

echo "### do something inside fs"
cd $MNT
sudo chmod 777 -R $MNT
#create a simple file
touch testfile
echo "testfile_content_123" > testfile
echo "ls $MNT"
ls -lsit $MNT
echo "cat testfile"
cat testfile

################################ app-initialization
echo -e "\n######### APP INIT"
echo $APP_INIT
$APP_INIT 2>&1 | tee $PFE_LOG_DIR/log.app-init
echo -e "######### APP INIT DONE\n"
#################################

sleep 3
echo "ls $MNT"
sudo ls -lsit $MNT
echo "ls $DB_ENVIRONMENT"
sudo ls -lsit $DB_ENVIRONMENT

cd $PFE_SCRIPT_DIR 
sync;sync
echo "### sudo umount $MNT"
sudo umount $MNT
sleep 3
echo "ls $MNT"
ls -lsit $MNT




#save a copy of the disk image
echo "### save base image"
cp $TGT_IMG ${TGT_REPLAY_IMG_BASE}  
sudo cp $TGT_IMG ${TGT_REPLAY_RAMIMG_BASE} #a copy in ram  

sudo rm -rf $MNT/*
sleep 3
echo -e "\n################ STAGE #1 DONE!"
date
