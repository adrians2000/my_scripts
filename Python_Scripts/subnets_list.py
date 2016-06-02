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
- use EC2 resource Vpc(vpc_id).subnetts.all() to display all subnets
'''
import sys, getopt
import boto3

opts, args = getopt.getopt(sys.argv[1:], "p:v:")

for opt, arg in opts:
    if opt in ("-p", "--profile"):
        profile_name = arg
    elif opt in ("-v", "--VPC" ):
        vpc_id = arg

try:
    profile_name, vpc_id
except:
    print ("Please define arguments:  -p Profile Name and -v VPC ID")
    exit(1)


# Open Session
session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')

vpc_connect = ec2.Vpc(vpc_id)
subnets = vpc_connect.subnets.all()

for subnet in subnets:
    name = subnet.tags
    for i in name:
        if i['Key'] == "Name":
            print (subnet.id, subnet.availability_zone, "There are",subnet.available_ip_address_count , "Ips available from range:" , subnet.cidr_block, "named:", i['Value'])
