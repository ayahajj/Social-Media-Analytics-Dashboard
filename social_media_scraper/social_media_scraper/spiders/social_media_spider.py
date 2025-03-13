import uuid
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.service import Service  # Add this import
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from .. import constants
import os

class SocialMediaSpider(scrapy.Spider):
    name = "social_media_spider"

    def __init__(self):
        driver_path = os.getcwd() + constants.CHROME_WEB_DRIVER_PATH        
        self.driver = webdriver.Chrome(service=Service(driver_path))
        self.posts_df = pd.DataFrame(columns=constants.POSTS_MODEL)
        
        self.run_scrape_pipeline()


    def run_scrape_pipeline(self):
        """
        Executes the scraping pipeline for Facebook, YouTube, and Instagram.

        Workflow:
        - Logs into Facebook and scrapes posts from the "aljazeerachannel" page.
        - Scrapes YouTube posts from the "aljazeera" channel.
        - Logs into Instagram and scrapes posts from "aljazeera".
        """
        if constants.IS_FACEBOOK_SCRAPE:
            try:
                self.posts_df = pd.DataFrame(columns=constants.POSTS_MODEL)
                self.login_facebook()
                self.scrape_facebook_posts(constants.SCRAPE_PLATFORM_FACEBOOK_USER, constants.POST_COUNT_TO_SCRAPE_PER_PLATFORM)
                self.save_data("facebook")
            except KeyboardInterrupt:
                print("\n\n","Facebook script stopped manually. Saving data...", "\n\n")
            except Exception as e:
                print( "\n\n",f"Facebook Scraping error occurred: {e}", "\n\n")
            
                
        if constants.IS_YOUTUBE_SCRAPE:
            try:
                self.posts_df = pd.DataFrame(columns=constants.POSTS_MODEL)
                self.scrape_youtube_posts(constants.SCRAPE_PLATFORM_YOUTUBE_USER, constants.POST_COUNT_TO_SCRAPE_PER_PLATFORM)
                self.save_data("youtube")       
            except KeyboardInterrupt:
                print("\n\n","Youtube script stopped manually. Saving data...", "\n\n")
            except Exception as e:
                print( "\n\n",f"Youtube Scraping error occurred: {e}", "\n\n")

   
        if constants.IS_INSTAGRAM_SCRAPE:
            try:
                self.posts_df = pd.DataFrame(columns=constants.POSTS_MODEL)
                self.login_instagram()
                self.scrape_instagram_posts(constants.SCRAPE_PLATFORM_INSTAGRAM_USER, constants.POST_COUNT_TO_SCRAPE_PER_PLATFORM)  
                self.save_data("instagram")                
            except KeyboardInterrupt:
                print("\n\n","Instagram script stopped manually. Saving data...", "\n\n")
            except Exception as e:
                print( "\n\n",f"Instagram Scraping error occurred: {e}", "\n\n")
     
        self.driver.quit()


    def login_facebook(self):
        """
        Logs into Facebook using stored credentials.
        """
        print("\n\n", "Navigating to Facebook Login page...", "\n\n")
        self.driver.get(constants.FACEBOOK_LOGIN_PAGE)
        self.driver.get(constants.FACEBOOK_LOGIN_PAGE)
        time.sleep(5)

        print("\n\n", "Entering Facebook Credentials...", "\n\n")
        email = self.driver.find_element(By.ID, "email")
        email.send_keys(constants.FACEBOOK_EMAIL)
        password = self.driver.find_element(By.ID, "pass")
        password.send_keys(constants.FACEBOOK_PASSWORD)
        password.send_keys(Keys.RETURN)

        print("\n\n", "Waiting for Facebook Login to complete...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))  # Example element
            )
        except Exception as e:
            print("\n\n", "Login failed or took too long:", e, "\n\n")

        time.sleep(10)


    def scrape_facebook_posts(self, facebook_page_name, target_post_count):
        """
        Scrapes posts from a specified Facebook page.
        Parameters:
            facebook_page_name (str): The name of the Facebook page to scrape.
            target_post_count (int): The number of posts to load..
        """
        print("\n\n", f"Navigating to {facebook_page_name} Facebook page...", "\n\n")
        
        user_id = facebook_page_name
        self.driver.get(f"https://www.facebook.com/{facebook_page_name}/")

        print("\n\n", "Waiting for Facebook page to load...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1yztbdb') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'xh8yej3') and contains(@class, 'x1ja2u2z')]"))
            )
            print("\n\n", "Facebook page loaded successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Facebook page did not load properly:", e, "\n\n")
        
        # Extract posts
        posts = self.facebook_scroll_and_scrape(target_post_count)
        
        total_posts = len(posts)  # Get total number of posts
        
        # Print the number of posts found
        print("\n\n", f"Number of Facebook posts found: {len(posts)}", "\n\n")
        time.sleep(5)
        
        # followers at time of scrape       
        try:
            followers = self.driver.find_element(By.XPATH, ".//a[contains(@href, 'https://www.facebook.com/aljazeerachannel/followers/')]").text
        except NoSuchElementException:
            followers = "NA"

        for index, post in enumerate(posts, start=1):
            print("\n\n", f"Facebook Post {index}/{total_posts} ({(index / total_posts) * 100:.2f}%) - Processing Start", "\n\n")
            
            try:
                post_id = str(uuid.uuid4())  # Generate a random UUID

                try:
                    post_likes = post.find_element(By.XPATH, ".//span[contains(@class, 'xt0b8zv') and contains(@class, 'x1jx94hy') and contains(@class, 'xrbpyxo') and contains(@class, 'xl423tq')]").text
                except NoSuchElementException:
                    post_likes = "NA"
                    
                try:
                    post_comments = post.find_elements(By.XPATH, ".//span[contains(@class, 'html-span') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1hl2dhg') and contains(@class, 'x16tdsg8') and contains(@class, 'x1vvkbs') and contains(@class, 'xkrqix3') and contains(@class, 'x1sur9pj')]")
                    post_comments = post_comments[0].text if len(post_comments) > 1 else "NA"
                except NoSuchElementException:
                    post_comments = "NA"

                try:
                    post_shares = post.find_elements(By.XPATH, ".//span[contains(@class, 'html-span') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1hl2dhg') and contains(@class, 'x16tdsg8') and contains(@class, 'x1vvkbs') and contains(@class, 'xkrqix3') and contains(@class, 'x1sur9pj')]")
                    post_shares = post_shares[1].text if len(post_shares) > 1 else "NA"
                except NoSuchElementException:
                    post_shares = "NA"

                try:
                    post_text = post.find_element(By.XPATH, ".//div[contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x1vvkbs') and contains(@class, 'x126k92a')]").text
                except NoSuchElementException:
                    post_text = "NA"

                try:
                    post_date = post.find_element(By.XPATH, ".//span[contains(@class, 'x1rg5ohu') and contains(@class, 'x6ikm8r') and contains(@class, 'x10wlt62') and contains(@class, 'x16dsc37') and contains(@class, 'xt0b8zv')]").text
                except NoSuchElementException:
                    post_date = "NA"

                # Identify Post Type
                post_type = self.get_facebook_post_type(post) if hasattr(self, 'get_facebook_post_type') else "NA"

                print("\n\n", f"Facebook post_text = {post_text}", "\n\n")
                print("\n\n", f"Facebook post_id = {post_id}", "\n\n")
                print("\n\n", f"Facebook post_date = {post_date}", "\n\n")
                print("\n\n", f"Facebook post_likes = {post_likes}", "\n\n")
                print("\n\n", f"Facebook post_comments = {post_comments}", "\n\n")
                print("\n\n", f"Facebook post_shares = {post_shares}", "\n\n")
                print("\n\n", f"Facebook followers = {followers}", "\n\n")
                print("\n\n", f"Facebook post_type = {post_type}", "\n\n")

                # Create a DataFrame from the new row
                new_row = pd.DataFrame([{
                    "user_id": user_id,
                    "platform": "Facebook",
                    "post_id": post_id,
                    "date": "NA",
                    "likes": post_likes,
                    "comments": post_comments,
                    "shares": post_shares,
                    "post_text": post_text,
                    "post_origin_text": post.text,
                    "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "views": "NA",
                    "followers": followers,
                    "country": "NA",
                    "content_type": post_type,
                    "sentiment_score": "NA"
                }])

                # Use pd.concat instead of append
                self.posts_df = pd.concat([self.posts_df, new_row], ignore_index=True)

            except Exception as e:
                print("\n\n", f"Unexpected error scraping Facebook post {post_id}: {e}", "\n\n")
            
            print("\n\n",f"Facebook  Post {index}/{total_posts} - Processing End", "\n\n")
            time.sleep(2)


    def facebook_scroll_and_scrape(self, target_post_count):
        """
        Scrolls the Facebook page and scrapes posts until the target post count is reached,
        or stops if fewer posts are available. Retries if no posts are found.

        :param target_post_count: The number of posts to scrape.
        """
        max_retries=30
        scroll_amount=1000
        retry_count = 0
        
        posts = []
        total_posts = 0

        while True:
            # Scroll the page
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(2)

            # Extract posts
            posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'x1yztbdb') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'x1ja2u2z')]")
            total_posts_old = total_posts
            total_posts = len(posts)

            print(f"\n\nFacebook Posts loaded: {total_posts}/{target_post_count} ({(total_posts / target_post_count) * 100:.2f}%) \n\n")

            # Reset retry counter if posts are found
            if total_posts > total_posts_old:
                retry_count = 0

            # Stop when the target post count is reached
            if total_posts >= target_post_count:
                print("\n\nTarget Facebook post count reached.\n\n")
                return posts[:target_post_count]  # Return only the target number of posts

            # Retry if no posts are found
            if retry_count < max_retries:
                print(f"\n\nNo nFacebook posts found. Retrying ({retry_count + 1}/{max_retries})...\n\n")
                retry_count += 1
                continue  # Try again without increasing scroll count

            # Stop if fewer posts than the target are available
            if total_posts < target_post_count:
                print("\n\nFacebook Stopping: Not enough posts available.\n\n")
                return posts  # Return all available posts

        return posts  # Return whatever is available
    

    def get_facebook_post_type(self, post):
        """
        Determines the type of a Facebook post.
        
        Parameters:
            post (WebElement): The Facebook post element.
        
        Returns:
            str: The post type, which can be 'image', 'video', or 'text'.
        """
        try:
            # Get all child elements within the post
            child_elements = post.find_elements(By.XPATH, ".//*")  

            for element in child_elements:
                post_classes = element.get_attribute("class")

                # Check for image post
                if element.tag_name == "img" and "x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r" in element.get_attribute("class"):
                    return "image"
                
                # Check for video post
                if element.tag_name == "video" and "x1lliihq x5yr21d xh8yej3" in element.get_attribute("class"):
                    return "video"
              
            return "text"  # Default to text post if no specific classes are found

        except Exception as e:
            print("\n\n", f"Error determining Facebook post type: {e}", "\n\n")
            return "unknown"


    def scrape_youtube_posts(self, youtube_page_name, target_post_count):
        """
        Scrapes posts from a specified Youtube page.
        Parameters:
            youtube_page_name (str): The name of the Youtube page to scrape.
            target_post_count (int): The number of posts to load..
        """
        print("\n\n", f"Navigating to {youtube_page_name} Youtube page...", "\n\n")
        
        user_id = youtube_page_name
        self.driver.get(f"https://www.youtube.com/@{youtube_page_name}/community/")

        print("\n\n", "Waiting for Youtube page to load...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'contents')]"))  # Updated XPath
            )
            print("\n\n", "Youtube page loaded successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Youtube page did not load properly:", e, "\n\n")
        
        # Extract posts
        posts = self.youtube_scroll_and_scrape(target_post_count)
        
        total_posts = len(posts)  # Get total number of posts
        
        # Print the number of posts found
        print("\n\n", f"Number of YouTube posts found: {len(posts)}", "\n\n")
        time.sleep(5)
        
        # followers at time of scrape       
        try:
            followers = self.driver.find_elements(By.XPATH, ".//span[contains(@class, 'yt-core-attributed-string') and contains(@class, 'yt-content-metadata-view-model-wiz__metadata-text') and contains(@class, 'yt-core-attributed-string--white-space-pre-wrap') and contains(@class, 'yt-core-attributed-string--link-inherit-color')]")[1].text
        except NoSuchElementException:
            followers = "NA"
            

        for index, post in enumerate(posts, start=1):
            
            print("\n\n", f"Youtube Post {index}/{total_posts} ({(index / total_posts) * 100:.2f}%) - Processing Start", "\n\n")
            try:
                post_id = str(uuid.uuid4())  # Generate a random UUID

                try:
                    post_likes = post.find_element(By.XPATH, ".//span[contains(@id, 'vote-count-middle') and contains(@class, 'style-scope') and contains(@class, 'ytd-comment-action-buttons-renderer')]").text
                except NoSuchElementException:
                    post_likes = "NA"
                    
                try:
                    post_comments = post.find_element(By.XPATH, ".//span[contains(@class, 'yt-core-attributed-string') and contains(@class, 'yt-core-attributed-string--white-space-no-wrap')]").text
                except NoSuchElementException:
                    post_comments = "NA"

                post_shares = "NA"

                try:
                    post_views = post.find_element(By.XPATH, ".//span[contains(@class, 'inline-metadata-item ') and contains(@class, 'style-scope') and contains(@class, 'ytd-video-meta-block')]").text
                except NoSuchElementException:
                    post_views = "NA"

                try:
                    post_text = post.find_element(By.XPATH, ".//yt-formatted-string[contains(@id, 'content-text') and contains(@class, 'style-scope') and contains(@class, 'ytd-backstage-post-renderer')]").text
                except NoSuchElementException:
                    post_text = "NA"

                try:
                    post_date = post.find_element(By.XPATH, ".//yt-formatted-string[contains(@id, 'published-time-text') and contains(@class, 'style-scope') and contains(@class, 'ytd-backstage-post-renderer')]").text
                except NoSuchElementException:
                    post_date = "NA"
                    
                # Identify Post Type
                post_type = self.get_youtube_post_type(post) if hasattr(self, 'get_youtube_post_type') else "NA"

                print("\n\n", f"Youtube post_text = {post_text}", "\n\n")
                print("\n\n", f"Youtube post_id = {post_id}", "\n\n")
                print("\n\n", f"Youtube post_date = {post_date}", "\n\n")
                print("\n\n", f"Youtube post_likes = {post_likes}", "\n\n")
                print("\n\n", f"Youtube post_comments = {post_comments}", "\n\n")
                print("\n\n", f"Youtube post_shares = {post_shares}", "\n\n")
                print("\n\n", f"Youtube post_views = {post_views}", "\n\n")
                print("\n\n", f"Youtube followers = {followers}", "\n\n")
                print("\n\n", f"Youtube post_type = {post_type}", "\n\n")

                # Create a DataFrame from the new row
                new_row = pd.DataFrame([{
                    "user_id": user_id,
                    "platform": "Youtube",
                    "post_id": post_id,
                    "date": post_date,
                    "likes": post_likes,
                    "comments": post_comments,
                    "shares": post_shares,
                    "post_text": post_text,
                    "post_origin_text": post.text,
                    "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "views": post_views,
                    "followers": followers,
                    "country": "NA",
                    "content_type": post_type,
                    "sentiment_score": "NA"
                }])

                # Use pd.concat instead of append
                self.posts_df = pd.concat([self.posts_df, new_row], ignore_index=True)

            except Exception as e:
                print("\n\n", f"Unexpected error scraping Youtube post {post_id}: {e}", "\n\n")
            
            print("\n\n",f"Youtube  Post {index}/{total_posts} - Processing End", "\n\n")
            time.sleep(2)
    
 
    def youtube_scroll_and_scrape(self, target_post_count):
        """
        Scrolls the YouTube page and scrapes posts until the target post count is reached,
        or stops if fewer posts are available. Retries if no posts are found.

        :param target_post_count: The number of posts to scrape.
        """
        max_retries=30
        scroll_amount=1000
        retry_count = 0
        
        posts = []
        total_posts = 0

        while True:
            # Scroll the page
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(2)
        
            # Extract posts
            posts = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'main') and contains(@class, 'style-scope') and contains(@class, 'ytd-backstage-post-renderer')]")
            total_posts_old = total_posts
            total_posts = len(posts)

            print(f"\n\nYoutube Posts loaded: {total_posts}/{target_post_count} ({(total_posts / target_post_count) * 100:.2f}%) \n\n")

            # Reset retry counter if posts are found
            if total_posts > total_posts_old:
                retry_count = 0

            # Stop when the target post count is reached
            if total_posts >= target_post_count:
                print("\n\nYoutube Target post count reached.\n\n")
                return posts[:target_post_count]  # Return only the target number of posts

            # Retry if no posts are found
            if retry_count < max_retries:
                print(f"\n\nNo nYoutube posts found. Retrying ({retry_count + 1}/{max_retries})...\n\n")
                retry_count += 1
                continue  # Try again without increasing scroll count

            # Stop if fewer posts than the target are available
            if total_posts < target_post_count:
                print("\n\nYoutube Stopping: Not enough posts available.\n\n")
                return posts  # Return all available posts

        return posts  # Return whatever is available

 
    def get_youtube_post_type(self, post):
        """
        Determines the type of a Youtube post.
        
        Parameters:
            post (WebElement): The Youtube post element.
        
        Returns:
            str: The post type, which can be 'image', 'video', or 'text'.
        """
        try:
            # Get all child elements within the post
            child_elements = post.find_elements(By.XPATH, ".//*")  

            all_classes = []  # Collect all classes
            element_info = []  # Collect element details for existence checks

            for element in child_elements:
                tag_name = element.tag_name  # Get element name
                element_id = element.get_attribute("id")  # Get element ID
                post_classes = element.get_attribute("class")  # Get element classes

                if post_classes:
                    class_list = post_classes.split()
                    all_classes.extend(class_list)  # Add classes as separate items
                else:
                    class_list = []

                # Store tag name, ID, and classes
                element_info.append({
                    "tag": tag_name,
                    "id": element_id if element_id else "None",
                    "classes": class_list
                })

            # Convert to set to remove duplicate classes
            unique_classes = set(all_classes)

            # Check for specific element existence
            for info in element_info:
                if info["tag"] == "ytd-backstage-image-renderer" and (("style-scope" in info["classes"] and "ytd-backstage-post-renderer" in info["classes"]) or ("style-scope" in info["classes"] and "ytd-post-multi-image-renderer" in info["classes"])):
                    return "image"

            # Check for specific element existence
            for info in element_info:
                if info["tag"] == "ytd-video-renderer" and "style-scope" in info["classes"] and "ytd-backstage-post-renderer" in info["classes"]:
                    return "video"
            
            # Check for specific element existence
            for info in element_info:
                if info["tag"] == "yt-formatted-string" and "style-scope" in info["classes"] and "ytd-backstage-post-renderer" in info["classes"]:
                    return "text"

            return "unknown"  # Default to unknown post if no specific conditions are met

        except Exception as e:
            print("\n\n", f"Error determining Youtube post type: {e}", "\n\n")
            return "unknown"


    def login_instagram(self):
        """
        Logs into Instagram using stored credentials.
        """
        print("\n\n", "Navigating to Instagram Login page...", "\n\n")
        self.driver.get(constants.INSTAGRAM_LOGIN_PAGE)
        time.sleep(5)

        print("\n\n", "Entering Instagram Credentials...", "\n\n")
        email = self.driver.find_element(By.NAME, "username")
        email.send_keys(constants.INSTAGRAM_USERNAME)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(constants.INSTAGRAM_PASSWORD)
        password.send_keys(Keys.RETURN)

        print("\n\n", "Waiting for Instagram Login to complete...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//main[@role='main']"))  # Example element
            )
        except Exception as e:
            print("\n\n", "Login failed or took too long:", e, "\n\n")

        time.sleep(10)


    def scrape_instagram_posts(self, instagram_page_name, target_post_count):
        """
        Scrapes posts from a specified Instagram page.
        Parameters:
            instagram_page_name (str): The name of the Instagram page to scrape.
            target_post_count (int): The number of scrolls to perform to load more posts.
        """
        print("\n\n", f"Navigating to {instagram_page_name} Instagram page...", "\n\n")
        
        user_id = instagram_page_name
        self.driver.get(f"https://www.instagram.com/{instagram_page_name}/")

        print("\n\n", "Waiting for Instagram page to load...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'x1lliihq') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'x4gyw5p') and contains(@class, 'x11i5rnm') and contains(@class, 'x1ntc13c') and contains(@class, 'x9i3mqj') and contains(@class, 'x2pgyrj')]"))  # Updated XPath
            )
            
            print("\n\n", "Instagram page loaded successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Instagram page did not load properly:", e, "\n\n")
        
        # Scroll to load posts
        total_posts_to_found = target_post_count     # Total number of scrolls
        
        # open first post
        # Wait until the element is clickable, then click
        try:
            first_post = self.driver.find_elements(By.XPATH, ".//div[contains(@class, '_aagu')]")[0]  # Updated XPath
        
            first_post = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, '_aagu')]"))
            )
            first_post.click()
            
            print("\n\n", "Instagram post opened successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Instagram post did not open properly:", e, "\n\n")
        
        time.sleep(2)
        
        # extract from post
        
        post = first_post
        
        # followers at time of scrape       
        try:
            followers = self.driver.find_elements(By.XPATH, ".//li[contains(@class, 'xl565be') and contains(@class, 'x1m39q7l') and contains(@class, 'x1uw6ca5') and contains(@class, 'x2pgyrj')]")[1].text
        except NoSuchElementException:
            followers = "NA"
            
        
        # loop over posts intended by clik on next, and exctract needs each time
        for i in range(0, total_posts_to_found):
            
            print("\n\n", f"Instagram Post {i}/{total_posts_to_found} ({(i / total_posts_to_found) * 100:.2f}%) - Processing Start", "\n\n")
            
            time.sleep(2)
            # extract values from post
            
            # click on next button
            try:            
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//article[contains(@role, 'presentation') and contains(@class, '_aatb') and contains(@class, '_aati')]"))
                )
                                
                post = self.driver.find_element(By.XPATH, ".//article[contains(@role, 'presentation') and contains(@class, '_aatb') and contains(@class, '_aati')]")
                
                print("\n\n","Instagram post " + str(i) + " Loaded", "\n\n")
                
            except Exception as e:
                print("\n\n","Instagram post " + str(i) + " Failed Loaded", str(e), "\n\n")
            
            time.sleep(2)
            
            try:
                post_id = str(uuid.uuid4())  # Generate a random UUID

                try:
                    post_likes = post.find_element(By.XPATH, ".//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x1fj9vlw') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'xt0psk2') and contains(@class, 'x1i0vuye') and contains(@class, 'xvs91rp') and contains(@class, 'x1s688f') and contains(@class, 'x5n08af') and contains(@class, 'x10wh9bi') and contains(@class, 'x1wdrske') and contains(@class, 'x8viiok') and contains(@class, 'x18hxmgj')]").text
                    #post_likes = post_likes[0].text if len(post_likes) > 1 else "NA"
                except NoSuchElementException:
                    post_likes = "N/A  e"

                post_comments = "NA"
                post_shares = "NA"

                try:
                    post_text = post.find_element(By.XPATH, ".//h1[contains(@class, '_ap3a') and contains(@class, '_aaco') and contains(@class, '_aacu') and contains(@class, '_aacx') and contains(@class, '_aad7') and contains(@class, '_aade')]").text
                    #post_text = post_text[0].text if len(post_text) > 1 else "NA"
                except NoSuchElementException:
                    post_text = "N/A ee"
     
                try:
                    post_date = post.find_element(By.XPATH, ".//time[contains(@class, 'x1p4m5qa')]").get_attribute("datetime")
                except NoSuchElementException:
                    post_date = "NA"

                # Identify Post Type
                post_type = self.get_instagram_post_type(post) if hasattr(self, 'get_instagram_post_type') else "NA"

                print("\n\n", f"Instagram post_text = {post_text}", "\n\n")
                print("\n\n", f"Instagram post_id = {post_id}", "\n\n")
                print("\n\n", f"Instagram post_date = {post_date}", "\n\n")
                print("\n\n", f"Instagram post_likes = {post_likes}", "\n\n")
                print("\n\n", f"Instagram post_comments = {post_comments}", "\n\n")
                print("\n\n", f"Instagram post_shares = {post_shares}", "\n\n")
                print("\n\n", f"Instagram followers = {followers}", "\n\n")
                print("\n\n", f"Instagram post_type = {post_type}", "\n\n")

                # Create a DataFrame from the new row
                new_row = pd.DataFrame([{
                    "user_id": user_id,
                    "platform": "Instagram",
                    "post_id": post_id,
                    "date": post_date,
                    "likes": post_likes,
                    "comments": post_comments,
                    "shares": post_shares,
                    "post_text": post_text,
                    "post_origin_text": post.text,
                    "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "views": "NA",
                    "followers": followers,
                    "country": "NA",
                    "content_type": post_type,
                    "sentiment_score": "NA"
                }])

                # Use pd.concat instead of append
                self.posts_df = pd.concat([self.posts_df, new_row], ignore_index=True)


            except Exception as e:
                print("\n\n", f"Unexpected error scraping Instagram post {post_id}: {e}", "\n\n")
            
            print("\n\n",f"Instagram  Post {i}/{total_posts_to_found} - Processing End", "\n\n")     
                        
           # click on next button
            try:
                next_btn = self.driver.find_element(By.XPATH, ".//div[contains(@class, ' _aaqg') and contains(@class, ' _aaqh')]")
            
                next_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, ' _aaqg') and contains(@class, ' _aaqh')]"))
                )
                next_btn.click()
                
                print("\n\n", "Instagram next_btn click successfully. ", "\n\n")
            except Exception as e:
                print("\n\n", "Instagram next_btn did not click properly:", e, "\n\n")


    def get_instagram_post_type(self, post):
        """
        Determines the type of a Instagram post.
        
        Parameters:
            post (WebElement): The Instagram post element.
        
        Returns:
            str: The post type, which can be 'image', 'video', or 'text'.
        """       
        try:
            # Get all child elements within the post
            child_elements = post.find_elements(By.XPATH, ".//*")  

            for element in child_elements:
                post_classes = element.get_attribute("class")

                # Check for video post
                if element.tag_name == "video" and "x1lliihq x5yr21d xh8yej3" in element.get_attribute("class"):
                    return "video"
                    
                # Check for image post
                if element.tag_name == "img" and "x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3" in element.get_attribute("class"):
                    return "image"
              
            return "text"  # Default to text post if no specific classes are found

        except Exception as e:
            print("\n\n", f"Error determining Instagram post type: {e}", "\n\n")
            return "unknown"

 
    def save_data(self, platform):
        """
        Save the scraped data to an Excel file.
        Parameters:
            platform (str): The name of the platform for which the data was scraped.
        """
        file_path = f"Scraping_Output/{platform}_data.xlsx"
        
        # Ensure directory exists
        os.makedirs("Scraping_Output", exist_ok=True)
        # Remove file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        with pd.ExcelWriter(f"Scraping_Output/{platform}_data.xlsx") as writer:
            self.posts_df.to_excel(writer, sheet_name="Posts", index=False)
        
        with pd.ExcelWriter(f"Scraping_Output/{platform}_data_backup.xlsx") as writer:
            self.posts_df.to_excel(writer, sheet_name="Posts", index=False)

        print("\n\n", f"Data saved to {platform}_data.xlsx", "\n\n")



