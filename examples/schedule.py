from SimpleSpider.simplespider.spider import Spider
from SimpleSpider.simplespider.schedule import Scheduler
from time import sleep


class Tester(Spider):
    """
    index_page : index/i
    detail_page : index/i/detail/j
    """
    def _get_page(self, url, retries=0):
        sleep(1)
        return url

    def on_result(self, result):
        print(result)

    def index_page(self, response):
        i = int(response.split('/')[1])
        for x in range(10):
            self.crawl('{}/detail/{}'.format(response, x), callback=self.detail_page)

        # self.crawl('index/{}'.format(i), callback=self.index_page)

    def detail_page(self, response):
        index, indexi, detail, detailj = response.split('/')
        return {
            index: indexi,
            detail: detailj
        }


if __name__ == '__main__':
    scheduler = Scheduler()
    t1 = Tester(name='t1', start_url='index/1', start_at='15:39', every='2m')
    t2 = Tester(name='t2', start_url='index/11', start_at='now')
    t3 = Tester(name='t3', start_url='index/21', start_at='now')
    scheduler.register_task([t1, t2, t3])
    scheduler.run()


