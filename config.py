import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the application"""

    # Bot configuration
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    #ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0"))  # Default to 0 if not set
    ADMIN_IDS: list = [int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS", "").split(',') if admin_id.strip().isdigit()]


ADMIN_IDS = Config.ADMIN_IDS
BOT_TOKEN = Config.BOT_TOKEN

# Validate critical configurations
if not Config.BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required in environment variables")

if __name__ == "__main__":
    print("=== Configuration Verification ===")
    print(f"Bot token: {'*****' if Config.BOT_TOKEN else 'Not set'}")
    print(f"Admin ID: {Config.ADMIN_IDS}")