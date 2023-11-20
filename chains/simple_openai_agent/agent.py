import dotenv

from langchain.schema.messages import BaseMessage
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

import memory
from schema.api import Session
from chains.chattable import Chattable
import store

_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI:"""


class SimpleOpenaiAgent(Chattable):
    def __init__(self, session: Session):
        super().__init__(session)
        dotenv.load_dotenv()
        self.llm = ChatOpenAI()

        prompt = ChatPromptTemplate.from_template(_TEMPLATE)

        history = memory.ORMChatMessageHistory(
            self.session.id, store.SQLALCHEMY_DATABASE_URL
        ).k_messages_as_string(5)
        print(history)

        self.chain = (
            {
                "history": ChatPromptTemplate.from_template(history),
                "input": RunnablePassthrough(),
            }
            | prompt
            | self.llm
        )

    def chat(self, message: BaseMessage) -> BaseMessage:
        return self.chain.invoke(input=message.content)

    @classmethod
    def agent(cls) -> str:
        return "simple_openai_agent"
