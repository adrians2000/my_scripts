#!/bin/bash
#######################
# A simple bash script 
# Introduction to:
# - undefined aguments 
# - "if" statement
# - "for" loop
# - print output
#######################
echo "Hello World"
echo  "This is your input: $1 $2 $3 $4"

if [ $1 -eq $2 ];
then
    echo  $1 "=" $2
else
    echo  $1 "!=" $2
fi

for item in `ls /home/`; 
do
    echo $item
done

echo "This for loop was executed " `ls /home/ | wc -l` "times"