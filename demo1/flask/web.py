import random
from flask import Flask
from celery import Celery, Task

def make_celery(app):
    celery = Celery(app.import_name, broker = app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    class ContextTask(Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return Task.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
#app.config.update(
#    CELERY_BROKER_URL='sqla+sqlite:///queue.db',
#    CELERY_RESULT_BACKEND='db+sqlite:///queue.db',
#    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
#)
celery = make_celery(app)

@app.route('/')
def homepage():
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    add_together.delay(a, b)
    return 'Create new task {} + {}'.format(a, b)

@celery.task()
def add_together(a, b):
    res = a + b
    print res
    return res

if __name__ == '__main__':
    app.run()
