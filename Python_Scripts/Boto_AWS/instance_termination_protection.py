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
- call resources
- use resources objects to change the instance's termiantion protection
'''

import getopt, sys
import boto3

opts, args = getopt.getopt(sys.argv[1:], "p:i:v:")

for opt, arg in opts:
    if opt in ("-v", "--value"):
        value = arg
    elif opt in ("-p", "--profile" ):
        profile_name = arg
    elif opt in ("-i", "--instance_id" ):
        instance_id = arg

try:
    profile_name
except:
    print ("Please define Profile Name using -p")
    exit(1)

try:
    instance_id
except:
    print ("Please define instance ID using -i ")
    exit(1)

try:
    value
except:
    print ("Please define Termination Protection Value (True/False) using -v")
    exit(1)

session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')

if value == "True":
    value=True
if value == "False":
    value=False    

instance = ec2.Instance(instance_id)
protect  = instance.modify_attribute(
    DisableApiTermination={
        'Value': value
    },
)

print ("Termination protection set to " , value, "for instance " , instance_id)
