#!/bin/sh
it=0
while [ $it -lt $VERIFIABLE_WORKLOADS_CNT ]
do

$VERIFIABLE_WORKLOADS_CNT[it]

let "it+=1"
done
