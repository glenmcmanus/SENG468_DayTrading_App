#!/bin/bash

my_pids=()
counter=0
i=0
n=5

echo m

for f in $1/*
do
  echo $counter

  if [[ ${#my_pids[@]} -eq n ]]
  then
    wait ${my_pids[$i]} 
    python3 WorkloadDispatcher.py $f &
    pid=&!
    my_pids[$i]=${pid}
  else
    python3 WorkloadDispatcher.py $f &
    pid=&!
    my_pids[$i]=${pid}
  fi

  counter=$((counter+1))
  i=$((i+1))
  i=$((i%n))

done

echo 'Done!'
