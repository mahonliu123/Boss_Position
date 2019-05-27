# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import  Item, Field


class BossItem(Item):
    company_name = Field()  # 公司名字
    industry = Field()      # 所在行业
    company_size = Field()  # 公司规模
    job_name = Field()      # 职业名称
    location = Field()      # 公司地点
    salary = Field()        # 薪水范围
    education = Field()     # 最低学历
    workyear = Field()      # 工作年限

