"""
This test case will print will the total no of instances launched and terminated today.
"""

import pytest
from asg_utility_functions import get_instances_launched_and_terminated


@pytest.fixture
def asg_name():
    return 'lv-test-cpu'


def test_instances_launched_and_terminated(asg_name):
    """
    This test will check the total number of instances launched and terminated today.
    @input:
        asg_name (string): Name of the Auto Scaling group.
    """
    launch_count, terminate_count = get_instances_launched_and_terminated(asg_name)
    print(f"Total number of instances launched today: {launch_count}")
    print(f"Total number of instances terminated today: {terminate_count}")
