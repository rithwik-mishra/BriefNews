"""FastAPI main entry point"""

from fastapi import FastAPI, HTTPException, Query, status, Depends
from typing import Annotated, Literal, TypeAlias, List, Optional
from enum import Enum
from .services import SummaryAPIService
from contextlib import asynccontextmanager
from .models import ArticleURLInput, ArticleOutput, TopicEnum

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
        summary="Sends news article URL as payload to the summarize function and returns a summary and sentiment analysis of the chosen article.",
        tags=["Routes"]
        )
async def summarize_article(api_service: APIServiceDI):
    pass

@app.get("/articles", summary="Gets all articles from the database.", tags=["Routes"])
def get_all_articles(api_service: APIServiceDI, 
                    topic: Annotated[
                        Optional[TopicEnum],
                        Query(
                            description="Optional topic arguement for news article keyword/subject selection",
                            enum=[e.value for e in TopicEnum]
                        )
                    ] = None):
    return api_service.get_all_articles(topic)



