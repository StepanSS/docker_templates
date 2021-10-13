""" Celery with Flask

    Run Celery worker 
    (use "--pool=solo" only for Windows see https://github.com/celery/celery/issues/4178 )
    # basically things become single threaded and are supported

    > .venv\Scripts\celery -A app.celery worker --loglevel=INFO --pool=solo

    Run beat (schedule)
    > .venv\Scripts\celery -A app.celery beat --loglevel=INFO

"""

from flask import Flask
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from time import sleep


logger = get_task_logger(__name__)

def make_celery(app):
    celery = Celery()
    celery.conf.update(app.config)

       

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.update(
    broker_url ='redis://localhost:6379',
    result_backend ='redis://localhost:6379'
)

celery = make_celery(app)

# =============================================================================
# add schedule task with: 

# 1. app.conf.beat_schedule
celery.conf.beat_schedule = {
        # Executes every 
        'add-every-minute-task': {
            'task': 'app.test',
            # 'schedule': crontab( minute='*'),
            'schedule': 10.0,
            'args': ['test from celery.conf.beat_schedule'],
        },
    }

# 2. @app.on_after_configure.connect
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(30.0, task_1.s(), name='add every 10')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(),
    #     task_1.s(),
    # )
    pass
# =============================================================================

@celery.task
def test(arg):
    print(arg)
    return arg


@celery.task()
def task_1():
    logger.info('task started')
    sleep(2)
    logger.info('complete')
    return 'task done'



@app.route('/')
def index():
    return f'hello '

@app.route('/cel')
def run_celery_job():
    task_1.delay()
    return f'task_1 started'





