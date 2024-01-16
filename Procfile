web: uvicorn main:socketio_app --reload --port=8000
worker: celery --app=worker.app worker --pool=solo --loglevel=info