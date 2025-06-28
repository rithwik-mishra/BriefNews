"""Business Logic Services for the BriefNews API"""
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from typing import List, Optional
from .models import ArticleOutput, ArticleURLInput, TopicEnum
import datetime
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ArticleUncrawlableError(Exception):
    pass

class SummaryAPIService:
    """Summarizer service meant to interface with API to extract article informations, generate a summary, and provide a sentiment analysis."""

    client = InferenceClient(
        provider="hf-inference",
        api_key=os.environ["HF_TOKEN"]
    )

    def crawl_articles(self, topic: Optional[TopicEnum]):
        """Crawl articles from the internet and save them to the database"""
        # Create Crawler using imposed conditions to minimize runtime and maximize relevency
        googleNews = GNews(
            language="en",
            country="US",
            max_results=10,
            exclude_websites = ['reuters.com', 'wsj.com', 'investors.com', 'barrons.com', 'politico.com', "androidpolice.com", "greekreporter.com"]
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

        def process_article(article):
            url = article['url']
            decoded_url = new_decoderv1(url, interval=5)
            thisArticle = googleNews.get_full_article(decoded_url['decoded_url'])

            if not thisArticle:
                print("Skipped Article")
                return None

            full_text = thisArticle.text

            published_date = datetime.datetime.now().date()  # Default to today
            if article.get('published date'):
                try:
                    published_date = datetime.datetime.strptime(article['published date'], '%a, %d %b %Y %H:%M:%S GMT').date()
                except:
                    published_date = datetime.datetime.now().date()

            output = ArticleOutput(
                title=article['title'],
                summary=self.summarize_text(full_text),
                url=url,
                date=published_date,
            )
            return output

        results = []
        for article in gnews_articles:
            result = process_article(article)
            if result is not None:
                results.append(result)

        articles = results
        return articles

    def summarize_article(self, article_input: ArticleURLInput) -> str:
        """Summarize the article and return the output"""
        googleNews = GNews()
        try:
            decoded_url = new_decoderv1(article_input.url, interval=5)
            thisArticle = googleNews.get_full_article(decoded_url['decoded_url'])
        except:
            thisArticle = googleNews.get_full_article(article_input.url)

        if not thisArticle:
            raise ArticleUncrawlableError() 

        full_text = thisArticle.text
        return self.summarize_text(full_text)
        

    def summarize_text(self, text: str) -> str:
        """Summarize given text using HuggingFace and return the output, truncating input to model's max token length."""
        # Clean and validate the text
        if not text or not text.strip():
            return "No content available to summarize."
        
        # Remove extra whitespace and normalize
        text = " ".join(text.split())
        
        # Truncate text if it's too long (BART model has ~1024 token limit)
        # Roughly 1 token = 4 characters, so limit to ~4000 characters
        max_length = 4000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        result = self.client.summarization(text)
        return result.summary_text

    