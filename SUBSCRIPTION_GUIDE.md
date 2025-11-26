# 💰 Subscription System Guide

## Overview

Your News Bot now has a two-tier subscription system:

- **Free Tier**: Limited access (10 articles/day, 2 sources)
- **Premium Tier**: Full access (100 articles/day, all sources, AI summaries)

## Features by Tier

### 📱 Free Tier

- ✅ 10 articles per day
- ✅ BBC & Guardian sources
- ✅ General & World categories
- ✅ 3 search results
- ❌ AI summaries
- ❌ Premium sources (TechCrunch, Wired, etc.)

### 🌟 Premium Tier ($3/month or $30/year)

- ✅ 100 articles per day
- ✅ ALL news sources (8+ sources)
- ✅ ALL categories
- ✅ AI-powered summaries
- ✅ 10 search results
- ✅ Priority support

## Setup Instructions

### 1. File Structure

Create these directories:

```bash
mkdir -p src/subscription
mkdir -p data
```

Add the subscription manager:

```bash
# Save subscription_manager.py to:
src/subscription/subscription_manager.py

# Save admin tool to root:
admin_tool.py
```

### 2. Payment Integration

The bot uses Buy Me a Coffee for payments:

- Link: https://buymeacoffee.com/mrlunatic
- Users click "Subscribe Now" button in bot
- After payment, they contact you for activation

### 3. Manual Activation Process

When a user subscribes:

1. **User subscribes** on Buy Me a Coffee
2. **User contacts you** via Telegram with:
   - Their Telegram username
   - Subscription email
   - Payment confirmation

3. **You activate** their account using admin tool:

```bash
python admin_tool.py

# Select option 1: Upgrade user to Premium
# Enter their Telegram User ID
# Enter duration (1 for monthly, 12 for yearly)
```

4. **User gets instant access** to all premium features

### 4. Find User's Telegram ID

Users can find their ID by:

1. Messaging @userinfobot on Telegram
2. It will reply with their User ID

Or you can add this to your bot:

```python
# In start command, show user their ID
user_id = update.effective_user.id
await update.message.reply_text(f"Your User ID: {user_id}")
```

## Admin Tool Usage

Run the admin tool:

```bash
python admin_tool.py
```

### Available Options:

**1. Upgrade user to Premium**

- Enter Telegram User ID
- Enter duration in months (1-12)
- Confirms and activates immediately

**2. View user status**

- Check any user's subscription status
- View usage stats
- See expiry date

**3. List all premium users**

- See all active premium subscribers
- View expiration dates
- Useful for renewal reminders

**4. Remove premium access**

- Downgrade user to free tier
- Use for refunds or violations

## Bot Commands for Users

### Basic Commands

- `/start` - Welcome message with tier info
- `/status` - View subscription status and usage
- `/premium` - See premium benefits and subscribe
- `/news` - Browse news (respects tier limits)
- `/search` - Search articles (limited by tier)
- `/sources` - View available sources

### Premium Features Access

**Free tier users see:**

- 🔒 locked sources
- 🔒 locked categories
- Upgrade prompts
- Daily limit warnings

**Premium users see:**

- ✅ All sources unlocked
- ✅ All categories unlocked
- Usage stats (e.g., 15/100 today)
- Expiry date

## Automated Payments (Optional Future Enhancement)

To automate the subscription process, you could:

### Option 1: Buy Me a Coffee Webhooks

- Set up webhooks in Buy Me a Coffee settings
- Receive notifications when users subscribe
- Auto-activate premium via API

### Option 2: Stripe Integration

```python
# Install stripe
pip install stripe

# Add Stripe checkout
# Auto-activate on successful payment
```

### Option 3: Telegram Stars (Native Payments)

- Use Telegram's built-in payment system
- No external payment processor needed
- Handle via bot API

## Managing Subscriptions

### Check Subscription Database

The subscription data is stored in `data/subscriptions.json`:

```json
{
  "123456789": {
    "tier": "premium",
    "upgraded_at": "2025-11-26T10:00:00",
    "expires_at": "2025-12-26T10:00:00",
    "months": 1,
    "daily_count": 5,
    "last_reset": "2025-11-26"
  }
}
```

### Backup Subscriptions

```bash
# Backup regularly
cp data/subscriptions.json data/subscriptions_backup_$(date +%Y%m%d).json
```

### Restore from Backup

```bash
# Restore if needed
cp data/subscriptions_backup_20251126.json data/subscriptions.json
```

## Renewal Reminders

To send renewal reminders, create a script:

```python
from datetime import datetime, timedelta
from subscription_manager import SubscriptionManager

manager = SubscriptionManager()

# Check for expiring subscriptions (within 7 days)
for user_id, data in manager.subscriptions.items():
    if data['tier'] == 'premium':
        expiry = datetime.fromisoformat(data['expires_at'])
        days_left = (expiry - datetime.now()).days

        if 0 < days_left <= 7:
            print(f"User {user_id} expires in {days_left} days")
            # Send reminder via bot
```

## Pricing Recommendations

### Monthly: $3

- Competitive with news apps
- Low barrier to entry
- Good for testing

### Yearly: $30 (17% discount)

- Better for committed users
- Reduces churn
- More predictable revenue

### Consider offering:

- 🎓 Student discount (50% off)
- 🎁 Referral bonus (1 free month)
- 💝 Lifetime deal ($99 one-time)

## Marketing Tips

### In-Bot Promotions

1. Show premium features in action
2. "Unlock 8 more sources" CTAs
3. Daily limit reached → upgrade prompt
4. Social proof ("Join 500+ premium users")

### Communication

- Weekly newsletter with exclusive content
- Premium-only features (e.g., daily digest)
- Early access to new sources
- Custom alerts/notifications

### Limited Time Offers

- Launch discount (50% off first month)
- Holiday sales (Black Friday, etc.)
- Referral program rewards

## Legal Considerations

### Terms of Service

Create a simple ToS covering:

- Subscription terms
- Refund policy (e.g., 7-day money back)
- Data usage
- Service availability

### Privacy Policy

Cover:

- What data you collect (Telegram ID, usage stats)
- How you store it (locally, encrypted)
- No selling to third parties

### Refund Policy

Recommend:

- 7-day full refund, no questions
- Pro-rated refunds after 7 days
- Refunds via original payment method

## Support

### Common User Questions

**Q: How do I activate premium after paying?**
A: Send your Telegram username and payment email to @YourSupportBot

**Q: Can I cancel anytime?**
A: Yes, just stop the subscription on Buy Me a Coffee

**Q: Do I get a refund if I cancel?**
A: Yes, within 7 days. After that, access continues until expiry.

**Q: What payment methods do you accept?**
A: Credit card, PayPal via Buy Me a Coffee

## Monitoring & Analytics

Track these metrics:

- Conversion rate (free → premium)
- Daily active users (free vs premium)
- Churn rate
- Most popular features
- Revenue (MRR, ARR)

```bash
# Simple analytics query
python -c "
from subscription_manager import SubscriptionManager
m = SubscriptionManager()
premium = sum(1 for u in m.subscriptions.values() if u.get('tier') == 'premium')
total = len(m.subscriptions)
print(f'Premium: {premium}/{total} ({premium/total*100:.1f}%)')
"
```

## Troubleshooting

### User can't access premium features after payment

1. Check their user ID is correct
2. Verify subscription in admin tool
3. Check expiry date hasn't passed
4. Restart bot: `docker-compose restart`

### Subscription data lost

1. Restore from backup
2. Check file permissions
3. Verify Docker volume mount

### Users reporting wrong tier

1. Clear bot cache (restart)
2. Check subscription data file
3. Verify expiry dates

## Scaling Considerations

### For 100+ users:

- Move to PostgreSQL database
- Add Redis for caching
- Implement proper webhook handling
- Add automated billing

### For 1000+ users:

- Use Stripe/Paddle for payments
- Add customer portal
- Implement usage-based pricing
- Add team/business plans

## Next Steps

1. ✅ Deploy bot with subscription system
2. 📢 Announce premium features
3. 🎯 Set up Buy Me a Coffee page
4. 💬 Create support channel
5. 📊 Monitor conversions
6. 🔄 Iterate based on feedback

---

**Need help?** Create an issue or contact support!
