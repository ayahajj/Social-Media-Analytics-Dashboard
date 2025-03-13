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
POST_COUNT_TO_SCRAPE_PER_PLATFORM = 5

#SCRAPE_PLATFORM_FACEBOOK_USER = "aljazeerachannel"
#SCRAPE_PLATFORM_YOUTUBE_USER = "aljazeera"
#SCRAPE_PLATFORM_INSTAGRAM_USER = "aljazeera"

SCRAPE_PLATFORM_FACEBOOK_USER = "aljazeera"
SCRAPE_PLATFORM_YOUTUBE_USER = "aljazeeraenglish"
SCRAPE_PLATFORM_INSTAGRAM_USER = "aljazeeraenglish"

IS_SIMULATE_SCRAPE = True

IS_FACEBOOK_SCRAPE = True
IS_YOUTUBE_SCRAPE = True
IS_INSTAGRAM_SCRAPE = True

#################################
# Dashboard Configurations
#################################

DASHBOARD_REFRESH_INTERVAL_MIN = 0.5          # mintutes interval to refresh the dashboard
SCRAPE_DATA_INTERVAL_MIN = 120              # mintutes interval to make a data scrape

POSTS_DATA_FILE_PATH = r"social_media_scraper\Final_Output\social_media_posts.xlsx"                         # File containing the posts data to show on dashboard
SCRAPE_THREAD_LOCK_FILE = r"social_media_scraper\Final_Output\scraper.lock"                                 # File to track running status of scraper
LAST_SUCCESSFUL_SCRAPE_TIME_FILE  = r"social_media_scraper\Final_Output\last_updated.txt"                   # File containing time interval for the last scrape made time
SCRAPE_PROCESS_EXECUTE_PATH = r"C:\Users\moham\Social Media Analytics Dashboard\social_media_scraper"       # Is the Path of the process to invoke scraper pipline

