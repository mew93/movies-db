
import scrapy
from scrapy.loader import ItemLoader
from imdbscrapper.items import MovieItem

class MovieSpider(scrapy.Spider):
	name = "movie"
	def __init__(self, *args, **kwargs): 
		super(MovieSpider, self).__init__(*args, **kwargs) 

		self.start_urls = [kwargs.get('start_url')] 

	def parse(self, response):
		item = MovieItem()
		for movie in response.css('div.title_bar_wrapper'):
			item['name'] = movie.css('div.title_wrapper h1::text').extract_first()
			item['year'] = movie.css('div.title_wrapper span a::text').extract_first()
			item['rating'] = movie.css('div.ratingValue strong span::text').extract()
			item['duration'] = movie.css('div.subtext time::text').extract()
		for genre in response.css('div.subtext a'):
			item['genre'] = genre.css('span.itemprop::text').extract_first()
		return item



