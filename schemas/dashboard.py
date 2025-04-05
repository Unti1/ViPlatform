

from pydantic import BaseModel


class DashboardSchema(BaseModel):
    title: str
    user_id: int
    group_id: int