"""FastAPI main entry point"""

from fastapi import FastAPI, HTTPException, Query, status, Depends, Body
from typing import Annotated, TypeAlias, Optional
from .services import SummaryAPIService, ArticleUncrawlableError
from .models import ArticleURLInput, TopicEnum, ArticleTextInput, ArticleOutput

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

## Features

- **Article Summarization**: Submit article URLs to get AI-generated summaries
- **Topic-based News**: Get articles filtered by specific topics (business, technology, science, health, politics)
- **Sentiment Analysis**: Receive sentiment insights along with summaries
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
    response_model=str,
    responses = {
        202: {
            "description": "Article successfully summarized",
            "content": {
                "application/json": {
                    "example": "This is a concise summary of the news article that provides the key points and main insights..."
                }
            }
        },
        400: {
            "description": "Article is unable to be crawled.",
            "content": {
                "application/json": {
                    "example": {"detail": "Article is unable to be crawled."}
                }
            }
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
    """
    Summarize a news article from its URL.
    
    This endpoint takes a news article URL, crawls the content, and returns an AI-generated summary.
    The summary is concise and focuses on the key points of the article.
    """
    try:
        return api_service.summarize_article(article_url)
    except ArticleUncrawlableError:
        raise HTTPException(400, detail="Article is unable to be crawled.")


@app.get(
    "/articles", 
    summary="Gets all articles along with their information and text summary based on selected topic", 
    response_model=list[ArticleOutput],
    responses={
        200: {
            "description": "List of articles with summaries",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "title": "Example News Article",
                            "summary": "This is a summary of the example news article...",
                            "url": "https://example.com/news-article",
                            "date": "2024-01-15"
                        }
                    ]
                }
            }
        }
    },
    tags=["Routes"]
)
def get_all_articles(
    api_service: APIServiceDI, 
    topic: Annotated[
        Optional[TopicEnum],
        Query(
            description="Optional topic argument for news article keyword/subject selection",
            enum=[e.value for e in TopicEnum]
        )
    ] = None
):
    """
    Retrieve articles filtered by topic.
    
    This endpoint returns a list of news articles with their summaries. 
    You can optionally filter by topic to get articles in specific categories.
    """
    return api_service.get_all_articles(topic)



