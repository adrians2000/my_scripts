#!/bin/bash
##########################################################################
# The purpose of this script is to remove all INFO and WARN messages from 
# a log file
##########################################################################
# Define variables, files and paths
app_home_folder="/opt/app"
log_file=$app_home_folder"/log/app.log"

# Convert curent time to epoch time
epoch_date=$(date +%s)

#One day in epoch is 86400
#one_day_in_epoch="86400"

# One week in epoch is 604800
one_week_in_epoch="604800"

one_week_ago=$(($epoch_date-$one_week_in_epoch))

# Get the month and day for a week ago
date_only_month_and_day=$(date -d @$one_week_ago "+%b %d")

# Check if log file exists
if [ -f $log_file ]; then

    # Check if log file contains entryes older than one week
    if [ `grep "$date_only_month_and_day"  $log_file` ]; then

        # Get the last line from a week ago 
        # Remove all lines that contain INFO
        last_line_of_date=$(grep -n "$date_only_month_and_day"  $log_file | awk -F ":" '{print $1}' | tail -n 1)
        ex +1,$last_line_of_date\g/":  INFO | "/d -cwq $log_file

        # Get the last line from a week ago 
        # Remove all lines that contain WARN
        last_line_of_date=$(grep -n "$date_only_month_and_day"  $log_file | awk -F ":" '{print $1}' | tail -n 1)
        ex +1,$last_line_of_date\g/":  WARN | "/d -cwq $log_file
    fi
fi

