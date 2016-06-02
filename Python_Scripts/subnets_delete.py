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
- use EC2 resource "subnet(subnet_id)" to delete the subnet
'''
import sys, getopt
import boto3

opts, args = getopt.getopt(sys.argv[1:], "p:s:")

for opt, arg in opts:
    if opt in ("-p", "--profile"):
        profile_name = arg
    elif opt in ("-s", "--Subnet Id" ):
        subnet_id = arg

try:
    profile_name, subnet_id
except:
    print ("Please define arguments: -p Profile Name and -s Subnet Id")
    exit(1)


# Open Session
session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')

subnet = ec2.Subnet(subnet_id)

response = subnet.delete(
    DryRun=False,

)

