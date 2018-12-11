from time import sleep


class Scheduler:

    def __init__(self, period=60):
        self._tasks = []
        self.period = period

    def run(self):
        while True:
            print('Scheduler run')
            for task in self._tasks:
                task.run()
            sleep(self.period)

    def register_task(self, tasks):
        self._tasks.extend(tasks)