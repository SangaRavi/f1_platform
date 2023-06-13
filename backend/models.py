from typing import Any, Dict, List
from pydantic import BaseModel


class PlotMetaData(BaseModel):
    id: str

    class Config:
        orm_mode = True


class PlotResponseModel(BaseModel):
    metadata: str
    data: Any

    class Config:
        orm_mode = True
