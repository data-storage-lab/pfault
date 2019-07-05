#!/usr/bin/env python

#rm useless lines in mysql wkld2 result log-4.txt
#./THISFILE log-4.txt
import sys
import re
from format_strace import lines2lists


if __name__ == "__main__":
    fn = sys.argv[1]
    f = open(fn)
    lines = f.readlines()
    for line in lines:
        if 'Warning:' in line and 'insecure.' in line:
            pass
        elif 'passed' in line:
            pass
        else:
            print line,
    



