from pydantic import BaseModel, Field
from typing import Annotated, Literal, List
from datetime import datetime, date as date_type

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

    date: Annotated[
        date_type,
        Field(
            description="The date of the original news article in YYYY-MM-DD format",
            default_factory=datetime.today().date
        )
    ]