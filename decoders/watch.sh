#!/bin/bash

watch -d -n 1 "\
cd $1 ;\
echo Decoded frames: \$(ls -lt | grep .hex | wc -l) ;\
echo  ;\
echo Last decoded frame data: ;\
cat /dev/null \$(ls -tr | grep .hex | head -n 1 ) ;\
cat /dev/null \$(ls -tr | grep .json | head -n 1 ) ;\
echo ;\
echo ;\
echo Last 30 decoded frame files: ;\
ls -lt | grep .json | head -n 30 ;\
cd .. ;\
"


