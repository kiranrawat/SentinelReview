from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.PRReviewer import PRReviewer
from api.models import PRUrl

app = FastAPI(
    title="Sentinel Review API", 
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/review-pr", tags=["Review PR"])
async def review_pr(body: PRUrl):
    pr_reviewer = PRReviewer()
    pr_review_response = await pr_reviewer.generate_pr_review(pr_url = body.pr_url)
    return {'pr_url': body.pr_url, 'review': pr_review_response}
