from datetime import datetime
import json
from typing import Any

from langchain.schema.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ChatMessage,
    FunctionMessage,
)
from langchain.memory.chat_message_histories.sql import BaseMessageConverter
from sqlalchemy import Column, Integer, UUID, Text, DateTime

from models.base import Base


TABLE_MESSAGE_STORE = "message_store"
COLUMN_SESSION_ID = "session_id"


class Message(Base):
    __tablename__ = TABLE_MESSAGE_STORE
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID, index=True)
    message = Column(Text)
    create_at = Column(DateTime, index=True)


def add_create_time(msg: BaseMessage) -> BaseMessage:
    if msg.additional_kwargs.get("create_at") is None:
        msg.additional_kwargs["create_at"] = datetime.timestamp(datetime.now())
    return msg


class CustomMessageConverter(BaseMessageConverter):
    """The custom message converter for SQLChatMessageHistory."""

    def __init__(self):
        self.model_class = Message

    def from_sql_model(self, sql_message: Any) -> BaseMessage:
        return _message_from_dict(json.loads(sql_message.message))

    def to_sql_model(self, message: BaseMessage, session_id: str) -> Any:
        return self.model_class(
            session_id=session_id,
            create_at=datetime.fromtimestamp(
                message.additional_kwargs.get("create_at")
            ),
            message=json.dumps(_message_to_dict(message)),
        )

    def get_sql_model_class(self) -> Any:
        return self.model_class


def _message_from_dict(message: dict) -> BaseMessage:
    _type = message["type"]
    if _type == "human":
        return HumanMessage(**message["data"])
    elif _type == "ai":
        return AIMessage(**message["data"])
    elif _type == "system":
        return SystemMessage(**message["data"])
    elif _type == "chat":
        return ChatMessage(**message["data"])
    elif _type == "function":
        return FunctionMessage(**message["data"])
    else:
        raise ValueError(f"Got unexpected message type: {_type}")


def _message_to_dict(message: BaseMessage) -> dict:
    return {"type": message.type, "data": message.dict()}
