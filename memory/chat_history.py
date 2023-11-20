from typing import List

from langchain.memory.chat_message_histories.sql import SQLChatMessageHistory
from langchain.schema.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    messages_to_dict,
)
from langchain.schema.messages import get_buffer_string
import models


class ORMChatMessageHistory(SQLChatMessageHistory):
    """
    Using custom message table name,
    custom session id field name,
    custom model Message < = > langchain BaseMessage conversion function
    """

    def __init__(
        self,
        session_id: str,
        connection_string: str,
    ):
        super().__init__(
            session_id,
            connection_string,
            models.TABLE_MESSAGE_STORE,
            models.COLUMN_SESSION_ID,
            models.CustomMessageConverter(),
        )

    def add_user_message(self, message: str) -> None:
        """Convenience method for adding a human message string to the store.

        Args:
            message: The string contents of a human message.
        """
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        """Convenience method for adding an AI message string to the store.

        Args:
            message: The string contents of an AI message.
        """
        self.add_message(AIMessage(content=message))

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in db"""
        message = models.message.add_create_time(message)
        with self.Session() as session:
            session.add(self.converter.to_sql_model(message, self.session_id))
            session.commit()

    def k_messages(self, k: int) -> List[BaseMessage]:
        """Retrieve the latest k messages from the database"""
        with self.Session() as session:
            result = (
                session.query(self.sql_model_class)
                .where(
                    getattr(self.sql_model_class, self.session_id_field_name)
                    == self.session_id
                )
                .order_by(self.sql_model_class.create_at.desc())
                .limit(k)  # Limit the result to k records
                .all()
            )

            messages = []
            for record in reversed(result):  # Reverse the order of the result
                messages.append(self.converter.from_sql_model(record))
            return messages

    def k_messages_as_string(self, k: int) -> str:
        return get_buffer_string(self.k_messages(k))
