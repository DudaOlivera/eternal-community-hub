from datetime import datetime
from pydantic import BaseModel


class MaintenanceCreate(BaseModel):
    reason: str
    estimated_duration: str
    author: str


class MaintenanceFinish(BaseModel):
    maintenance_id: int


class MaintenanceResponse(BaseModel):
    id: int
    reason: str
    estimated_duration: str
    author: str
    is_active: bool
    started_at: datetime | None
    finished_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
