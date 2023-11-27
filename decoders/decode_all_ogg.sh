#!/bin/bash

# How to use:
#./decode_all_ogg.sh gnuradio_file_py ogg_directory/ decoded_directory/

cwd=$(pwd)

cd $2
files=$(ls *.ogg)
cd $cwd

for file in $files; do
	echo Processing $file
	python3 $cwd/$1 --ogg-file "$2/$file" --decoded-file "$3/$file"
done
cd $cwd

