from typing import Dict, Type

from schema.api import Session
from chains.chattable import Chattable
from chains.fake_echo_agent import FakeEchoAgent
from chains.simple_openai_agent import SimpleOpenaiAgent

chattable_mapping: Dict[str, Type[Chattable]] = {}

chattable_list = [FakeEchoAgent, SimpleOpenaiAgent]


def get_chattable_map():
    if len(chattable_mapping) == len(chattable_list):
        return chattable_mapping
    for c in chattable_list:
        chattable_mapping[c.agent()] = c

    return chattable_mapping


def load_chattable(session: Session) -> Chattable:
    """

    :param session:
    :return:
    """

    # get session.agent.id
    agent_id = session.agent.id

    # find the Chattable implementation class based on the mapping relationship
    chattable_class = get_chattable_map().get(agent_id)

    if chattable_class:
        # init Chattable implementation classes base on session parameters
        chattable_instance = chattable_class(session=session)
        return chattable_instance
    else:
        raise ErrorChattable(
            f"no corresponding Chattable implementation class found by agent: {agent_id}"
        )


class ErrorChattable(Exception):
    pass
