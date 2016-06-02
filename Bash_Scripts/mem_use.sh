#!/bin/bash
#################################
# Live monitoring of memory usage
# Time interval can be changed 
#################################

time_interval="10"
while true
do
    dat=`date | awk '{print $4}'`
    mem=`free  -m | tail -n 2 | head -n 1 | awk  '{print $4}'`
    echo $dat $mem
    sleep $time_interval
done
