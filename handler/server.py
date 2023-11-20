import logging

from langchain.schema import HumanMessage, BaseMessage
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from fastapi import Depends
from sqlalchemy import orm

import models
import store
from schema import api
import chains
import memory
from handler import session
from chains import Chattable


class SessionService:
    db: orm.Session

    def __init__(self, db: Depends(store.get_db())):
        self.db = db

        # TODO use redis cache
        set_llm_cache(InMemoryCache())

    def _load_chattable(self, session_id: str) -> Chattable:
        """

        :param session_id:
        :return:
        """
        model_session = self._get_session(session_id)
        return chains.load_chattable(session=session.to_api_session(model_session))

    def _get_session(self, session_id: str) -> models.Session:
        db = self.db
        item = db.query(models.Session).get({"id": session_id})

        return item

    def send_message(self, req: api.RequestSendMessage) -> api.ResponseSendMessage:
        # init chat message history with orm provider
        chat_history = memory.ORMChatMessageHistory(
            req.session_id, store.SQLALCHEMY_DATABASE_URL
        )

        # load chat-able of current session
        chattable = self._load_chattable(req.session_id)

        if req.additional_kwargs is None:
            req.additional_kwargs = {}
        input = HumanMessage(
            content=req.content, additional_kwargs=req.additional_kwargs
        )

        # save chat input to chat message history
        chat_history.add_message(input)

        output = {}
        try:
            output = chattable.chat(message=input)
        except Exception as e:
            logging.error(
                f"Failed to chat on chattable agent {chattable.agent}. Error: {e}"
            )

        # save chat output to chat message history
        chat_history.add_message(output)

        return api.ResponseSendMessage(
            content=output.content,
            type=output.type,
            additional_kwargs=output.additional_kwargs,
        )

    def create_session(
        self, req: api.RequestCreateSession
    ) -> api.ResponseCreateSession:
        db = self.db
        session_obj = session.from_api_session(req)
        db.add(session_obj)
        self.db.commit()

        return api.ResponseCreateSession(id=str(session_obj.id))

    def list_sessions(self, req: api.RequestListSessions) -> api.ResponseListSessions:
        db = self.db

        items = (
            db.query(models.Session).filter(models.Session.user_id == req.user_id).all()
        )

        return api.ResponseListSessions(items=session.to_api_session_list(items))
