from celery import Celery
from celery.utils.log import get_logger
import time
import redis
import socketio

logger = get_logger(__name__)
app = Celery("worker", broker="redis://localhost:6379/0")
db = redis.from_url("redis://localhost:6379/1")
redis_manager = socketio.RedisManager("redis://localhost:6379", write_only=True)


@app.task(bind=True)
def task(self):
    n = 100
    for i in range(n):
        progress = (i + 1) / n
        logger.info(f"Processing: {progress}")
        db.set("progress", progress)
        redis_manager.emit("trigger-event", {"event": "progress"})
        time.sleep(0.1)
