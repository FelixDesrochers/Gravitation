#!/bin/bash


for i in `seq 0.3 0.05 8`
do
    for j in 1 2 3 4 5
    do
        python Monte_Carlo.py $i $j
    done
done
