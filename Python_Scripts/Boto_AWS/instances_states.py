#!/usr/bin/env python3
'''
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
- call EC2 resources to display all instances
'''

import getopt, sys
import boto3
import time

opts, args = getopt.getopt(sys.argv[1:], "p:")

for opt, arg in opts:
    if opt in ("-p", "--profile" ):
        profile_name = arg

try:
    profile_name
except:
    print ("Please define Profile name using the -p argument")
    exit(1)

session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')
print ("------------------------------------------------")
print ("List all EC2 instances and their states:")
print ("------------------------------------------------")
for instance in ec2.instances.all():
    print ("EC2 instance: ", instance.id, "is " ,instance.state['Name'])

