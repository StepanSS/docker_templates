""" Test Celery 

    Run Celery worker (use "--pool=solo" only for Windows)
    > celery -A tasks.app worker --loglevel=INFO --pool=solo
    # from venv
    > .venv\Scripts\celery -A tasks.app worker --loglevel=INFO --pool=solo

    Run beat (schedule)
    > .venv\Scripts\celery -A tasks.app beat --loglevel=INFO

"""
from celery import Celery


app = Celery( backend='redis://localhost', broker='redis://localhost//')

# =============================================================================
# add schedule task with: 

# 1. app.conf.beat_schedule
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

# 2. @app.on_after_configure.connect
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 5 seconds.
    sender.add_periodic_task(5.0, test.s('hello'), name='add every 5')

    # sender.add_periodic_task(10.0, add.s(5,22), name='add every 10')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)
# =============================================================================

@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    return x + y
