"""Business Logic Services for the BriefNews API"""
import newspaper
from typing import List, Dict
from .models import ArticleOutput, ArticleURLInput

class SummaryAPIService:
    """Summarizer service meant to interface with API to extract article informations, generate a summary, and provide a sentiment analysis."""

    articles: List[ArticleOutput]  # List to store articles
    def __init__(self):
        """Initialize the SummaryAPIService"""
        self.articles = []

    def is_updated(self) -> bool:
        """Check if the articles are updated and from today's date"""
        if not self.articles:
            return False
        return self.articles[0].

    def guardian_crawler(self):
        """Crawl articles from The Guardian and save them to database"""
        guardian = newspaper.build("https://www.theguardian.com/international")
        # Get details of the most recent 15 articles from the international topic
        for i in range(25):
            article = guardian.articles[i]
            ouput = ArticleOutput(
                title=article.title,
                authors=article.authors,
                summary="", # Placeholder for summary generation
                sentiment="neutral",  # Placeholder for sentiment analysis
                url=article.source_url
                date=article.publish_date if article.publish_date else None
            )
            self.articles.append(ouput)
        
    def cnn_crawler(self):
        """Crawl articles from The Guardian and save them to database"""
        cnn = newspaper.build("https://edition.cnn.com")
        # Get details of the most recent 15 articles from the CNN mobile site
        for i in range(25):
            article = cnn.articles[i]
            ouput = ArticleOutput(
                title=article.title,
                authors=article.authors,
                summary="", # Placeholder for summary generation
                sentiment="neutral",  # Placeholder for sentiment analysis
                url=article.source_url
            )
            self.articles.append(ouput)

    def get_all_articles(self) -> List[ArticleOutput]:
        """Retrieve all articles from the database"""
        return self.articles

    def summarize_article(self, article_input: ArticleURLInput) -> ArticleOutput:
        """Summarize the article and return the output"""
        pass