"""
This test checks if the Auto Scaling group has more than 1 instance and if the instances are distributed across multiple Availability Zones.
"""

import pytest
from asg_utility_functions import get_auto_scaling_group_instance_details, get_instance_availability_zone


@pytest.mark.parametrize("asg_name", ["lv-test-cpu"])
def test_multiple_instances_and_availability_zones(asg_name):
    """
    This test checks if the Auto Scaling group has more than 1 instance and if the instances are distributed across multiple Availability Zones.
    @inputs:
        asg_name (string): Name of the Auto Scaling group.
    """
    instances = get_auto_scaling_group_instance_details(asg_name)
    assert len(instances) > 1, f"Auto Scaling group '{asg_name}' should have more than 1 instance."
    first_instance_availability_zone = instances[0]['AvailabilityZone']
    availability_zones = []
    for instance in instances:
        _, _, availability_zone = get_instance_availability_zone(instance['InstanceId'])
        availability_zones.append(availability_zone)
    other_instances_availability_zone = availability_zones[1:]
    assert first_instance_availability_zone not in other_instances_availability_zone, f"Auto Scaling group '{asg_name}' instances are not " \
                                                                                      f"distributed across multiple Availability Zones."
