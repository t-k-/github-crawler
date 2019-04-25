#!/bin/bash
file=$1
cat $file | sort | uniq | while read l; do
	echo $l
done
