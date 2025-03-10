#################################
# Scraper Configurations
#################################

CHROME_WEB_DRIVER_PATH = r"\social_media_scraper\driver\chromedriver-win64\chromedriver.exe"

POSTS_MODEL = [
            "user_id", 
            "platform", 
            "post_id", 
            "date", 
            "likes", 
            "comments", 
            "shares", 
            "post_text", 
            "post_origin_text", 
            "date_scraped", 
            "views", 
            "followers", 
            "country", 
            "content_type", 
            "sentiment_score"
        ]

# Facebook
FACEBOOK_LOGIN_PAGE = "https://www.facebook.com/login/"

FACEBOOK_EMAIL = "mohammad.sobbahi@gmail.com"   #"mohammad.sobbahi2001@gmail.com"
FACEBOOK_PASSWORD = "Moh@mmad"  #"P@ssw0rd1234"

# Instagram
INSTAGRAM_LOGIN_PAGE = "https://www.instagram.com/accounts/login/"

INSTAGRAM_USERNAME = "test.mohammad2001"   #email=  mohammad.sobbahi2001@gmail.com
INSTAGRAM_PASSWORD = "P@ssw0rd1234"

# Users To Scrape
POST_COUNT_TO_SCRAPE_PER_PLATFORM = 2
SCRAPE_PLATFORM_FACEBOOK_USER = "aljazeerachannel"
SCRAPE_PLATFORM_YOUTUBE_USER = "aljazeera"
SCRAPE_PLATFORM_INSTAGRAM_USER = "aljazeera"

#################################
# Dashboard Configurations
#################################


