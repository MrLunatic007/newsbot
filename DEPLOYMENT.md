# Telegram News Bot - Deployment Guide

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Telegram Bot Token (from @BotFather)
- HuggingFace Token (optional, for AI summaries)

### 1. Setup Environment Variables

Create a `.env` file in the project root:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Optional (for AI summaries)
HF_TOKEN=your_huggingface_token_here
```

### 2. Build and Run with Docker

```bash
# Build the Docker image
docker-compose build

# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### 3. Test Your Bot

1. Open Telegram and search for your bot
2. Send `/start` to begin
3. Try these commands:
   - `/news` - Browse news by source
   - `/search bitcoin` - Search for specific topics
   - `/sources` - View all available sources
   - `/help` - Show help message

## 📦 Alternative: Run Without Docker

If you prefer not to use Docker:

```bash
# Install dependencies
uv pip install python-telegram-bot feedparser

# Run the bot
python telegram_bot.py
```

## 🔧 Configuration

### Add More News Sources

Edit `src/source/newsSourceFetcher.py` and add to the `RSS_FEEDS` dictionary:

```python
"source_name": {
    "general": "https://example.com/rss.xml",
    "technology": "https://example.com/tech/rss.xml",
}
```

### Customize Bot Behavior

Edit `telegram_bot.py`:

- Modify `max_articles` in fetch calls
- Change button layouts
- Add new commands

## 🌐 Deploy to Cloud

### Deploy to DigitalOcean/AWS/GCP

1. **Create a server** (smallest instance is fine)
2. **Install Docker**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. **Clone your repo**:
   ```bash
   git clone your-repo-url
   cd news-bot
   ```
4. **Setup environment**:
   ```bash
   nano .env  # Add your tokens
   ```
5. **Run the bot**:
   ```bash
   docker-compose up -d
   ```

### Deploy to Railway.app (Free Tier)

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `HF_TOKEN`
5. Railway will auto-deploy!

### Deploy to Render.com (Free Tier)

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Background Worker"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install uv && uv pip install --system -r requirements.txt`
   - **Start Command**: `python telegram_bot.py`
5. Add environment variables
6. Deploy!

## 📊 Monitoring

### View Logs

```bash
# With Docker Compose
docker-compose logs -f newsbot

# Follow last 100 lines
docker-compose logs -f --tail=100 newsbot

# Check if bot is running
docker-compose ps
```

### Health Check

The bot includes a health check endpoint. Check status:

```bash
docker inspect telegram-news-bot --format='{{.State.Health.Status}}'
```

## 🛠️ Troubleshooting

### Bot Not Responding

1. **Check logs**:

   ```bash
   docker-compose logs newsbot
   ```

2. **Verify token**:

   ```bash
   echo $TELEGRAM_BOT_TOKEN
   ```

3. **Restart bot**:
   ```bash
   docker-compose restart
   ```

### "No articles found" Error

- RSS feeds can be temporarily down
- Try a different source or category
- Check if the feed URL is still valid

### AI Summaries Not Working

- Ensure `HF_TOKEN` is set in `.env`
- Check HuggingFace API status
- The bot works fine without AI summaries (uses RSS summaries)

## 🔒 Security Best Practices

1. **Never commit `.env` file**

   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use environment variables** for all secrets

3. **Keep Docker image updated**:

   ```bash
   docker-compose pull
   docker-compose up -d
   ```

4. **Limit bot access** via Telegram's BotFather settings

## 📈 Scaling

### Multiple Instances

To run multiple bots (different tokens):

```yaml
# docker-compose.yml
services:
  newsbot1:
    build: .
    env_file: .env.bot1

  newsbot2:
    build: .
    env_file: .env.bot2
```

### Rate Limiting

The bot uses Telegram's default rate limits. For heavy usage:

- Add request throttling
- Cache frequently requested content
- Use a database for state management

## 📝 Maintenance

### Update Dependencies

```bash
# Rebuild with latest packages
docker-compose build --no-cache
docker-compose up -d
```

### Backup Configuration

```bash
# Backup .env file
cp .env .env.backup

# Export Docker image
docker save telegram-news-bot > newsbot.tar
```

## 💡 Tips

- Start with a few sources, add more as needed
- RSS feeds are more reliable than web scraping
- Monitor logs for errors and user feedback
- Consider adding analytics to track popular topics

## 🆘 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Test RSS feeds manually
4. Check Telegram Bot API status

## 📜 License

MIT License - Feel free to modify and distribute!
