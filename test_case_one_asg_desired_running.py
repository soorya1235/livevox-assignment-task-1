"""
Test case to verify that the desired capacity of an Auto Scaling group matches the number of running instances.
"""

import pytest
from asg_utility_functions import get_auto_scaling_group_instance_desired_capacity_details


@pytest.mark.parametrize("asg_name", ["lv-test-cpu"])
def test_desired_capacity_matches_running_instances(asg_name):
    """
    This test checks if the desired capacity of an Auto Scaling group matches the number of running instances.
    @input:
        asg_name (string): Name of the Auto Scaling group.
    """
    desired_capacity, running_instances = get_auto_scaling_group_instance_desired_capacity_details(asg_name)
    assert desired_capacity == running_instances, f"Mismatch in Auto Scaling group '{asg_name}': Desired={desired_capacity}, Running={running_instances}"
