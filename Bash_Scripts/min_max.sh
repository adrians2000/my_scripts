#!/bin/bash
###################################################
# You have an application that creates files 
# that have a time stamp in their name
# The purpose of this script is to calculate the
# time (min/max) for the file to be created on the 
# Linux machine 
###################################################
# Input argument
while getopts ":f:" opt; do
    case $opt in
    #setting argument to variable for later usage
        f)
            folder=$OPTARG
            ;;
       '?')
            echo "Invalid Argument, onyl -f is valid"
            exit 0
            ;;
        :)
            echo "Option -$OPTARG requires an argument"
            exit 0
    esac
done

if [ -z $folder ]; then
    echo "There is no argument added to the script, please use -f and specify the folder"
    exit 0
fi

# Define and remove possible existing temp files
temp_file="/tmp/dif_time_file"
temp_diff_file="/tmp/diff_file"
rm -rf $temp_file $temp_diff_file

# Put ls output into temp file so it can be parsed 
ls -l --time-style=+%s $folder | awk '{print $6 $7}' >> $temp_file

# Get time stamps 
for item in `cat $temp_file`;
do
    time_created=${item:0:10}
    time_stamp_date=${item:20:4}-${item:24:2}-${item:26:2}
    time_stamp_time=${item:28:2}:${item:30:2}:${item:32:2}

    epoch_timestamp=$(date -d "$time_stamp_date $time_stamp_time" +%s)
 
    echo $(($time_created - $epoch_timestamp)) >> $temp_diff_file
done

# Get Min and Max time
echo "Minimum time"
min=$((`cat $temp_diff_file | sort -n | head -n1` /60))
echo $min
echo "Maximum time"
max=$((`cat $temp_diff_file | sort -n | tail  -n1` /60)):$((`cat $temp_diff_file | sort -n | tail  -n1`%60))
echo $max

# Remove temp files
rm -rf $temp_file $temp_diff_file