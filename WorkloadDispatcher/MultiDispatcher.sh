#!/bin/bash

python3 WorkloadDispatcher.py dropall

for f in $1/*
do
  echo $f
  python3 WorkloadDispatcher.py $1"/$f"
done

echo 'Done!'