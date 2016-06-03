#!/bin/bash
################
# Let's presume you have lots of files in the /tmp folder that need to be uploaded 
# to AWS S3 in a bucket in a specific folder. Files need to be uploaded in that folder   
# path and create a date folder inside. So, files that are created in a day should be 
# uploaded to the corresponding folder day. 
# Script usage:
# - use -n to specify search pattern
# - use -b to specify the AWS S3 bucket (e.g s3://my_bucket_1221)
# - use -f to specify the folder path (e.g folder1/folder2/folder2)
################
while getopts ":n:b:f:" opt; do
    case $opt in
    #setting argument to variable for later usage
        n)
            name=$OPTARG
            ;;
        b)
            bucket=$OPTARG
            ;;
        f)
            folder=$OPTARG
            ;;
       '?')
            echo "Invalid Argument, onyl -n, -b, -f are valid"
            exit 0
            ;;
        :)
            echo "Option -$OPTARG requires an argument"
            exit 0
    esac
done

# Check if arguments are present
if [ -z $name ]; then
    echo "Please use -n and specify the search criteria"
    exit 0
elif [ -z $bucket ]; then
    echo "Please use -b and specify the bucket name"
    exit 0
elif [ -z $folder ]; then
    echo "Please use -f and specify the folder from the S3 bucket where the files will be uploaded "
    echo "DO NOT specify the date, oly the folder"
    exit 0
fi

today_is=$(date "+%Y-%m-%d")
log_folder="/tmp"
number_of_today_files=$(ls -ltr --time-style="+%Y-%m-%d" $log_folder | grep -i "$name" | grep "$today_is" | head -n -2 | wc -l)

# Check if there are files older than today
number_of_days=$(ls -ltr --time-style="+%Y-%m-%d" $log_folder | grep -i "$name" | grep -v "$today_is" | awk '{print $6}' | uniq | wc -l)

if [ $number_of_days -ne 0 ];
then
    for day in `seq $number_of_days`
    do
        day=$(ls -ltr --time-style="+%Y-%m-%d" $log_folder | grep -i "$name" | grep -v "$today_is" | awk '{print $6}' | uniq | head -n $day | tail -n 1)
        upload_folder="/home/ec2-user/tmp_upload/$name/$day"
        mkdir -p $upload_folder
        cd $log_folder && mv `ls -ltr --time-style="+%Y-%m-%d" $log_folder | grep -i "$name" | grep "$day" | awk '{print $NF}'` $upload_folder
        find $upload_folder -size 0 | xargs -r rm
        aws s3 cp $upload_folder s3://$bucket/$folder/$day --recursive --region eu-west-1     
    done
else
    if [ $number_of_today_files -ne 0 ];
    then
        upload_today_folder="/home/ec2-user/tmp_upload/$name/$today_is"
        mkdir -p $upload_today_folder
        cd $log_folder && mv `ls -ltr --time-style="+%Y-%m-%d" $log_folder | grep -i "$name" | grep "$today_is" | head -n -2 | awk '{print $NF}'` $upload_today_folder
        find $upload_today_folder -size 0 | xargs -r rm
        aws s3 cp $upload_today_folder s3://$bucket/$folder/$today_is --recursive --region eu-west-1
    else
        echo "There are no today files"
    fi
fi