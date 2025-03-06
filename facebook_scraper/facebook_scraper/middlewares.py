from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import credentials  # Import credentials

class SeleniumMiddleware:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(service=Service("C:/Users/moham/facebook_scraper/facebook_scraper/driver/chromedriver-win64/chromedriver.exe"), options=chrome_options)
        self.login_to_facebook()

    def login_to_facebook(self):
        """Logs into Facebook using stored credentials."""
        self.driver.get("https://www.facebook.com/login")
        time.sleep(3)

        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "pass")
        login_button = self.driver.find_element(By.NAME, "login")

        email_input.send_keys(credentials.FACEBOOK_EMAIL)
        password_input.send_keys(credentials.FACEBOOK_PASSWORD)
        login_button.click()

        time.sleep(5)  # Wait for login to complete

    def scroll_down(self):
        """Scrolls down the page to load more posts."""
        for _ in range(5):  # Adjust for more scrolling
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(5)

        self.scroll_down()  # Scroll down to load more posts

        return HtmlResponse(url=request.url, body=self.driver.page_source, encoding='utf-8', request=request)
