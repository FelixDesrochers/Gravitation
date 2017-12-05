#!/bin/bash


for i in `seq 0.5 59.5`
do
    for j in 1 2 3 4 5
    do
        python Monte_Carlo.py $i $j
    done
done
