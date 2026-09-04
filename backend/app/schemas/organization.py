from pydantic import BaseModel
import uuid


class OrganizationCreate(BaseModel):
    name: str
    description: str | None = None


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str | None

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    repository_url: str | None = None
    organization_id: uuid.UUID


class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: str | None
    repository_url: str | None
    organization_id: uuid.UUID

    class Config:
        from_attributes = True
