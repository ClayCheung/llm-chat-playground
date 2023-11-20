from typing import Optional, Dict, List
from pydantic import BaseModel


class Agent(BaseModel):
    id: str
    params: Optional[Dict[str, str]]


class Session(BaseModel):
    id: str
    user_id: str
    session_params: Optional[Dict[str, str]]
    agent: Agent


class RequestCreateSession(BaseModel):
    user_id: str
    session_params: Optional[Dict[str, str]]
    agent: Agent


class ResponseCreateSession(BaseModel):
    id: str


class RequestListSessions(BaseModel):
    user_id: str


class ResponseListSessions(BaseModel):
    items: List[Session]


class RequestSendMessage(BaseModel):
    session_id: str
    content: str
    """The string contents of the message."""

    additional_kwargs: Optional[Dict[str, str]]
    """Any additional information."""


class ResponseSendMessage(BaseModel):
    content: str
    """The string contents of the message."""

    additional_kwargs: Optional[Dict[str, str]]
    """Any additional information."""

    type: str
