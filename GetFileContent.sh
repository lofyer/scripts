#!/bin/bash
FILES=`find . -type f`
echo $FILES
for i in $FILES
	do
		echo "++++++++++++++++++++++++++" >> m
		echo $i >> m
		echo "++++++++++++++++++++++++++" >> m
		cat $i >> m
	done
