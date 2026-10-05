import tweepy
from typing import Optional
from configs.app_config import (X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET, X_BEARER_TOKEN)
from utilities.utils import log_message

async def create_x_client_v2() -> Optional[tweepy.Client]:
    """Create Tweepy V2 Client (OAuth 2.0 Bearer Token for Free tier)."""
    try:
        if not X_BEARER_TOKEN:
            raise ValueError("X_BEARER_TOKEN not set in config")
        client = tweepy.Client(bearer_token=X_BEARER_TOKEN, consumer_key=X_API_KEY, consumer_secret=X_API_SECRET, 
                               access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)
        me = client.get_me()
        if not me.data:
            raise ValueError("Auth failed: No user data")
        # log_message(f"X V2 client initialized for @{me.data.username}")
        return client
    except Exception as exc:
        log_message(f"X V2 client init error: {exc}")
        return None

async def post_price_update_to_x(message: str) -> bool:
    """Post tweet using V2 endpoint (/2/tweets) — works on Free tier."""
    client = await create_x_client_v2()
    if not client:
        return False

    tweet = message[:277] + "…" if len(message) > 280 else message

    try:
        response = client.create_tweet(text=tweet)
        if response.data and 'id' in response.data:
            tweet_id = response.data['id']
            log_message(f"Tweet posted (ID: {tweet_id}) ({len(tweet)} chars): {tweet[:60]}…")
            return True
        else:
            log_message("X V2 post response empty or missing 'id'")
            return False
    except tweepy.Forbidden as exc:
        log_message(f"X V2 post forbidden: {exc}")
        return False
    except tweepy.TweepyException as exc:
        log_message(f"X V2 post error: {exc}")
        return False
    except Exception as exc:
        log_message(f"Unexpected X V2 error: {exc}")
        return False
