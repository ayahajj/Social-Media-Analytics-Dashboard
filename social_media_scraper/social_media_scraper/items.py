# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SocialMediaScraperItem(scrapy.Item):
    user_id = scrapy.Field()
    platform = scrapy.Field()
    post_id = scrapy.Field()
    date = scrapy.Field()
    likes = scrapy.Field()
    comments = scrapy.Field()
    shares = scrapy.Field()
    views = scrapy.Field()
    followers = scrapy.Field()
    country = scrapy.Field()
    content_type = scrapy.Field()
    sentiment_score = scrapy.Field()

class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    post_id = scrapy.Field()
    comment_text = scrapy.Field()
    comment_date = scrapy.Field()
    comment_sentiment = scrapy.Field()
    