#!/bin/bash
#set the parameters of workload 4

###################### app env var
export N_THR=2 #n threads
export N_TXN_PER_THR=2 #txn per thread
export N_KEY_PER_TXN=2 #keys per txn
export N_WORK_KEYS=100
((N_META_KEYS = N_THR * N_TXN_PER_THR))
((N_TOT_KEYS = N_META_KEYS + N_WORK_KEYS))
((WORK_KEY_START = N_META_KEYS + 1))
export N_META_KEYS
export N_TOT_KEYS
export WORK_KEY_START
export WORK_KEY_END=$N_TOT_KEYS

echo "N_THR = $N_THR"
echo "N_TXN_PER_THR = $N_TXN_PER_THR"
echo "N_KEY_PER_TXN = $N_KEY_PER_TXN"
echo "N_META_KEYS = $N_META_KEYS"
echo "N_WORK_KEYS = $N_WORK_KEYS"
echo "N_TOT_KEYS = $N_TOT_KEYS"
echo "WORK_KEY_START = $WORK_KEY_START"
echo "WORK_KEY_END = $WORK_KEY_END"

export TEST_DB_NAME=TC
###################### app env var
