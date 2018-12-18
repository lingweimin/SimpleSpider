from datetime import datetime, timedelta, time
import re
from time import sleep, ctime
from simplespider.utils import singleton
from .threadpool import ThreadPool
from .config import *
from .db import db


class Plan:
    freq_maps = {'w': 'weeks', 'd': 'days', 'h': 'hours', 'm': 'minutes', 's': 'seconds'}
    spec_freq_names = {'everyday': (1, 'd'), 'everyhour': (1, 'h'), 'everyweek': (1, 'w')}
    every_pattern = '(\d{0,3})([a-zA-Z])'
    start_at_pattern = '(\d{1,2}):(\d{2})'

    def __init__(self, start_at='now'):
        if start_at == 'now':
            self.start_time = datetime.now()
        else:
            self.start_time = start_at if isinstance(start_at, datetime) else self._parse_start_at(start_at)
        self.run_time = self.start_time
        self.his = []

    def __repr__(self):
        return '<{} object at {}>'.format(self.__class__.__name__, hex(id(self)))

    def _parse_start_at(self, start_at_str):
        match = re.match(self.start_at_pattern, start_at_str)
        if match:
            hour, minute = int(match.group(1)), int(match.group(2))
            return datetime.combine(datetime.today(), time(hour=hour, minute=minute))

        raise ValueError('The param start_at cannot be recognized.')

    def update(self, status=100):
        raise NotImplementedError()


class SinglePlan(Plan):

    def __init__(self, start_at='now'):
        super(__class__, self).__init__(start_at)

    def update(self, status=100):
        self.his = [(self.run_time, status)]
        self.run_time = None


class FreqPlan(Plan):

    def __init__(self, start_at='now', every=None):
        """

        :param start_at: 'now' or specify time 'hh:MM' eg. '8:00'
        :param every: '1d', 'd', '2d', '5w'
        """
        super(__class__, self).__init__(start_at)
        value, name = self.spec_freq_names.get(every, None) or self._parse_every(every)
        d = {self.freq_maps.get(name): value}
        self.freq = timedelta(**d)

    def update(self, status=100):
        self.his.append((self.run_time, status))
        self.run_time = self.next_run

    @property
    def next_run(self):
        return self.run_time + self.freq

    def _parse_every(self, every_str):
        match = re.match(self.every_pattern, every_str)
        if match:
            if match.group(2) in self.freq_maps.keys():
                g1 = int(match.group(1)) if match.group(1) else 1
                return g1, match.group(2)

        raise ValueError('The param every cannot be recognized.')


@singleton
class Scheduler:

    def __init__(self, period=15):
        self._tasks = []
        self.period = period
        self.threadpool = None
        self.use_database = SCHEDULER_USE_DATABASE
        self.db = db

    def __repr__(self):
        return '<{} object at {}>'.format(self.__class__.__name__, hex(id(self)))

    def run(self):
        self.threadpool = ThreadPool(len(self._tasks))
        self.threadpool.debug = True
        self.threadpool.run()
        while True:
            for task in self._tasks:
                # task.start()
                if not task.is_running:
                    self._start_task(task)
            sleep(self.period)

    def register_task(self, tasks):
        self._tasks.extend(tasks)
        # if self.use_database:
        #     for task in self._tasks:
        #         db.Task.add(task)

    def _start_task(self, task):
        if task.plan \
                and task.plan.run_time \
                and task.plan.run_time < datetime.now():
            print('{} task {} (run time {}) start.'.format(ctime(), task.name, task.plan.run_time))
            self.threadpool.execute(name=task.name, runnable=task.start)
