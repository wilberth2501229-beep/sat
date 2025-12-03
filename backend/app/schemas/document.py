"""
Pydantic Schemas - Documents
"""
from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# Document Upload
class DocumentUpload(BaseModel):
    document_type: str
    title: str
    description: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    tags: Optional[List[str]] = []
    metadata: Optional[Dict] = {}


# Document Response
class DocumentResponse(BaseModel):
    id: int
    user_id: int
    document_type: str
    title: str
    description: Optional[str]
    file_name: str
    file_size: int
    mime_type: str
    is_encrypted: bool
    status: str
    issue_date: Optional[datetime]
    expiry_date: Optional[datetime]
    metadata: Dict
    tags: List[str]
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# Document Update
class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict] = None


# Document List Filters
class DocumentFilters(BaseModel):
    document_type: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
