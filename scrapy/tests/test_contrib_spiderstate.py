import os
from datetime import datetime
from twisted.trial import unittest

from scrapy.contrib.spiderstate import SpiderState
from scrapy.spider import BaseSpider


class SpiderStateTest(unittest.TestCase):

    def test_store_load(self):
        jobdir = self.mktemp()
        os.mkdir(jobdir)
        spider = BaseSpider(name='default')
        dt = datetime.now()

        ss = SpiderState(jobdir)
        ss.spider_opened(spider)
        spider.state['one'] = 1
        spider.state['dt'] = dt
        ss.spider_closed(spider)

        spider2 = BaseSpider(name='default')
        ss2 = SpiderState(jobdir)
        ss2.spider_opened(spider2)
        self.assertEqual(spider.state, {'one': 1, 'dt': dt})
        ss2.spider_closed(spider2)

    def test_state_attribute(self):
        # state attribute must be present if jobdir is not set, to provide a
        # consistent interface 
        spider = BaseSpider(name='default')
        ss = SpiderState()
        ss.spider_opened(spider)
        self.assertEqual(spider.state, {})
        ss.spider_closed(spider)
