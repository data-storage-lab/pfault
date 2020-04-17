Copyright 2019 Runzhou Han hanrz@iastate.edu

=====================================================================================================================================

# INTRODUCTION

=====================================================================================================================================

This is a collection of Lustre log (Lustre version 2.10, Linux kernel version 3.10.0-957.1.3.el7_lustre.x86_64 ) under abnormal situations (power fault emulation).

The fault models injected are generated according to PFault (J. Cao, ICS 18').

Logs are collected from different Lustre nodes: 1 client node, 1 MGS node, 1 MDS node, 3 OSS nodes.

3 different lustre failure scenario is discussed in PFault: DevFail (lustre server's storage device disabled using iscsi logout), Network (lustre server's network interface disabled), Inconsist (lustre server's metadata inconsist).

In each failure scenario, 5 different failure case are discussed: MGS failure, MDS failure, OSS#2 failure, 3 OSSes failure, MDS&OSS#2 failure.

Under each failure case, log is seperated into 7 phases:

1. Log after Lustre mount
2. Log after garbage removing and aging workload*
3. Log after verification workload*
4. Log after running lfsck (Lustre file system checker) under normal operation
5. Log after fault injection and run lfsck under abnormal situation
6. Log after running check workload*
7. Log after Lustre system recovery

* workloads are defined in PFault (J. Cao, ICS 18)




