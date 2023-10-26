from celery import Celery, Task
from flask import Flask
from celery.schedules import crontab,schedule
from datetime import timedelta

# Boilerplate code for celery intialization
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    celery_app.conf.beat_schedule = {
    'monthly_user_report': {
        'task': 'app.task.send_user_monthly_report_task',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
        # 'schedule': timedelta(minutes=1),
        },
    'buy_something': {
        'task': 'app.task.send_visit_email_task',
        'schedule': crontab(hour=17, minute=0),
        # 'schedule': timedelta(minutes=1),
        },
    }
    return celery_app

