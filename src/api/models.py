from pydantic import BaseModel, Field

class PRUrl(BaseModel):
    pr_url: str = Field(pattern=r"^https://github\.com/(.*)/(.*)/pull/(.*)", examples=[
        'https://github.com/org/repo/pull/pull_number',
        'https://github.com/kiranrawat/SentinelReview/pull/1'
    ])