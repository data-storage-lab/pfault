#!/bin/sh
it=0
while [ $it -lt $AGE_WORKLOADS_CNT ]
do

$AGE_WORKLOADS[it]

let "it+=1"
done
