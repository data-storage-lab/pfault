# README #
This repository contains the source code for "PFault: A General Framework for Analyzing the 
Reliability of High-Performance Parallel File Systems", which is published in the 
32nd ACM/SIGARCH International Conference on Supercomputing (ICS'18, http://ics2018.ict.ac.cn/)
 and its' follow-up journal version.

## Introduction to PFault ##
The description of each component is as follows:

**Failure State Emulator**:

Including the Virtual Device Manager and Fault Models.

- *Virtual Device Manager*:
  - Source code in "pf_virtual_device_manager" folder
  - Manages the persistent state of the target Parallel File System (PFS)


- *Fault Models*:
  - Source code in "pf_failure_state_emulator" folder
  - Injects faults based on the following fault models (Please refer to the paper for their description):
    - Whole Device Failure
    - Network Partitioning
    - Global Inconsistency


**PFS worker**:
  - Source code in "pf_pfs_worker"
  - Generates I/O operations for aging purpose and checks correctness of the recovery

**PFS Checker**:
  - Source code in "pf_pfs_checker" folder
  - Invokes the default FSCK component of the target PFS
  
**Orchestrator**:
  - Source code in "pf_pfs_orchestrator" folder
  - Controls and coordinates the overall workflow of PFault automatically

For more information you could refer to our research paper 
at http://ics2018.ict.ac.cn/essay/ics18-cameraready-submitted.pdf

## PFault Initiation Guidance ##

Steps to initiate the tool:

  1.  (Optional) Required to be able to run sudo commands

  2.  Make tgtd first:
 
      cd /path/to/pfault/pf_virtual_device_manager/iscsi
      make

  3.  Set password-less ssh for all the servers and clients
  
  4.  Copy configuration template:

      cd /path/to/pfault/configuration
      cp configuration_template.sh configuration.sh

      Fill the configuration.sh with the required Lustre setup

  5.  Run "Virtual Device Manager" to build the Lustre Cluster 

      cd /path/to/pfault/pf_virtual_device_manager/
      ./vdm.sh

  6.  Run any workloads on the cluster. For example, there are few workloads in the folder:
      /path/to/pfault/workload_example
  
  7.  The user may select the various failure models in "Failure State Emulator"

PFault log trace has been uploaded. Log description is contained in the README.md file under folder '/log trace'.

## Contact ##
Contact: hanrz@iastate.edu ogatla@iastate.edu 
