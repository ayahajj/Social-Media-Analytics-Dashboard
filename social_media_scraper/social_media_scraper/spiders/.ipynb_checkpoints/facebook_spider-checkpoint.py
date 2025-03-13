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

class FacebookSpider(scrapy.Spider):
    name = "facebook_spider"

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(r'C:\Users\moham\Social Media Analytics Dashboard\facebook_scraper\facebook_scraper\driver\chromedriver-win64\chromedriver.exe'))
        self.posts_df = pd.DataFrame(columns=[
            "user_id", "platform", "post_id", "date", "likes", "comments", "shares", "post_text", "post_origin_text", "date_scraped", "views", "followers", "country", "content_type", "sentiment_score"
        ])
            
        try:
            a = ""
            #self.login_facebook()
            #self.scrape_facebook_posts()            
        except KeyboardInterrupt:
            print("Script stopped manually. Saving data...")
            self.save_data("facebook")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.save_data("facebook")
        
        try:
            a = ""
            #self.scrape_youtube_posts()            
        except KeyboardInterrupt:
            print("Script stopped manually. Saving data...")
            self.save_data("youtube")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.save_data("youtube")
      
        try:
            a = ""
            self.login_instagram()
            self.scrape_instagram_posts()            
        except KeyboardInterrupt:
            print("Script stopped manually. Saving data...")
            self.save_data("instagram")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.save_data("instagram")
        
        
        self.driver.quit()


    def get_facebook_post_type(self, post):
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
            print(f"Error determining post type: {e}")
            return "unknown"


    def login_facebook(self):
        print("Navigating to login page...")
        self.driver.get("https://www.facebook.com/login")
        time.sleep(2)

        print("Entering credentials...")
        email = self.driver.find_element(By.ID, "email")
        email.send_keys("mohammad.sobbahi2001@gmail.com")  # Replace with your email
        password = self.driver.find_element(By.ID, "pass")
        password.send_keys("P@ssw0rd1234")  # Replace with your password
        password.send_keys(Keys.RETURN)

        print("Waiting for login to complete...")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='main']"))  # Example element
            )
        except Exception as e:
            print("Login failed or took too long:", e)

        time.sleep(10)


    def save_data(self, platform):
        """Save data to Excel files."""
        with pd.ExcelWriter(platform + "_data.xlsx") as writer:
            self.posts_df.to_excel(writer, sheet_name="Posts", index=False)

        print("\n\n", "Data saved to " + platform + "_data.xlsx", "\n\n")


    def scrape_facebook_posts(self):
        print("\n\n", "Navigating to Aljazeera Channel page...", "\n\n")
        
        user_id = "aljazeerachannel"
        self.driver.get("https://www.facebook.com/aljazeerachannel/")

        print("\n\n", "Waiting for page to load...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1yztbdb') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'xh8yej3') and contains(@class, 'x1ja2u2z')]"))  # Updated XPath
            )
            print("\n\n", "Page loaded successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Page did not load properly:", e, "\n\n")
        
        # Scroll to load posts (adjust the range for more posts)
        total_scrolls = 800  # Total number of scrolls
        scroll_amount = 600  # Pixels to scroll down

        # Scroll to load posts (adjust the range for more posts)
        for scroll_count in range(1, total_scrolls + 1):  # Start from 1 for better readability
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(2)
            print("\n\n", f"Scroll {scroll_count}/{total_scrolls} completed ({(scroll_count / total_scrolls) * 100:.2f}%)", "\n\n")

        # Extract posts
        posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'x1yztbdb') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'x1ja2u2z')]")
        
        total_posts = len(posts)  # Get total number of posts
        
        # Print the number of posts found
        print("\n\n", f"Number of posts found: {len(posts)}", "\n\n")
        time.sleep(5)

        for index, post in enumerate(posts, start=1):
            print("\n\n",f"Post {index}/{total_posts} - Processing Start", "\n\n")
            
            try:
                post_id = str(uuid.uuid4())  # Generate a random UUID

                try:
                    post_likes = post.find_element(By.XPATH, ".//span[contains(@class, 'xt0b8zv') and contains(@class, 'x1jx94hy') and contains(@class, 'xrbpyxo') and contains(@class, 'xl423tq')]").text
                except NoSuchElementException:
                    post_likes = "N/A"
                    
                try:
                    post_comments = post.find_elements(By.XPATH, ".//span[contains(@class, 'html-span') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1hl2dhg') and contains(@class, 'x16tdsg8') and contains(@class, 'x1vvkbs') and contains(@class, 'xkrqix3') and contains(@class, 'x1sur9pj')]")
                    post_comments = post_comments[0].text if len(post_comments) > 1 else "N/A"
                except NoSuchElementException:
                    post_comments = "N/A"

                try:
                    post_shares = post.find_elements(By.XPATH, ".//span[contains(@class, 'html-span') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1hl2dhg') and contains(@class, 'x16tdsg8') and contains(@class, 'x1vvkbs') and contains(@class, 'xkrqix3') and contains(@class, 'x1sur9pj')]")
                    post_shares = post_shares[1].text if len(post_shares) > 1 else "N/A"
                except NoSuchElementException:
                    post_shares = "N/A"

                try:
                    post_text = post.find_element(By.XPATH, ".//div[contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x1vvkbs') and contains(@class, 'x126k92a')]").text
                except NoSuchElementException:
                    post_text = "N/A"

                try:
                    post_date = post.find_element(By.XPATH, ".//span[contains(@class, 'x1rg5ohu') and contains(@class, 'x6ikm8r') and contains(@class, 'x10wlt62') and contains(@class, 'x16dsc37') and contains(@class, 'xt0b8zv')]").text
                except NoSuchElementException:
                    post_date = "N/A"

                # Identify Post Type
                post_type = self.get_facebook_post_type(post) if hasattr(self, 'get_facebook_post_type') else "N/A"

                print("\n\n", f"post_text = {post_text}", "\n\n")
                print("\n\n", f"post_id = {post_id}", "\n\n")
                print("\n\n", f"post_date = {post_date}", "\n\n")
                print("\n\n", f"post_likes = {post_likes}", "\n\n")
                print("\n\n", f"post_comments = {post_comments}", "\n\n")
                print("\n\n", f"post_shares = {post_shares}", "\n\n")
                print("\n\n", f"post_type = {post_type}", "\n\n")

                # Create a DataFrame from the new row
                new_row = pd.DataFrame([{
                    "user_id": user_id,
                    "platform": "Facebook",
                    "post_id": post_id,
                    "date": "N/A",
                    "likes": post_likes,
                    "comments": post_comments,
                    "shares": post_shares,
                    "post_text": post_text,
                    "post_origin_text": post.text,
                    "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "views": "N/A",
                    "followers": "N/A",
                    "country": "N/A",
                    "content_type": post_type,
                    "sentiment_score": "N/A"
                }])

                # Use pd.concat instead of append
                self.posts_df = pd.concat([self.posts_df, new_row], ignore_index=True)

                # Save data incrementally
                self.save_data("facebook")

            except Exception as e:
                print("\n\n", f"Unexpected error scraping post {post_id}: {e}", "\n\n")
            
            print("\n\n",f"Post {index}/{total_posts} - Processing End", "\n\n")
            time.sleep(2)
 
 
    def get_youtube_post_type(self, post):
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
            print(f"Error determining post type: {e}")
            return "unknown"


    def scrape_youtube_posts(self):
        print("\n\n", "Navigating to Aljazeera Community page...", "\n\n")
        
        user_id = "aljazeeraenglish"
        self.driver.get("https://www.youtube.com/@aljazeera/community/")

        print("\n\n", "Waiting for page to load...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'contents')]"))  # Updated XPath
            )
            print("\n\n", "Page loaded successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Page did not load properly:", e, "\n\n")
        
        # Scroll to load posts (adjust the range for more posts)
        total_scrolls = 100  # Total number of scrolls
        scroll_amount = 600  # Pixels to scroll down

        # Scroll to load posts (adjust the range for more posts)
        for scroll_count in range(1, total_scrolls + 1):  # Start from 1 for better readability
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(1)
            print("\n\n", f"Scroll {scroll_count}/{total_scrolls} completed ({(scroll_count / total_scrolls) * 100:.2f}%)", "\n\n")

        # Extract posts
        posts = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'main') and contains(@class, 'style-scope') and contains(@class, 'ytd-backstage-post-renderer')]")
        
        total_posts = len(posts)  # Get total number of posts
        
        # Print the number of posts found
        print("\n\n", f"Number of posts found: {len(posts)}", "\n\n")
        time.sleep(5)

        for index, post in enumerate(posts, start=1):
            
            print("\n\n",f"Post {index}/{total_posts} - Processing Start", "\n\n")
            try:
                post_id = str(uuid.uuid4())  # Generate a random UUID

                try:
                    post_likes = post.find_element(By.XPATH, ".//span[contains(@id, 'vote-count-middle') and contains(@class, 'style-scope') and contains(@class, 'ytd-comment-action-buttons-renderer')]").text
                except NoSuchElementException:
                    post_likes = "N/A"
                    
                try:
                    post_comments = post.find_element(By.XPATH, ".//span[contains(@class, 'yt-core-attributed-string') and contains(@class, 'yt-core-attributed-string--white-space-no-wrap')]").text
                except NoSuchElementException:
                    post_comments = "N/A"

                post_shares = "N/A"

                try:
                    post_views = post.find_element(By.XPATH, ".//span[contains(@class, 'inline-metadata-item ') and contains(@class, 'style-scope') and contains(@class, 'ytd-video-meta-block')]").text
                except NoSuchElementException:
                    post_views = "N/A"

                try:
                    post_text = post.find_element(By.XPATH, ".//yt-formatted-string[contains(@id, 'content-text') and contains(@class, 'style-scope') and contains(@class, 'ytd-backstage-post-renderer')]").text
                except NoSuchElementException:
                    post_text = "N/A"

                try:
                    post_date = post.find_element(By.XPATH, ".//yt-formatted-string[contains(@id, 'published-time-text') and contains(@class, 'style-scope') and contains(@class, 'ytd-backstage-post-renderer')]").text
                except NoSuchElementException:
                    post_date = "N/A"

                # Identify Post Type
                post_type = self.get_youtube_post_type(post) if hasattr(self, 'get_youtube_post_type') else "N/A"

                print("\n\n", f"post_text = {post_text}", "\n\n")
                print("\n\n", f"post_id = {post_id}", "\n\n")
                print("\n\n", f"post_date = {post_date}", "\n\n")
                print("\n\n", f"post_likes = {post_likes}", "\n\n")
                print("\n\n", f"post_comments = {post_comments}", "\n\n")
                print("\n\n", f"post_shares = {post_shares}", "\n\n")
                print("\n\n", f"post_views = {post_views}", "\n\n")
                print("\n\n", f"post_type = {post_type}", "\n\n")

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
                    "followers": "N/A",
                    "country": "N/A",
                    "content_type": post_type,
                    "sentiment_score": "N/A"
                }])

                # Use pd.concat instead of append
                self.posts_df = pd.concat([self.posts_df, new_row], ignore_index=True)

                # Save data incrementally
                self.save_data("youtube")

            except Exception as e:
                print("\n\n", f"Unexpected error scraping post {post_id}: {e}", "\n\n")
            
            print("\n\n",f"Post {index}/{total_posts} - Processing End", "\n\n")
            time.sleep(2)
            











    def get_instagram_post_type(self, post):
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
            print(f"Error determining post type: {e}")
            return "unknown"





    def login_instagram(self):
        print("Navigating to login page...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        print("Entering credentials...")
        email = self.driver.find_element(By.NAME, "username")
        email.send_keys("test.mohammad2001")  # Replace with your email      email=  mohammad.sobbahi2001@gmail.com
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys("P@ssw0rd1234")  # Replace with your password
        password.send_keys(Keys.RETURN)

        print("Waiting for login to complete...")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//main[@role='main']"))  # Example element
            )
        except Exception as e:
            print("\n\n", "Login failed or took too long:", e, "\n\n")

        time.sleep(10)


    def scrape_instagram_posts(self):
        print("\n\n", "Navigating to Aljazeera Instagram page...", "\n\n")
        
        user_id = "aljazeera"
        self.driver.get("https://www.instagram.com/aljazeera/")

        print("\n\n", "Waiting for page to load...", "\n\n")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'x1lliihq') and contains(@class, 'x1n2onr6') and contains(@class, 'xh8yej3') and contains(@class, 'x4gyw5p') and contains(@class, 'x11i5rnm') and contains(@class, 'x1ntc13c') and contains(@class, 'x9i3mqj') and contains(@class, 'x2pgyrj')]"))  # Updated XPath
            )
            
            print("\n\n", "Page loaded successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Page did not load properly:", e, "\n\n")
        
        # Scroll to load posts (adjust the range for more posts)
        total_posts_to_found = 200  # Total number of scrolls
        
        
        # open first post
        # Wait until the element is clickable, then click
        try:
            first_post = self.driver.find_elements(By.XPATH, ".//div[contains(@class, '_aagu')]")[0]  # Updated XPath
        
            first_post = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, '_aagu')]"))
            )
            first_post.click()
            
            print("\n\n", "Post opened successfully. ", "\n\n")
        except Exception as e:
            print("\n\n", "Post did not open properly:", e, "\n\n")
        
        time.sleep(2)
        
        # extract from post
        
        post = first_post
        
        # loop over posts intended by clik on next, and exctract needs each time
        for i in range(0, total_posts_to_found):
            
            print("\n\n",f"Post {str(i)}/{total_posts_to_found} - Processing Start", "\n\n")
            
            time.sleep(2)
            # extract values from post
            
            # click on next button
            try:            
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, ".//article[contains(@role, 'presentation') and contains(@class, '_aatb') and contains(@class, '_aati')]"))
                )
                
                print("\n\n","Post " + str(i) + " Loaded111", "\n\n")
                
                post = self.driver.find_element(By.XPATH, ".//article[contains(@role, 'presentation') and contains(@class, '_aatb') and contains(@class, '_aati')]")
                
                print("\n\n","Post " + str(i) + " Loaded", "\n\n")
                
            except Exception as e:
                print("\n\n","Post " + str(i) + " Failed Loaded", str(e), "\n\n")
            
            time.sleep(2)
                
            
            try:
                post_id = str(uuid.uuid4())  # Generate a random UUID

                try:
                    post_likes = post.find_element(By.XPATH, ".//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x1fj9vlw') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'xt0psk2') and contains(@class, 'x1i0vuye') and contains(@class, 'xvs91rp') and contains(@class, 'x1s688f') and contains(@class, 'x5n08af') and contains(@class, 'x10wh9bi') and contains(@class, 'x1wdrske') and contains(@class, 'x8viiok') and contains(@class, 'x18hxmgj')]").text
                    #post_likes = post_likes[0].text if len(post_likes) > 1 else "N/A"
                except NoSuchElementException:
                    post_likes = "N/A  e"

                post_comments = "N/A"
                post_shares = "N/A"

                try:
                    post_text = post.find_element(By.XPATH, ".//h1[contains(@class, '_ap3a') and contains(@class, '_aaco') and contains(@class, '_aacu') and contains(@class, '_aacx') and contains(@class, '_aad7') and contains(@class, '_aade')]").text
                    #post_text = post_text[0].text if len(post_text) > 1 else "N/A"
                except NoSuchElementException:
                    post_text = "N/A ee"
     
                try:
                    post_date = post.find_element(By.XPATH, ".//time[contains(@class, 'x1p4m5qa')]").text
                except NoSuchElementException:
                    post_date = "N/A"

                # Identify Post Type
                post_type = self.get_instagram_post_type(post) if hasattr(self, 'get_instagram_post_type') else "N/A"

                print("\n\n", f"post_text = {post_text}", "\n\n")
                print("\n\n", f"post_id = {post_id}", "\n\n")
                print("\n\n", f"post_date = {post_date}", "\n\n")
                print("\n\n", f"post_likes = {post_likes}", "\n\n")
                print("\n\n", f"post_comments = {post_comments}", "\n\n")
                print("\n\n", f"post_shares = {post_shares}", "\n\n")
                print("\n\n", f"post_type = {post_type}", "\n\n")

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
                    "views": "N/A",
                    "followers": "N/A",
                    "country": "N/A",
                    "content_type": post_type,
                    "sentiment_score": "N/A"
                }])

                # Use pd.concat instead of append
                self.posts_df = pd.concat([self.posts_df, new_row], ignore_index=True)

                # Save data incrementally
                self.save_data("instagram")

            except Exception as e:
                print("\n\n", f"Unexpected error scraping post {post_id}: {e}", "\n\n")
            
            print("\n\n",f"Post {str(i)}/{total_posts_to_found} - Processing End", "\n\n")            
                        
           # click on next button
            try:
                next_btn = self.driver.find_element(By.XPATH, ".//div[contains(@class, ' _aaqg') and contains(@class, ' _aaqh')]")
            
                next_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//div[contains(@class, ' _aaqg') and contains(@class, ' _aaqh')]"))
                )
                next_btn.click()
                
                print("\n\n", "next_btn click successfully. ", "\n\n")
            except Exception as e:
                print("\n\n", "next_btn did not click properly:", e, "\n\n")
            
            


 