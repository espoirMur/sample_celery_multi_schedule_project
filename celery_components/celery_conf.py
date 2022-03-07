
CELERY_REDIS_SCHEDULER_URL = "redis://127.0.0.1:6379"
print("****** CELERY_REDIS_SCHEDULER_URL: ", CELERY_REDIS_SCHEDULER_URL)
redbeat_redis_url = CELERY_REDIS_SCHEDULER_URL
broker_url = CELERY_REDIS_SCHEDULER_URL
result_backend = CELERY_REDIS_SCHEDULER_URL
task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = ['pickle']
enable_utc = False
task_track_started = True
task_send_sent_event = True
