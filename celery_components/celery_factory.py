from celery import Celery


celery = Celery('tasks_runner')
celery.config_from_object('celery_components.celery_conf')
