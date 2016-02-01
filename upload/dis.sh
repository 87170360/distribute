#!/bin/sh

echo $1

Date=`date +%Y_%m_%d`

PACKET_PATH=${PWD}

rm -rf data

mkdir -p ${HOME}/backup/

mkdir -p ${HOME}/frame_exec/

if [ -d "${HOME}/frame_exec/bin" ]; then
	cd ${HOME}/frame_exec/

	cp -f ${EXEC_HOME}/bin/lua/common/common_config.lua ${HOME}/backup/

	tar -zcvf bin_${Date}.tar.gz bin

	mv bin_${Date}.tar.gz ${HOME}/backup/
fi

cd ${PACKET_PATH}

unzip $1 -d data

cd data

chmod +x *.sh
