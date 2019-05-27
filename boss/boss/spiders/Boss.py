# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BossItem



class BossSpider(RedisCrawlSpider):
    name = 'Boss'
    allowed_domains = ['zhipin.com']
    redis_key = 'Boss:start_urls'

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="home-sider"]/div[@class="job-menu"]'), callback='parse_page'),
    )


    def parse_page(self, response):
        # 将区域由所在城市转向全国，若想指定城市，则改动sel-city-后面的序号即可
        all_area = response.xpath('//dd[@class="city-wrapper"]/a[@ka="sel-city-100010000"]')
        for a in all_area:
            if a:
                yield response.follow(a, self.parse_item)

    def parse_item(self, response):
        item = BossItem()
        job_list = response.xpath('//div[@class="job-list"]/ul/li')
        for job in job_list:
            item['company_name'] = job.xpath('.//div[@class="company-text"]/h3/a/text()').extract_first()
            company_info = job.xpath('.//div[@class="company-text"]/p/text()').extract()
            item['industry'] = company_info[0]
            item['company_size'] = company_info[-1]
            item['job_name'] = job.xpath('.//div[@class="job-title"]/text()').extract_first()
            lwe_info = job.xpath('.//div[@class="info-primary"]/p/text()').extract()
            item['location'] = lwe_info[0]
            item['salary'] = job.xpath('.//span[@class="red"]/text()').extract_first()
            item['education'] = lwe_info[2]
            item['workyear'] = lwe_info[1]
            yield item
        # 翻页直至最后一页
        next_page = response.xpath('//div[@class="page"]/a[last()]')
        for a in next_page:
            if a:
                yield response.follow(a, self.parse_item)
