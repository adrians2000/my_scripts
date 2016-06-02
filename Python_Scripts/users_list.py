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
- use IAM resource "users.all" to get all users
- use IAM resource "groups.all" to list each user's group 
'''
import sys, select, os, getopt
import boto3
import time

opts, args = getopt.getopt(sys.argv[1:], "s:p:i:t:g:")

for opt, arg in opts:
    if opt in ("-p", "--profile" ):
        profile_name = arg

try:
    profile_name
except:
    print ("Please enter -p Profile Name")
    exit(1)

session = boto3.session.Session(profile_name = profile_name)
iam = session.resource('iam')

users = iam.users.all()
for user in users:
    user_id = user.name

    print ("User" , "\033[31m" + user_id + "\033[0m", "has the following group/s:" )

    user1 = iam.User(user_id)

    groups = user1.groups.all()

    for group in groups:
        print (group.name)
    print ("----------------------------------------")

    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        break
