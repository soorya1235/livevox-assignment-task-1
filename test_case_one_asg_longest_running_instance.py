from datetime import timedelta
import pytest
from asg_utility_functions import get_auto_scaling_group_instance_details, get_instance_launch_time, calculate_uptime

AUTO_SCALING_GROUP_NAME = 'lv-test-cpu'


@pytest.fixture(scope="module")
def get_asg_instances():
    return get_auto_scaling_group_instance_details(AUTO_SCALING_GROUP_NAME)


def test_longest_running_instance(get_asg_instances):
    if get_asg_instances:
        longest_running_instance_id = None
        longest_running_duration = None
        all_instance_up_time = []
        instance_uptime = []
        for instance in get_asg_instances:
            instance_id = instance['InstanceId']
            launch_time = get_instance_launch_time(instance_id)
            if launch_time:
                uptime = calculate_uptime(launch_time)
                all_instance_up_time.append(uptime)
                if longest_running_duration is None or uptime > longest_running_duration:
                    longest_running_duration = uptime
                    longest_running_instance_id = instance_id
                    instance_uptime.append({'instance_name': instance['InstanceId'], 'uptime': longest_running_duration})
        print(f"Instance Uptime Details is", instance_uptime)
        print(f"Longest running instance ID: {longest_running_instance_id}, Uptime: {longest_running_duration}")
