#!/bin/bash

python3 WorkloadDispatcher.py dropall

for f in $1
do
  python3 WorkloadDispatcher.py $1 "$f"
done