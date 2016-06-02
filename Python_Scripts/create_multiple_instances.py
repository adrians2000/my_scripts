#!/usr/bin/env python3
'''
This script is used to launch one or more EC2 instances in AWS
from the command line
AWS developed a SDK for Python called bobo
More about bobto can be found here:
https://boto3.readthedocs.io/en/latest/

First the user has to log into the AWS console and create access keys
Create ~/.aws/credentials
Add the credentials following the example:
[my_profile]
region = eu-west-1
aws_access_key_id = 12ei23h
aws_secret_access_key = qiwehq

The script......
- Input arguments
- open session
- call resources
- use resources objects to create new EC2 instances
'''

import sys, getopt
import boto3
import time

opts, args = getopt.getopt(sys.argv[1:], "s:p:n:t:g:k:")

for opt, arg in opts:
    if opt in ("-s", "--subnet"):
        subnet = arg
    elif opt in ("-p", "--profile" ):
        profile_name = arg
    elif opt in ("-t", "--instance_Type" ):
        instance_type = arg
    elif opt in ("-g", "--security_group" ):
        group = arg
    elif opt in ("-n", "--number of instances" ):
        num = arg
    elif opt in ("-k", "--SSH Key" ):
        key = arg    

try:
    instance_type
except:
    instance_type = "t2.micro"
    
try:
    num
except:
    num = "1"    

try:
    subnet, profile_name, key, group
except:
    print ("Please define arguments:  -p Profile Name, -s Subnet and -g Security Group and -k ssh key")
    exit(1)

# Open Session
session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')

for i in range(int(num)):
    instance = ec2.create_instances(
        DryRun=False,
        ImageId='ami-e4d18e93',
        InstanceType = instance_type,
        KeyName = key,
        MinCount = 1,
        MaxCount = 1,
        UserData = 'Base64-encoded',
        DisableApiTermination=False,
        NetworkInterfaces=[
            {
                'DeviceIndex': 0,
                'SubnetId': subnet,
                'AssociatePublicIpAddress': True,
                'Groups': [group]
            }
        ]
    )

print ("Successfully launched ", num , "EC2 Instances")
