from threading import Thread, Lock
from simplespider.utils import singleton
from time import ctime, sleep


def lock(lock_obj):
    def decorator(f):
        def inner(*args, **kwargs):
            try:
                lock_obj.acquire()
                return f(*args, **kwargs)
            finally:
                lock_obj.release()
        return inner
    return decorator


class CallBackThread(Thread):

    def __init__(self, callback=None, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.callback = callback

    def run(self):
        super(__class__, self).run()
        if self.callback:
            self.callback(self)


@singleton
class ThreadPool:
    pool_lock = Lock()
    waiting_lock = Lock()

    def __init__(self, size=10, debug=False):
        # limit of the pool
        self.size = size
        # id list to mark the running threads
        self.idx = list(range(size))
        # thread pool
        self.pool = []
        # waiting queue to hold the tasks if thread pool is full
        self.waiting = []
        self.poll_period = 1
        self.debug = debug
        # self.pool_lock = Lock()
        # self.waiting_lock = Lock()
        # self.total_runs = 0

    def __repr__(self):
        return '<{} object size: {}, running: {}>'.format(self.__class__.__name__, self.size, self.running)

    @property
    def running(self):
        return len(self.pool)

    def execute(self, runnable, args=None, name=None):
        """
        To start a thread to run if the running is under the limit size otherwise push into the waiting queue
        :param runnable:
        :param args:
        :param name:
        :return:
        """
        if self.running < self.size:
            args = args or ()
            thread = CallBackThread(name=name, target=runnable, args=args)
            thread.start()
            self._add_to_pool(thread)
            if self.debug:
                print('{} thread {} of name {} is running. pool: {}'.format(
                    ctime(),
                    thread.id,
                    name or '***',
                    self.idx))
        else:
            self._push_to_waiting((name, runnable, args))

    def on_thread_end(self, thread):
        # next = self.poll()
        # if not next:
        #     func, args = next
        #     thread.target =
        # else:
        self._remove_from_pool(thread)
        if self.debug:
            print('{}: thread {} is done. pool: {}'.format(ctime(), thread.id, self.idx))

    def run(self):
        Thread(target=self._poll).start()

    def _poll(self):
        while True:
            self._check_threads_end()

            while len(self.waiting) > 0 and self.running < self.size:
                next_r = self._pop_from_waiting()
                if next_r:
                    name, runnable, args = next_r
                    self.execute(name=name, runnable=runnable, args=args)
            else:
                sleep(self.poll_period)

    @lock(pool_lock)
    def _check_threads_end(self):
        for thread in self.pool:
            if not thread.is_alive():
                self.on_thread_end(thread)

    @lock(pool_lock)
    def _add_to_pool(self, thread):
        thread.id = self.idx.pop(0)
        #self.lock(self.pool.append)(thread)
        self.pool.append(thread)

    def _remove_from_pool(self, thread):
        #self.lock(self.pool.remove)(thread)
        id = thread.id
        self.idx.append(id)
        self.pool.remove(thread)

    @lock(waiting_lock)
    def _pop_from_waiting(self):
        if self.waiting:
            name, func, args = self.waiting.pop(0)
            return name, func, args

    @lock(waiting_lock)
    def _push_to_waiting(self, obj):
        self.waiting.append(obj)
        if self.debug:
            print('pool full. push into waiting queue. size: {}'.format(len(self.waiting)))



