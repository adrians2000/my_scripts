#!/usr/bin/env python3
import sys
import getopt
import boto3
import argparse
import conf

def main():
    session = boto3.session.Session(profile_name = conf.profile)
    
    ec2_r = session.resource('ec2')
    ec2_c = session.client('ec2')

    vpc = ec2_r.create_vpc(CidrBlock= conf.vpc_range )
    igw = ec2_r.create_internet_gateway()

    vpc_c = ec2_r.Vpc(vpc.id)
    
    tag_vpc(conf.vpc_name, ec2_c, vpc)
    attach_igw(ec2_c, vpc, igw)
    get_main_route_table(ec2_c, vpc)
    add_igw_to_main_route_table(ec2_c, igw, vpc)
    create_subnets(conf.az_list, conf.pub_subnet, ec2_r, conf.zone, vpc)
    create_subnets(conf.az_list, conf.private_subnet, ec2_r, conf.zone, vpc)
    pub_subnets_to_ext_route_table(ec2_c, vpc)
    create_elastic_IP_and_nat(ec2_c, vpc_c, vpc)
    create_route_tables_for_nated_subnets(ec2_c, vpc_c, vpc)

def tag_vpc(vpc_name, ec2_c, vpc):
    tag_rt = ec2_c.create_tags(
        Resources=[
            vpc.id,
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': vpc_name
            },
        ]
    )

def attach_igw(ec2_c, vpc, igw):
    attach_igw = ec2_c.attach_internet_gateway(
        InternetGatewayId=igw.id,
        VpcId=vpc.id,
    )


def get_main_route_table(ec2_c, vpc):
    route_tables = ec2_c.describe_route_tables()

    for table in route_tables['RouteTables']:
        if table['VpcId'] == vpc.id:
            public_route_table_ID = table['RouteTableId']

    return public_route_table_ID

def add_igw_to_main_route_table(ec2_c, igw, vpc):
    public_route_table_ID = get_main_route_table(ec2_c, vpc)

    edit_main_route_table = ec2_c.create_route(
        RouteTableId=public_route_table_ID,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw.id,
    )

    tag_rt = ec2_c.create_tags(
        Resources=[
            public_route_table_ID,
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'External'
            },
        ]
    )

def create_subnets(az_list, subnet_dict, ec2_r, zone, vpc):
    for az in az_list:
        az_subnet = az
        range = (az + '_range')
        
        Cidr_Block = subnet_dict[range]
        A_Zone = zone + az_subnet

        subnet = ec2_r.create_subnet(
            DryRun=False,
            VpcId=vpc.id,
            CidrBlock=Cidr_Block,
            AvailabilityZone=A_Zone
        )

        subnet = ec2_r.Subnet(subnet.id)

        tag = subnet.create_tags(
        DryRun=False,
        Tags=[
            {
                'Key': 'Name',
                'Value': subnet_dict['tag'] + "_" + az
            },
        ]
        )

def pub_subnets_to_ext_route_table(ec2_c, vpc):
    public_route_table_ID = get_main_route_table(ec2_c, vpc)

    subnets = ec2_c.describe_subnets()

    for public_subnet in subnets['Subnets']:
        if public_subnet['VpcId'] == vpc.id:
            if "public" in public_subnet['Tags'][0]['Value']:
                subnet = public_subnet['SubnetId']

                associate_pub_subnets = ec2_c.associate_route_table(
                    SubnetId=subnet,
                    RouteTableId=public_route_table_ID
                )

def create_elastic_IP_and_nat(ec2_c, vpc_c, vpc):
    subnets = vpc_c.subnets.all()
    for subnet in subnets:
        if subnet.vpc_id == vpc.id:
            if "public" in subnet.tags[0]['Value']:
                elastic_ip = ec2_c.allocate_address()
                eip_id = elastic_ip['AllocationId']

                nat = ec2_c.create_nat_gateway(
                    SubnetId = subnet.id,
                    AllocationId = eip_id
                )
                

def create_route_tables_for_nated_subnets(ec2_c, vpc_c, vpc):
    subnets = vpc_c.subnets.all()
    print("Creating route table for nated subs:")
    for subnet in subnets:
        if subnet.vpc_id == vpc.id:
            if "nated" in subnet.tags[0]['Value']:

                private_route_table = ec2_c.create_route_table(
                    VpcId = vpc.id
                )

                associate_pub_subnets = ec2_c.associate_route_table(
                    SubnetId=subnet.id,
                    RouteTableId=private_route_table['RouteTable']['RouteTableId']
                )

# TODO
# Tag route tables

if __name__ == "__main__":
    main()