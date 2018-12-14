import unittest
from simplespider.threadpool import threadpool, ThreadPool


class ThreadPoolTestCase(unittest.TestCase):

    def test_singleton(self):
        threadpool2 = ThreadPool()
        self.assertEqual(id(threadpool), id(threadpool2))

    def test_running(self):
        self.assertEqual(threadpool.running, 0)
