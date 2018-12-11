from SimpleSpider.simplespider.spider import Spider
from time import sleep


class Tester(Spider):
    """
    index_page : index/i
    detail_page : index/i/detail/j
    """
    def _get_page(self, url, retries=0):
        sleep(2)
        return url

    def on_result(self, result):
        print(result)

    def index_page(self, response):
        i = int(response.split('/')[1])
        i += 1
        for x in range(10):
            self.crawl('{}/detail/{}'.format(response, x), callback=self.detail_page)

        self.crawl('index/{}'.format(i), callback=self.index_page)

    def detail_page(self, response):
        index, indexi, detail, detailj = response.split('/')
        return {
            index: indexi,
            detail: detailj
        }


if __name__ == '__main__':
    t = Tester(start_url='index/1')
    t.start()


