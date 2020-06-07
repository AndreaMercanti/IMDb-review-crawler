# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapingItem
import json
from datetime import datetime
from ..db import DBManager

DATASET_PATH = 'movie_dataset.json'

class FetcherSpider(scrapy.Spider):
    name = 'fetcher'
    allowed_domains = ['imdb.com']

    def __init__(self, **kwargs):
        self.ajax_url = None
        self.filmID = None
        self.filmTitle = None
        super().__init__(**kwargs)

    def start_requests(self):
        with open(DATASET_PATH, 'r') as file:
            movie = json.loads(file.readline())
            self.filmID = movie['imdbID']
            self.filmTitle = movie['Title']
            dbMgr = DBManager.getInstance()
            dbMgr.addFilm(self.filmID, self.filmTitle)
            self.ajax_url = 'https://www.imdb.com/title/{}/reviews/_ajax?sort=userRating&dir=desc&ratingFilter=0'.format(self.filmID)
            yield scrapy.Request(self.ajax_url, callback=self.parse, dont_filter=True)

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
            yield scrapy.Request(self.ajax_url + '&ref_=undefined&paginationKey=' + next_page, callback=self.parse)
