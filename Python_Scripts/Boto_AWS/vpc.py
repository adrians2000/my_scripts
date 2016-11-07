#!/usr/bin/env python3
import sys
import getopt
import boto3
import argparse
import conf

profile = "demo"

session = boto3.session.Session(profile_name = profile)
ec2_r = session.resource('ec2')
ec2_c = session.client('ec2')

vpc = ec2_r.create_vpc(CidrBlock= vpc_range )
igw = ec2_r.create_internet_gateway()

vpc_c = ec2_r.Vpc(vpc.id)

def main():
    tag_vpc(vpc_names, ec2_c)
    attach_igw(ec2_c)
    add_igw_to_main_route_table(ec2_c)
    create_public_subnets(az_list, pub_subnet, ec2_r)
    create_private_subnets(az_list, private_subnet, ec2_r)
    pub_subnets_to_ext_route_table(ec2_c)
    create_elastic_IP_and_nat(ec2_c)
    create_route_tables_for_nated_subnets(ec2_c)

def tag_vpc(vpc_name, ec2_c):
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

def attach_igw(ec2_c):
    attach_igw = ec2_c.attach_internet_gateway(
        InternetGatewayId=igw.id,
        VpcId=vpc.id,
    )


def get_main_route_table(ec2_c):
    route_tables = ec2_c.describe_route_tables()

    for table in route_tables['RouteTables']:
        if table['VpcId'] == vpc.id:
            public_route_table_ID = table['RouteTableId']

    return public_route_table_ID

def add_igw_to_main_route_table(ec2_c):
    public_route_table_ID = get_main_route_table(ec2_c)

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

def create_public_subnets(az_list, pub_subnet, ec2_r):
    for az in az_list:
        az_subnet = az
        if az == "x":
            az_subnet = "a"
        range = (az + '_range')
        Cidr_Block = pub_subnet[range]
        A_Zone = zone + az_subnet

        subnet_pub = ec2_r.create_subnet(
            DryRun=False,
            VpcId=vpc.id,
            CidrBlock=Cidr_Block,
            AvailabilityZone=A_Zone
        )

        subnet = ec2_r.Subnet(subnet_pub.id)

        tag = subnet.create_tags(
        DryRun=False,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'public_' + az
            },
        ]
        )

def create_private_subnets(az_list, private_subnet, ec2_r):
    for az in az_list:
        az_subnet = az
        if az == "x":
            az_subnet = "a"
        range = (az + '_range')
        Cidr_Block = private_subnet[range]
        A_Zone = zone + az_subnet

        subnet_pub = ec2_r.create_subnet(
            DryRun=False,
            VpcId=vpc.id,
            CidrBlock=Cidr_Block,
            AvailabilityZone=A_Zone
        )

        subnet = ec2_r.Subnet(subnet_pub.id)

        tag = subnet.create_tags(
        DryRun=False,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'nated_' + az
            },
        ]
        )

def pub_subnets_to_ext_route_table(ec2_c):
    public_route_table_ID = get_main_route_table(ec2_c)

    subnets = ec2_c.describe_subnets()

    for public_subnet in subnets['Subnets']:
        if public_subnet['VpcId'] == vpc.id:
            if "public" in public_subnet['Tags'][0]['Value']:
                subnet = public_subnet['SubnetId']

                associate_pub_subnets = ec2_c.associate_route_table(
                SubnetId=subnet,
                RouteTableId=public_route_table_ID
                )

def create_elastic_IP_and_nat(ec2_c):
    subnets = vpc_c.subnets.all()

    for subnet in subnets:
        if subnet.vpc_id == vpc.id:
            if "public" in subnet.tags[0]['Value']:
                elastic_ip = ec2_c.allocate_address()
                eip_id = elastic_ip['AllocationId']

                nat = ec2_c.create_nat_gateway(
                    SubnetId=subnet.id,
                    AllocationId=eip_id
                )

def create_route_tables_for_nated_subnets(ec2_c):
    subnets = vpc_c.subnets.all()

    for subnet in subnets:
        if subnet.vpc_id == vpc.id:
            if "nated" in subnet.tags[0]['Value']:

                private_route_table = ec2_c.create_route_table(
                    VpcId=vpc.id
                )

                associate_pub_subnets = ec2_c.associate_route_table(
                    SubnetId=subnet.id,
                    RouteTableId=private_route_table['RouteTable']['RouteTableId']
                )

# TODO
# Tag route tables

#if __name__ == "__main__":
#    main()
