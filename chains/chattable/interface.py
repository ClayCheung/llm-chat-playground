from typing import Optional, Dict
from abc import ABC, abstractmethod

from langchain.schema.messages import BaseMessage

from schema.api import Session


class Chattable(ABC):
    session: Optional[Session]

    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def chat(self, message: BaseMessage) -> BaseMessage:
        pass

    @classmethod
    def agent(cls) -> str:
        return cls.session.agent.id
