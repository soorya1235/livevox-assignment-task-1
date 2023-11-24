"""
This test case will check if the next scheduled action for the Auto Scaling group.
"""

from datetime import datetime, timezone
from asg_utility_functions import get_next_scheduled_action
import pytest


@pytest.fixture
def asg_name():
    return 'lv-test-cpu'


def test_next_scheduled_action(asg_name):
    """
    This test checks if the next scheduled action for the Auto Scaling group .
    @input:
        asg_name (string): Name of the Auto Scaling group.
    """
    next_scheduled_action = get_next_scheduled_action(asg_name)
    if next_scheduled_action:
        start_time = next_scheduled_action['StartTime']
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        diff_time = current_time - start_time
        total_seconds = int(diff_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        print(f"Next Scheduled Action:")
        print(f"Start Time: {start_time}")
        print(f"Elapsed Time: {hours:02d}:{minutes:02d}:{total_seconds:02d}")
    else:
        print("No scheduled actions found for the Auto Scaling Group.")
