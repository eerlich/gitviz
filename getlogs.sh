#!/bin/bash
datadir=gitviz_data
mkdir -p $datadir
matcher=origin
git branch -a --v | tr -s ' ' | cut -f2 -d' '
branches=`git branch -a --v --sort=committerdate | tr \* " " | tr -s ' ' | cut -f2 -d' ' | grep $matcher`
i=0
maxi=5
while read -r line; do
    i=$((i+1))
    fname=`echo ${line} | tr \/ _`.json
    ./log2json.sh "$line" > "$datadir"/"$fname"
    if [ "$i" -gt "$maxi" ]; then break; fi
done <<< "$branches"

