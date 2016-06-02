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
- call EC2 resources to display all Security Groups and their names
'''
import getopt, sys
import boto3

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

groups = ec2.security_groups.all()

print ("------------------------------------------------")
print ("List all Security Groups and their names:")
print ("------------------------------------------------")
for group in groups:
    print (group.group_id, " -> ", group.group_name)

