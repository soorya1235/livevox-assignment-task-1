import os
from datetime import datetime, timezone

import boto3
import pytest

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_DEFAULT_REGION']


def get_instance_launch_time(instance_id):
    """
    This function will return the launch time of the instance
    @input:
        instance_id (string): Instance ID.
    @output:
        launch_time (datetime): Launch time of the instance.
    """
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        if not response['Reservations']:
            pytest.fail(f"Instance '{instance_id}' not found.")
        reservation = response['Reservations'][0]
        instance = reservation['Instances'][0]
        launch_time = instance['LaunchTime']
    except Exception as e:
        print(f"Error: {e}")
    return launch_time


def calculate_uptime(launch_time):
    """
    This function will return the uptime of the instance
    @input:
        launch_time (datetime): Launch time of the instance.
    @output:
        uptime (datetime): Uptime of the instance.
    """
    current_time = datetime.now(timezone.utc)
    uptime = current_time - launch_time
    return uptime


def get_instance_security_image_vpc_details(instance_id):
    """
    This function will return security groups, image id and vpc id of the instance
    @input (string):
        instance_id (string): Instance ID.
    @output (dict): security groups, image id and vpc id of the instance
    """
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        if not response['Reservations']:
            pytest.fail(f"Instance '{instance_id}' not found.")
        reservation = response['Reservations'][0]
        instance = reservation['Instances'][0]
    except Exception as e:
        pytest.fail(f"Error: {e}")
    return {
        'security_groups': [group['GroupId'] for group in instance['SecurityGroups']],
        'image_id': instance['ImageId'],
        'vpc_id': instance['VpcId']
    }


def get_auto_scaling_group_instance_desired_capacity_details(asg_name):
    """
    This Function will Get the desired capacity and number of running instances for an Auto Scaling group.
    @input:
        asg_name (string): Name of the Auto Scaling group.
    @output:
        desired_capacity (int): Desired capacity of the Auto Scaling group.
        running_instances (int): Number of running instances in the Auto Scaling group.
    """
    autoscaling_client = boto3.client('autoscaling', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                                      region_name=aws_region)
    try:
        response = autoscaling_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
        if not response['AutoScalingGroups']:
            pytest.fail(f"Auto Scaling group '{asg_name}' not found.")
        auto_scaling_group = response['AutoScalingGroups'][0]
        desired_capacity = auto_scaling_group['DesiredCapacity']
        running_instances = len(auto_scaling_group['Instances'])
    except Exception as e:
        pytest.fail(f"Exception Occurred : {e}")
    return desired_capacity, running_instances


def get_next_scheduled_action(asg_name):
    """
    This function will return the next scheduled action for the Auto Scaling group.
    @input:
        asg_name (string): Name of the Auto Scaling group.
    @output:
        next_scheduled_action (dict): Next scheduled action for the Auto Scaling group.
    """
    autoscaling_client = boto3.client('autoscaling', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                                      region_name=aws_region)
    try:
        response = autoscaling_client.describe_scheduled_actions(AutoScalingGroupName=asg_name)
        scheduled_actions = response.get('ScheduledUpdateGroupActions', [])
        if not scheduled_actions:
            return None
        sorted_actions = sorted(scheduled_actions, key=lambda x: x['StartTime'])
        next_scheduled_action = sorted_actions[0]
    except Exception as e:
        print(f"Error: {e}")
    return next_scheduled_action


def get_auto_scaling_group_instance_details(asg_name):
    """
    This Function will get the instance details in the auto scaling group.
    @input:
        asg_name (string): Name of the Auto Scaling group.
    @output:
        instances (dict): Instance details in the auto scaling group.
    """
    autoscaling_client = boto3.client('autoscaling', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                                      region_name=aws_region)
    try:
        response = autoscaling_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
        if not response['AutoScalingGroups']:
            pytest.fail(f"Auto Scaling group '{asg_name}' not found.")
        auto_scaling_group = response['AutoScalingGroups'][0]
        instances = auto_scaling_group.get('Instances', [])
    except Exception as e:
        pytest.fail(f"Error: {e}")
    return instances


def get_instance_availability_zone(instance_id):
    """
    This Function will get the instance availability zone details.
    @input:
        instance_id (string): Instance ID.
    @output:
        instance_id (string): Instance ID.
        state (string): Instance state.
        availability_zone (string): Availability Zone.
    """
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        if not response['Reservations']:
            pytest.fail(f"Instance '{instance_id}' not found.")
        reservation = response['Reservations'][0]
        instance = reservation['Instances'][0]
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        availability_zone = instance['Placement']['AvailabilityZone']
    except Exception as e:
        pytest.fail(f"Error: {e}")
    return instance_id, state, availability_zone


def get_instances_launched_and_terminated(asg_name):
    """
    This function will return the total number of instances launched and terminated today.
    @input:
        asg_name (string): Name of the Auto Scaling group.
    """
    autoscaling_client = boto3.client('autoscaling')
    ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)
    try:
        response = autoscaling_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
        if not response['AutoScalingGroups']:
            pytest.fail(f"Auto Scaling group '{asg_name}' not found.")
        auto_scaling_group = response['AutoScalingGroups'][0]
        instances = auto_scaling_group.get('Instances', [])
        launch_count = 0
        terminate_count = 0
        if not instances:
            return launch_count, terminate_count
        current_date = datetime.utcnow().date()
        for instance in instances:
            instance_id = instance['InstanceId']
            launch_time = get_instance_launch_time(instance_id)
            if launch_time and launch_time.date() == current_date:
                launch_count += 1
            response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
            status = response['InstanceStatuses'][0]
            if 'Events' in status:
                for event in status['Events']:
                    event_date = event['NotBefore'].date()
                    if event_date == current_date and event['EventType'] == 'terminate':
                        terminate_count += 1
    except Exception as e:
        print(f"Error: {e}")
    return launch_count, terminate_count
