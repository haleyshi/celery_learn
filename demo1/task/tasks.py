from celery import Celery

#app = Celery('tasks', broker='sqla+sqlite:///celerydb.sqlite')
#app = Celery('tasks', broker='redis://localhost:6379/0')
app = Celery('tasks', broker='amqp://guest@localhost//')

@app.task
def add(a, b):
    return a + b


if __name__ == '__main__':
    add.delay(3, 5)