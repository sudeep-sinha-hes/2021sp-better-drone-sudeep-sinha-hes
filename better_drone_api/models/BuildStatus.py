from enum import Enum


class BuildStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
