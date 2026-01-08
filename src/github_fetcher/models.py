from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class GitUser(BaseModel):
    login: str
    id: int
    node_id: Optional[str] = None
    avatar_url: Optional[str] = None
    gravatar_id: Optional[str] = None
    url: Optional[str] = None
    html_url: Optional[str] = None
    type: Optional[str] = None


class Repository(BaseModel):
    url: Optional[str] = None
    svn_url: Optional[str] = None


class PRRef(BaseModel):
    sha: str
    ref: str
    label: Optional[str] = None
    repo: Optional[Repository] = None


class PRDetails(BaseModel):
    title: str
    body: Optional[str] = None
    user: GitUser
    created_at: datetime
    updated_at: datetime
    merged: bool
    mergeable: Optional[bool] = None
    commits: int
    additions: int
    deletions: int
    changed_files: int
    head: PRRef
    base: PRRef


class PRFile(BaseModel):
    sha: str
    filename: str
    status: Literal[
        "added", "modified", "removed", "renamed", "copied", "changed", "unchanged"
    ]
    additions: int
    deletions: int
    changes: int
    blob_url: Optional[str] = None
    raw_url: Optional[str] = None
    contents_url: Optional[str] = None
    patch: Optional[str] = None
    previous_filename: Optional[str] = None
    original_file_raw_url: Optional[str] = None
