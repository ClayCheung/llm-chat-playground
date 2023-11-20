import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import schema.api as api
from handler import server
from store import db


def init_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logging()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# init session service
svc = server.SessionService(db=next(db.get_db()))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/CreateSession")
def create_session(req: api.RequestCreateSession) -> api.ResponseCreateSession:
    return svc.create_session(req)


@app.post("/ListSessions")
def list_sessions(req: api.RequestListSessions) -> api.ResponseListSessions:
    return svc.list_sessions(req)


@app.post("/SendMessage")
async def send_message(req: api.RequestSendMessage) -> api.ResponseSendMessage:
    return svc.send_message(req)
