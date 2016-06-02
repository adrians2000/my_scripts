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
- use EC2 resource "create_subnet" to create a new subnet based on 
the arguments added to the script
- use resource "ec2.Vpc(vpc_id).subnets.all" to list all subnets and get the 
newly created subnet's ID
- use EC2 resource "subnet(subnet_id)" to add a tag to the newly created subnet
'''

import sys, getopt
import boto3

opts, args = getopt.getopt(sys.argv[1:], "p:v:c:a:n:")

for opt, arg in opts:
    if opt in ("-p", "--profile"):
        profile_name = arg
    elif opt in ("-v", "--VPC" ):
        vpc_id = arg
    elif opt in ("-c", "--CidrBlock" ):
        cidr_block = arg
    elif opt in ("-a", "--Availability Zone" ):
        zone = arg
    elif opt in ("-n", "--Subnet Name" ):
        subnet_name = arg

try:
    subnet_name
except:
    subnet_name = "Test_new"    

try:
    profile_name, vpc_id, cidr_block, zone
except:
    print ("Please define arguments: -p Profile Name, -v VPC, -a Availability Zone, -c CidrBlock")
    exit(1)


# Open Session
session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')

response = ec2.create_subnet(
    DryRun=False,
    VpcId=vpc_id,
    CidrBlock=cidr_block,
    AvailabilityZone=zone
)

vpc_connect = ec2.Vpc(vpc_id)
subnets = vpc_connect.subnets.all()

for subnet in subnets:
    if subnet.cidr_block == cidr_block:
        subnet_id = subnet.id

subnet = ec2.Subnet(subnet_id)

tag = subnet.create_tags(
    DryRun=False,
    Tags=[
        {
            'Key': 'Name',
            'Value': subnet_name
        },
    ]
)
