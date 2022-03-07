import pytz
from celery import Task
from datetime import timedelta
from celery_components.custom_crontab import CustomCrontab

class BaseTask(Task):
    autoretry_for = (Exception, )
    retry_kwargs = {'max_retries': 12, 'countdown': 60 * 60}  # retry every hour for 12 times
    retry_backoff = False
    name = "my smaple task"
    active = True
    customers = [{"id": 1, "c_name": "name", "c_timezone": "America/Chicago"}, {"id": 2, "c_name": "nam2", "c_timezone": "Canada/Eastern"}]

    def run(self, *args, **kwargs):
        print("This is a sample task I am running and scheduling")
    
    def get_schedule(self, time_period,  customer):
        """
        return the schedule for the task
        """
        self.build_schedules(customer)
        if self.active:
            schedule = self.time_period_schedule[time_period]
        else:
            schedule = timedelta(days=9000) # never run
        return {self.name: {'task': self.name, 'schedule': schedule}}

    def build_schedules(self, customer):
        self.time_period_schedule = {'daily': CustomCrontab(minute=30, hour=14, tz=pytz.timezone(customer.get("c_timezone"))),
                                     'weekly': CustomCrontab(minute=30, hour=14, day_of_week=1, tz=pytz.timezone(customer.get("c_timezone"))),
                                     'monthly': CustomCrontab(minute=30, hour=14, day_of_month=1, tz=pytz.timezone(customer.get("c_timezone"))),
                                     'quarterly': CustomCrontab(minute=30, hour=14, day_of_month=1, month_of_year='*/3', tz=pytz.timezone(customer.get("c_timezone"))),
                                     'yearly': CustomCrontab(minute=30, hour=14, day_of_month=1, month_of_year=1, tz=pytz.timezone(customer.get("c_timezone")))}


class TaskRunner:
    def configure_celery_instance(self, celery_instance):
        """
        this configure the celery instance and register the tasks for all customers.
        it also generate the task schedule.
        """
        task = BaseTask()
        for customer in task.customers:
            for time_period in ["daily", "weekly", "monthly", "quarterly", "yearly"]:
                celery_instance.register_task(task)
                card_schedule = task.get_schedule(time_period, customer)
                celery_instance.conf.beat_schedule.update(card_schedule)
        return celery_instance
