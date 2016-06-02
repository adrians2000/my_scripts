#!/bin/bash
###########################################################
# If you have a list of hosts that you want to set 
# ssh key based authentication you have to create a file
# and inside that file list all the hosts.
# Run the script and just enter the LDAP (or your) password
# when asked
###########################################################

# Define arguments
while getopts ":f:" opt; do
    case "$opt" in
        f) #
            file=$OPTARG
              ;;
        '?')
            echo "Only -f is valid"
            exit 1
            ;;
    esac
done

# Check if -f argument is given 
if [ -z $file ]; then
    echo "There is no argument added to the script, please use -f and specify the file"
    exit 0
fi

# Create ~/.ssh/config
mkdir -p ~/.ssh
touch   ~/.ssh/config

if  grep "StrictHostKeyChecking no" ~/.ssh/config ; then
	echo "No need to modify .ssh/config"
else
	echo "Host *" >>  ~/.ssh/config
	echo "StrictHostKeyChecking no" >>   ~/.ssh/config
	echo "UserKnownHostsFile=/dev/null" >>  ~/.ssh/config
fi

echo -n Enter your LDAP Password: 
read -s password
echo

for i in `cat  $file` ; do

/usr/bin/expect << EOD
        spawn ssh-copy-id $i
expect {
	"*$i' password*"
}
send "$password\r"
expect {
	"*please try again*"
	"*password* "
}
sleep 1
send "exit\r"

expect eof

done

