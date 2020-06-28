# -*- coding: utf-8 -*-
import scrapy
import json
from .spider_helper import SpiderHelper
from ..db import DBManager
from sqlalchemy.exc import IntegrityError

DATASET_PATH = 'movie_dataset.json'

class FetcherSpider(scrapy.Spider):
    name = 'fetcher'
    allowed_domains = ['imdb.com']

    def start_requests(self):
        with open(DATASET_PATH, 'r') as file:
            for line in file.readlines():
                movie = json.loads(line)
                
                film_id = movie['imdbID']
                film_title = movie['Title']
                ajax_url = 'https://www.imdb.com/title/{}/reviews/_ajax?sort=userRating&dir=desc&ratingFilter=0'.format(film_id)
                
                helper = SpiderHelper(ajax_url, film_id)
                
                dbMgr = DBManager.getInstance()
                try:
                    dbMgr.addFilm(film_id, film_title)
                except IntegrityError:
                    print('The film already exists')
                
                yield scrapy.Request(ajax_url, callback=helper.parse, dont_filter=True)
