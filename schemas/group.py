from pydantic import BaseModel, ConfigDict


class GroupSchema(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)