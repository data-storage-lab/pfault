#!/usr/bin/env python

#calculate time based log
#input file format:

#read
#Wed Mar  5 11:48:21 EST 2014
#Wed Mar  5 13:27:33 EST 2014
#check:  newck*-1 -------*-99
#Wed Mar  5 13:27:33 EST 2014
#Wed Mar  5 13:28:18 EST 2014

#usage:
#./THIS_PY TIME_LOG > result

#e.g.:
#./print_err_trend.py /home/zhengm/logs-folder/logs-tc-wkld4_THR-2-TXN-10-KEY-10_fail-0-unseri-small-fs-xfs-cutopt-EXHAUSTIVE_CUT-100.131010112829/tmp 1573

import sys
import re

def lines2lists(f):
    """input a file,
       convert each line to a list,
       output a list of lists"""

    ret_lines = [] 
    seperator = re.compile(r',| +|-|:|\n|\t|=+|!|#|\[|\]|\(|\)|\<|\>|\"')
    lines = f.readlines()

    for line in lines:
        line_splitted = seperator.split(line)
        line_filtered = filter(None, line_splitted)
        ret_lines.append(line_filtered)

    return ret_lines

def sec2datetime(seconds):
    """ convert seconds to day, hour, min, sec"""

    days = seconds // (3600*24)
    hours = seconds % (3600*24) //3600 
    mins =  seconds % (3600*24) % 3600 // 60
    secs = seconds % (3600*24) % 3600 % 60
    
    print_str = str(days) + " d, " + str(hours) + " h, " + str(mins) + " m, " + str(secs) + " s"
    return print_str 
    

    
def calTime(lines):
    """
    get time lines; for simpilicy,  assume four time lines are in the same Month
    ['read']
    ['Wed', 'Mar', '5', '11', '48', '21', 'EST', '2014']
    ['Wed', 'Mar', '5', '13', '27', '33', 'EST', '2014']
    ['check', 'newck*', '1', '*', '99']
    ['Wed', 'Mar', '5', '13', '27', '33', 'EST', '2014']
    ['Wed', 'Mar', '5', '13', '28', '18', 'EST', '2014']
    """
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    time_lines = []
    for line in lines:
        if len(line) == 8 and line[0] in days: # a valid time line
            this_day = int(line[2])
            this_hour = int(line[3])
            this_min = int(line[4])
            this_sec = int(line[5])
            this_time = this_day*24*3600 + this_hour*3600+this_min*60+this_sec
            this_line = [this_day, this_hour, this_min, this_sec, this_time]
            time_lines.append(this_line)

    read_seconds = time_lines[1][-1] - time_lines[0][-1]
    check_seconds = time_lines[3][-1] - time_lines[2][-1]
    tot_seconds = read_seconds + check_seconds

    read_time = sec2datetime(read_seconds)
    check_time = sec2datetime(check_seconds)
    tot_time = sec2datetime(tot_seconds)

    print "read time: " + read_time
    print "check time: " + check_time
    print "total time: " + tot_time
    print "total seconds: " + str(tot_seconds)

    return

if __name__ == "__main__":
    fn = sys.argv[1]
    f = open(fn)
    usefullines = lines2lists(f)
    calTime(usefullines)
   
    #for line in usefullines:
        #line_str = ' '.join(line)
        #print line_str
     #       print line
    
