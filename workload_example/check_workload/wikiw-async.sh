#!/usr/bin/env bash
dd if=$PFAULT_DIRECTOR/workload_example/data/enwiki-20170201-pages-meta-history2.xml-p000051985p000056274.7z of=/$CLIENT_LUSTRE_MOUNTPOINT/unsync bs=1M count=300
sleep 60
