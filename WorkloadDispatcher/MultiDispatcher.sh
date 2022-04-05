#!/bin/bash

my_pids=()
i=0
n=5

for f in $1/*
do
  echo $f

  if [ ${#my_pids[@]} -eq $n ]
  then
    wait ${my_pids[$i]}
    python3 WorkloadDispatcher.py $f &
    my_pids[$i]=(&!)
  else
    python3 WorkloadDispatcher.py $f &
    my_pids+=(&!)
  fi

  i=$((i+1))
  i=$((i%n))

done

echo 'Done!'