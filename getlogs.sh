#!/bin/bash

branches=`git branch -a --sort=committerdate`
i=0
maxi=5
while read -r line; do
    i=$((i+1))
    echo "foo $line"
    if [ "$i" -gt "$maxi" ]; then break; fi
done <<< "$branches"

