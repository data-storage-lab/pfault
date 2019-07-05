#/usr/bin/env bash

#get pattern io #s based on diff patterns
#require the results of map_io2ReqAndFile.sh
#/PATH/THISFILE io2ReqAndFile.simple.sim [io2file.dynamic.sim]

absme=`readlink -f $0`
abshere=`dirname $absme`

io2ReqAndFile=$1 #io2ReqAndFile.simple.sim

$abshere/getPatternIO_transition.py $io2ReqAndFile > patternIO_transition.txt
$abshere/getPatternIO_jump.py $io2ReqAndFile > patternIO_jump.txt
$abshere/getPatternIO_repetitive.py $io2ReqAndFile > patternIO_repetitive.txt
$abshere/getPatternIO_head.py $io2ReqAndFile > patternIO_head.txt

if [[ $2 ]];then
    io2file_dynamic=$2 #io2file.dynamic.sim
    $abshere/getPatternIO_mmap.py $io2file_dynamic > patternIO_mmap.txt

    $abshere/rank_ioSeq.py patternIO_transition.txt patternIO_jump.txt patternIO_repetitive.txt patternIO_head.txt patternIO_mmap.txt > patternIO.rank.txt
else

    $abshere/rank_ioSeq.py patternIO_transition.txt patternIO_jump.txt patternIO_repetitive.txt patternIO_head.txt > patternIO.rank.txt
fi

#separate each rank to a diff file
$abshere/separate_ranks.py patternIO.rank.txt


