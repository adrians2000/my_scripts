#!/bin/bash
#####################################################
# The purpose of this script is to disable 
# all enabled workflows in Mediation Zone
# - Creates a list that contains all enabled workflows
# - Disables all wf from that list
# - Enables all wf from the input file
# Input file can be the same file as for disabled
#####################################################
# Define arguments
while getopts ":o:f:" opt; do
    case "$opt" in
        o) #
            operation=$OPTARG
              ;;
        f) #
            input_file=$OPTARG
              ;;
        '?')
            echo "Only -o and -f are valid"
            exit 1
            ;;
    esac
done

# Check if -o argument is given 
if [ -z $operation ]; then
    echo "There is no argument added to the script, please use -o and specify enable or disable"
    exit 0
fi

# Define variables
date=$(date "+%Y-%m-%d_%H:%M:%S:%3N")
file="/tmp/wfgr_en_$date"
pass="mzadmin_pass"

if [ $operation == "disable" ]; then
    mzsh mzadmin/$pass wfgrouplist | tr -d '\r' | grep " E " | awk '{print $1}' > $file
    mzsh mzadmin/$pass wfgroup$operation `cat $file`
    echo $file "contains all WF that were disabled"
elif [ $operation == "enable" ]; then
    if [ -z $input_file ]; then
        echo "Please specify file with -f"
        exit 0
    else
        if [ -f $input_file ]; then
            mzsh mzadmin/$pass wfgroup$operation `cat $file`
        else
            echo "$input_file is not there, please check it's existance and try again"
        fi
    fi
else
    echo "Unknown operation, only enable/disable is permited"
fi

