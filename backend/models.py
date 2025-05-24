"""Data Models for the BriefNews API"""

from pydantic import BaseModel, Field
from typing import Annotated, Literal, TypeAlias

# Input Models:

class ArticleURL(BaseModel):
    url: Annotated[str, Field(description="The URL of the news article to summarize. Must be a valid URL.")]

# Output Models:
class ArticleOutput(BaseModel):
    title: Annotated[str, Field(description="The title of the news article")]
    summary: Annotated[str, Field(description="The summary of the news article")]
    sentiment: Annotated[Literal["positive", "negative", "neutral"], Field(description="The sentiment of the news article, measured as positive, negative, or neutral")]
    url: Annotated[str, Field(description="The URL of the news article")]
    
