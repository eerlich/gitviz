#!/bin/bash
datadir=gitviz_data
mkdir -p $datadir
branches=`git branch -a --sort=committerdate | tr \* " "`
i=0
maxi=5
while read -r line; do
    i=$((i+1))
    fname=`echo ${line} | tr \/ _`.json
    ./log2json.sh "$line" > "$datadir"/"$fname"
    if [ "$i" -gt "$maxi" ]; then break; fi
done <<< "$branches"

