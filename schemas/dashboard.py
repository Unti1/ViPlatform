

from pydantic import BaseModel


class DashboardSchema(BaseModel):
    title: str
    group_id: int