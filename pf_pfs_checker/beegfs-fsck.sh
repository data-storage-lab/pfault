#!/bin/bash
beegfs-ctl --listtargets --nodetype=meta --state
beegfs-ctl --listtargets --nodetype=storage --state
beegfs-fsck --checkfs --readOnly --databasePath=/mnt/ssd/fsck
beegfs-fsck --checkfs --noFetch --databasePath=/mnt/ssd/fsck
