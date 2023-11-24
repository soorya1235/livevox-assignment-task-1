"""
This test checks if the security groups, image id and vpc id are same for all the instances in the auto scaling group
"""
import pytest
from asg_utility_functions import get_auto_scaling_group_instance_details, get_instance_security_image_vpc_details


@pytest.mark.parametrize("asg_name", ["lv-test-cpu"])
def test_security_group_image_id_vpc_id(asg_name):
    """
    This test checks if the security groups, image id and vpc id are same for all the instances in the auto scaling group
    @input:
        asg_name (string): Name of the Auto Scaling group.
    """
    instances = get_auto_scaling_group_instance_details(asg_name)
    assert len(instances) > 0, f"Auto Scaling group '{asg_name}' should have at least one running instance."
    first_instance_info = get_instance_security_image_vpc_details(instances[0]['InstanceId'])
    for instance in instances[1:]:
        instance_info = get_instance_security_image_vpc_details(instance['InstanceId'])
        assert instance_info['security_groups'] == first_instance_info['security_groups'], \
            f"Security Groups are different for instances in Auto Scaling group '{asg_name}'."
        assert instance_info['image_id'] == first_instance_info['image_id'], \
            f"Image ID is different for instances in Auto Scaling group '{asg_name}'."
        assert instance_info['vpc_id'] == first_instance_info['vpc_id'], \
            f"VPC ID is different for instances in Auto Scaling group '{asg_name}'."
