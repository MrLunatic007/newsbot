"""
Telegram News Bot with Subscription System
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

from src.source.newsSourceFetcher import NewsSourceFetcher, NewsSourceFetcherError
from src.summarizer.newsSummarizer import NewsSummarizer, NewsSummarizerError
from src.getter.newsGetter import NewsGetter, NewsGetterError
from src.parser.newsParser import NewsParser, NewsParserError
from src.subscription.subscription_manager import SubscriptionManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramNewsBot:
    def __init__(self):
        self.source_fetcher = NewsSourceFetcher()
        self.summarizer = NewsSummarizer()
        self.parser = NewsParser()
        self.subscription_manager = SubscriptionManager()

        # Buy Me a Coffee link
        self.PAYMENT_LINK = "https://buymeacoffee.com/mrlunatic"

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command - show welcome message"""
        user_id = update.effective_user.id
        tier = self.subscription_manager.get_user_tier(user_id)

        welcome_text = (
            "📰 *Welcome to News Bot!*\n\n"
            "Get the latest news summaries from top sources.\n\n"
            f"Current Plan: *{tier.upper()}* {'🌟' if tier == 'premium' else '📱'}\n\n"
            "*Commands:*\n"
            "/news - Browse news by source\n"
            "/search - Search for specific topics\n"
            "/sources - View available sources\n"
            "/premium - Upgrade to Premium\n"
            "/status - Check your subscription\n"
            "/help - Show help message\n\n"
        )

        if tier == "free":
            welcome_text += (
                "🎁 *Free Plan Includes:*\n"
                "• 10 articles per day\n"
                "• BBC & Guardian sources\n"
                "• General & World news\n\n"
                "✨ Upgrade to Premium for unlimited access!"
            )

        await update.message.reply_text(welcome_text, parse_mode="Markdown")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user's subscription status"""
        user_id = update.effective_user.id
        limits = self.subscription_manager.get_limits(user_id)
        tier = limits["tier"]

        status_text = f"📊 *Your Subscription Status*\n\n"
        status_text += (
            f"Plan: *{tier.upper()}* {'🌟' if tier == 'premium' else '📱'}\n\n"
        )

        if tier == "free":
            status_text += (
                f"Today's Usage: {limits['current_usage']}/{limits['daily_articles']} articles\n"
                f"Available Sources: {len(limits['sources'])}\n"
                f"AI Summaries: {'✅' if limits['ai_summaries'] else '❌'}\n"
                f"Search Results: {limits['search_results']} per query\n\n"
                "🎯 *Free Plan Features:*\n"
                "• 10 articles daily\n"
                "• BBC & Guardian\n"
                "• General & World categories\n"
                "• Basic summaries\n\n"
            )
        else:
            from datetime import datetime

            expiry = datetime.fromisoformat(limits["expires_at"])
            status_text += (
                f"Today's Usage: {limits['current_usage']}/{limits['daily_articles']} articles\n"
                f"Expires: {expiry.strftime('%B %d, %Y')}\n"
                f"Available Sources: All\n"
                f"AI Summaries: ✅\n\n"
                "🌟 *Premium Features Active:*\n"
                "• 100 articles daily\n"
                "• All news sources\n"
                "• All categories\n"
                "• AI-powered summaries\n"
                "• Priority support\n\n"
            )

        keyboard = [
            [InlineKeyboardButton("⬆️ Upgrade to Premium", callback_data="show_premium")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            status_text, parse_mode="Markdown", reply_markup=reply_markup
        )

    async def premium_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show premium upgrade options"""
        premium_text = (
            "✨ *Upgrade to Premium*\n\n"
            "Unlock all features and support development!\n\n"
            "🌟 *Premium Benefits:*\n"
            "• 100 articles per day (vs 10)\n"
            "• Access ALL news sources\n"
            "• All categories unlocked\n"
            "• AI-powered summaries\n"
            "• 10 search results (vs 3)\n"
            "• Priority support\n"
            "• No ads (coming soon)\n\n"
            "💰 *Pricing:*\n"
            "• $3/month - Monthly\n"
            "• $30/year - Annual (2 months free!)\n\n"
            "Support indie development! ❤️\n\n"
            f"[Subscribe via Buy Me a Coffee]({self.PAYMENT_LINK})\n\n"
            "After subscribing, send /activate with your email to activate Premium!"
        )

        keyboard = [
            [InlineKeyboardButton("💳 Subscribe Now", url=self.PAYMENT_LINK)],
            [
                InlineKeyboardButton(
                    "🔄 I Already Subscribed", callback_data="activate_premium"
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            premium_text,
            parse_mode="Markdown",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        help_text = (
            "📰 *News Bot Help*\n\n"
            "*Commands:*\n"
            "• /news - Browse news by source and category\n"
            "• /search <keyword> - Search for specific topics\n"
            "• /sources - View available news sources\n"
            "• /premium - Upgrade to Premium\n"
            "• /status - Check subscription status\n"
            "• /help - Show this message\n\n"
            "*Examples:*\n"
            "• /search artificial intelligence\n"
            "• /search bitcoin\n"
            "• /news (then select source)\n\n"
            "*Premium Features:*\n"
            "Upgrade with /premium for unlimited access!"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def sources_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show available sources"""
        user_id = update.effective_user.id
        available_sources = self.subscription_manager.get_available_sources(user_id)
        tier = self.subscription_manager.get_user_tier(user_id)

        all_sources = self.source_fetcher.get_available_sources()

        text = f"📰 *Available Sources ({tier.upper()} Plan)*\n\n"

        for source, categories in sorted(all_sources.items()):
            if source in available_sources or tier == "premium":
                text += f"✅ *{source.upper()}*\n"
            else:
                text += f"🔒 *{source.upper()}* (Premium)\n"

            text += f"  Categories: {', '.join(sorted(categories)[:3])}"
            if len(categories) > 3:
                text += f"..."
            text += "\n\n"

        if tier == "free":
            text += "\n🌟 Upgrade to /premium for access to all sources!"

        await update.message.reply_text(text, parse_mode="Markdown")

    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show news source selection"""
        user_id = update.effective_user.id

        # Check daily limit
        if not self.subscription_manager.can_access_feature(user_id, "daily_limit"):
            limits = self.subscription_manager.get_limits(user_id)
            await update.message.reply_text(
                f"❌ Daily limit reached ({limits['daily_articles']} articles)\n\n"
                "Upgrade to Premium for 100 articles/day!\n"
                "Use /premium to learn more.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("⬆️ Upgrade", callback_data="show_premium")]]
                ),
            )
            return

        available_sources = self.subscription_manager.get_available_sources(user_id)

        keyboard = []
        row = []

        source_emojis = {
            "bbc": "📰",
            "guardian": "🗞️",
            "techcrunch": "💻",
            "wired": "🔧",
            "nytimes": "🌍",
            "reuters": "📡",
            "arstechnica": "⚙️",
            "aljazeera": "🌐",
        }

        for source in sorted(available_sources):
            emoji = source_emojis.get(source, "📰")
            row.append(
                InlineKeyboardButton(
                    f"{emoji} {source.upper()}", callback_data=f"source_{source}"
                )
            )
            if len(row) == 2:
                keyboard.append(row)
                row = []

        if row:
            keyboard.append(row)

        # Add premium button if free tier
        tier = self.subscription_manager.get_user_tier(user_id)
        if tier == "free":
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "🌟 Unlock All Sources", callback_data="show_premium"
                    )
                ]
            )

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Choose a news source:", reply_markup=reply_markup
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()

        data = query.data
        user_id = update.effective_user.id

        if data == "show_premium":
            await self.show_premium_inline(query)

        elif data == "activate_premium":
            await query.edit_message_text(
                "🔑 *Activate Premium*\n\n"
                "After subscribing on Buy Me a Coffee:\n"
                "1. Note your subscription email\n"
                "2. Contact @YourSupportUsername with:\n"
                "   - Your Telegram username\n"
                "   - Subscription email\n"
                "   - Payment confirmation\n\n"
                "We'll activate your account within 24 hours!\n\n"
                "Or contact support: support@yourbot.com",
                parse_mode="Markdown",
            )

        elif data.startswith("source_"):
            source = data.replace("source_", "")

            # Check if user can access this source
            if not self.subscription_manager.can_access_feature(
                user_id, "source", source
            ):
                await query.edit_message_text(
                    f"🔒 *{source.upper()}* is a Premium feature\n\n"
                    "Upgrade to access all news sources!",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "⬆️ Upgrade Now", callback_data="show_premium"
                                )
                            ]
                        ]
                    ),
                )
                return

            await self.show_categories(query, source)

        elif data.startswith("category_"):
            parts = data.replace("category_", "").split("_")
            source = parts[0]
            category = "_".join(parts[1:])

            # Check category access
            available_cats = self.subscription_manager.get_available_categories(user_id)
            if available_cats != "all" and category not in available_cats:
                await query.edit_message_text(
                    f"🔒 *{category.upper()}* category is Premium only\n\n"
                    "Upgrade to access all categories!",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "⬆️ Upgrade Now", callback_data="show_premium"
                                )
                            ]
                        ]
                    ),
                )
                return

            await self.fetch_and_send_news(query, source, category)

    async def show_premium_inline(self, query):
        """Show premium info inline"""
        premium_text = (
            "✨ *Premium Plan*\n\n"
            "🌟 *Benefits:*\n"
            "• 100 articles/day\n"
            "• All sources\n"
            "• All categories\n"
            "• AI summaries\n\n"
            "💰 $3/month or $30/year\n\n"
            f"[Subscribe Now]({self.PAYMENT_LINK})"
        )

        keyboard = [
            [InlineKeyboardButton("💳 Subscribe", url=self.PAYMENT_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="back_sources")],
        ]

        await query.edit_message_text(
            premium_text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True,
        )

    async def show_categories(self, query, source: str):
        """Show category selection for a source"""
        user_id = query.from_user.id
        sources = self.source_fetcher.get_available_sources()
        categories = sources.get(source, {})
        available_cats = self.subscription_manager.get_available_categories(user_id)

        keyboard = []
        row = []
        for i, category in enumerate(sorted(categories), 1):
            # Check if category is available
            is_available = available_cats == "all" or category in available_cats
            button_text = (
                category.capitalize() if is_available else f"🔒 {category.capitalize()}"
            )

            row.append(
                InlineKeyboardButton(
                    button_text, callback_data=f"category_{source}_{category}"
                )
            )
            if i % 2 == 0:
                keyboard.append(row)
                row = []

        if row:
            keyboard.append(row)

        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_sources")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"Choose a category from *{source.upper()}*:",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    async def fetch_and_send_news(self, query, source: str, category: str):
        """Fetch news and send to user"""
        user_id = query.from_user.id

        await query.edit_message_text(
            f"🔍 Fetching {source.upper()} - {category} news..."
        )

        try:
            # Get max articles based on tier
            max_articles = (
                3 if self.subscription_manager.get_user_tier(user_id) == "free" else 5
            )

            articles = self.source_fetcher.fetch_news_articles(
                source, category, max_articles=max_articles
            )

            if not articles:
                await query.edit_message_text(
                    f"❌ No articles found for {source} - {category}"
                )
                return

            await query.edit_message_text(
                f"✅ Found {len(articles)} articles from {source.upper()}!\n"
                f"Sending them now..."
            )

            for i, article in enumerate(articles, 1):
                # Increment usage
                self.subscription_manager.increment_usage(user_id)

                text = (
                    f"📰 *Article {i}/{len(articles)}*\n\n"
                    f"*{article['title']}*\n\n"
                    f"📅 {article['published']}\n\n"
                )

                if article["summary"]:
                    summary = article["summary"][:500]
                    if len(article["summary"]) > 500:
                        summary += "..."
                    text += f"{summary}\n\n"

                text += f"[Read more]({article['link']})"

                await query.message.reply_text(
                    text, parse_mode="Markdown", disable_web_page_preview=True
                )

        except NewsSourceFetcherError as e:
            await query.edit_message_text(f"❌ Error: {e}")
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            await query.edit_message_text(f"❌ An error occurred: {str(e)[:100]}")

    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Search for news by keyword"""
        user_id = update.effective_user.id

        # Check daily limit
        if not self.subscription_manager.can_access_feature(user_id, "daily_limit"):
            await update.message.reply_text(
                "❌ Daily limit reached!\n\n"
                "Upgrade to Premium for more articles.\n"
                "Use /premium to learn more."
            )
            return

        if not context.args:
            await update.message.reply_text(
                "Please provide a search keyword.\n\n"
                "Example: /search artificial intelligence"
            )
            return

        keyword = " ".join(context.args)
        max_results = self.subscription_manager.can_access_feature(
            user_id, "search_results"
        )

        await update.message.reply_text(
            f"🔍 Searching for: *{keyword}*...", parse_mode="Markdown"
        )

        try:
            results = self.source_fetcher.search_across_sources(
                keyword, max_per_source=1
            )

            if not results:
                await update.message.reply_text(f"❌ No articles found for '{keyword}'")
                return

            total = sum(len(articles) for articles in results.values())
            sent = 0

            for source, articles in results.items():
                for article in articles:
                    if sent >= max_results:
                        break

                    self.subscription_manager.increment_usage(user_id)

                    text = f"📰 *{source.upper()}*\n\n" f"*{article['title']}*\n\n"

                    if article["summary"]:
                        summary = article["summary"][:400]
                        if len(article["summary"]) > 400:
                            summary += "..."
                        text += f"{summary}\n\n"

                    text += f"[Read more]({article['link']})"

                    await update.message.reply_text(
                        text, parse_mode="Markdown", disable_web_page_preview=True
                    )
                    sent += 1

                if sent >= max_results:
                    break

            if total > max_results:
                tier = self.subscription_manager.get_user_tier(user_id)
                if tier == "free":
                    await update.message.reply_text(
                        f"📊 Showing {max_results} of {total} results\n\n"
                        "🌟 Upgrade to Premium for 10 results per search!",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "⬆️ Upgrade", callback_data="show_premium"
                                    )
                                ]
                            ]
                        ),
                    )

        except Exception as e:
            logger.error(f"Error searching: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)[:100]}")

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")

        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again later."
            )


def main():
    """Start the bot"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        return

    bot = TelegramNewsBot()
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("news", bot.news_command))
    application.add_handler(CommandHandler("search", bot.search_command))
    application.add_handler(CommandHandler("sources", bot.sources_command))
    application.add_handler(CommandHandler("premium", bot.premium_command))
    application.add_handler(CommandHandler("status", bot.status_command))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_error_handler(bot.error_handler)

    logger.info("Starting News Bot with Subscription System...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
