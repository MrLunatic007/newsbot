"""
Fetches news articles using RSS feeds - much more reliable than web scraping
Updated with working RSS feeds as of 2024/2025
"""

import feedparser
from typing import List, Dict, Optional
from datetime import datetime


class NewsSourceFetcherError(Exception):
    """Gets raised when fetching news sources fails"""

    pass


class NewsSourceFetcher:
    """Fetches news articles from various sources using RSS feeds"""

    # Updated RSS feeds - verified working feeds
    RSS_FEEDS = {
        "bbc": {
            "general": "http://feeds.bbci.co.uk/news/rss.xml",
            "world": "http://feeds.bbci.co.uk/news/world/rss.xml",
            "uk": "http://feeds.bbci.co.uk/news/uk/rss.xml",
            "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
            "politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
            "health": "http://feeds.bbci.co.uk/news/health/rss.xml",
            "education": "http://feeds.bbci.co.uk/news/education/rss.xml",
            "science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
            "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "entertainment": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
        },
        "guardian": {
            "general": "https://www.theguardian.com/world/rss",
            "world": "https://www.theguardian.com/world/rss",
            "uk": "https://www.theguardian.com/uk-news/rss",
            "business": "https://www.theguardian.com/business/rss",
            "technology": "https://www.theguardian.com/technology/rss",
            "science": "https://www.theguardian.com/science/rss",
            "environment": "https://www.theguardian.com/environment/rss",
            "politics": "https://www.theguardian.com/politics/rss",
        },
        "nytimes": {
            "general": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "world": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "us": "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
            "business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
            "science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
            "health": "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
        },
        "techcrunch": {
            "general": "https://techcrunch.com/feed/",
            "startups": "https://techcrunch.com/category/startups/feed/",
            "ai": "https://techcrunch.com/category/artificial-intelligence/feed/",
            "apps": "https://techcrunch.com/category/apps/feed/",
            "security": "https://techcrunch.com/category/security/feed/",
        },
        "arstechnica": {
            "general": "https://feeds.arstechnica.com/arstechnica/index",
            "technology": "https://feeds.arstechnica.com/arstechnica/technology-lab",
            "science": "https://feeds.arstechnica.com/arstechnica/science",
            "policy": "https://feeds.arstechnica.com/arstechnica/tech-policy",
        },
        "wired": {
            "general": "https://www.wired.com/feed/rss",
            "business": "https://www.wired.com/feed/business/rss",
            "gear": "https://www.wired.com/feed/gear/rss",
            "science": "https://www.wired.com/feed/science/rss",
            "security": "https://www.wired.com/feed/security/rss",
        },
        "reuters": {
            "general": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
            "world": "https://www.reutersagency.com/feed/?best-topics=international-news&post_type=best",
            "business": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
            "technology": "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best",
        },
        "aljazeera": {
            "general": "https://www.aljazeera.com/xml/rss/all.xml",
            "news": "https://www.aljazeera.com/xml/rss/all.xml",
        },
    }

    def get_available_sources(self) -> Dict[str, List[str]]:
        """Returns all available news sources and their categories"""
        return {
            source: list(categories.keys())
            for source, categories in self.RSS_FEEDS.items()
        }

    def fetch_news_articles(
        self, source: str, category: str = "general", max_articles: int = 10
    ) -> List[Dict[str, str]]:
        """
        Fetches news articles from RSS feed

        Args:
            source: News source (e.g., 'bbc', 'guardian')
            category: News category (e.g., 'technology', 'world')
            max_articles: Maximum number of articles to return

        Returns:
            List of article dictionaries with title, summary, link, published date
        """
        try:
            source_lower = source.lower()
            category_lower = category.lower()

            # Check if source exists
            if source_lower not in self.RSS_FEEDS:
                available = ", ".join(self.RSS_FEEDS.keys())
                raise NewsSourceFetcherError(
                    f"Source '{source}' not available. Available sources: {available}"
                )

            # Check if category exists for this source
            if category_lower not in self.RSS_FEEDS[source_lower]:
                available = ", ".join(self.RSS_FEEDS[source_lower].keys())
                raise NewsSourceFetcherError(
                    f"Category '{category}' not available for {source}. "
                    f"Available categories: {available}"
                )

            # Get the RSS feed URL
            feed_url = self.RSS_FEEDS[source_lower][category_lower]

            # Parse the feed
            print(f"   📡 Fetching from: {feed_url}")
            feed = feedparser.parse(feed_url)

            # Check for feed errors
            if hasattr(feed, "bozo_exception"):
                print(f"   ⚠ Feed warning: {feed.bozo_exception}")

            if not feed.entries:
                raise NewsSourceFetcherError(
                    f"No articles found in {source} {category} feed. "
                    f"The RSS feed might be temporarily unavailable."
                )

            # Extract article information
            articles = []
            for entry in feed.entries[:max_articles]:
                # Get summary/description
                summary = entry.get("summary", "")
                if not summary:
                    summary = entry.get("description", "")
                if not summary:
                    summary = entry.get("content", [{}])[0].get("value", "")

                article = {
                    "title": entry.get("title", "No title"),
                    "summary": summary,
                    "link": entry.get("link", ""),
                    "published": entry.get("published", entry.get("updated", "")),
                    "source": source,
                    "category": category,
                }
                articles.append(article)

            return articles

        except NewsSourceFetcherError:
            raise
        except Exception as e:
            raise NewsSourceFetcherError(f"Error fetching articles from {source}: {e}")

    def search_articles_by_keyword(
        self,
        keyword: str,
        source: str,
        category: str = "general",
        max_results: int = 10,
    ) -> List[Dict[str, str]]:
        """
        Fetches articles and filters by keyword in title or summary

        Args:
            keyword: Keyword to search for
            source: News source
            category: News category
            max_results: Max filtered results to return

        Returns:
            Filtered list of articles containing the keyword
        """
        try:
            # Fetch more articles to search through
            articles = self.fetch_news_articles(source, category, max_articles=50)

            # Filter by keyword (case-insensitive)
            keyword_lower = keyword.lower()
            filtered = [
                article
                for article in articles
                if keyword_lower in article["title"].lower()
                or keyword_lower in article["summary"].lower()
            ]

            return filtered[:max_results]

        except Exception as e:
            raise NewsSourceFetcherError(f"Error searching articles: {e}")

    def search_across_sources(
        self, keyword: str, sources: Optional[List[str]] = None, max_per_source: int = 3
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Search for keyword across multiple sources

        Args:
            keyword: Keyword to search for
            sources: List of sources to search (if None, searches all)
            max_per_source: Max results per source

        Returns:
            Dictionary mapping source names to article lists
        """
        if sources is None:
            sources = list(self.RSS_FEEDS.keys())

        results = {}

        for source in sources:
            try:
                # Try general category first
                articles = self.search_articles_by_keyword(
                    keyword, source, "general", max_per_source
                )
                if articles:
                    results[source] = articles
            except NewsSourceFetcherError:
                # Skip sources that fail
                continue

        return results
