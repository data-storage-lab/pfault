# README #
This repository contains the research prototype of PFault  which has been used for the following works: 

- "[A Study of Failure Recovery and Logging of High-Performance Parallel File Systems](https://dl.acm.org/doi/10.1145/3483447)",
Runzhou Han, Om R. Gatla, Mai Zheng, Jinrui Cao, Di Zhang, Dong Dai, Yong Chen, and Jonathan Cook.
ACM Transactions on Storage ([TOS](https://dl.acm.org/journal/tos)), Volume 18, Issue 2, 2022.

- "[SentiLog: Anomaly Detection on Parallel File Systems via Log-based Sentiment Analysis](https://dl.acm.org/doi/10.1145/3465332.3470873)",
Di Zhang, Dong Dai, Runzhou Han, and Mai Zheng,
Proceedings of the 13th ACM Workshop on Hot Topics in Storage and File Systems ([HotStorage](https://www.hotstorage.org/2021/)), 2021.

- "[Fingerprinting the Checker Policies of Parallel File Systems](https://ieeexplore.ieee.org/document/9307050)",
Runzhou Han, Duo Zhang, and Mai Zheng,
Proceedings of the 5th ACM/IEEE International Parallel Data Systems Workshop ([PDSW](http://www.pdsw.org/index.shtml)) at ACM/IEEE Supercomputing (SC), 2020

- "[PFault: A General Framework for Analyzing the Reliability of High-Performance Parallel File Systems](https://dl.acm.org/doi/10.1145/3205289.3205302)", 
Jinrui Cao, Om Rameshwar Gatla, Mai Zheng, Dong Dai, Vidya Eswarappa, Yan Mu, and Yong Chen. 
Proceedings of the 32nd ACM/SIGARCH International Conference on Supercomputing ([ICS](https://www.ics-conference.org/index.html)), 2018.

- "[A Generic Framework for Testing Parallel File Systems](https://ieeexplore.ieee.org/document/7836568)",
Jinrui Cao, Simeng Wang, Dong Dai, Mai Zheng, and Yong Chen.
Proceedings of the 1st ACM/IEEE Joint International Workshop on Parallel Data Storage and Data Intensive Scalable Computing Systems ([PDSW](http://www.pdsw.org/index.shtml)) at ACM/IEEE Supercomputing (SC), 2016.

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
  - Source code in "pf_orchestrator" folder
  - Controls and coordinates the overall workflow of PFault automatically

For more information you could refer to our research paper 
at http://ics2018.ict.ac.cn/essay/ics18-cameraready-submitted.pdf

## PFault Initiation Guidance ##

Steps to initiate the tool:

  1.  (Optional) Required to be able to run sudo commands

  2.  Make tgtd first:
 
      ```cd /path/to/pfault/pf_virtual_device_manager/iscsi```
      
      ```make```

  3.  Set password-less ssh for all the servers and clients
  
  4.  Copy configuration template:

      ```cd /path/to/pfault/configuration```
      
      ```cp configuration_template.sh configuration.sh```

      Fill the configuration.sh with the required Lustre setup

  5.  Run "Virtual Device Manager" to build the Lustre Cluster 

      ```cd /path/to/pfault/pf_virtual_device_manager/```
      
      ```./vdm.sh```

  6.  Run any workloads on the cluster. For example, there are few workloads in the folder:
      /path/to/pfault/workload_example
  
  7.  The user may select the various failure models in "Failure State Emulator"



Users may also use the orchestrator to run the experiments automatically with following steps:
  - In configuration.sh, select a fault model by setting the variable "FAULT_MODEL" and set up other orchestrator variables as well
  - ```/path/to/pfault/pf_orchestrator/orchestrator```

The orchestrator will first run the aging workload on client node, and then do fault injection correspondingly, and finally run the checking workload. Three log files will be created during each run. 

We also provide log trace generated during our experiments. Log files along with their description are provided in folders under '/log trace'.

## Contact ##
Contact: hanrz@iastate.edu ogatla@iastate.edu 
