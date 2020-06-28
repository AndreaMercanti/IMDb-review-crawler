import scrapy
from ..items import ScrapingItem
from datetime import datetime


class SpiderHelper(object):
    """Class that assists the spider in fetching correctly the reviews per film"""
    
    def __init__(self, ajaxURL, filmID):
        self.ajaxURL = ajaxURL
        self.filmID = filmID

    def parse(self, response):
        item = ScrapingItem()
        reviews = response.css('.collapsable')
        
        for review in reviews:
            user = review.css(".display-name-link a::text").get()
            rating_components = review.css(".rating-other-user-rating span::text").extract()
            date = review.css(".review-date::text").get()
            review_components = review.css(".show-more__control::text").extract()

            # PARSING AND BETTER FORMATTING THE DIFFERENT ELEMS
            date = datetime.strptime(date, '%d %B %Y').date() # creating a date object
            review_str = ''.join(review_components[0:-2]) # compacting all the review components into one string, but the last two
            rating = ''.join(rating_components) # compacting all rating components into one string
            
            item['filmID'] = self.filmID
            item['user'] = user
            item['rating'] = rating
            item['date'] = date
            item['review'] = review_str
            
            yield item
        
        next_page = response.css(".load-more-data").xpath('@data-key').get()
        if next_page is not None:
            yield scrapy.Request(self.ajaxURL + '&ref_=undefined&paginationKey=' + next_page, callback=self.parse)
