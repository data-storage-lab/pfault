#!/bin/bash

absme=`readlink -f $0`
abshere=`dirname $absme`

echo 
echo -e "Executing generate_ranked_io.sh"


echo "Log Directory: ${PFE_LOG_DIR}"
echo "Total replayed IOs: ${TOT_IO_CNT}"

cd ${PFE_LOG_DIR}

if [[ -z "${PFE_LOG_DIR}" ]];then
    echo "Log directory path not set, exiting..."
    exit 1
fi


if [ ! -d ${PFE_LOG_DIR} ];then
    echo "no $PFE_LOG_DIR, please ensure that this directory is available"
    exit 2
fi

echo "Creating ${PFE_LOG_DIR}/ranked_io.txt"
grep -c "Fix?" log.fswkld-* | sed -r 's/^.{11}//' | sed 's/.fsck[0-9]*:/-/g' | sort -t '-' -k 2 -r | sed '/[0-9]-0/d' | cut -d '-' -f1 > ${PFE_LOG_DIR}/ranked_io.txt
echo "Done"

