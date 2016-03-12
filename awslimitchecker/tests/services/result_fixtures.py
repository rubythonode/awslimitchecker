"""
awslimitchecker/tests/services/result_fixtures.py

The latest version of this package is available at:
<https://github.com/jantman/awslimitchecker>

################################################################################
Copyright 2015 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of awslimitchecker, also known as awslimitchecker.

    awslimitchecker is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    awslimitchecker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with awslimitchecker.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/pydnstest> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
################################################################################
"""

import sys
from datetime import datetime
import boto3
from boto3.utils import ServiceContext
from dateutil.tz import tzutc

# https://code.google.com/p/mock/issues/detail?id=249
# py>=3.4 should use unittest.mock not the mock package on pypi
if (
        sys.version_info[0] < 3 or
        sys.version_info[0] == 3 and sys.version_info[1] < 4
):
    from mock import Mock
else:
    from unittest.mock import Mock

# boto3 response fixtures


def get_boto3_resource_model(service_name, resource_name):
    """
    Return a boto3 resource model class for the given service_name and
    resource_name (type).

    NOTE that when the boto3.session.Session object is instantiated, the
     underlying botocore Session will attempt HTTP requests to 169.254.169.254
     to retrieve Instance Metadata and an IAM Role. In order to prevent this,
     you should simply export some bogus AWS credential environment variables.

    :param service_name: name of the service
    :type service_name: str
    :param resource_name: name of the resource type/model to get
    :type resource_name: str
    :return: boto3 resource model class
    """
    session = boto3.session.Session(region_name='us-east-1')
    loader = session._session.get_component('data_loader')
    json_resource_model = loader.load_service_model(service_name,
                                                    'resources-1')
    service_resource = session.resource(service_name)
    service_model = service_resource.meta.client.meta.service_model

    resource_model = json_resource_model['resources'][resource_name]
    resource_cls = session.resource_factory.load_from_definition(
        resource_name=resource_name,
        single_resource_json_definition=resource_model,
        service_context=ServiceContext(
            service_name=service_name,
            resource_json_definitions=json_resource_model['resources'],
            service_model=service_model,
            service_waiter_model=None
        )
    )
    return resource_cls

# get some resource models for specs...
Instance = get_boto3_resource_model('ec2', 'Instance')
SecurityGroup = get_boto3_resource_model('ec2', 'SecurityGroup')
ClassicAddress = get_boto3_resource_model('ec2', 'ClassicAddress')
VpcAddress = get_boto3_resource_model('ec2', 'VpcAddress')
NetworkInterface = get_boto3_resource_model('ec2', 'NetworkInterface')


class EBS(object):

    test_find_usage_ebs = {
        'Volumes': [
            # 500G magnetic
            {
                'VolumeId': 'vol-1',
                'Size': 500,
                'VolumeType': 'standard',
                'Iops': None,
                # boilerplate sample response
                'SnapshotId': 'string',
                'AvailabilityZone': 'string',
                'State': 'available',
                'CreateTime': datetime(2015, 1, 1),
                'Attachments': [
                    {
                        'VolumeId': 'string',
                        'InstanceId': 'string',
                        'Device': 'string',
                        'State': 'attached',
                        'AttachTime': datetime(2015, 1, 1),
                        'DeleteOnTermination': True
                    },
                ],
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
                'Encrypted': False,
                'KmsKeyId': 'string'
            },
            # 8G magnetic
            {
                'VolumeId': 'vol-2',
                'Size': 8,
                'VolumeType': 'standard',
                'Iops': None,
            },
            # 15G general purpose SSD, 45 IOPS
            {
                'VolumeId': 'vol-3',
                'Size': 15,
                'VolumeType': 'gp2',
                'Iops': 45,
            },
            # 30G general purpose SSD, 90 IOPS
            {
                'VolumeId': 'vol-4',
                'Size': 30,
                'VolumeType': 'gp2',
                'Iops': 90,
            },
            # 400G PIOPS, 700 IOPS
            {
                'VolumeId': 'vol-5',
                'Size': 400,
                'VolumeType': 'io1',
                'Iops': 700,
            },
            # 100G PIOPS, 300 IOPS
            {
                'VolumeId': 'vol-6',
                'Size': 100,
                'VolumeType': 'io1',
                'Iops': 300,
            },
            # othertype
            {
                'VolumeId': 'vol-7',
                'VolumeType': 'othertype',
            },
        ]
    }

    test_find_usage_snapshots = {
        'Snapshots': [
            {
                'SnapshotId': 'snap-1',
                'VolumeId': 'string',
                'State': 'completed',
                'StateMessage': 'string',
                'StartTime': datetime(2015, 1, 1),
                'Progress': 'string',
                'OwnerId': 'string',
                'Description': 'string',
                'VolumeSize': 123,
                'OwnerAlias': 'string',
                'Tags': [
                    {
                        'Key': 'string',
                        'Value': 'string'
                    },
                ],
                'Encrypted': False,
                'KmsKeyId': 'string',
                'DataEncryptionKeyId': 'string'
            },
            {'SnapshotId': 'snap-2'},
            {'SnapshotId': 'snap-3'},
        ]
    }


class VPC(object):
    test_find_usage_vpcs = {
        'Vpcs': [
            {
                'VpcId': 'vpc-1',
                'State': 'available',
                'CidrBlock': 'string',
                'DhcpOptionsId': 'string',
                'Tags': [
                    {
                        'Key': 'fooTag',
                        'Value': 'fooVal'
                    },
                ],
                'InstanceTenancy': 'default',
                'IsDefault': False
            },
            {'VpcId': 'vpc-2'},
        ]
    }

    test_find_usage_subnets = {
        'Subnets': [
            {
                'SubnetId': 'string',
                'State': 'available',
                'VpcId': 'vpc-1',
                'CidrBlock': 'string',
                'AvailableIpAddressCount': 123,
                'AvailabilityZone': 'string',
                'DefaultForAz': False,
                'MapPublicIpOnLaunch': True,
                'Tags': [
                    {
                        'Key': 'tagKey',
                        'Value': 'tagVal'
                    },
                ]
            },
            {'VpcId': 'vpc-1'},
            {'VpcId': 'vpc-2'},
        ]
    }

    test_find_usage_acls = {
        'NetworkAcls': [
            {
                'NetworkAclId': 'acl-1',
                'VpcId': 'vpc-1',
                'IsDefault': True,
                'Entries': [
                    {
                        'RuleNumber': 123,
                        'Protocol': 'string',
                        'RuleAction': 'allow',
                        'Egress': True,
                        'CidrBlock': 'string',
                        'IcmpTypeCode': {
                            'Type': 123,
                            'Code': 123
                        },
                        'PortRange': {
                            'From': 123,
                            'To': 123
                        }
                    },
                    {
                        'RuleNumber': 124,
                        'Protocol': 'string',
                        'RuleAction': 'allow',
                        'Egress': False,
                        'CidrBlock': 'string',
                        'IcmpTypeCode': {
                            'Type': 123,
                            'Code': 123
                        },
                        'PortRange': {
                            'From': 124,
                            'To': 124
                        }
                    },
                    {
                        'RuleNumber': 125,
                        'Protocol': 'string',
                        'RuleAction': 'deny',
                        'Egress': False,
                        'CidrBlock': 'string',
                        'IcmpTypeCode': {
                            'Type': 123,
                            'Code': 123
                        },
                        'PortRange': {
                            'From': 125,
                            'To': 125
                        }
                    },
                ],
                'Associations': [
                    {
                        'NetworkAclAssociationId': 'string',
                        'NetworkAclId': 'string',
                        'SubnetId': 'string'
                    },
                ],
                'Tags': [
                    {
                        'Key': 'tagKey',
                        'Value': 'tagVal'
                    },
                ]
            },
            {
                'NetworkAclId': 'acl-2',
                'VpcId': 'vpc-1',
                'Entries': [1],
            },
            {
                'NetworkAclId': 'acl-3',
                'VpcId': 'vpc-2',
                'Entries': [1, 2, 3, 4, 5],
            },
        ]
    }

    test_find_usage_route_tables = {
        'RouteTables': [
            {
                'RouteTableId': 'rt-1',
                'VpcId': 'vpc-1',
                'Routes': [
                    {
                        'DestinationCidrBlock': 'string',
                        'DestinationPrefixListId': 'string',
                        'GatewayId': 'string',
                        'InstanceId': 'string',
                        'InstanceOwnerId': 'string',
                        'NetworkInterfaceId': 'string',
                        'VpcPeeringConnectionId': 'string',
                        'NatGatewayId': 'string',
                        'State': 'active',
                        'Origin': 'CreateRouteTable'
                    },
                    {'foo': 'bar', 'baz': 'blam'},
                    {'foo': 'bar', 'baz': 'blam'},
                ],
                'Associations': [
                    {
                        'RouteTableAssociationId': 'string',
                        'RouteTableId': 'string',
                        'SubnetId': 'string',
                        'Main': True
                    },
                ],
                'Tags': [
                    {
                        'Key': 'tagKey',
                        'Value': 'tagVal'
                    },
                ],
                'PropagatingVgws': [
                    {
                        'GatewayId': 'string'
                    },
                ]
            },
            {
                'RouteTableId': 'rt-2',
                'VpcId': 'vpc-1',
                'Routes': [
                    {'foo': 'bar', 'baz': 'blam'},
                ],
            },
            {
                'RouteTableId': 'rt-3',
                'VpcId': 'vpc-2',
                'Routes': [
                    {'foo': 'bar', 'baz': 'blam'},
                    {'foo': 'bar', 'baz': 'blam'},
                    {'foo': 'bar', 'baz': 'blam'},
                    {'foo': 'bar', 'baz': 'blam'},
                    {'foo': 'bar', 'baz': 'blam'},
                ],
            }
        ]
    }

    test_find_usage_internet_gateways = {
        'InternetGateways': [
            {
                'InternetGatewayId': 'gw-1',
                'Attachments': [
                    {
                        'VpcId': 'string',
                        'State': 'attached'
                    },
                ],
                'Tags': [
                    {
                        'Key': 'tagKey',
                        'Value': 'tagVal'
                    },
                ]
            },
            {'InternetGatewayId': 'gw-2'}
        ]
    }


class RDS(object):
    test_find_usage_instances = []
    # first result page
    test_find_usage_instances.append({
        'DBInstances': [
            {
                'PubliclyAccessible': False,
                'MasterUsername': 'myuser',
                'LicenseModel': 'general-public-license',
                'VpcSecurityGroups': [
                    {
                        'Status': 'active',
                        'VpcSecurityGroupId': 'sg-aaaaaaaa'
                    }
                ],
                'InstanceCreateTime': 1429910904.366,
                'OptionGroupMemberships': [
                    {
                        'Status': 'in-sync',
                        'OptionGroupName': 'default:mysql-5-6'
                    }
                ],
                'PendingModifiedValues': {
                    'MultiAZ': None,
                    'MasterUserPassword': None,
                    'Port': None,
                    'Iops': None,
                    'AllocatedStorage': None,
                    'EngineVersion': None,
                    'BackupRetentionPeriod': None,
                    'DBInstanceClass': None,
                    'DBInstanceIdentifier': None
                },
                'Engine': 'mysql',
                'MultiAZ': True,
                'LatestRestorableTime': 1435966800.0,
                'DBSecurityGroups': [
                    {
                        'Status': 'active',
                        'DBSecurityGroupName': 'mydb-dbsecuritygroup-aaaa'
                    }
                ],
                'DBParameterGroups': [
                    {
                        'DBParameterGroupName': 'default.mysql5.6',
                        'ParameterApplyStatus': 'in-sync'
                    }
                ],
                'ReadReplicaSourceDBInstanceIdentifier': None,
                'AutoMinorVersionUpgrade': True,
                'PreferredBackupWindow': '07:00-08:00',
                'DBSubnetGroup': {
                    'VpcId': 'vpc-abcdef01',
                    'Subnets': [
                        {
                            'SubnetStatus': 'Active',
                            'SubnetIdentifier': 'subnet-aaaaaaaa',
                            'SubnetAvailabilityZone': {
                                'Name': 'us-east-1d',
                                'ProvisionedIopsCapable': False
                            }
                        },
                        {
                            'SubnetStatus': 'Active',
                            'SubnetIdentifier': 'subnet-22222222',
                            'SubnetAvailabilityZone': {
                                'Name': 'us-east-1a',
                                'ProvisionedIopsCapable': False
                            }
                        }
                    ],
                    'DBSubnetGroupName': 'mydb-dbsubnetgroup-abcd',
                    'SubnetGroupStatus': 'Complete',
                    'DBSubnetGroupDescription': 'Subnet group for RDS instance'
                },
                'SecondaryAvailabilityZone': 'us-east-1a',
                'ReadReplicaDBInstanceIdentifiers': [],
                'AllocatedStorage': 200,
                'BackupRetentionPeriod': 7,
                'DBName': 'wordpress',
                'PreferredMaintenanceWindow': 'tue:08:00-tue:09:00',
                'Endpoint': {
                    'Port': 3306,
                    'Address': 'foo.bar.us-east-1.rds.amazonaws.com'
                },
                'DBInstanceStatus': 'available',
                'StatusInfos': None,
                'EngineVersion': '5.6.22',
                'CharacterSetName': None,
                'AvailabilityZone': 'us-east-1d',
                'Iops': None,
                'DBInstanceClass': 'db.t2.small',
                'DBInstanceIdentifier': 'foo'
            },
        ],
        'NextToken': 'string'
    })
    # second result page
    test_find_usage_instances.append({
        'DBInstances': [
            {
                'PubliclyAccessible': False,
                'MasterUsername': 'myuser2',
                'LicenseModel': 'postgresql-license',
                'VpcSecurityGroups': [
                    {
                        'Status': 'active',
                        'VpcSecurityGroupId': 'sg-12345678'
                    }
                ],
                'InstanceCreateTime': 1432238504.239,
                'OptionGroupMemberships': [
                    {
                        'Status': 'in-sync',
                        'OptionGroupName': 'default:postgres-9-3'
                    }
                ],
                'PendingModifiedValues': {
                    'MultiAZ': None,
                    'MasterUserPassword': None,
                    'Port': None,
                    'Iops': None,
                    'AllocatedStorage': None,
                    'EngineVersion': None,
                    'BackupRetentionPeriod': None,
                    'DBInstanceClass': None,
                    'DBInstanceIdentifier': None
                },
                'Engine': 'postgres',
                'MultiAZ': False,
                'LatestRestorableTime': 1435966550.0,
                'DBSecurityGroups': [
                    {
                        'Status': 'active',
                        'DBSecurityGroupName': 'sg1234-dbsecuritygroup-abcd'
                    }
                ],
                'DBParameterGroups': [
                    {
                        'DBParameterGroupName': 'default.postgres9.3',
                        'ParameterApplyStatus': 'in-sync'
                    }
                ],
                'ReadReplicaSourceDBInstanceIdentifier': None,
                'AutoMinorVersionUpgrade': True,
                'PreferredBackupWindow': '03:09-03:39',
                'DBSubnetGroup': {
                    'VpcId': 'vpc-87654321',
                    'Subnets': [
                        {
                            'SubnetStatus': 'Active',
                            'SubnetIdentifier': 'subnet-a1234567',
                            'SubnetAvailabilityZone': {
                                'Name': 'us-east-1e',
                                'ProvisionedIopsCapable': False
                            }
                        },
                        {
                            'SubnetStatus': 'Active',
                            'SubnetIdentifier': 'subnet-b1234567',
                            'SubnetAvailabilityZone': {
                                'Name': 'us-east-1a',
                                'ProvisionedIopsCapable': False
                            }
                        },
                        {
                            'SubnetStatus': 'Active',
                            'SubnetIdentifier': 'subnet-c1234567',
                            'SubnetAvailabilityZone': {
                                'Name': 'us-east-1d',
                                'ProvisionedIopsCapable': False
                            }
                        }
                    ],
                    'DBSubnetGroupName': 'mydb-dbsubnetgroup-abcdef',
                    'SubnetGroupStatus': 'Complete',
                    'DBSubnetGroupDescription': 'Subnet group for RDS instance'
                },
                'SecondaryAvailabilityZone': None,
                'ReadReplicaDBInstanceIdentifiers': ['db-123', 'db-456'],
                'AllocatedStorage': 50,
                'BackupRetentionPeriod': 1,
                'DBName': 'mydbname',
                'PreferredMaintenanceWindow': 'mon:05:11-mon:05:41',
                'Endpoint': {
                    'Port': 5432,
                    'Address': 'baz.blam.us-east-1.rds.amazonaws.com'
                },
                'DBInstanceStatus': 'available',
                'StatusInfos': None,
                'EngineVersion': '9.3.6',
                'CharacterSetName': None,
                'AvailabilityZone': 'us-east-1a',
                'Iops': None,
                'DBInstanceClass': 'db.t2.small',
                'DBInstanceIdentifier': 'baz'
            }
        ]
    })

    test_find_usage_snapshots = []
    # first result page
    test_find_usage_snapshots.append({
        "DBSnapshots": [
            {
                "AllocatedStorage": 100,
                "AvailabilityZone": "us-east-1a",
                "DBInstanceIdentifier": "foo-db",
                "DBSnapshotIdentifier": "foo-db-final-snapshot",
                "Engine": "postgres",
                "EngineVersion": "9.3.3",
                "InstanceCreateTime": 1408035263.101,
                "Iops": 1000,
                "LicenseModel": "postgresql-license",
                "MasterUsername": "dbfoouser",
                "OptionGroupName": "default:postgres-9-3",
                "PercentProgress": 100,
                "Port": 5432,
                "SnapshotCreateTime": 1408454469.536,
                "SnapshotType": "manual",
                "SourceRegion": None,
                "Status": "available",
                "VpcId": None
            },
            {
                "AllocatedStorage": 50,
                "AvailabilityZone": "us-east-1d",
                "DBInstanceIdentifier": "bd1t3lf90p3lqdx",
                "DBSnapshotIdentifier":
                    "rds:bd1t3lf90p3lqdx-2015-06-29-07-02",
                "Engine": "mysql",
                "EngineVersion": "5.6.22",
                "InstanceCreateTime": 1429910904.366,
                "Iops": None,
                "LicenseModel": "general-public-license",
                "MasterUsername": "dbuser3",
                "OptionGroupName": "default:mysql-5-6",
                "PercentProgress": 100,
                "Port": 3306,
                "SnapshotCreateTime": 1435561349.441,
                "SnapshotType": "automated",
                "SourceRegion": None,
                "Status": "available",
                "VpcId": "vpc-1ee8937b"
            },
        ],
        'NextToken': 'string'
    })
    test_find_usage_snapshots.append({
        'DBSnapshots': [
            {
                "AllocatedStorage": 25,
                "AvailabilityZone": "us-east-1d",
                "DBInstanceIdentifier": "md1e8qwtegkjdgy",
                "DBSnapshotIdentifier":
                    "rds:md1e8qwtegkjdgy-2015-06-29-07-06",
                "Engine": "postgres",
                "EngineVersion": "9.3.6",
                "InstanceCreateTime": 1433883813.314,
                "Iops": None,
                "LicenseModel": "postgresql-license",
                "MasterUsername": "dbuser4",
                "OptionGroupName": "default:postgres-9-3",
                "PercentProgress": 100,
                "Port": 5432,
                "SnapshotCreateTime": 1435561593.669,
                "SnapshotType": "automated",
                "SourceRegion": None,
                "Status": "available",
                "VpcId": "vpc-1ee8937b"
            },
        ],
    })

    test_find_usage_param_groups = []
    test_find_usage_param_groups.append({
        "DBParameterGroups": [
            {
                "DBParameterGroupFamily": "mysql5.6",
                "DBParameterGroupName": "default.mysql5.6",
                "Description":
                    "Default parameter group for mysql5.6"
            },
            {
                "DBParameterGroupFamily": "mysql5.6",
                "DBParameterGroupName": "my_mysql5.6",
                "Description":
                    "My custom parameter group for mysql5.6"
            },
        ],
        'NextToken': 'string'
    })
    test_find_usage_param_groups.append({
        'DBParameterGroups': [
            {
                "DBParameterGroupFamily": "postgres9.3",
                "DBParameterGroupName": "default.postgres9.3",
                "Description":
                    "Default parameter group for postgres9.3"
            }
        ]
    })

    test_find_usage_subnet_groups = []
    test_find_usage_subnet_groups.append({
        "DBSubnetGroups": [
            {
                "DBSubnetGroupDescription":
                    "Subnet group for CloudFormation RDS instance",
                "DBSubnetGroupName":
                    "SubnetGroup1",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1d",
                            "ProvisionedIopsCapable": False
                        },
                        "SubnetIdentifier": "subnet-38e87861",
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a",
                            "ProvisionedIopsCapable": False
                        },
                        "SubnetIdentifier": "subnet-4f027f38",
                        "SubnetStatus": "Active"
                    }
                ],
                "VpcId": "vpc-1ee8937b"
            },
        ],
        'NextToken': 'string'
    })
    test_find_usage_subnet_groups.append({
        'DBSubnetGroups': [
            {
                "DBSubnetGroupDescription":
                    "Created from the RDS Management Console",
                "DBSubnetGroupName": "default",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1e",
                            "ProvisionedIopsCapable": False
                        },
                        "SubnetIdentifier": "subnet-49071f61",
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a",
                            "ProvisionedIopsCapable": False
                        },
                        "SubnetIdentifier": "subnet-6fe23c18",
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1d",
                            "ProvisionedIopsCapable": False
                        },
                        "SubnetIdentifier": "subnet-a9b54df0",
                        "SubnetStatus": "Active"
                    }
                ],
                "VpcId": "vpc-c300b9a6"
            },
            {
                "DBSubnetGroupDescription":
                    "Subnet group for CloudFormation RDS instance",
                "DBSubnetGroupName":
                    "SubnetGroup2",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-1a",
                            "ProvisionedIopsCapable": False
                        },
                        "SubnetIdentifier": "subnet-0b037e7c",
                        "SubnetStatus": "Active"
                    }
                ],
                "VpcId": "vpc-73ec9716"
            },
        ],
    })

    test_find_usage_option_groups = []
    test_find_usage_option_groups.append({
        "OptionGroupsList": [
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'aurora',
                'MajorEngineVersion': '5.6',
                'OptionGroupDescription': 'Default option group for aurora 5.6',
                'OptionGroupName': 'default:aurora-5-6',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'mariadb',
                'MajorEngineVersion': '10.0',
                'OptionGroupDescription':
                    'Default option group for mariadb 10.0',
                'OptionGroupName': 'default:mariadb-10-0',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'mysql',
                'MajorEngineVersion': '5.1',
                'OptionGroupDescription': 'Default option group for mysql 5.1',
                'OptionGroupName': 'default:mysql-5-1',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'mysql',
                'MajorEngineVersion': '5.5',
                'OptionGroupDescription': 'Default option group for mysql 5.5',
                'OptionGroupName': 'default:mysql-5-5',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'mysql',
                'MajorEngineVersion': '5.6',
                'OptionGroupDescription': 'Default option group for mysql 5.6',
                'OptionGroupName': 'default:mysql-5-6',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'mariadb',
                'MajorEngineVersion': '10.0',
                'OptionGroupDescription':
                    'Custom option group for mariadb 10.0',
                'OptionGroupName': 'my_mariadb-10-0',
                'Options': []
            },
        ],
        'NextToken': 'string'
    })
    test_find_usage_option_groups.append({
        'OptionGroupsList': [
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'mysql',
                'MajorEngineVersion': '5.7',
                'OptionGroupDescription': 'Default option group for mysql 5.7',
                'OptionGroupName': 'default:mysql-5-7',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'oracle-se',
                'MajorEngineVersion': '11.2',
                'OptionGroupDescription':
                    'Default option group for oracle-se 11.2',
                'OptionGroupName': 'default:oracle-se-11-2',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'oracle-se1',
                'MajorEngineVersion': '11.2',
                'OptionGroupDescription':
                    'Default option group for oracle-se1 11.2',
                'OptionGroupName': 'default:oracle-se1-11-2',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'postgres',
                'MajorEngineVersion': '9.3',
                'OptionGroupDescription':
                    'Default option group for postgres 9.3',
                'OptionGroupName': 'default:postgres-9-3',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'postgres',
                'MajorEngineVersion': '9.4',
                'OptionGroupDescription':
                    'Default option group for postgres 9.4',
                'OptionGroupName': 'default:postgres-9-4',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'oracle-se1',
                'MajorEngineVersion': '11.2',
                'OptionGroupDescription':
                    'Custom option group for oracle-se1 11.2',
                'OptionGroupName': 'my_oracle-se1-11-2',
                'Options': []
            },
            {
                'AllowsVpcAndNonVpcInstanceMemberships': True,
                'EngineName': 'postgres',
                'MajorEngineVersion': '9.4',
                'OptionGroupDescription':
                    'Custom option group for postgres 9.4',
                'OptionGroupName': 'my_postgres-9-4',
                'Options': []
            },
        ]
    })

    test_find_usage_event_subscriptions = []
    test_find_usage_event_subscriptions.append({
        "EventSubscriptionsList": [
            {
                'CustomerAwsId': 'string',
                'CustSubscriptionId': 'string',
                'SnsTopicArn': 'string',
                'Status': 'string',
                'SubscriptionCreationTime': 'string',
                'SourceType': 'string',
                'SourceIdsList': [
                    'string',
                ],
                'EventCategoriesList': [
                    'string',
                ],
                'Enabled': True
            }
        ],
        "NextToken": 'string'
    })
    test_find_usage_event_subscriptions.append({
        "EventSubscriptionsList": [
            {
                'CustomerAwsId': 'string',
                'CustSubscriptionId': 'string',
                'SnsTopicArn': 'string',
                'Status': 'string',
                'SubscriptionCreationTime': 'string',
                'SourceType': 'string',
                'SourceIdsList': [
                    'string',
                ],
                'EventCategoriesList': [
                    'string',
                ],
                'Enabled': False
            }
        ]
    })

    test_find_usage_security_groups = []
    test_find_usage_security_groups.append({
        "DBSecurityGroups": [
            {
                "DBSecurityGroupDescription": "Frontend Access",
                "DBSecurityGroupName":
                    "SecurityGroup1",
                "EC2SecurityGroups": [
                    {
                        "EC2SecurityGroupId": "sg-c6dd95a2",
                        "EC2SecurityGroupName":
                            "EC2SG1",
                        "EC2SecurityGroupOwnerId": None,
                        "Status": "authorized"
                    }
                ],
                "IPRanges": [],
                "OwnerId": "123456789012",
                "VpcId": None
            },
            {
                "DBSecurityGroupDescription": "empty",
                "DBSecurityGroupName":
                    "MyEmptySecurityGroup",
                "EC2SecurityGroups": [],
                "IPRanges": [],
                "OwnerId": "123456789012",
                "VpcId": None
            },
            {
                "DBSecurityGroupDescription":
                    "default:vpc-a926c2cc",
                "DBSecurityGroupName": "default:vpc-a926c2cc",
                "EC2SecurityGroups": [],
                "IPRanges": [],
                "OwnerId": "123456789012",
                "VpcId": "vpc-a926c2cc"
            },
        ],
        'NextToken': 'string'
    })
    test_find_usage_security_groups.append({
        'DBSecurityGroups': [
            {
                "DBSecurityGroupDescription": "Frontend Access",
                "DBSecurityGroupName": "SecurityGroup2",
                "EC2SecurityGroups": [
                    {
                        "EC2SecurityGroupId": "sg-aaaaaaaa",
                        "EC2SecurityGroupName": "SGName-aaaaaaaa",
                        "EC2SecurityGroupOwnerId": None,
                        "Status": "authorized"
                    },
                    {
                        "EC2SecurityGroupId": "sg-bbbbbbbb",
                        "EC2SecurityGroupName": "SGName-bbbbbbbb",
                        "EC2SecurityGroupOwnerId": None,
                        "Status": "authorized"
                    },
                    {
                        "EC2SecurityGroupId": "sg-cccccccc",
                        "EC2SecurityGroupName": "SGName-cccccccc",
                        "EC2SecurityGroupOwnerId": None,
                        "Status": "authorized"
                    },
                ],
                "IPRanges": [],
                "OwnerId": "123456789012",
                "VpcId": "vpc-73ec9716"
            },
            {
                'VpcId': None,
                'DBSecurityGroupDescription':
                    'awslimitchecker test',
                'IPRanges': [
                    {
                        'Status': 'authorized',
                        'CIDRIP': '76.122.124.15/32'
                    },
                    {
                        'Status': 'authorized',
                        'CIDRIP': '66.6.152.59/32'
                    }
                ],
                'OwnerId': '123456789012',
                'EC2SecurityGroups': [],
                'DBSecurityGroupName': 'alctest'
            }
        ],
    })

    test_find_usage_reserved_instances = []
    test_find_usage_reserved_instances.append({
        'ReservedDBInstances': [
            {
                'ReservedDBInstanceId': 'string',
                'ReservedDBInstancesOfferingId': 'string',
                'DBInstanceClass': 'string',
                'StartTime': datetime(2015, 1, 1),
                'Duration': 123,
                'FixedPrice': 123.0,
                'UsagePrice': 123.0,
                'CurrencyCode': 'string',
                'DBInstanceCount': 123,
                'ProductDescription': 'string',
                'OfferingType': 'string',
                'MultiAZ': False,
                'State': 'string',
                'RecurringCharges': [
                    {
                        'RecurringChargeAmount': 123.0,
                        'RecurringChargeFrequency': 'string'
                    },
                ]
            },
        ],
        'NextToken': 'string'
    })
    test_find_usage_reserved_instances.append({
        'ReservedDBInstances': [
            {
                'ReservedDBInstanceId': 'string',
                'ReservedDBInstancesOfferingId': 'string',
                'DBInstanceClass': 'string',
                'StartTime': datetime(2015, 1, 1),
                'Duration': 123,
                'FixedPrice': 123.0,
                'UsagePrice': 123.0,
                'CurrencyCode': 'string',
                'DBInstanceCount': 123,
                'ProductDescription': 'string',
                'OfferingType': 'string',
                'MultiAZ': True,
                'State': 'string',
                'RecurringCharges': [
                    {
                        'RecurringChargeAmount': 123.0,
                        'RecurringChargeFrequency': 'string'
                    },
                ]
            },
        ],
    })

    test_update_limits_from_api = {
        'AccountQuotas': [
            {
                'Max': 200,
                'AccountQuotaName': 'DBInstances',
                'Used': 124
            },
            {
                'Max': 201,
                'AccountQuotaName': 'ReservedDBInstances',
                'Used': 96},
            {
                'Max': 100000,
                'AccountQuotaName': 'AllocatedStorage',
                'Used': 8320
            },
            {
                'Max': 25,
                'AccountQuotaName': 'DBSecurityGroups',
                'Used': 15
            },
            {
                'Max': 20,
                'AccountQuotaName': 'AuthorizationsPerDBSecurityGroup',
                'Used': 5
            },
            {
                'Max': 50,
                'AccountQuotaName': 'DBParameterGroups',
                'Used': 39
            },
            {
                'Max': 150,
                'AccountQuotaName': 'ManualSnapshots',
                'Used': 76
            },
            {
                'Max': 21,
                'AccountQuotaName': 'EventSubscriptions',
                'Used': 1
            },
            {
                'Max': 202,
                'AccountQuotaName': 'DBSubnetGroups',
                'Used': 89
            },
            {
                'Max': 22,
                'AccountQuotaName': 'OptionGroups',
                'Used': 2
            },
            {
                'Max': 23,
                'AccountQuotaName': 'SubnetsPerDBSubnetGroup',
                'Used': 14
            },
            {
                'Max': 5,
                'AccountQuotaName': 'ReadReplicasPerMaster',
                'Used': 4
            },
            {
                'Max': 40,
                'AccountQuotaName': 'DBClusters',
                'Used': 3
            },
            {
                'Max': 51,
                'AccountQuotaName': 'DBClusterParameterGroups',
                'Used': 6
            },
            {
                'Max': 98,
                'AccountQuotaName': 'Foo',
                'Used': 99
            }
        ],
        'ResponseMetadata': {
            'HTTPStatusCode': 200,
            'RequestId': '95729212-e5ab-11e5-8250-91a417accabb'
        }
    }

    test_find_usage_clusters = {
        'DBClusters': [
            {
                'AllocatedStorage': 1,
                'AvailabilityZones': ['us-east-1c', 'us-east-1d', 'us-east-1e'],
                'BackupRetentionPeriod': 1,
                'DBClusterIdentifier': 'foo',
                'DBClusterMembers': [
                    {
                        'DBClusterParameterGroupStatus': 'in-sync',
                        'DBInstanceIdentifier': 'foo',
                        'IsClusterWriter': True
                    },
                    {
                        'DBClusterParameterGroupStatus': 'in-sync',
                        'DBInstanceIdentifier': 'foo-replica',
                        'IsClusterWriter': False
                    }
                ],
                'DBClusterParameterGroup': 'default.aurora5.6',
                'DBSubnetGroup': 'foo-subnet-group',
                'DatabaseName': 'foo',
                'EarliestRestorableTime': datetime(
                    2016, 3, 9, 3, 21, 32, 789000, tzinfo=tzutc()
                ),
                'Endpoint': 'foo.us-east-1.rds.amazonaws.com',
                'Engine': 'aurora',
                'EngineVersion': '5.6.10a',
                'LatestRestorableTime': datetime(
                    2016, 3, 10, 23, 50, 52, 156000, tzinfo=tzutc()
                ),
                'MasterUsername': 'foomaster',
                'Port': 3306,
                'PreferredBackupWindow': '03:20-03:50',
                'PreferredMaintenanceWindow': 'sun:06:45-sun:07:15',
                'Status': 'available',
                'StorageEncrypted': False,
                'VpcSecurityGroups': [
                    {
                        'Status': 'active',
                        'VpcSecurityGroupId': 'sg-705e9e15'
                    }
                ]
            },
            {
                'AllocatedStorage': 1,
                'AvailabilityZones': ['us-east-1b', 'us-east-1c', 'us-east-1e'],
                'BackupRetentionPeriod': 1,
                'DBClusterIdentifier': 'bar-db',
                'DBClusterMembers': [
                    {
                        'DBClusterParameterGroupStatus': 'in-sync',
                        'DBInstanceIdentifier': 'bar-db02',
                        'IsClusterWriter': True
                    },
                    {
                        'DBClusterParameterGroupStatus': 'in-sync',
                        'DBInstanceIdentifier': 'bar-db01',
                        'IsClusterWriter': False
                    }
                ],
                'DBClusterParameterGroup': 'default.aurora5.6',
                'DBSubnetGroup': 'bar-db',
                'EarliestRestorableTime': datetime(
                    2016, 3, 9, 3, 1, 24, 936000, tzinfo=tzutc()
                ),
                'Endpoint': 'bar.us-east-1.rds.amazonaws.com',
                'Engine': 'aurora',
                'EngineVersion': '5.6.10a',
                'LatestRestorableTime': datetime(
                    2016, 3, 10, 23, 50, 31, 500000, tzinfo=tzutc()
                ),
                'MasterUsername': 'bar',
                'Port': 3306,
                'PreferredBackupWindow': '03:00-04:00',
                'PreferredMaintenanceWindow': 'fri:04:00-fri:05:00',
                'Status': 'available',
                'StorageEncrypted': False,
                'VpcSecurityGroups': [
                    {
                        'Status': 'active',
                        'VpcSecurityGroupId': 'sg-fb351a82'
                    }
                ]
            }
        ],
        'ResponseMetadata': {
            'HTTPStatusCode': 200,
            'RequestId': 'xxxxxxxxxxxxx'
        }
    }

    test_find_usage_cluster_param_groups = {
        'DBClusterParameterGroups': [
            {
                'DBClusterParameterGroupName': 'default.aurora5.6',
                'DBParameterGroupFamily': 'aurora5.6',
                'Description': 'Default cluster parameter group for aurora5.6'
            },
            {
                'DBClusterParameterGroupName': 'mygroup',
                'DBParameterGroupFamily': 'aurora5',
                'Description': 'my other group'
            },
            {
                'DBClusterParameterGroupName': 'default.aurora5',
                'DBParameterGroupFamily': 'aurora5',
                'Description': 'Default cluster parameter group for aurora5'
            }
        ],
        'ResponseMetadata': {
            'HTTPStatusCode': 200,
            'RequestId': '8ac3376d-e71f-11e5-b90b-6d8b9a79b973'
        }
    }


class ELB(object):

    test_find_usage = {
            # this is a subset of response items
            'LoadBalancerDescriptions': [
                {
                    'LoadBalancerName': 'elb-1',
                    'ListenerDescriptions': [
                        {'foo': 'bar'},
                    ],
                },
                {
                    'LoadBalancerName': 'elb-2',
                    'ListenerDescriptions': [
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                    ],
                },
                {
                    'LoadBalancerName': 'elb-3',
                    'ListenerDescriptions': [
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                    ],
                },
                {
                    'LoadBalancerName': 'elb-4',
                    'ListenerDescriptions': [
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                        {'foo': 'bar'},
                    ],
                },
            ],
        }


class ElastiCache(object):
    test_find_usage_nodes = []
    # first page of results
    test_find_usage_nodes.append({
        'CacheClusters': [
            {
                'Engine': 'memcached',
                'CacheParameterGroup': {
                    'CacheNodeIdsToReboot': [],
                    'CacheParameterGroupName': 'default.memcached1.4',
                    'ParameterApplyStatus': 'in-sync'
                },
                'CacheClusterId': 'memcached1',
                'CacheSecurityGroups': [],
                'ConfigurationEndpoint': {
                    'Port': 11211,
                    'Address': 'memcached1.vfavzi.cfg.use1.'
                               'cache.amazonaws.com'
                },
                'CacheClusterCreateTime': 1431109646.755,
                'ReplicationGroupId': None,
                'AutoMinorVersionUpgrade': True,
                'CacheClusterStatus': 'available',
                'NumCacheNodes': 1,
                'PreferredAvailabilityZone': 'us-east-1d',
                'SecurityGroups': [
                    {
                        'Status': 'active',
                        'SecurityGroupId': 'sg-11111111'
                    }
                ],
                'CacheSubnetGroupName': 'csg-memcached1',
                'EngineVersion': '1.4.14',
                'PendingModifiedValues': {
                    'NumCacheNodes': None,
                    'EngineVersion': None,
                    'CacheNodeIdsToRemove': None
                },
                'CacheNodeType': 'cache.t2.small',
                'NotificationConfiguration': None,
                'PreferredMaintenanceWindow': 'mon:05:30-mon:06:30',
                'CacheNodes': [
                    {
                        'CacheNodeId': '0001',
                        'Endpoint': {
                            'Port': 11211,
                            'Address': 'memcached1.vfavzi.0001.'
                                       'use1.cache.amazonaws.com'
                        },
                        'CacheNodeStatus': 'available',
                        'ParameterGroupStatus': 'in-sync',
                        'CacheNodeCreateTime': 1431109646.755,
                        'SourceCacheNodeId': None
                    }
                ]
            },
            {
                'Engine': 'redis',
                'CacheParameterGroup': {
                    'CacheNodeIdsToReboot': [],
                    'CacheParameterGroupName': 'default.redis2.8',
                    'ParameterApplyStatus': 'in-sync'
                },
                'CacheClusterId': 'redis1',
                'CacheSecurityGroups': [
                    {
                        'Status': 'active',
                        'CacheSecurityGroupName': 'csg-redis1'
                    }
                ],
                'ConfigurationEndpoint': None,
                'CacheClusterCreateTime': 1412253787.914,
                'ReplicationGroupId': None,
                'AutoMinorVersionUpgrade': True,
                'CacheClusterStatus': 'available',
                'NumCacheNodes': 2,
                'PreferredAvailabilityZone': 'us-east-1a',
                'SecurityGroups': None,
                'CacheSubnetGroupName': None,
                'EngineVersion': '2.8.6',
                'PendingModifiedValues': {
                    'NumCacheNodes': None,
                    'EngineVersion': None,
                    'CacheNodeIdsToRemove': None
                },
                'CacheNodeType': 'cache.m3.medium',
                'NotificationConfiguration': None,
                'PreferredMaintenanceWindow': 'mon:05:30-mon:06:30',
                'CacheNodes': [
                    {
                        'CacheNodeId': '0001',
                        'Endpoint': {
                            'Port': 6379,
                            'Address': 'redis1.vfavzi.0001.use1.cache.'
                                       'amazonaws.com'
                        },
                        'CacheNodeStatus': 'available',
                        'ParameterGroupStatus': 'in-sync',
                        'CacheNodeCreateTime': 1412253787.914,
                        'SourceCacheNodeId': None
                    },
                    {
                        'CacheNodeId': '0002',
                        'Endpoint': {
                            'Port': 6379,
                            'Address': 'redis1.vfavzi.0002.use1.cache.'
                                       'amazonaws.com'
                        },
                        'CacheNodeStatus': 'available',
                        'ParameterGroupStatus': 'in-sync',
                        'CacheNodeCreateTime': 1412253787.914,
                        'SourceCacheNodeId': None
                    }
                ]
            }
        ],
        'NextToken': 'string',
    })
    # second page of results
    test_find_usage_nodes.append({
        'CacheClusters': [
            {
                'Engine': 'redis',
                'CacheParameterGroup': {
                    'CacheNodeIdsToReboot': [],
                    'CacheParameterGroupName': 'default.redis2.8',
                    'ParameterApplyStatus': 'in-sync'
                },
                'CacheClusterId': 'redis2',
                'CacheSecurityGroups': [
                    {
                        'Status': 'active',
                        'CacheSecurityGroupName': 'csg-redis2'
                    }
                ],
                'ConfigurationEndpoint': None,
                'CacheClusterCreateTime': 1412253787.123,
                'ReplicationGroupId': None,
                'AutoMinorVersionUpgrade': True,
                'CacheClusterStatus': 'available',
                'NumCacheNodes': 4,
                'PreferredAvailabilityZone': 'us-east-1a',
                'SecurityGroups': None,
                'CacheSubnetGroupName': None,
                'EngineVersion': '2.8.6',
                'PendingModifiedValues': {
                    'NumCacheNodes': None,
                    'EngineVersion': None,
                    'CacheNodeIdsToRemove': None
                },
                'CacheNodeType': 'cache.m3.medium',
                'NotificationConfiguration': None,
                'PreferredMaintenanceWindow': 'mon:05:30-mon:06:30',
                'CacheNodes': None,
            },
        ],
    })

    test_find_usage_subnet_groups = []
    # first page of results
    test_find_usage_subnet_groups.append({
        'CacheSubnetGroups': [
            {
                'Subnets': [
                    {
                        'SubnetIdentifier': 'subnet-62e8783b',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1d'}
                    },
                    {
                        'SubnetIdentifier': 'subnet-0b037e7c',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1a'
                        }
                    }
                ],
                'CacheSubnetGroupName': 'break-memca-135tjabqoyywd',
                'VpcId': 'vpc-73ec9716',
                'CacheSubnetGroupDescription': 'memcached'
            },
            {
                'Subnets': [
                    {
                        'SubnetIdentifier': 'subnet-38e87861',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1d'
                        }
                    },
                    {
                        'SubnetIdentifier': 'subnet-4f027f38',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1a'
                        }
                    }
                ],
                'CacheSubnetGroupName': 'break-memca-6yi6axon9ol9',
                'VpcId': 'vpc-1ee8937b',
                'CacheSubnetGroupDescription': 'memcached'
            },
        ],
        'NextToken': 'str'
    })
    # second page of results
    test_find_usage_subnet_groups.append({
        'CacheSubnetGroups': [
            {
                'Subnets': [
                    {
                        'SubnetIdentifier': 'subnet-49071f61',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1e'
                        }
                    },
                    {
                        'SubnetIdentifier': 'subnet-6fe23c18',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1a'
                        }
                    },
                    {
                        'SubnetIdentifier': 'subnet-a9b54df0',
                        'SubnetAvailabilityZone': {
                            'Name': 'us-east-1d'
                        }
                    }
                ],
                'CacheSubnetGroupName': 'lsp-d-redis-14d9407dl05er',
                'VpcId': 'vpc-c300b9a6',
                'CacheSubnetGroupDescription': 'redis'
            },
        ],
    })

    test_find_usage_parameter_groups = []
    # first page of results
    test_find_usage_parameter_groups.append({
        'CacheParameterGroups': [
            {
                'CacheParameterGroupName': 'default.memcached1.4',
                'CacheParameterGroupFamily': 'memcached1.4',
                'Description': 'Default for memcached1.4'
            },
            {
                'CacheParameterGroupName': 'default.redis2.6',
                'CacheParameterGroupFamily': 'redis2.6',
                'Description': 'Default for redis2.6'
            },
        ],
        'NextToken': 'foo'
    })
    # second page of results
    test_find_usage_parameter_groups.append({
        'CacheParameterGroups': [
            {
                'CacheParameterGroupName': 'default.redis2.8',
                'CacheParameterGroupFamily': 'redis2.8',
                'Description': 'Default for redis2.8'
            }
        ],
    })

    test_find_usage_security_groups = []
    # first page of results
    test_find_usage_security_groups.append({
        'CacheSecurityGroups': [
            {
                'OwnerId': '123456789012',
                'CacheSecurityGroupName': 'default',
                'Description': 'default',
                'EC2SecurityGroups': []
            },
        ],
        'NextToken': 'foo'
    })
    # second page of results
    test_find_usage_security_groups.append({
        'CacheSecurityGroups': [
            {
                'OwnerId': '123456789012',
                'CacheSecurityGroupName': 'csg1',
                'Description': 'foo bar',
                'EC2SecurityGroups': [
                    {
                        'EC2SecurityGroupName': 'ec2-sg1',
                        'Status': 'authorized',
                        'EC2SecurityGroupOwnerId': '123456789012'
                    }
                ]
            }
        ]
    })


class EC2(object):

    @property
    def test_instance_usage(self):
        mock_inst1A = Mock(spec_set=Instance)
        type(mock_inst1A).id = '1A'
        type(mock_inst1A).instance_type = 't2.micro'
        type(mock_inst1A).spot_instance_request_id = None
        type(mock_inst1A).placement = {'AvailabilityZone': 'az1a'}
        type(mock_inst1A).state = {'Code': 16, 'Name': 'running'}

        mock_inst1B = Mock(spec_set=Instance)
        type(mock_inst1B).id = '1B'
        type(mock_inst1B).instance_type = 'r3.2xlarge'
        type(mock_inst1B).spot_instance_request_id = None
        type(mock_inst1B).placement = {'AvailabilityZone': 'az1a'}
        type(mock_inst1B).state = {'Code': 0, 'Name': 'pending'}

        mock_inst2A = Mock(spec_set=Instance)
        type(mock_inst2A).id = '2A'
        type(mock_inst2A).instance_type = 'c4.4xlarge'
        type(mock_inst2A).spot_instance_request_id = None
        type(mock_inst2A).placement = {'AvailabilityZone': 'az1a'}
        type(mock_inst2A).state = {'Code': 32, 'Name': 'shutting-down'}

        mock_inst2B = Mock(spec_set=Instance)
        type(mock_inst2B).id = '2B'
        type(mock_inst2B).instance_type = 't2.micro'
        type(mock_inst2B).spot_instance_request_id = '1234'
        type(mock_inst2B).placement = {'AvailabilityZone': 'az1a'}
        type(mock_inst2B).state = {'Code': 64, 'Name': 'stopping'}

        mock_inst2C = Mock(spec_set=Instance)
        type(mock_inst2C).id = '2C'
        type(mock_inst2C).instance_type = 'm4.8xlarge'
        type(mock_inst2C).spot_instance_request_id = None
        type(mock_inst2C).placement = {'AvailabilityZone': 'az1a'}
        type(mock_inst2C).state = {'Code': 16, 'Name': 'running'}

        mock_instStopped = Mock(spec_set=Instance)
        type(mock_instStopped).id = '2C'
        type(mock_instStopped).instance_type = 'm4.8xlarge'
        type(mock_instStopped).spot_instance_request_id = None
        type(mock_instStopped).placement = {'AvailabilityZone': 'az1a'}
        type(mock_instStopped).state = {'Code': 80, 'Name': 'stopped'}

        mock_instTerm = Mock(spec_set=Instance)
        type(mock_instTerm).id = '2C'
        type(mock_instTerm).instance_type = 'm4.8xlarge'
        type(mock_instTerm).spot_instance_request_id = None
        type(mock_instTerm).placement = {'AvailabilityZone': 'az1a'}
        type(mock_instTerm).state = {'Code': 48, 'Name': 'terminated'}

        return_value = [
            mock_inst1A,
            mock_inst1B,
            mock_inst2A,
            mock_inst2B,
            mock_inst2C,
            mock_instStopped,
            mock_instTerm
        ]
        return return_value

    @property
    def test_instance_usage_key_error(self):
        mock_inst1A = Mock(spec_set=Instance)
        type(mock_inst1A).id = '1A'
        type(mock_inst1A).instance_type = 'foobar'
        type(mock_inst1A).spot_instance_request_id = None
        type(mock_inst1A).placement = {'AvailabilityZone': 'az1a'}
        type(mock_inst1A).state = {'Code': 16, 'Name': 'running'}
        return [mock_inst1A]

    @property
    def test_find_usage_networking_sgs(self):
        mock_sg1 = Mock(spec_set=SecurityGroup)
        type(mock_sg1).id = 'sg-1'
        type(mock_sg1).vpc_id = 'vpc-aaa'
        type(mock_sg1).ip_permissions = []
        type(mock_sg1).ip_permissions_egress = []
        mock_sg2 = Mock(spec_set=SecurityGroup)
        type(mock_sg2).id = 'sg-2'
        type(mock_sg2).vpc_id = None
        type(mock_sg2).ip_permissions = [1, 2, 3, 4, 5, 6]
        type(mock_sg2).ip_permissions_egress = [8, 9, 10]
        mock_sg3 = Mock(spec_set=SecurityGroup)
        type(mock_sg3).id = 'sg-3'
        type(mock_sg3).vpc_id = 'vpc-bbb'
        type(mock_sg3).ip_permissions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        type(mock_sg3).ip_permissions_egress = [6, 7, 8, 9]
        mock_sg4 = Mock(spec_set=SecurityGroup)
        type(mock_sg4).id = 'sg-4'
        type(mock_sg4).vpc_id = 'vpc-aaa'
        type(mock_sg4).ip_permissions = [1, 2, 3]
        type(mock_sg4).ip_permissions_egress = [21, 22, 23, 24]

        return_value = [
            mock_sg1,
            mock_sg2,
            mock_sg3,
            mock_sg4,
        ]
        return return_value

    test_get_reserved_instance_count = {
        'ReservedInstances': [
            {
                'ReservedInstancesId': 'res1',
                'InstanceType': 'it1',
                'AvailabilityZone': 'az1',
                'Start': datetime(2015, 1, 1),
                'End': datetime(2015, 1, 1),
                'Duration': 123,
                'UsagePrice': 12,
                'FixedPrice': 14,
                'InstanceCount': 1,
                'ProductDescription': 'Linux/UNIX',
                'State': 'active',
                'Tags': [
                    {
                        'Key': 'tagKey',
                        'Value': 'tagVal'
                    },
                ],
                'InstanceTenancy': 'default',
                'CurrencyCode': 'USD',
                'OfferingType': 'Heavy Utilization',
                'RecurringCharges': [
                    {
                        'Frequency': 'Hourly',
                        'Amount': 123.0
                    },
                ]
            },
            {
                'ReservedInstancesId': 'res2',
                'InstanceType': 'it2',
                'AvailabilityZone': 'az1',
                'InstanceCount': 1,
                'State': 'retired',
            },
            {
                'ReservedInstancesId': 'res3',
                'InstanceType': 'it1',
                'AvailabilityZone': 'az1',
                'InstanceCount': 9,
                'State': 'active',
            },
            {
                'ReservedInstancesId': 'res4',
                'InstanceType': 'it2',
                'AvailabilityZone': 'az2',
                'InstanceCount': 98,
                'State': 'active',
            },
        ]
    }

    @property
    def test_find_usage_networking_eips(self):
        mock_addr1 = Mock(spec_set=VpcAddress)
        type(mock_addr1).domain = 'vpc'
        mock_addr2 = Mock(spec_set=VpcAddress)
        type(mock_addr2).domain = 'vpc'
        mock_addr3 = Mock(spec_set=ClassicAddress)
        type(mock_addr3).domain = 'standard'
        return {
            'Classic': [mock_addr3],
            'Vpc': [mock_addr1, mock_addr2]
        }

    @property
    def test_find_usage_networking_eni_sg(self):
        mock_if1 = Mock(spec_set=NetworkInterface)
        type(mock_if1).id = 'if-1'
        type(mock_if1).groups = []
        type(mock_if1).vpc = Mock()

        mock_if2 = Mock(spec_set=NetworkInterface)
        type(mock_if2).id = 'if-2'
        type(mock_if2).groups = [1, 2, 3]
        type(mock_if2).vpc = Mock()

        mock_if3 = Mock(spec_set=NetworkInterface)
        type(mock_if3).id = 'if-3'
        type(mock_if3).groups = [1, 2, 3, 4, 5, 6, 7, 8]
        type(mock_if3).vpc = Mock()

        mock_if4 = Mock(spec_set=NetworkInterface)
        type(mock_if4).id = 'if-4'
        type(mock_if4).groups = [1, 2, 3, 4, 5, 6, 7, 8]
        type(mock_if4).vpc = None
        return [mock_if1, mock_if2, mock_if3, mock_if4]

    test_update_limits_from_api = {
        'ResponseMetadata': {
            'HTTPStatusCode': 200,
            'RequestId': '16b85906-ab0d-4134-b8bb-df3e6120c6c7'
        },
        'AccountAttributes': [
            {
                'AttributeName': 'supported-platforms',
                'AttributeValues': [
                    {
                        'AttributeValue': 'EC2'
                    },
                    {
                        'AttributeValue': 'VPC'
                    }
                ]
            },
            {
                'AttributeName': 'vpc-max-security-groups-per-interface',
                'AttributeValues': [
                    {
                        'AttributeValue': '5'
                    }
                ]
            },
            {
                'AttributeName': 'max-elastic-ips',
                'AttributeValues': [
                    {
                        'AttributeValue': '40'
                    }
                ]
            },
            {
                'AttributeName': 'max-instances',
                'AttributeValues': [
                    {
                        'AttributeValue': '400'
                    }
                ]
            },
            {
                'AttributeName': 'vpc-max-elastic-ips',
                'AttributeValues': [
                    {
                        'AttributeValue': '200'
                    }
                ]
            },
            {
                'AttributeName': 'default-vpc',
                'AttributeValues': [
                    {
                        'AttributeValue': 'none'
                    }
                ]
            }
        ]
    }
