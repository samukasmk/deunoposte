# -*- coding: utf-8 -*-

import scrapy
from dateparser import parse


class DeunoposteSpider(scrapy.Spider):
    name = 'deunoposte'
    follow_pages = 'false'
    start_urls = [
        'http://resultadodojogodobicho.deunopostehoje.com/11-horas',
        'http://resultadodojogodobicho.deunopostehoje.com/14-horas/',
        'http://resultadodojogodobicho.deunopostehoje.com/sao-paulo/',
        'http://resultadodojogodobicho.deunopostehoje.com/corujinha/',
    ]

    def parse(self, response):
        self.log(f'--------- Parsing page: {response.url}')
        posts = response.css('div.post')
        for item in self.parse_posts_items(posts):
            yield item

        if self.follow_pages.lower() == 'true':
            next_link = response.css('a[class=nextpostslink]::attr(href)').extract_first()
            if next_link:
                yield scrapy.Request(next_link, callback=self.parse)

    def parse_posts_items(self, posts):
        for post in posts:
            item = {}

            post_title = post.css('a[rel=bookmark]::text')
            item['game'] = post_title.re_first('\[(.*)\-.*\]')
            item['state'] = post_title.re_first('\[.*\-(.*)\]')
            item['date'] = post_title.re_first('([0-9]{2,}\/[0-9]{2,}\/[0-9]{4})')

            if item['date']:
                item['date'] = parse(item['date']).date()

            post_results = post.css('div.resultado ::text')
            for line in post_results:
                results = line.re('^[\s]*([1-9][0-9]*).*([0-9]{4}).*([0-9]{2,})[\s]*')
                if results:
                    item['position'], item['result'], *extra_info = results

                    if len(extra_info) > 1:
                        item['ten'], item['animal'] = extra_info

                    yield item
