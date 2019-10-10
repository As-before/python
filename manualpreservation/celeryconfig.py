# -*- coding:utf-8 -*- 

__author__ = 'xhp'
from kombu import Queue 			
from kombu import Exchange

enable_utc = True
timezone = 'Asia/Shanghai'

task_queues = (
    Queue('default', exchange=Exchange('tasks', type='direct'), routing_key='task.#'),
    Queue('snapshot', exchange=Exchange('web', type='direct'), routing_key='websnap'),
    Queue('page', exchange=Exchange('page', type='direct'), routing_key='page'),
)

task_default_queue = 'default'
task_default_exchange = 'tasks'
task_default_exchange_type = 'direct'
task_default_routing_key = 'task.#'

task_routes = {
    'scrapyTask.scrapyNormal': {'queue': 'snapshot', 'routing_key': 'websnap'},
    # 'testdb.updatePage':{'queue':'page','routing_key':'page'}
    # 'tasks.add': {'queue': 'priority_low','routing_key':'priority_low'},
    # 'tasks.testRequest': {'queue': 'priority_high','routing_key':'priority_high'}
}

# task_annotations = {
#    'scrapyTask.scrapyNormal': {'rate_limit': '10/m'}
# }

# result_serializer = 'json'


# REDIS_HOST = '10.0.5.34'
# REDIS_PORT = '6379'
# REDIS_DB = 13

# broker_url = 'pyamqp://splab:splab@10.10.181.207:5672/splab'
# broker_url = 'amqp://test:test@10.0.5.191:5672/test'
# result_backend = 'db+postgresql://splab:splab@10.10.181.207/splab'
# result_backend = 'redis://%s:%s/%s'%(REDIS_HOST,REDIS_PORT,REDIS_DB)
broker_url = 'amqp://ivan:cat@localhost:5672/myvhost'
result_backend = 'redis://localhost:6379/0'
