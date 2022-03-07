from celery_components.celery_factory import celery as celery_app
from tasks import TaskRunner
from redbeat import RedBeatScheduler


if __name__ == '__main__':
    task_runner = TaskRunner()
    celery = task_runner.configure_celery_instance(celery_app)
    beat = celery.Beat(scheduler=RedBeatScheduler, loglevel="DEBUG", pidfile="/tmp/celerybeat.pid")
    beat.run()
