from SimpleSpider.simplespider.threadpool import ThreadPool
from time import ctime, sleep
from threading import Thread
from random import randint

TASK_ID = 0
threadpool = ThreadPool(5, debug=True)


def task(task_id, sec):
    # print('{}: task {} is working, sleep for {}s.'.format(ctime(), task_id, sec))
    sleep(sec)


def gen_tasks(pause_at=8):
    count = 0
    while True:
        sec = randint(5, 10)
        global TASK_ID
        TASK_ID += 1
        name = 'task_{}'.format(TASK_ID)
        threadpool.execute(runnable=task, args=(TASK_ID, sec), name=name)
        count += 1
        sleep(1)
        if count % pause_at == 0:
            sleep(60)


if __name__ == '__main__':
    threadpool.run()
    for i in range(1):
        t = Thread(target=gen_tasks)
        t.start()
