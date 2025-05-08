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

# Facebook Login Link
FACEBOOK_LOGIN_PAGE = "https://www.facebook.com/login/"

# Facebook Login Credentials
FACEBOOK_EMAIL = "mohammad.sobbahi@gmail.com"   #"mohammad.sobbahi2001@gmail.com"
FACEBOOK_PASSWORD = "Moh@mmad"  #"P@ssw0rd1234"

# Instagram Login Link
INSTAGRAM_LOGIN_PAGE = "https://www.instagram.com/accounts/login/"

# Instagram Login Credentials
INSTAGRAM_USERNAME = "test.mohammad2001"   #email=  mohammad.sobbahi2001@gmail.com
INSTAGRAM_PASSWORD = "P@ssw0rd1234"

# Posts To Scrape Count
POST_COUNT_TO_SCRAPE_PER_PLATFORM = 100

# Users per each paltform
SCRAPE_PLATFORM_FACEBOOK_USER = "aljazeera"
SCRAPE_PLATFORM_YOUTUBE_USER = "aljazeeraenglish"
SCRAPE_PLATFORM_INSTAGRAM_USER = "aljazeeraenglish"

# Whether to simulate scraper or not
IS_SIMULATE_SCRAPE = False

# which platfrom to scrape
IS_FACEBOOK_SCRAPE = True
IS_YOUTUBE_SCRAPE = True
IS_INSTAGRAM_SCRAPE = True

#################################
# Dashboard Configurations
#################################
 
# mintutes interval to refresh the dashboard
DASHBOARD_REFRESH_INTERVAL_MIN = 5

# mintutes interval to make a data scrape run
SCRAPE_DATA_INTERVAL_MIN = 30

# File containing the posts data to show on dashboard
POSTS_DATA_FILE_PATH = r"social_media_scraper\Final_Output\social_media_posts.xlsx"

# File to track running status of scraper
SCRAPE_THREAD_LOCK_FILE = r"social_media_scraper\Final_Output\scraper.lock"  

# File containing time interval for the last scrape made time
LAST_SUCCESSFUL_SCRAPE_TIME_FILE  = r"social_media_scraper\Final_Output\last_updated.txt"      

# Is the Path of the process to invoke scraper pipline
import os

BASE_DIR = os.getcwd()
SCRAPE_PROCESS_EXECUTE_PATH = os.path.join(BASE_DIR, "social_media_scraper")

