=====================================================================================================================================

# INTRODUCTION

=====================================================================================================================================

This is a collection of BeeGFS log (BeeGFS version 7.1.15) under three abnormal situations (power fault emulation) according to PFault (J. Cao, ICS 18').

Logs are collected from a six-node Lustre cluster which consists of one client node, one MGS node, one MDS node and three OSS nodes.

During each experiment, Log is divided into three phases:

1. Log after aging workload, before fault injection
2. Log after fault injection & running BeeGFS file system checker
3. Log after checking workload

In client folder, two logs from BeeGFS file system checker are collected during each experiment.






