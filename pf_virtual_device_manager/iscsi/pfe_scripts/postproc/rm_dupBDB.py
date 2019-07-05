#!/usr/bin/env python
#rm duplicated BDBxxx lines

import sys
import re


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        f = open(filename)
        linecnt = 0
        faultcnt = 0
        BDB_found = 0
        prev_BDB = 'nothing'
        for line in f:
            linecnt += 1
            wordlist = line.split()
            if len(wordlist) > 0:
                numstr = wordlist[0].strip()
                if 'BDB' in numstr: # a BDBxxx line
                    if numstr == prev_BDB: # same as previous BDBxxx
                        pass #skip this line
                    else: # a diff BDBxxx
                        print line,
                        prev_BDB = numstr
                else:#not a BDBxxx line
                    print line,
                    prev_BDB= 'nothing'
