#!/usr/bin/env bash

cd $CLIENT_LUSTRE_MOUNTPOINT/m101
mImgtbl rawdir images-rawdir.tbl
sleep 60
mProjExec -p rawdir images-rawdir.tbl template.hdr projdir stats.tbl
sleep 60
mImgtbl projdir images.tbl
sleep 60
mAdd -p projdir images.tbl template.hdr final/m101_uncorrected.fits
sleep 60
mJPEG -gray final/m101_uncorrected.fits 20% 99.98% loglog -out final/m101_uncorrected.jpg
sleep 60
mOverlaps images.tbl diffs.tbl
sleep 60
mDiffExec -p projdir diffs.tbl template.hdr diffdir
sleep 60
mFitExec diffs.tbl fits.tbl diffdir
sleep 60
mBgModel images.tbl fits.tbl corrections.tbl
sleep 60
mBgExec -p projdir images.tbl corrections.tbl corrdir
sleep 60
mAdd -p corrdir images.tbl template.hdr final/m101_mosaic.fits
sleep 60
mJPEG -gray final/m101_mosaic.fits 0s max gaussian-log -out final/m101_mosaic.jpg

