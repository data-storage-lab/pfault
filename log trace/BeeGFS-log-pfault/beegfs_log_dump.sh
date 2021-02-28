#!/bin/bash
export num=3
export affected_node="meta+storage1"
export fault="b-Inconsist"
# mgmt
mkdir -p /home/runzhou/BeeGFS-log/mgmt_log/${fault}/${affected_node} && scp -r root@10.0.0.137:/var/log/beegfs-* /home/runzhou/BeeGFS-log/mgmt_log/${fault}/${affected_node}/$num
ssh root@10.0.0.137 <<EOF
rm -rf /var/log/beegfs-*
systemctl stop beegfs-mgmtd
systemctl start beegfs-mgmtd
EOF

# meta
mkdir -p /home/runzhou/BeeGFS-log/meta_log/${fault}/${affected_node} && scp -r root@10.0.0.123:/var/log/beegfs-* /home/runzhou/BeeGFS-log/meta_log/${fault}/${affected_node}/$num
ssh root@10.0.0.123 <<EOF
rm -rf /var/log/beegfs-*
systemctl stop beegfs-meta
systemctl start beegfs-meta
EOF

# storage 0
mkdir -p /home/runzhou/BeeGFS-log/storage0_log/${fault}/${affected_node} && scp -r root@10.0.0.8:/var/log/beegfs-* /home/runzhou/BeeGFS-log/storage0_log/${fault}/${affected_node}/$num
ssh root@10.0.0.8 <<EOF
rm -rf /var/log/beegfs-*
systemctl stop beegfs-storage
systemctl start beegfs-storage
EOF

# storage1
mkdir -p /home/runzhou/BeeGFS-log/storage1_log/${fault}/${affected_node} && scp -r root@10.0.0.108:/var/log/beegfs-* /home/runzhou/BeeGFS-log/storage1_log/${fault}/${affected_node}/$num
ssh root@10.0.0.108 <<EOF
rm -rf /var/log/beegfs-*
systemctl stop beegfs-storage
systemctl start beegfs-storage
EOF

# storage2
mkdir -p /home/runzhou/BeeGFS-log/storage2_log/${fault}/${affected_node} && scp -r root@10.0.0.203:/var/log/beegfs-* /home/runzhou/BeeGFS-log/storage2_log/${fault}/${affected_node}/$num
ssh root@10.0.0.203 <<EOF
rm -rf /var/log/beegfs-*
systemctl stop beegfs-storage
systemctl start beegfs-storage
EOF

# client
mkdir -p /home/runzhou/BeeGFS-log/client_log/${fault}/${affected_node} && scp -r root@10.0.0.121:/var/log/beegfs-client* /home/runzhou/BeeGFS-log/client_log/${fault}/${affected_node}/beegfs-client.$num && scp -r root@10.0.0.121:/var/log/beegfs-fsck* /home/runzhou/BeeGFS-log/client_log/${fault}/${affected_node}/
ssh root@10.0.0.121 <<EOF
rm -rf /var/log/beegfs-*
systemctl stop beegfs-client
systemctl stop beegfs-helperd
systemctl start beegfs-helperd
systemctl start beegfs-client
EOF



# remove old log files parallelly. Doesn't work.
# parallel-ssh -i -h /home/runzhou/BeeGFS-log/pssh_hosts rm -rf /var/log/beegfs-*
