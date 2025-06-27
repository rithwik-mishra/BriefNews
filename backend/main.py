"""FastAPI main entry point"""

from fastapi import FastAPI, HTTPException, Query, status, Depends, Body
from typing import Annotated, TypeAlias, Optional
from .services import SummaryAPIService, ArticleUncrawlableError
from .models import ArticleURLInput, TopicEnum, ArticleTextInput

# Create a single instance of the service
api_service = SummaryAPIService()

app = FastAPI(
    title="BriefNews Backend API by Rithwik Mishra",
    contact={
        "name": "Rithwik Mishra",
        "url": "https://github.com/rithwik-mishra",
    },
    openapi_tags=[
        {"name": "Routes", "description": "All of the routes used in the BriefNews API"}
    ],
    description="""
## Introduction

This is the backend API for BriefNews, a news summarization service with a focus on providing concise and actionable insights along with sentiment analyses.
    """,
)

def get_api_service():
    """Dependency injection function that returns the singleton instance"""
    return api_service

APIServiceDI: TypeAlias = Annotated[SummaryAPIService, Depends(get_api_service)]

# Routes:
@app.post(
    "/summarize",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Sends news article URL as payload to the summarize function and returns a summary of the chosen article.",
    responses = {
        400: {
            "description": "Article is unable to be crawled."
        }
    },
    tags=["Routes"]
)
def summarize_article(
    api_service: APIServiceDI, 
    article_url: Annotated[
        ArticleURLInput,
        Body(
            description="The article url that contains the direct link to the article's text for summarization."
        )
    ]
):
    try:
        return api_service.summarize_article(article_url)
    except ArticleUncrawlableError:
        raise HTTPException(400, detail="Article is unable to be crawled.")


@app.get("/articles", summary="Gets all articles along with their information and text summary based on selected topic", tags=["Routes"])
def get_all_articles(
    api_service: APIServiceDI, 
    topic: Annotated[
        Optional[TopicEnum],
        Query(
            description="Optional topic arguement for news article keyword/subject selection",
            enum=[e.value for e in TopicEnum]
        )
    ] = None
):
    return api_service.get_all_articles(topic)



