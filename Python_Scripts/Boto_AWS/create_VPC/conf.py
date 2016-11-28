#!/usr/bin/env python3
import sys
import getopt
import argparse

pub_subnet = {}
private_subnet = {}
vpc_range = ""
vpc_name = ""
profile = ""
zone = ""
az_list = ""

def main():
    global pub_subnet, private_subnet, vpc_range, vpc_name, profile, az_list, zone

    optparser = argparse.ArgumentParser(description="Create VPC vars/opts")
    optparser.add_argument("-p", "--profile", help="aws credentials profile")
    optparser.add_argument("region", type=str.lower, choices=['n_virginia', 'us-east-1', 'ohio', 'us-east-2', 'n_california', 'us-west-1',
        'oregon', 'us-west-2', 'ireland', 'eu-west-1', 'frankfurt', 'eu-central-1', 'tokyo', 'ap-northeast-1', 'seoul', 'ap-northeast-2',
        'singapore', 'ap-southeast-1', 'sydney', 'ap-southeast-2', 'mumbai', 'ap-south-1', 'sao_paulo', 'sa-east-1'], help="AWS region")
    optparser.add_argument("-r", "--vpc_range", type=str, nargs='?')
    optparser.add_argument("-n", "--vpc_name", type=str, nargs='?')
    args = optparser.parse_args()
    vpc_range = args.vpc_range
    vpc_name = args.vpc_name
    profile = args.profile
    
    zone_dict = {
        "n_virginia": ["us-east-1", "abde"],
        "us-east-1": ["us-east-1", "abde"],
        "ohio": ["us-east-2", "abc"],
        "us-east-2": ["us-east-2", "abc"],
        "n_california": ["us-west-1", "ab"],
        "us-west-1": ["us-west-1", "ab"],
        "oregon": ["us-west-2", "abc"],
        "us-west-2": ["us-west-2", "abc"],
        "ireland": ["eu-west-1", "abc"],
        "eu-west-1": ["eu-west-1", "abc"],
        "frankfurt": ["eu-central-1", "ab"],
        "eu-central-1": ["eu-central-1", "ab"],
        "tokyo": ["ap-northeast-1", "ac"],
        "ap-northeast-1": ["ap-northeast-1", "ac"],
        "seoul": ["ap-northeast-2", "ac"],
        "ap-northeast-2": ["ap-northeast-2", "ac"],
        "singapore": ["ap-southeast-1", "ab"],
        "ap-southeast-1": ["ap-southeast-1", "ab"],
        "sydney": ["ap-southeast-2", "abc"],
        "ap-southeast-2": ["ap-southeast-2", "abc"],
        "mumbai": ["ap-south-1", "ab"],
        "ap-south-1": ["ap-south-1", "ab"],
        "sao_paulo": ["sa-east-1", "abc"],
        "sa-east-1": ["sa-east-1", "abc"]
    }
    
    #does not have a default, new region will break it
    zone = zone_dict[args.region][0]
    az_list = zone_dict[args.region][1]

    if vpc_range == None:
        vpc_range = '172.10.10.0/18'

    if vpc_name == None:
        vpc_name = "New_Vpc"

    vpc_parts = vpc_range.split('.')

    num_public = '.'.join(vpc_parts[:3])

    num_last = int(vpc_parts[2]) + 1
    num_private = '.'.join([vpc_parts[0], vpc_parts[1], str(num_last)])

    pub_subnet = {'a_range': num_public + '.0/26' , 'b_range': num_public + '.64/26' ,
                  'c_range': num_public + '.128/26', 'd_range': num_public + '.128/26' ,
                  'e_range': num_public + '.196/26', 'tag' : 'public'}
    private_subnet = {'a_range': num_private +'.0/26', 'b_range': num_private + '.64/26' ,
                      'c_range': num_private +'.128/26', 'd_range': num_private +'.128/26',
                      'e_range': num_private + '.196/26', 'tag': 'nated'}
    
main()