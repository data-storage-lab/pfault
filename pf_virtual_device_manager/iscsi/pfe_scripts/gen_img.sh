#!/usr/bin/env bash
#generate virtual disk images (i.e., files) for backing store 

IMAGE_DIR=~/pfe_images #also used in pfe_local_conf.sh; keep consistent
if [ ! -d $IMAGE_DIR ];then
    echo "no $IMAGE_DIR, creating one ..."
    sudo mkdir $IMAGE_DIR 
    sudo chmod 777 $IMAGE_DIR 
fi

cd $IMAGE_DIR

sudo apt install xfsprogs
sudo apt install btrfs-tools
sudo apt install f2fs-tools

dd if=/dev/zero of=img.128M.empty bs=1M count=128


cp img.128M.empty img.128M.empty.ext4
cp img.128M.empty img.128M.empty.ext3
cp img.128M.empty img.128M.empty.xfs
cp img.128M.empty img.128M.empty.btrfs
cp img.128M.empty img.128M.empty.f2fs


mkfs -t ext4 -F img.128M.empty.ext4
mkfs -t ext3 -F img.128M.empty.ext3
mkfs.xfs img.128M.empty.xfs
mkfs.btrfs img.128M.empty.btrfs
mkfs.f2fs img.128M.empty.f2fs

#sudo chmod 777 -R ~/images
sudo chmod 777 -R $IMAGE_DIR
