"""Business Logic Services for the BriefNews API"""
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from newspaper import Article
from typing import List, Dict, Optional
from .models import ArticleOutput, ArticleURLInput, TopicEnum
import datetime


class SummaryAPIService:
    """Summarizer service meant to interface with API to extract article informations, generate a summary, and provide a sentiment analysis."""

    def crawl_articles(self, topic: Optional[TopicEnum]):
        """Crawl articles from the internet and save them to the database"""
        # Create Crawler using imposed conditions to minimize runtime and maximize relevency
        googleNews = GNews(
            language="en",
            country="US",
            max_results=25,
            start_date=datetime.datetime.now() - datetime.timedelta(days=1),
            end_date=datetime.datetime.now(),
        )
        if topic:
            return googleNews.get_news_by_topic(topic)
        else:
            return googleNews.get_top_news()
        

    def get_all_articles(self, topic: Optional[TopicEnum]) -> List[ArticleOutput]:
        """Returns information about articles for a given topic using our output model"""

        gnews_articles = self.crawl_articles(topic)
        articles: List[ArticleOutput] = []
        googleNews = GNews()
        
        for article in gnews_articles:
            # Resolve RSS URL and crawl article for full text
            url=article['url']
            decoded_url = new_decoderv1(url, interval=5)
            try:
                thisArticle = googleNews.get_full_article(decoded_url['decoded_url'])
            except:
                print("Skipped Article")
                continue
            
            authors = thisArticle.authors if thisArticle else [""]
            full_text = thisArticle.text if thisArticle else ""
            
            # Parse the published date from GNews article
            published_date = datetime.datetime.now().date()  # Default to today
            if article.get('published date'):
                try:
                    published_date = datetime.datetime.strptime(article['published date'], '%a, %d %b %Y %H:%M:%S GMT').date()
                except:
                    published_date = datetime.datetime.now().date()
            
            # Create ArticleOutput model for each article URL and store
            output = ArticleOutput(
                title=article['title'],
                authors=authors,
                summary=self.summarize_text(full_text),
                sentiment="neutral",
                url=url,
                date=published_date,
            )
            articles.append(output)

        return articles

    def summarize_article(self, article_input: ArticleURLInput) -> None:
        """Summarize the article and return the output"""
        #TODO
        pass

    def summarize_text(self, text: str) -> str:
        """Summarize given text using HuggingFace and return the output"""
        #TODO
        return text

    