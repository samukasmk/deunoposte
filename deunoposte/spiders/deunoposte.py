# -*- coding: utf-8 -*-

import scrapy
from dateparser import parse
from deunoposte.items import GameResultItem


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
        self.log(f'Start parsing page: {response.url}')
        posts = response.css('div.post')
        for item in self.parse_posts_items(posts):
            yield item

        if self.follow_pages.lower() == 'true':
            next_link = response.css('a[class=nextpostslink]::attr(href)').extract_first()
            if next_link:
                yield scrapy.Request(next_link, callback=self.parse)

    def parse_posts_items(self, posts):
        for post in posts:
            post_title = post.css('a[rel=bookmark]::text')
            game = post_title.re_first('\[(.*)\-.*\]')
            state = post_title.re_first('\[.*\-(.*)\]')
            date = post_title.re_first('([0-9]{2,}\/[0-9]{2,}\/[0-9]{4})')

            if date:
                date = parse(date).date()

            post_results = post.css('div.resultado ::text')
            for line in post_results:
                position = line.re_first('^[\s]*([1-9][0-9]*)')
                result = line.re_first('\s([0-9]{4})\s')
                ten = line.re_first('([0-9]{2})\s*[a-zA-Z\u00C0-\u00FF]')
                animal = line.re_first('\s([a-zA-Z\u00C0-\u00FF]{3,})[\s]*')

                if result:
                    yield GameResultItem(game=game,
                                         state=state,
                                         date=date,
                                         position=position,
                                         result=result,
                                         ten=ten,
                                         animal=animal)
