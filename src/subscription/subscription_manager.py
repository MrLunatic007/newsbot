"""
Subscription Manager - Handles free/premium tiers
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from pathlib import Path


class SubscriptionManager:
    def __init__(self, db_path: str = "data/subscriptions.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.subscriptions = self._load_subscriptions()

        # Feature limits
        self.LIMITS = {
            "free": {
                "daily_articles": 10,
                "sources": ["bbc", "guardian"],
                "ai_summaries": False,
                "search_results": 3,
                "categories": ["general", "world"],
            },
            "premium": {
                "daily_articles": 100,
                "sources": "all",  # Access to all sources
                "ai_summaries": True,
                "search_results": 10,
                "categories": "all",
            },
        }

    def _load_subscriptions(self) -> Dict:
        """Load subscriptions from JSON file"""
        if self.db_path.exists():
            try:
                with open(self.db_path, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_subscriptions(self):
        """Save subscriptions to JSON file"""
        with open(self.db_path, "w") as f:
            json.dump(self.subscriptions, f, indent=2)

    def get_user_tier(self, user_id: int) -> str:
        """Get user's subscription tier"""
        user_id = str(user_id)

        if user_id not in self.subscriptions:
            return "free"

        user_data = self.subscriptions[user_id]

        # Check if premium subscription is still valid
        if user_data.get("tier") == "premium":
            expiry = datetime.fromisoformat(user_data.get("expires_at", "2000-01-01"))
            if datetime.now() < expiry:
                return "premium"
            else:
                # Subscription expired
                self.subscriptions[user_id]["tier"] = "free"
                self._save_subscriptions()

        return "free"

    def upgrade_to_premium(self, user_id: int, months: int = 1) -> bool:
        """Upgrade user to premium"""
        user_id = str(user_id)

        expires_at = datetime.now() + timedelta(days=30 * months)

        self.subscriptions[user_id] = {
            "tier": "premium",
            "upgraded_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "months": months,
        }

        self._save_subscriptions()
        return True

    def get_user_stats(self, user_id: int) -> Dict:
        """Get user's usage statistics"""
        user_id = str(user_id)

        if user_id not in self.subscriptions:
            self.subscriptions[user_id] = {
                "tier": "free",
                "daily_count": 0,
                "last_reset": datetime.now().date().isoformat(),
            }
            self._save_subscriptions()

        user_data = self.subscriptions[user_id]

        # Reset daily count if it's a new day
        last_reset = user_data.get("last_reset", datetime.now().date().isoformat())
        if last_reset != datetime.now().date().isoformat():
            user_data["daily_count"] = 0
            user_data["last_reset"] = datetime.now().date().isoformat()
            self._save_subscriptions()

        return user_data

    def increment_usage(self, user_id: int):
        """Increment user's daily article count"""
        user_id = str(user_id)
        stats = self.get_user_stats(user_id)
        stats["daily_count"] = stats.get("daily_count", 0) + 1
        self.subscriptions[user_id] = stats
        self._save_subscriptions()

    def can_access_feature(self, user_id: int, feature: str, value: any = None) -> bool:
        """Check if user can access a feature"""
        tier = self.get_user_tier(user_id)
        limits = self.LIMITS[tier]

        if feature == "source":
            if limits["sources"] == "all":
                return True
            return value in limits["sources"]

        elif feature == "ai_summaries":
            return limits["ai_summaries"]

        elif feature == "category":
            if limits["categories"] == "all":
                return True
            return value in limits["categories"]

        elif feature == "daily_limit":
            stats = self.get_user_stats(user_id)
            return stats.get("daily_count", 0) < limits["daily_articles"]

        elif feature == "search_results":
            return limits["search_results"]

        return False

    def get_limits(self, user_id: int) -> Dict:
        """Get user's current limits"""
        tier = self.get_user_tier(user_id)
        stats = self.get_user_stats(user_id)
        limits = self.LIMITS[tier].copy()
        limits["current_usage"] = stats.get("daily_count", 0)
        limits["tier"] = tier

        if tier == "premium":
            user_data = self.subscriptions.get(str(user_id), {})
            limits["expires_at"] = user_data.get("expires_at", "N/A")

        return limits

    def get_available_sources(self, user_id: int) -> list:
        """Get list of sources user can access"""
        tier = self.get_user_tier(user_id)

        if self.LIMITS[tier]["sources"] == "all":
            return [
                "bbc",
                "guardian",
                "nytimes",
                "techcrunch",
                "wired",
                "arstechnica",
                "reuters",
                "aljazeera",
            ]

        return self.LIMITS[tier]["sources"]

    def get_available_categories(self, user_id: int) -> list:
        """Get list of categories user can access"""
        tier = self.get_user_tier(user_id)

        if self.LIMITS[tier]["categories"] == "all":
            return "all"

        return self.LIMITS[tier]["categories"]
