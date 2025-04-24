from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Provider(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    id: UUID
    name: str
    npi: str
    profession: str
