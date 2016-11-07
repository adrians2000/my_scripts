#!/usr/bin/env python3
import sys
import getopt
import argparse

def main():
    optparser = argparse.ArgumentParser(description="Create VPC vars/opts")
    optparser.add_argument("-p", "--profile", help="aws credentials profile")
    optparser.add_argument("region", type=str.lower, choices=['n_virginia', 'us-east-1', 'ohio', 'us-east-2', 'n_california', 'us-west-1',
        'oregon', 'us-west-2', 'ireland', 'eu-west-1', 'frankfurt', 'eu-central-1', 'tokyo', 'ap-northeast-1', 'seoul', 'ap-northeast-2',
        'singapore', 'ap-southeast-1', 'sydney', 'ap-southeast-2', 'mumbai', 'ap-south-1', 'sao_paulo', 'sa-east-1'], help="AWS region")
    optparser.add_argument("vpc_range", type=str, nargs='?')
    optparser.add_argument("vpc_name", type=str, nargs='?')
    args = optparser.parse_args()
    vpc_range = args.vpc_range
    vpc_name = args.vpc_name

    if args.region == "n_virginia" or args.region == "us-east-1":
        zone = "us-east-1"
        az_list = "abde"
    elif args.region == "ohio" or args.region == "us-east-2":
        zone = "us-east-2"
        az_list = "abc"
    elif args.region == "n_california" or args.region == "us-west-1":
        zone = "us-west-1"
        az_list = "ab"
    elif args.region == "oregon" or args.region == "us-west-2":
        zone = "us-west-2"
        az_list = "abc"
    elif args.region == "ireland" or args.region == "eu-west-1":
        zone = "eu-west-1"
        az_list = "abc"
    elif args.region == "frankfurt" or args.region == "eu-central-1":
        zone = "eu-central-1"
        az_list = "ab"
    elif args.region == "tokyo" or args.region == "ap-northeast-1":
        zone = "ap-northeast-1"
        az_list = "ac"
    elif args.region == "seoul" or args.region == "ap-northeast-2":
        zone = "ap-northeast-2"
        az_list = "ac"
    elif args.region == "singapore" or args.region == "ap-southeast-1":
        zone = "ap-southeast-1"
        az_list = "ab"
    elif args.region == "sydney" or args.region == "ap-southeast-2":
        zone = "ap-southeast-2"
        az_list = "abc"
    elif args.region == "mumbai" or args.region == "ap-south-1":
        zone = "ap-south-1"
        az_list = "ab"
    elif args.region == "sao_paulo" or args.region == "sa-east-1":
        zone = "sa-east-1"
        az_list = "abc"

    if vpc_range == None:
        vpc_range = '172.10.10.0/18'

    if vpc_name == None:
        vpc_name = "New_Vpc"

    if "/" in vpc_range[-2:]:
        num_range = vpc_range[:-4]
    else:
        num_range = vpc_range[:-5]

    if "." in num_range[-2:]:
        num_first = num_range[:-1]
        num_last = num_range[-1:]
    elif "." in num_range[-3:]:
        num_first = num_range[:-2]
        num_last = num_range[-2:]
    elif "." in num_range[-4:]:
        num_first = num_range[:-3]
        num_last = num_range[-3:]

    num_last = int(num_last) + 1
    num_last = str(num_last)
    num_private = num_first + num_last
    num_public = num_range

    pub_subnet = {'a_range' : num_public + '.0/26' , 'b_range' : num_public + '.64/26' ,
                  'c_range': num_public + '.128/26', 'd_range' : num_public + '.128/26' ,
                  'e_range' : num_public + '.196/26'}
    private_subnet = {'a_range' : num_private +'.0/26', 'b_range' : num_private + '.64/26' ,
                      'c_range': num_private +'.128/26', 'd_range' : num_private +'.128/26',
                      'e_range' : num_private + '.196/26'}

    return[]

if __name__ == "__main__":
    main()
