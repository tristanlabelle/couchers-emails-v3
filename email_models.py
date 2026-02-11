from dataclasses import dataclass
from datetime import date

@dataclass
class UserInfo:
    name: str
    age: int
    city: str
    avatar_url: str

@dataclass
class HostRequestReceived:
    user_name: str
    surfer: UserInfo
    from_date: date
    to_date: date
    text: str
    view_url: str
    quick_decline_url: str