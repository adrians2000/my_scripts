#!/bin/bash
############################################
# In case you have a lot of zip files inside
# of lots of folders and you want to search 
# for a string in all zip files
#############################################
# Define arguments
while getopts ":s:" opt; do
    case "$opt" in
        s) #
            string=$OPTARG
              ;;
        '?')
            echo "Only -s is valid"
            exit 1
            ;;
    esac
done

# Check if -s argument is given 
if [ -z $string ]; then
    echo "There is no argument added to the script, please use -s and specify the string"
    exit 0
fi

path="Path_to_files"
tm_dir="/tmp/result_file"

for dir in `ls $path`; do
    cd $path/$dir
    for zip_file in `ls`; do
        unzip $zip_file
        grep -i "$string" preferences.txt
        if [ $? -eq 0 ]; then
            echo $dir " -> " $zip_file >> $tmp_dir
        fi
    done
done

