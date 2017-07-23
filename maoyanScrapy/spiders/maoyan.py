# -*- coding: utf-8 -*-
import scrapy

from maoyanScrapy.items import MovieItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/board/4']

    def parse(self, response):

        movies = response.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div')
        for movie in movies:
            item = MovieItem()
            title = movie.xpath('.//div/p/a/text()').extract_first()
            star = movie.xpath('.//div/p/text()').extract_first()
            releasetime = movie.xpath('.//div[1]/p[3]/text()').extract_first()
            score = movie.xpath('.//div/p/i[1]/text()').extract_first() + movie.xpath('.//div[2]/p/i[2]/text()').extract_first()
            item['title'] = title
            item['star'] = star.strip()
            item['releasetime'] = releasetime[5:]
            item['score'] = score
            yield item

        next = response.xpath('//*[@id="app"]/div/div/div[2]/ul/li/a/@href').extract()[-1]
        url = response.urljoin(next)
        print(url)
        yield scrapy.Request(url, callback=self.parse)
