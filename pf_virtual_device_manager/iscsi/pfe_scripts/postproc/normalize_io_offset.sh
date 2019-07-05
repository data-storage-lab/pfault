#/usr/bin/env bash

#divide IO offset by 1024

#usage:
#./thisfile formatted.io.txt

#cut the IO offset column from $1
#output=io_offset_1024.txt

cut -d' ' -f4 $1 > tmp_io_file


while read p; do
  echo $((p / 1024)) # >> $output
done < tmp_io_file 

rm tmp_io_file
