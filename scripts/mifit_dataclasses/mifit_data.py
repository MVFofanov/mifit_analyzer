from dataclasses import dataclass

from activity.activity import ActivityData
from activity_stage.activity_stage import ActivityStageData
from sleep.sleep import SleepData
from sleep_activity.sleep_activity import SleepActivityData


@dataclass(slots=True, frozen=True)
class MiFitData:
    sleep: SleepData
    activity: ActivityData
    sleep_activity: SleepActivityData
    activity_stage: ActivityStageData
