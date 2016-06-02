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
- use resources objects to stop, start or terminate the EC2 instance
'''
import getopt, sys
import boto3
import time

opts, args = getopt.getopt(sys.argv[1:], "o:p:i:")

for opt, arg in opts:
    if opt in ("-o", "--stop_start_terminate"):
        operation = arg
    elif opt in ("-p", "--profile" ):
        profile_name = arg
    elif opt in ("-i", "--instance_id" ):
        instance_id = arg

try:
    profile_name
except:
    print ("Please define Profile name using the -p argument")
    exit(1)

try:
    operation 
except:
    print ("Please define Operation Stop/Start/Terminate using the -o argument")
    exit(1)

try:
    instance_id 
except:
    print ("Please enter instance ID using the -i argument")
    exit(1)

# Open Session
session = boto3.session.Session(profile_name = profile_name)
ec2 = session.resource('ec2')

operation_id = ec2.Instance(instance_id)

# Stopping/Starting/Terminating the instance
if operation.lower() in ['start', 'stop', 'terminate']:
    if operation.lower() == "stop":
        print ("Stopping instance " , instance_id , "...")
        check_status = "stopped"
        operation_id.stop()
    if operation.lower() == "start":
        print ("Starting instance " , instance_id , "...")
        check_status = "running"
        operation_id.start()
    if operation.lower() == "terminate":
        print ("Terminating instance " , instance_id , "...")
        check_status = "terminated"
        operation_id.terminate()
else:
    print ("Invalid argument, please enter -o start or -o stop")
    exit(1)
       
# Check if the instance was stopped or started
print ("Checking if the instance is actually " + check_status + " ...")

time.sleep(30)

if operation_id.state['Name'] == check_status:
    print ("Instance " + operation_id.id + " is " + check_status)
else:
    print ("Is not " + check_status + " go online and check what's happening")
    exit(1)
