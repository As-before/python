from celery import Celery ,platforms

# 我们这里案例使用redis作为broker
app = Celery('tasks',backend='amqp', broker='amqp://guest:guest@10.0.6.54:5672/')
platforms.C_FORCE_ROOT = True


# 创建任务函数
@app.task
def my_task(i):
    print("任务函数正在执行....")
    return i
