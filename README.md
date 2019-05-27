# Boss_Position

 爬取BOSS直聘上全国所有行业的职位信息，
 采用scrapy-redis分布式架构的CrawlRedisSpider，提高爬取速度。
 #
 在中间件中添加headers，IP，cookies等，
 在爬取一定数量页面后，会弹出需要拖动滑块的验证页面，
 在中间件中使用selenium打开验证页面，由于使用selenium定位滑块会被检测，所以先计算出滑块的初始位置和最终位置使用pyautogui这个库来操作鼠标拖动滑块
 #
 爬取一定数量后会被封IP24小时，所以若要爬取大量数据必须用代理IP
