from sqlalchemy import Column, Integer, String, UUID, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Session(Base):
    """
    1 human talk to 1 agent session
    """

    __tablename__ = "session"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    session_params = Column(Text)
    agent_id = Column(String(20), index=True)
    agent_params = Column(Text)
