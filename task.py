from celery import Celery
from threading import Thread
import time



def send_task_and_get_results(i):
    app = Celery('tasks', roker='amqp://guest:guest@10.0.6.54:5672/')
    app.conf.CELERY_RESULT_BACKEND = 'amqp://guest:guest@10.0.6.54:5672/'
    result = app.send_task('tasks.my_task', args=(i))
    print('amqp://guest:guest@10.0.6.54:5672/', result.get())


if __name__ == '__main__':
    for i in range(100):
        send_task_and_get_results(i)
