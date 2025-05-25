"""Business Logic Services for the BriefNews API"""
import newspaper
from typing import List, Dict
from .database import get_db_connection, Article, init_db

class SummaryAPIService:
    """Summarizer service meant to interface with API to extract article informations, generate a summary, and provide a sentiment analysis."""

    def __init__(self):
        # Initialize database
        init_db()
        self.db = get_db_connection()

    def save_article(self, title: str, url: str, summary: str, authors: str, published_date: str) -> Article:
        """Save an article to the database"""
        article = Article(
            title=title,
            url=url,
            summary=summary,
            authors=authors,
            published_date=published_date
        )
        self.db.add(article)
        self.db.commit()
        self.db.refresh(article)
        return article

    def guardian_crawler(self):
        """Crawl articles from The Guardian and save them to database"""
        guardian = newspaper.build("https://www.theguardian.com/international")
        # Get details of the most recent 15 articles from the international topic
        i = 0
        while i < 15 and i < len(guardian.articles):
            article = guardian.articles[i]
            try:
                # Download and parse the article
                article.download()
                article.parse()
                
                # Save to database
                self.save_article(
                    title=article.title,
                    url=article.url,
                    summary=article.summary,
                    authors=", ".join(article.authors) if article.authors else "",
                    published_date=article.publish_date
                )
                print(f"Saved article: {article.title}")
            except Exception as e:
                print(f"Error processing article {article.url}: {str(e)}")
            i += 1
        
    def cnn_crawler(self):
        """Crawl articles from The Guardian and save them to database"""
        cnn = newspaper.build("https://edition.cnn.com")
        # Get details of the most recent 15 articles from the CNN mobile site
        i = 0
        while i < 15 and i < len(cnn.articles):
            article = cnn.articles[i]
            try:
                # Download and parse the article
                article.download()
                article.parse()
                
                # Save to database
                self.save_article(
                    title=article.title,
                    url=article.url,
                    summary=article.summary,
                    authors=", ".join(article.authors) if article.authors else "",
                    published_date=article.publish_date
                )
                print(f"Saved article: {article.title}")
            except Exception as e:
                print(f"Error processing article {article.url}: {str(e)}")
            i += 1

    def get_all_articles(self) -> List[Article]:
        """Retrieve all articles from the database"""
        return self.db.query(Article).all()
