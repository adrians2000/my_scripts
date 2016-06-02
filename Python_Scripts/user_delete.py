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
- use IAM resource "remove_group" to remove the user from all groups
- use IAM resource "iam.User(user).delete" to delete the user 
'''
import sys, getopt
import boto3
import time

opts, args = getopt.getopt(sys.argv[1:], "p:u:")

for opt, arg in opts:
    if opt in ("-p", "--profile"):
        profile_name  = arg
    elif opt in ("-u", "--user" ):
        user = arg

# Open Session
session = boto3.session.Session(profile_name = profile_name)
iam = session.resource('iam')

group_name = iam.User(user)
groups = group_name.groups.all()

for group in groups:
    response = group_name.remove_group(
        GroupName=group.name,
    )

del_user = iam.User(user)
response = del_user.delete()

print ("User ", user , "was deleted" )
