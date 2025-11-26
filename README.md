# 📰 News Bot - Telegram Edition

A Telegram bot that delivers news summaries from top sources with a freemium subscription model.

## ✨ Features

### 🆓 Free Tier
- 10 articles per day
- BBC & Guardian news sources
- General & World categories
- Basic RSS summaries
- Search with 3 results

### 🌟 Premium Tier ($3/month)
- 100 articles per day
- **All 8+ news sources** (BBC, Guardian, NYTimes, TechCrunch, Wired, Reuters, Ars Technica, Al Jazeera)
- **All categories** (Technology, Business, Science, etc.)
- **AI-powered summaries**
- Search with 10 results
- Priority support

## 🚀 Quick Start

### 1. Prerequisites
- Docker & Docker Compose
- Telegram Bot Token (from @BotFather)
- HuggingFace Token (optional, for AI summaries)

### 2. Setup

```bash
# Clone the repository
git clone your-repo-url
cd news-bot

# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_telegram_token
HF_TOKEN=your_huggingface_token
EOF

# Setup subscription system
chmod +x setup_subscription.sh
./setup_subscription.sh

# Start the bot
chmod +x start_bot.sh
./start_bot.sh
```

### 3. Test Your Bot

Open Telegram and send:
- `/start` - Welcome message
- `/news` - Browse news
- `/premium` - See premium features

## 📁 Project Structure

```
news-bot/
├── telegram_bot.py              # Main Telegram bot
├── main.py                      # CLI version
├── admin_tool.py                # Subscription management
├── docker-compose.yml           # Docker config
├── Dockerfile                   # Docker build
├── requirements.txt             # Dependencies
├── .env                         # Your secrets (don't commit!)
├── data/
│   └── subscriptions.json       # User database
└── src/
    ├── source/
    │   └── newsSourceFetcher.py # RSS feed handler
    ├── getter/
    │   └── newsGetter.py        # Article fetcher
    ├── parser/
    │   └── newsParser.py        # HTML parser
    ├── summarizer/
    │   └── newsSummarizer.py    # AI summarizer
    └── subscription/
        └── subscription_manager.py  # Subscription logic
```

## 💰 Monetization

### Payment Setup
1. Users subscribe via [Buy Me a Coffee](https://buymeacoffee.com/mrlunatic)
2. They send you their Telegram ID
3. You activate premium using admin tool

### Manage Subscriptions

```bash
# Run admin tool
python admin_tool.py

# Options:
# 1. Upgrade user to Premium
# 2. View user status
# 3. List all premium users
# 4. Remove premium access
```

## 🤖 Bot Commands

| Command | Description | Availability |
|---------|-------------|--------------|
| `/start` | Welcome + tier info | All |
| `/news` | Browse news by source | All |
| `/search <keyword>` | Search articles | All |
| `/sources` | View available sources | All |
| `/status` | Check subscription status | All |
| `/premium` | Upgrade to Premium | All |
| `/help` | Show help message | All |

## 🎯 Available News Sources

| Source | Free | Premium |
|--------|------|---------|
| BBC | ✅ | ✅ |
| Guardian | ✅ | ✅ |
| NYTimes | ❌ | ✅ |
| TechCrunch | ❌ | ✅ |
| Wired | ❌ | ✅ |
| Ars Technica | ❌ | ✅ |
| Reuters | ❌ | ✅ |
| Al Jazeera | ❌ | ✅ |

## 🔧 Configuration

### Customize Limits

Edit `src/subscription/subscription_manager.py`:

```python
self.LIMITS = {
    "free": {
        "daily_articles": 10,          # Articles per day
        "sources": ["bbc", "guardian"], # Available sources
        "ai_summaries": False,         # AI summaries
        "search_results": 3,           # Search limit
    },
    "premium": {
        "daily_articles": 100,
        "sources": "all",
        "ai_summaries": True,
        "search_results": 10,
    }
}
```

### Add More Sources

Edit `src/source/newsSourceFetcher.py`:

```python
RSS_FEEDS = {
    "newsource": {
        "general": "https://example.com/rss.xml",
        "technology": "https://example.com/tech/rss.xml",
    }
}
```

## 🚢 Deployment

### Docker (Recommended)

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

### Cloud Platforms

**Railway.app** (Easiest):
1. Push to GitHub
2. Connect to Railway
3. Add environment variables
4. Deploy!

**DigitalOcean/AWS/GCP**:
1. Create droplet/instance
2. Install Docker
3. Clone repo
4. Run `./start_bot.sh`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Analytics

### View Stats

```bash
# Quick stats
python -c "
from src.subscription.subscription_manager import SubscriptionManager
m = SubscriptionManager()
total = len(m.subscriptions)
premium = sum(1 for u in m.subscriptions.values() if u.get('tier') == 'premium')
print(f'Total: {total}, Premium: {premium} ({premium/total*100:.1f}%)')
"
```

### Track Metrics
- Daily/Monthly Active Users
- Free → Premium conversion rate
- Daily article consumption
- Popular sources/categories
- Churn rate

## 🛡️ Security

- Subscriptions stored locally in JSON
- No passwords (using Telegram ID)
- Environment variables for secrets
- Docker volume for persistence
- Regular backups recommended

## 📝 Documentation

- [SUBSCRIPTION_GUIDE.md](SUBSCRIPTION_GUIDE.md) - Full subscription guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands
- [CHECKLIST.md](CHECKLIST.md) - Setup checklist

## 🐛 Troubleshooting

### Bot not responding
```bash
docker-compose logs -f
docker-compose restart
```

### Subscription not working
```bash
python admin_tool.py
# Check user status (option 2)
# Manually upgrade (option 1)
```

### Daily limit not resetting
- Automatic reset at midnight UTC
- Check user's `last_reset` field in database

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📜 License

MIT License - Feel free to modify and distribute!

## 💬 Support

- Issues: Create GitHub issue
- Questions: Open discussion
- Premium support: support@yourbot.com

## 🎯 Roadmap

- [ ] Automated payment processing
- [ ] Webhook integration
- [ ] Email notifications
- [ ] Usage analytics dashboard
- [ ] Mobile app
- [ ] Team/Business plans
- [ ] API access
- [ ] Custom news sources

## 🌟 Show Your Support

If you find this project useful:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 📢 Share with others

---

**Made with ❤️ by [@mrlunatic](https://buymeacoffee.com/mrlunatic)**

**Support development:** [Buy Me a Coffee](https://buymeacoffee.com/mrlunatic)
