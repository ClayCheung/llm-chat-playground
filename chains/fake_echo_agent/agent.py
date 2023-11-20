from langchain.schema.messages import BaseMessage, AIMessage

from schema.api import Session
from chains.chattable import Chattable


class FakeEchoAgent(Chattable):
    def __init__(self, session: Session):
        super().__init__(session)

    def chat(self, message: BaseMessage) -> BaseMessage:
        return AIMessage(content=message.content)

    @classmethod
    def agent(cls) -> str:
        return "fake_echo_agent"
