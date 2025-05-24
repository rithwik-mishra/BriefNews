"""FastAPI main entry point"""

from fastapi import FastAPI, HTTPException, status
from typing import Annotated, Literal, TypeAlias

app = FastAPI(
    title="BriefNews Backend API",
    contact={
        "name": "Rithwik Mishra",
        "url": "https://github.com/rithwik-mishra",
        "email": "mishra.rithwik@gmail.com",
    },
    description="Backend API for BriefNews, a news summarization service with a focus on providing concise and actionable insights along with sentiment analyses.",
)

# Routes:
@app.post(
        "/summarize",
        status_code=status.HTTP_202_ACCEPTED,
        summary="Sends news article URL as payload to the summarize function and returns a summary and sentiment analysis of the chosen article.",
        )
async def summarize_article():
    pass

@app.get("/random", summary="Gets the title, summary, sentiment, and URL of a random current news article." )
async def get_random_article():
    pass



