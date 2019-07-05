#!/usr/bin/env bash

sudo chmod 777 -R $MNT
#mkdir `dirname $TC_WKLD2_DB_FILE`
mkdir `dirname $TC_WKLD4_DB_FILE`

$APP_DIR/./initer.x

