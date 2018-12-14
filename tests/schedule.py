import unittest
from SimpleSpider.simplespider.schedule import FreqPlan
from datetime import datetime, timedelta, time


class FrequencyTestCase(unittest.TestCase):

    def test_new(self):
        start_date = datetime.combine(datetime.today(), time(hour=8))
        plan = FreqPlan(every='d', start_at='8:00')
        self.assertEqual(plan.start_time, start_date)
        self.assertEqual(plan.next_run, start_date + timedelta(days=1))

    def test_update(self):
        start_date = datetime.combine(datetime.today(), time(hour=12, minute=30))
        plan = FreqPlan(every='2d', start_at='12:30')
        self.assertEqual(plan.start_time, start_date)
        self.assertEqual(plan.next_run, start_date + timedelta(days=2))
        plan.update()
        self.assertEqual(plan.run_time, start_date + timedelta(days=2))
        self.assertEqual(plan.next_run, start_date + timedelta(days=4))
