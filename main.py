from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from worker import task
import redis

import socketio

redis_manager = socketio.AsyncRedisManager("redis://localhost:6379")
socketio_server = socketio.AsyncServer(async_mode="asgi", client_manager=redis_manager)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
socketio_app = socketio.ASGIApp(socketio_server=socketio_server, other_asgi_app=app)

db = redis.from_url("redis://localhost:6379/1", decode_responses=True)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/start")
async def start(request: Request):
    db.set("progress", 0)
    task.s().apply_async()


@app.get("/progress")
async def progress(request: Request):
    progress = 100 * float(db.get("progress") or 0)
    return templates.TemplateResponse(
        "progressbar.html", {"request": request, "progress": progress}
    )
