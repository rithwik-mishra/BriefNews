from pydantic import BaseModel, Field
from typing import Annotated, Literal, List
from datetime import datetime, date as date_type
from enum import Enum

class ArticleURLInput(BaseModel):
    """Article URL Input Model"""
    url: Annotated[
        str, 
        Field(description="The URL of the news article to summarize. Must be a valid URL.")
    ]

class ArticleTextInput(BaseModel):
    """Article URL Input Model"""
    text: Annotated[
        str, 
        Field(description="The full pasted text of the news article to summarize")
    ]

class ArticleOutput(BaseModel):
    """Article output model with summary and sentiment analysis"""
    title: Annotated[
        str, 
        Field(description="The title of the original news article")
    ]

    summary: Annotated[
        str, 
        Field(description="The summary of the news article")
    ]

    url: Annotated[
        str, 
        Field(description="The URL of the original news article")
    ]

    date: Annotated[
        date_type,
        Field(
            description="The date of the original news article in YYYY-MM-DD format",
            default_factory=datetime.today().date
        )
    ]
    
class TopicEnum(str, Enum):
    business = "business"
    technology = "technology"
    science = "science"
    health = "health"
    politics = "politics"