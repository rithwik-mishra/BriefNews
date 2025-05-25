"""FastAPI main entry point"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Literal, TypeAlias, List
from .services import SummaryAPIService

app = FastAPI(
    title="BriefNews Backend API by Rithwik Mishra",
    contact={
        "name": "Rithwik Mishra",
        "url": "https://github.com/rithwik-mishra",
        "email": "mishra.rithwik@gmail.com",
    },
    openapi_tags=[
        {"name": "Routes", "description": "All of the routes used in the BriefNews API"}
    ],
    description="""
## Introduction

This is the backend API for BriefNews, a news summarization service with a focus on providing concise and actionable insights along with sentiment analyses.
    """,
)

# Data Models:
class ArticleURLInput(BaseModel):
    """Article URL Input Model"""
    url: Annotated[
        str, 
        Field(description="The URL of the news article to summarize. Must be a valid URL.")
    ]

class ArticleOutput(BaseModel):
    """Article output model with summary and sentiment analysis"""
    title: Annotated[
        str, 
        Field(description="The title of the original news article")
    ]

    authors: Annotated[
        List[str],
        Field(description="The author(s) of the original news article")
    ]

    summary: Annotated[
        str, 
        Field(description="The summary of the news article")
    ]

    sentiment: Annotated[
        Literal["positive", "negative", "neutral"], 
        Field(description="The sentiment of the news article, measured as positive, negative, or neutral")
    ]

    url: Annotated[
        str, 
        Field(description="The URL of the original news article")
    ]

# Routes:
@app.post(
        "/summarize",
        status_code=status.HTTP_202_ACCEPTED,
        summary="Sends news article URL as payload to the summarize function and returns a summary and sentiment analysis of the chosen article.",
        tags=["Routes"]
        )
async def summarize_article():
    pass

@app.get("/random", summary="Gets the title, summary, sentiment, and URL of a random current news article.", tags=["Routes"])
async def get_random_article():
    pass



