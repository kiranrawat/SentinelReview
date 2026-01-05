from pydantic import BaseModel
from typing import Optional

class GitUser(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str

class Repository(BaseModel):
    url: str
    svn_url: str

class GitCommits(BaseModel):
    sha: str
    label: str
    ref: str
    repo: Repository

class PRDetails(BaseModel):
    title: str
    body: str
    user: GitUser
    created_at: str
    updated_at: str
    merged: bool
    mergeable: Optional[bool] = None
    commits: int
    additions: int
    deletions: int
    changed_files: int
    head: GitCommits
    base: GitCommits

class PRFile(BaseModel):
    sha: str
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str
    original_file_raw_url: Optional[str] = None
    contents_url: str
    patch: str