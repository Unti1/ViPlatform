

from pydantic import BaseModel


class DashboardSchema(BaseModel):
    user_id: int
    group_id: int
    title: str