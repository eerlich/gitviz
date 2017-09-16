#!/bin/bash
rm -r gitviz_data
rm *.json

git fetch
./getlogs.sh
python getgraphs.py
