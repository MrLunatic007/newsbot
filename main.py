from src.summarizer.newsSummarizer import NewsSummarizer, NewsSummarizerError
from src.getter.newsGetter import NewsGetter, NewsGetterError
from src.parser.newsParser import NewsParser, NewsParserError
from src.source.newsSourceFetcher import NewsSourceFetcher, NewsSourceFetcherError
from typing import Optional


class NewsBot:
    def __init__(self) -> None:
        self.source_fetcher = NewsSourceFetcher()
        self.parser = NewsParser()
        self.summarizer = NewsSummarizer()

    def show_available_sources(self):
        """Display all available news sources and categories"""
        sources = self.source_fetcher.get_available_sources()

        print("\n📰 Available News Sources:")
        print("=" * 60)
        for source, categories in sorted(sources.items()):
            print(f"\n{source.upper()}:")
            print(f"  Categories: {', '.join(sorted(categories))}")
        print("=" * 60)

    def get_news_summaries(
        self,
        source: str,
        category: str = "general",
        keyword: Optional[str] = None,
        max_articles: int = 5,
        use_ai_summary: bool = False,
    ):
        """
        Fetches and displays news articles

        Args:
            source: News source (e.g., 'bbc', 'guardian')
            category: Category (e.g., 'technology', 'world')
            keyword: Optional keyword to filter articles
            max_articles: Number of articles to process
            use_ai_summary: Whether to generate AI summaries (slower)
        """
        try:
            print(f"\n🔍 Fetching {source.upper()} - {category} news...")

            # Fetch articles
            if keyword:
                print(f"   Searching for keyword: '{keyword}'")
                articles = self.source_fetcher.search_articles_by_keyword(
                    keyword, source, category, max_articles
                )
            else:
                articles = self.source_fetcher.fetch_news_articles(
                    source, category, max_articles
                )

            if not articles:
                print(f"❌ No articles found")
                if keyword:
                    print(f"   Try a different keyword or check other categories")
                return

            print(f"✓ Found {len(articles)} article(s)\n")

            # Process each article
            for i, article in enumerate(articles, 1):
                print("=" * 70)
                print(f"📰 Article {i}/{len(articles)}")
                print("=" * 70)
                print(f"Title: {article['title']}")
                print(f"Published: {article['published']}")
                print(f"Link: {article['link']}")
                print()

                # Show RSS summary (always available)
                if article["summary"]:
                    print("Summary:")
                    print(article["summary"])
                    print()

                # Optionally generate AI summary
                if use_ai_summary:
                    try:
                        print("🤖 Generating AI summary...")
                        getter = NewsGetter(url=article["link"])
                        raw_html = getter.fetch_html()
                        full_article = self.parser.parse_article(raw_html)

                        if full_article and len(full_article.strip()) > 100:
                            ai_summary = self.summarizer.summarizer(full_article)
                            print("AI Summary:")
                            print(ai_summary)
                            print()
                        else:
                            print("⚠ Article content too short for AI summary\n")

                    except (NewsGetterError, NewsParserError, NewsSummarizerError) as e:
                        print(f"⚠ Could not generate AI summary: {str(e)[:100]}...\n")

        except NewsSourceFetcherError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def search_everywhere(self, keyword: str, max_per_source: int = 2):
        """Search for a keyword across all news sources"""
        print(f"\n🔍 Searching all sources for: '{keyword}'...")

        try:
            results = self.source_fetcher.search_across_sources(
                keyword, max_per_source=max_per_source
            )

            if not results:
                print(f"❌ No articles found containing '{keyword}'")
                return

            print(f"✓ Found results in {len(results)} source(s)\n")

            for source, articles in results.items():
                print("=" * 70)
                print(f"📰 {source.upper()} ({len(articles)} articles)")
                print("=" * 70)

                for article in articles:
                    print(f"\n• {article['title']}")
                    print(f"  🔗 {article['link']}")
                    if article["summary"]:
                        # Truncate long summaries
                        summary = article["summary"][:200]
                        if len(article["summary"]) > 200:
                            summary += "..."
                        print(f"  {summary}")
                print()

        except Exception as e:
            print(f"❌ Error: {e}")


def main() -> None:
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           📰 NEWS BOT - RSS Feed Edition 📰              ║")
    print("╚════════════════════════════════════════════════════════════╝")

    bot = NewsBot()

    while True:
        print("\nOptions:")
        print("  1. View available sources")
        print("  2. Get news by source and category")
        print("  3. Search news by keyword in one source")
        print("  4. Search keyword across ALL sources")
        print("  5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            bot.show_available_sources()

        elif choice == "2":
            source = input(
                "\nEnter news source (e.g., bbc, guardian, techcrunch): "
            ).strip()
            category = input(
                "Enter category (e.g., technology, world, business): "
            ).strip()

            if not category:
                category = "general"

            try:
                max_articles = int(
                    input("How many articles? (default: 5): ").strip() or "5"
                )
            except ValueError:
                max_articles = 5

            ai_option = input("Generate AI summaries? (slower) [y/N]: ").strip().lower()
            use_ai = ai_option in ["y", "yes"]

            bot.get_news_summaries(
                source, category, max_articles=max_articles, use_ai_summary=use_ai
            )

        elif choice == "3":
            keyword = input("\nEnter keyword to search: ").strip()
            source = input("Enter news source (e.g., bbc, guardian): ").strip()
            category = input("Enter category (default: general): ").strip() or "general"

            try:
                max_articles = int(
                    input("How many articles? (default: 5): ").strip() or "5"
                )
            except ValueError:
                max_articles = 5

            bot.get_news_summaries(
                source, category, keyword, max_articles, use_ai_summary=False
            )

        elif choice == "4":
            keyword = input("\nEnter keyword to search across all sources: ").strip()

            try:
                max_per = int(
                    input("Max results per source? (default: 2): ").strip() or "2"
                )
            except ValueError:
                max_per = 2

            bot.search_everywhere(keyword, max_per)

        elif choice == "5":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
