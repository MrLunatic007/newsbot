"""
Simple News Bot - Just uses RSS feed summaries (no web scraping needed!)
Much faster and more reliable
"""

import feedparser
from typing import Optional


class SimpleNewsBot:
    RSS_FEEDS = {
        "bbc": {
            "general": "http://feeds.bbci.co.uk/news/rss.xml",
            "world": "http://feeds.bbci.co.uk/news/world/rss.xml",
            "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "business": "http://feeds.bbci.co.uk/news/business/rss.xml",
            "science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        },
        "cnn": {
            "general": "http://rss.cnn.com/rss/cnn_topstories.rss",
            "world": "http://rss.cnn.com/rss/cnn_world.rss",
            "technology": "http://rss.cnn.com/rss/cnn_tech.rss",
        },
        "guardian": {
            "general": "https://www.theguardian.com/uk/rss",
            "world": "https://www.theguardian.com/world/rss",
            "technology": "https://www.theguardian.com/technology/rss",
        },
    }

    def get_news(
        self, source: str, category: str = "general", keyword: Optional[str] = None
    ):
        """Get news summaries from RSS feeds"""

        if source not in self.RSS_FEEDS:
            print(f"❌ Unknown source. Available: {', '.join(self.RSS_FEEDS.keys())}")
            return

        if category not in self.RSS_FEEDS[source]:
            print(
                f"❌ Unknown category. Available: {', '.join(self.RSS_FEEDS[source].keys())}"
            )
            return

        feed_url = self.RSS_FEEDS[source][category]
        print(f"\n🔍 Fetching {source.upper()} - {category} news...\n")

        feed = feedparser.parse(feed_url)

        if not feed.entries:
            print("❌ No articles found")
            return

        count = 0
        for entry in feed.entries[:10]:
            # Filter by keyword if provided
            if keyword:
                keyword_lower = keyword.lower()
                if (
                    keyword_lower not in entry.title.lower()
                    and keyword_lower not in entry.get("summary", "").lower()
                ):
                    continue

            count += 1
            print("=" * 70)
            print(f"📰 {entry.title}")
            print("=" * 70)
            print(f"🔗 {entry.link}")
            print(f"📅 {entry.get('published', 'N/A')}")

            if entry.get("summary"):
                print(f"\n{entry.summary}\n")

            if count >= 5:
                break

        if count == 0 and keyword:
            print(f"❌ No articles found matching '{keyword}'")


def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║           📰 SIMPLE NEWS BOT 📰                       ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\nAvailable sources: bbc, cnn, guardian")
    print("Available categories: general, world, technology, business, science")

    bot = SimpleNewsBot()

    while True:
        print("\n" + "-" * 60)
        source = input("News source (or 'quit'): ").strip().lower()

        if source in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break

        category = input("Category (default: general): ").strip().lower() or "general"
        keyword = input("Filter by keyword (optional): ").strip()

        bot.get_news(source, category, keyword if keyword else None)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
