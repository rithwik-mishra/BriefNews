"""Business Logic Services for the BriefNews API"""
import newspaper
from typing import List, Dict
from .models import ArticleOutput, ArticleURLInput
import datetime

class SummaryAPIService:
    """Summarizer service meant to interface with API to extract article informations, generate a summary, and provide a sentiment analysis."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SummaryAPIService, cls).__new__(cls)
            cls._instance.articles = []
        return cls._instance

    def __init__(self):
        """Initialize the SummaryAPIService"""
        if not hasattr(self, 'articles'):
            self.articles = []

    def is_updated(self) -> bool:
        """Check if the articles are updated and from today's date"""
        if not self.articles:
            return False
        return self.articles[0].date is not None and self.articles[0].date.date() == datetime.datetime.now().date()

    def npr_crawler(self):
        """Crawl articles from NPR and save them to database"""
        npr = newspaper.build("https://www.npr.org/sections/national/")
        # Get details of the most recent 15 articles from the international topic
        length = min(15, len(npr.articles))  # Limit to 15 articles or less if fewer are available
        for i in range(length):
            article = npr.articles[i]
            article.download()
            article.parse()
            ouput = ArticleOutput(
                title=article.title,
                authors=article.authors,
                summary="", # Placeholder for summary generation
                sentiment="neutral",  # Placeholder for sentiment analysis
                url=article.url,
                date=article.publish_date  # Use publish date or current date if not available
            )
            self.articles.append(ouput)
        
    def cnn_crawler(self):
        """Crawl articles from The Guardian and save them to database"""
        cnn = newspaper.build("https://edition.cnn.com/us")
        # Get details of the most recent 15 articles from the CNN mobile site
        length = min(15, len(cnn.articles))  # Limit to 15 articles or less if fewer are available
        for i in range(length):
            article = cnn.articles[i]
            article.download()
            article.parse()
            ouput = ArticleOutput(
                title=article.title,
                authors=article.authors,
                summary="", # Placeholder for summary generation
                sentiment="neutral",  # Placeholder for sentiment analysis
                url=article.url,
                date=article.publish_date.date()  # Use publish date or current date if not available
            )
            self.articles.append(ouput)

    def get_all_articles(self) -> List[ArticleOutput]:
        """Retrieve all articles from the database"""
        return self.articles

    def summarize_article(self, article_input: ArticleURLInput) -> None:
        """Summarize the article and return the output"""
        pass