#/usr/bin/env bash

#no strace/pin call info available, just use debugfs

#read formatted io files, map each io to the original requests and  db files
#add TC-specific directory for debugfs inode block mapping
#cd LOG_DIR
#~/0repos/emulator-iscsi/pfe_scripts/postproc/map_io2ReqAndFile_NoCalltrace_TC.sh ./ 

LOG_DIR=$1
OUTPUT_DIR=$LOG_DIR #put output in the  log dir

img_file=$LOG_DIR/iscsi-bs-128M.work
formatted_io_file=$LOG_DIR/formatted.io.txt
req_file=$LOG_DIR/pfe_io_header_log.work.od
#formatted_map_file=$LOG_DIR/formatted.map.sim #syscall-IO map





absme=`readlink -f $0`
abshere=`dirname $absme`


#map each splitted IO (default 4KB) to the original request (maybe > 4KB)
#./THISFILE formatted_io IO_HEAD_LOG 
#./THISFILE formatted.io.txt pfe_io_header_log.work.od > io2req.txt 
$abshere/map_io2req.py $formatted_io_file $req_file > $OUTPUT_DIR\io2req.sim

#map each io to a file name
#use debugfs to get blocks of each file
#/PATH/THISFILE img_file formatted.io.txt interesting_subdir
#/PATH/THISFILE img.137.2fscked formatted.io.txt "myEnvironment" > formatted.io2file.sim
$abshere/map_io2file_static.py $img_file $formatted_io_file > $OUTPUT_DIR\io2file.static.sim

#map io 2 file based on syscall trace
#$abshere/map_io2file_dynamic.py  $formatted_map_file > io2file.dynamic-full.sim
#$abshere/simplify_io2file_dynamic.py  io2file.dynamic-full.sim > io2file.dynamic.sim

#merge static and dynamic io2file mappings
#$abshere/merge_StaticDynamicMap.py io2file.static.sim io2file.dynamic.sim > io2file.merged.sim


$abshere/merge_ioReqAndFile.py $OUTPUT_DIR\io2req.sim $OUTPUT_DIR\io2file.static.sim > $OUTPUT_DIR\io2ReqAndFile.sim 
#$abshere/merge_ioReqAndFile.py io2req.sim io2file.merged.sim > io2ReqFileCall.sim 
#$abshere/rmCallInfo.py io2ReqFileCall.sim > io2ReqAndFile.sim 

$abshere/simplify_ioReqAndFileMap.py $OUTPUT_DIR\io2ReqAndFile.sim > $OUTPUT_DIR\io2ReqAndFile.simple.sim


#get pattern ios
$abshere/getPatternIO.sh  $OUTPUT_DIR\io2ReqAndFile.simple.sim
