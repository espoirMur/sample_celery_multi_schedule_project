from celery_components.celery_factory import celery as celery_app
from tasks import TaskRunner


if __name__ == '__main__':
    task_runner  = TaskRunner()
    celery = task_runner.configure_celery_instance(celery_app)
    worker = celery.Worker(log_level='WARN', task_events=True)
    worker.start()
