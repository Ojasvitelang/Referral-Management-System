# File paths for JSON storage
USERS_FILE = "data/users.json"
REFERRALS_FILE = "data/referrals.json"
LOGS_FILE = "data/logs.json"

# Points configuration
POINTS_REFERRAL = 50             # Points awarded for submitting a referral
POINTS_CONVERSION = 250          # Base points when referral converts
REVENUE_BONUS_RATE = 0.01        # Additional % of admission fee

# Tier thresholds (auto-calculated weekly)
TIERS = [
    {"name": "Diamond", "min_points": 50000},
    {"name": "Gold", "min_points": 25000},
    {"name": "Silver", "min_points": 10000},
    {"name": "Bronze", "min_points": 0}
]

# Session timeout (in minutes)
SESSION_TIMEOUT_MINUTES = 15

# Date format for consistency
DATE_FORMAT = "%Y-%m-%d"
