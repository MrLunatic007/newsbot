# 🚀 Quick Reference - Subscription System

## 📋 File Structure
```
news-bot/
├── telegram_bot.py              # Main bot with subscription
├── admin_tool.py                # Manage subscriptions
├── setup_subscription.sh        # Setup script
├── data/
│   └── subscriptions.json       # User database (auto-created)
└── src/
    └── subscription/
        └── subscription_manager.py
```

## 🎯 Quick Commands

### Start the Bot
```bash
./start_bot.sh
```

### Manage Subscriptions
```bash
python admin_tool.py
```

### Upgrade a User
```bash
python admin_tool.py
# Option 1, enter User ID and months
```

### Check Subscription Stats
```bash
python -c "
from src.subscription.subscription_manager import SubscriptionManager
m = SubscriptionManager()
print(f'Total users: {len(m.subscriptions)}')
premium = sum(1 for u in m.subscriptions.values() if u.get('tier') == 'premium')
print(f'Premium users: {premium}')
"
```

## 💰 Pricing
- **Free**: 10 articles/day, 2 sources
- **Premium**: $3/month or $30/year
  - 100 articles/day
  - All sources (8+)
  - AI summaries
  - All categories

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome + tier info |
| `/status` | Subscription status |
| `/premium` | Upgrade info |
| `/news` | Browse news |
| `/search` | Search articles |
| `/sources` | View sources |

## 🔧 Admin Tasks

### Activate Premium (Manual)
1. User subscribes on Buy Me a Coffee
2. User sends you their Telegram ID
3. Run: `python admin_tool.py`
4. Select option 1
5. Enter User ID and duration

### Find User's Telegram ID
Users message @userinfobot on Telegram

### Backup Subscriptions
```bash
cp data/subscriptions.json backup_$(date +%Y%m%d).json
```

### View All Premium Users
```bash
python admin_tool.py
# Option 3
```

## 🎨 Customize Limits

Edit `subscription_manager.py`:

```python
self.LIMITS = {
    "free": {
        "daily_articles": 10,      # Change this
        "sources": ["bbc", "guardian"],  # Add sources
        "ai_summaries": False,
    },
    "premium": {
        "daily_articles": 100,     # Change this
        "sources": "all",
        "ai_summaries": True,
    }
}
```

## 📊 Feature Comparison

| Feature | Free | Premium |
|---------|------|---------|
| Daily Articles | 10 | 100 |
| Sources | BBC, Guardian | All (8+) |
| Categories | 2 | All |
| AI Summaries | ❌ | ✅ |
| Search Results | 3 | 10 |

## 🔗 Payment Link
https://buymeacoffee.com/mrlunatic

Update in `telegram_bot.py`:
```python
self.PAYMENT_LINK = "https://buymeacoffee.com/mrlunatic"
```

## 🐛 Troubleshooting

**Bot not respecting limits?**
```bash
docker-compose restart
```

**User stuck on free tier?**
```bash
python admin_tool.py
# Option 2, check user status
# Option 1, upgrade if needed
```

**Subscription data lost?**
```bash
# Restore from backup
cp backup_20251126.json data/subscriptions.json
docker-compose restart
```

## 📈 Growth Tips

1. **Trial Period**: Offer 7-day free trial
2. **Referral**: 1 free month for referrals
3. **Content**: Weekly exclusive digest
4. **Social Proof**: "Join 100+ premium users"
5. **Limited Offer**: "50% off this week only"

## 🎯 Conversion Tactics

- Show upgrade prompt at daily limit
- Highlight locked sources with 🔒
- Display premium benefits in /status
- Add "Upgrade" button to errors
- Send reminder at 80% daily limit

## 📞 Support Template

**When user subscribes:**
```
Thanks for subscribing! 🎉

To activate Premium:
1. Note your Telegram User ID: [Get from @userinfobot]
2. Send me:
   - User ID
   - Subscription email
   - Payment confirmation

I'll activate within 24 hours!
```

## 🔐 Security

- Subscriptions stored in `data/subscriptions.json`
- File permissions: 600 (read/write owner only)
- Docker volume: persistent storage
- No passwords stored (using Telegram ID)

## 📝 To-Do for Production

- [ ] Set up automated payments
- [ ] Add renewal reminders
- [ ] Create support chat
- [ ] Add analytics dashboard
- [ ] Implement webhooks
- [ ] Add refund system
- [ ] Create email notifications
- [ ] Add usage reports

## 🚨 Important Notes

1. **Backup regularly**: `data/subscriptions.json`
2. **Monitor expiries**: Check admin tool weekly
3. **Support response**: Within 24 hours
4. **Payment processing**: Manual for now
5. **Refund window**: 7 days recommended

## 📚 Documentation

- `SUBSCRIPTION_GUIDE.md` - Full guide
- `DEPLOYMENT.md` - Deployment steps
- `CHECKLIST.md` - Setup checklist

---

**Quick Help:**
- Bot issues: Check logs with `docker-compose logs -f`
- Subscription issues: Use `admin_tool.py`
- Payment issues: Check Buy Me a Coffee dashboard
