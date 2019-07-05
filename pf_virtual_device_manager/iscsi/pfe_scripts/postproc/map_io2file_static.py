#!/usr/bin/env python

#map each io to a file name based on  fs structure on disk (static)
#use debugfs to get blocks of each file
#/PATH/THISFILE img_file formatted.io.txt 
#/PATH/THISFILE img.137.2fscked formatted.io.txt > formatted.io2file.sim

import sys
import re
import tempfile
from format_strace import lines2lists
from subprocess import call, STDOUT

def debugfs_blocks(img_file, inode):
    """ debugfs: blocks <inode> """
    cmd_file = tempfile.NamedTemporaryFile() 
    out_file = tempfile.NamedTemporaryFile() #

    call(["echo", "blocks <" + inode + ">"], stdout=cmd_file, stderr=STDOUT)
    #call(["cat",cmd_file.name])

    call(["debugfs", "-f", cmd_file.name, img_file.name], stdout=out_file, stderr=STDOUT)
    out_file.seek(0)
    #call(["cat",out_file.name])

    #for out_line in out_file.readlines():
    #    print out_line

    #out_file content e.g.:
    #   debugfs 1.42 (29-Nov-2011)
    #   debugfs: blocks <11>
    #   518 519 520 521 522 523 524 525 526 527 528 529
 
    return out_file
     

def debugfs_ls(img_file):
    """ debugfs: ls -l """
    cmd_file = tempfile.NamedTemporaryFile() 
    out_file = tempfile.NamedTemporaryFile() #

    call(["echo", "ls", "-l"], stdout=cmd_file, stderr=STDOUT)

    call(["debugfs", "-f", cmd_file.name, img_file.name], stdout=out_file, stderr=STDOUT)
    out_file.seek(0)

    return out_file


def debugfs_ls_dir(img_file, directory):
    """ debugfs: ls -l directory"""
    cmd_file = tempfile.NamedTemporaryFile() 
    out_file = tempfile.NamedTemporaryFile() #

    call(["echo", "ls", "-l", directory], stdout=cmd_file, stderr=STDOUT)

    call(["debugfs", "-f", cmd_file.name, img_file.name], stdout=out_file, stderr=STDOUT)
    out_file.seek(0)

    return out_file


 
def get_blocks2files_map(img_file, directories):
    """
    input: img_file
    output:
    [ ['inode', 'file_name', 'file_blocks'],
      ['inode', 'file_name', 'file_blocks'],
      ...
    ]
    """

    out_file = debugfs_ls(img_file)
    out_lists = lines2lists(out_file)

    #directory = "myEnvironment"
    for directory in directories:
        out_file = debugfs_ls_dir(img_file, directory)
        subdir_inode_lists = lines2lists(out_file)
        out_lists = out_lists + subdir_inode_lists

    ret_lists = []
    for line in out_lists:
        if len(line) == 9:
            inode = line[0]
            file_name = line[-1]
#            print inode + " " + file_name 
            new_line = [inode, file_name]

            out_file = debugfs_blocks(img_file, inode)

            #out_file content e.g.:
            #   debugfs 1.42 (29-Nov-2011)
            #   debugfs: blocks <11>
            #   518 519 520 521 522 523 524 525 526 527 528 529
            for out_line in out_file.readlines():
                if "debugfs" not in out_line: #last line blocks
                    #print out_line
                    new_line.append(out_line)
            ret_lists.append(new_line)

    #add journal blocks 
    journal_inode = '8'#journal inode is typically 8
    new_line = [journal_inode, 'fs-journal']

    out_file = debugfs_blocks(img_file, journal_inode)

    for out_line in out_file.readlines():
        if "debugfs" not in out_line: #last line blocks
            #print out_line
            new_line.append(out_line)

    ret_lists.append(new_line)

    return ret_lists


def get_io_list(io_file):
    ret_list = []
    io_lists = lines2lists(io_file)
    #a line(list):
    #1392469373081108 IO# 1 1024 1024 000100000004000000003333000342d20000ff8d000000010000000000000000
    for line in io_lists:
        io_num = line[2]
        offset = line[3]
        #byte_offset = int(line[3])
        #blk_size = 1024
        #blk_offset = str(byte_offset/blk_size)
        #blk_offset = str(byte_offset)
        #ret_list.append(blk_offset)
        io_str = io_num + " " + offset
        ret_list.append(io_str)

    return ret_list

def map_io2file_static(io_offset, blocks2files_map):
    """
    map a block to file
    """
    blk_size = 1024 #fs use 1KB block
    blk_num = str(int(io_offset)/blk_size)

    ret_list = []
    for elem in blocks2files_map:
        blocks_str = elem[2] #['inode', 'file_name', 'file_blocks'],
        blocks_list = blocks_str.split()
        if blk_num in blocks_list: 
            file_name = elem[1]
            return file_name
    return "" #no matching file



if __name__ == "__main__":
    img_file = open(sys.argv[1]) #name of img
    #directory = sys.argv[3] #directory
    directories = sys.argv[3:] #directory list
    blocks2files_map = get_blocks2files_map(img_file, directories)
    #for elem in blocks2files_map:
    #    print elem

    io_file = open(sys.argv[2])
    io_list = get_io_list(io_file)
    for io_str in io_list:
        io_list = io_str.split() #[io_num, io_offset]
        io_offset = io_list[-1]
        file_name = map_io2file_static(io_offset, blocks2files_map)
        if file_name == "":
            file_name = "NA"
        print io_str + " " + file_name


    


