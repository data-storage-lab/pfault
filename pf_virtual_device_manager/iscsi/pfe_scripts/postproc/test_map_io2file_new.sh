#/usr/bin/env bash
#read formatted io files, map each io to the original requests and  db files
#cd LOG_DIR
#~/0repos/emulator-iscsi/pfe_scripts/postproc/map_io2ReqAndFile.sh img.137.2fscked formatted.io.txt  pfe_io_header_log.work.od 

img_file=/home/zhengm/logs-folder/logs-tc-wkld4_THR-2-TXN-10-KEY-10_fail-0-unseri-small-fs-ext3-cutopt-EXHAUSTIVE_CUT-100.140205001533.ACD.strace/iscsi-bs-128M.work
formatted_io_file=/home/zhengm/logs-folder/logs-tc-wkld4_THR-2-TXN-10-KEY-10_fail-0-unseri-small-fs-ext3-cutopt-EXHAUSTIVE_CUT-100.140205001533.ACD.strace/formatted.io.txt





#map each io to a file name
#use debugfs to get blocks of each file
#/PATH/THISFILE img_file formatted.io.txt 
#/PATH/THISFILE img.137.2fscked formatted.io.txt > formatted.io2file.sim
~/0repos/emulator-iscsi/pfe_scripts/postproc//map_io2file_new.py $img_file $formatted_io_file "myEnvironment"  > tmp.io2file.sim


