#!/usr/bin/env bash
#format windows log file
#./THISFILE /PATH/WIN_LOG_DIR

absme=`readlink -f $0`
abshere=`dirname $absme`

    
INPUT_DIR=$1
OUTPUT_DIR=$INPUT_DIR.formatted
mkdir $OUTPUT_DIR


#input file to be formatted
TS_FILENAME=log.work-timestamp

#save config file
cp $INPUT_DIR/w*_config.txt $OUTPUT_DIR
#save io file
cp $INPUT_DIR/formatted.io.txt $OUTPUT_DIR

#format ts file
$abshere/format_winlog.py  $INPUT_DIR/$TS_FILENAME  > $OUTPUT_DIR/$TS_FILENAME

#format output-* files
for file in $INPUT_DIR/output*; do
    file_basename=${file##*/}
    result=$OUTPUT_DIR/$file_basename
    :> $result 
    echo -e "\n################# Start processing $file" 

    $abshere/format_winlog.py $file > $result

    echo -e "###Done with $file_basename\n" 
done

