#!/usr/bin/env python3
"""
Admin tool to manage subscriptions
Use this to manually upgrade users after they subscribe via Buy Me a Coffee
"""

import sys
from src.subscription.subscription_manager import SubscriptionManager


def main():
    manager = SubscriptionManager()

    print("=" * 60)
    print("  📰 News Bot - Subscription Admin Tool")
    print("=" * 60)
    print()

    while True:
        print("\nOptions:")
        print("  1. Upgrade user to Premium")
        print("  2. View user status")
        print("  3. List all premium users")
        print("  4. Remove premium access")
        print("  5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            try:
                user_id = int(input("Enter Telegram User ID: ").strip())
                months = int(input("Duration in months (default 1): ").strip() or "1")

                confirm = input(
                    f"\nUpgrade user {user_id} to Premium for {months} month(s)? (y/n): "
                ).lower()

                if confirm == "y":
                    manager.upgrade_to_premium(user_id, months)
                    print(
                        f"✅ User {user_id} upgraded to Premium for {months} month(s)!"
                    )
                else:
                    print("❌ Cancelled")

            except ValueError:
                print("❌ Invalid input")

        elif choice == "2":
            try:
                user_id = int(input("Enter Telegram User ID: ").strip())
                limits = manager.get_limits(user_id)

                print(f"\n{'=' * 60}")
                print(f"User ID: {user_id}")
                print(f"Tier: {limits['tier'].upper()}")
                print(
                    f"Daily Usage: {limits['current_usage']}/{limits['daily_articles']}"
                )

                if limits["tier"] == "premium":
                    print(f"Expires: {limits['expires_at']}")

                print(f"{'=' * 60}")

            except ValueError:
                print("❌ Invalid user ID")

        elif choice == "3":
            print(f"\n{'=' * 60}")
            print("Premium Users:")
            print(f"{'=' * 60}")

            count = 0
            for user_id, data in manager.subscriptions.items():
                if data.get("tier") == "premium":
                    count += 1
                    print(f"User ID: {user_id}")
                    print(f"  Expires: {data.get('expires_at', 'N/A')}")
                    print(f"  Upgraded: {data.get('upgraded_at', 'N/A')}")
                    print()

            if count == 0:
                print("No premium users found")
            else:
                print(f"Total premium users: {count}")

            print(f"{'=' * 60}")

        elif choice == "4":
            try:
                user_id = int(input("Enter Telegram User ID: ").strip())
                user_id_str = str(user_id)

                if user_id_str in manager.subscriptions:
                    confirm = input(
                        f"\nRemove premium access for user {user_id}? (y/n): "
                    ).lower()

                    if confirm == "y":
                        manager.subscriptions[user_id_str]["tier"] = "free"
                        manager._save_subscriptions()
                        print(f"✅ Premium access removed for user {user_id}")
                    else:
                        print("❌ Cancelled")
                else:
                    print(f"❌ User {user_id} not found in database")

            except ValueError:
                print("❌ Invalid user ID")

        elif choice == "5":
            print("\n👋 Goodbye!")
            break

        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
