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
- use IAM resource "add_group" to add a user to a specified group 
'''

import sys, getopt
import boto3
import time

opts, args = getopt.getopt(sys.argv[1:], "p:u:g:")

for opt, arg in opts:
    if opt in ("-p", "--profile"):
        profile_name  = arg
    elif opt in ("-u", "--user" ):
        user = arg
    elif opt in ("-g", "--group" ):
        group = arg

try:
    profile_name, user, group
except:
    print ("Please define arguments: -p Profile Name, -u User Name, -g Group Name")
    exit(1)

session = boto3.session.Session(profile_name = profile_name)
iam = session.resource('iam')

group_name = iam.User(user)
response = group_name.add_group(
    GroupName=group,
 
)

