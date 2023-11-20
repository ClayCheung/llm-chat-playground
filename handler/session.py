import json
import uuid
from typing import List

from models.session import Session
import schema.api as api


def from_api_session(req: api.RequestCreateSession) -> Session:
    """
    convert api session (without id) to model session (with uuid type id)
    :param req:
    :return:
    """
    return Session(
        id=uuid.uuid4().hex,
        user_id=req.user_id,
        session_params=json.dumps(req.session_params),
        agent_id=req.agent.id,
        agent_params=json.dumps(req.agent.params),
    )


def to_api_session_list(objs: List[Session]) -> List[api.Session]:
    api_sessions = []
    for obj in objs:
        api_session = to_api_session(obj)
        api_sessions.append(api_session)
    return api_sessions


def to_api_session(obj: Session) -> api.Session:
    """
     convert model session to api session
    :param obj:
    :return:
    """
    return api.Session(
        id=str(obj.id),
        user_id=obj.user_id,
        session_params=json.loads(obj.session_params),
        agent=api.Agent(
            id=obj.agent_id,
            params=json.loads(obj.agent_params),
        ),
    )
