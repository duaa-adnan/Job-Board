from typing import Literal

from pydantic import BaseModel, Field


class JobIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = ""
    status: Literal["open", "closed"] = "open"


class JobOut(JobIn):
    id: int
    model_config = {"from_attributes": True}
    