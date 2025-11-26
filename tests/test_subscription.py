#!/usr/bin/env python3
"""
Test script to verify subscription system is working correctly
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.subscription.subscription_manager import SubscriptionManager
        print("  ✅ subscription_manager imported")
    except ImportError as e:
        print(f"  ❌ Failed to import subscription_manager: {e}")
        return False
    
    try:
        from src.source.newsSourceFetcher import NewsSourceFetcher
        print("  ✅ newsSourceFetcher imported")
    except ImportError as e:
        print(f"  ❌ Failed to import newsSourceFetcher: {e}")
        return False
    
    return True

def test_directories():
    """Test that required directories exist"""
    print("\n📁 Testing directories...")
    
    required_dirs = [
        "src/subscription",
        "data",
        "logs"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path} exists")
        else:
            print(f"  ❌ {dir_path} missing")
            all_exist = False
    
    return all_exist

def test_subscription_manager():
    """Test subscription manager functionality"""
    print("\n⚙️  Testing subscription manager...")
    
    try:
        from src.subscription.subscription_manager import SubscriptionManager
        
        manager = SubscriptionManager()
        print("  ✅ SubscriptionManager initialized")
        
        # Test free tier
        test_user_id = 999999999
        tier = manager.get_user_tier(test_user_id)
        if tier == "free":
            print("  ✅ Default tier is 'free'")
        else:
            print(f"  ❌ Expected 'free', got '{tier}'")
            return False
        
        # Test upgrade
        manager.upgrade_to_premium(test_user_id, 1)
        tier = manager.get_user_tier(test_user_id)
        if tier == "premium":
            print("  ✅ Upgrade to premium works")
        else:
            print(f"  ❌ Expected 'premium', got '{tier}'")
            return False
        
        # Test limits
        limits = manager.get_limits(test_user_id)
        if limits['tier'] == 'premium':
            print("  ✅ get_limits() works")
        else:
            print("  ❌ get_limits() failed")
            return False
        
        # Clean up test user
        if str(test_user_id) in manager.subscriptions:
            del manager.subscriptions[str(test_user_id)]
            manager._save_subscriptions()
        
        print("  ✅ All subscription manager tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Subscription manager test failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n🔐 Testing environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    hf_token = os.getenv("HF_TOKEN")
    
    if telegram_token:
        print("  ✅ TELEGRAM_BOT_TOKEN is set")
    else:
        print("  ❌ TELEGRAM_BOT_TOKEN is missing")
        print("     Add it to your .env file")
    
    if hf_token:
        print("  ✅ HF_TOKEN is set")
    else:
        print("  ⚠️  HF_TOKEN is missing (optional)")
        print("     AI summaries won't work without it")
    
    return bool(telegram_token)

def test_database():
    """Test database file creation"""
    print("\n💾 Testing database...")
    
    try:
        from src.subscription.subscription_manager import SubscriptionManager
        
        manager = SubscriptionManager()
        db_path = Path("data/subscriptions.json")
        
        if db_path.exists():
            print(f"  ✅ Database file created at {db_path}")
            
            # Check if writable
            test_user = 888888888
            manager.get_user_tier(test_user)
            manager._save_subscriptions()
            print("  ✅ Database is writable")
            
            # Clean up
            if str(test_user) in manager.subscriptions:
                del manager.subscriptions[str(test_user)]
                manager._save_subscriptions()
            
            return True
        else:
            print(f"  ❌ Database file not created")
            return False
            
    except Exception as e:
        print(f"  ❌ Database test failed: {e}")
        return False

def test_admin_tool():
    """Test admin tool exists and is executable"""
    print("\n🛠️  Testing admin tool...")
    
    admin_path = Path("admin_tool.py")
    if admin_path.exists():
        print("  ✅ admin_tool.py exists")
        
        if os.access(admin_path, os.X_OK):
            print("  ✅ admin_tool.py is executable")
        else:
            print("  ⚠️  admin_tool.py not executable")
            print("     Run: chmod +x admin_tool.py")
        
        return True
    else:
        print("  ❌ admin_tool.py not found")
        return False

def main():
    print("=" * 60)
    print("  🧪 Subscription System Test Suite")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Directories": test_directories(),
        "Environment": test_environment(),
        "Subscription Manager": test_subscription_manager(),
        "Database": test_database(),
        "Admin Tool": test_admin_tool(),
    }
    
    print("\n" + "=" * 60)
    print("  📊 Test Results")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("  🎉 All tests passed! System is ready.")
        print("=" * 60)
        print("\n  Next steps:")
        print("  1. Run: ./start_bot.sh")
        print("  2. Test bot with /start in Telegram")
        print("  3. Use admin_tool.py to manage subscriptions")
        return 0
    else:
        print("  ⚠️  Some tests failed. Please fix the issues above.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
