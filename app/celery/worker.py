from app.web import create_app

flask_app = create_app()

if "celery" not in flask_app.extensions:
    raise RuntimeError(
        "Celery is not configured. Please set REDIS_URI environment variable."
    )

celery_app = flask_app.extensions["celery"]
