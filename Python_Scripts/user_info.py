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
- use IAM resource "iam.get_user" to access user info
- use IAM resource "iam.list_access_keys" to get the user's access key
- use IAM resource "groups.all" to get the user's groups 
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

try:
    profile_name, user
except:
    print ("Please define arguments: -p Profile Name and -u User Name")
    exit(1)

# Open Session
session = boto3.session.Session(profile_name = profile_name)
iam  = session.client('iam')

response = iam.get_user(
    UserName=user
)
info = response['User'] 
print ("User: ", info['UserName'])
print ("ID:   ", info['UserId'])
#print ("KEY:  ", info['Arn'])
key = iam.list_access_keys(
    UserName=user
)
info2 = key['AccessKeyMetadata'] 
keys = info2[0]
print ("AccessKey: ", keys['AccessKeyId'])

iam1  = session.resource('iam')

user1 = iam1.User(user)
groups = user1.groups.all()

print ("Group/s:")
for group in groups:
    print ("------",group.name)

