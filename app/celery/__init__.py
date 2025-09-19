import os
from flask import Flask
from celery import Celery
from celery import Celery, Task
from celery.signals import setup_logging


@setup_logging.connect
def config_loggers(*args, **kwargs):
    """Configure Celery to use our centralized logging system"""
    from app.logging import configure_logging
    from app.logging.config import DevelopmentConfig, ProductionConfig
    import os

    env = os.getenv('FLASK_ENV', 'production')
    if env == 'development':
        configure_logging(DevelopmentConfig())
    else:
        configure_logging(ProductionConfig())


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = None
    if os.name == "posix":
        celery_app = Celery(app.name, task_cls=FlaskTask)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
    else:
        celery_app = Celery(app.name)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        celery_app.Task = FlaskTask

    app.extensions["celery"] = celery_app

    return celery_app
