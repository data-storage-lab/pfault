#!/usr/bin/env bash


####################################### Check
echo -e "\n### Do Check Start"

#$APP_DIR/./checker.x
#CHECK_OUTPUT=$PFE_LOG_DIR/output.cut-$CUT_IO_NUM

OUTPUT_FILENAME=output.cut-$CUT_IO_NUM
DB_READ_RESULT=$PFE_LOG_DIR/$OUTPUT_FILENAME
: > $DB_READ_RESULT




if [ $PROFILER_CK == "pintool" ];then

    PINTOOL_LOG=$PFE_LOG_DIR/pintool.log.ck-$CUT_IO_NUM
    pin -injection child -t /home/zhengm/pin-2.13-62141-gcc.4.4.7-linux/source/tools/mai_PinTool/obj-intel64/mai_trace.so -logfile $PINTOOL_LOG -- $APP_DIR/checker.x | tee $DB_READ_RESULT

elif [ $PROFILER_CK == "strace" ]; then
    STRACE_LOG=$PFE_LOG_DIR/strace-checklog-$CUT_IO_NUM
    strace -tttTx -ff -s 64 -e write=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 -o $STRACE_LOG  $APP_DIR/./checker.x | tee $DB_READ_RESULT

else
    $APP_DIR/./checker.x | tee $DB_READ_RESULT
fi


echo -e "#### Do Check Finished\n"
#########################################
