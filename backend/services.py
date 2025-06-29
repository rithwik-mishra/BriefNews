"""Business Logic Services for the BriefNews API"""
from gnews import GNews
from googlenewsdecoder import new_decoderv1
from typing import List, Optional
from .models import ArticleOutput, ArticleURLInput, TopicEnum
import datetime
import os
from huggingface_hub import InferenceClient, AsyncInferenceClient
from dotenv import load_dotenv
import asyncio

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
    
    async_client = AsyncInferenceClient(
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
            exclude_websites = ['reuters.com', 'wsj.com', 'investors.com', 'barrons.com', 'politico.com', "androidpolice.com", "greekreporter.com", "forbes.com", "marketwatch.com", "axios.com"]
        )
        if topic:
            return googleNews.get_news_by_topic(topic)
        else:
            return googleNews.get_top_news()

    async def get_all_articles(self, topic: Optional[TopicEnum]) -> List[ArticleOutput]:
        """Returns information about articles for a given topic using our output model"""

        gnews_articles = self.crawl_articles(topic)
        
        # Increased semaphore limit for better concurrency
        semaphore = asyncio.Semaphore(10)
        
        async def decode_url(url: str):
            """Async wrapper for URL decoding"""
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, new_decoderv1, url, 5)
        
        async def fetch_article(url: str):
            """Async wrapper for article fetching"""
            loop = asyncio.get_event_loop()
            googleNews = GNews()
            return await loop.run_in_executor(None, googleNews.get_full_article, url)
        
        async def process_article(article):
            try:
                url = article['url']
                
                # Decode URL concurrently
                decoded_url_result = await decode_url(url)
                decoded_url = decoded_url_result['decoded_url']
                
                # Fetch article concurrently
                thisArticle = await fetch_article(decoded_url)

                if not thisArticle:
                    print(f"Skipped Article: {url}")
                    return None

                full_text = thisArticle.text

                published_date = datetime.datetime.now().date()  # Default to today
                if article.get('published date'):
                    try:
                        published_date = datetime.datetime.strptime(article['published date'], '%a, %d %b %Y %H:%M:%S GMT').date()
                    except:
                        published_date = datetime.datetime.now().date()

                # Use semaphore to limit concurrent summarization calls
                async with semaphore:
                    summary = await self.summarize_text_async(full_text)

                output = ArticleOutput(
                    title=article['title'],
                    summary=summary,
                    url=decoded_url,
                    date=published_date,
                )
                return output
            except Exception as e:
                print(f"Error processing article {article.get('title', 'Unknown')}: {str(e)}")
                return None

        # Create tasks for all articles
        tasks = [process_article(article) for article in gnews_articles]
        
        # Run all concurrently with asyncio.gather
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and None values, return valid results
        articles = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Exception occurred: {result}")
                continue
            if result is not None:
                articles.append(result)
        
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

    async def summarize_text_async(self, text: str) -> str:
        """Async version of summarize_text using HuggingFace async client"""
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
        
        result = await self.async_client.summarization(text)
        return result.summary_text

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

    