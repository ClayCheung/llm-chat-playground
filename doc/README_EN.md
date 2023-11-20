# llm-chat-playground

`llm-chat-playground` is a platform for publishing and using chat applications based on LLM agents. In user experience,
the function is similar to poe.com
A chatbot platform that allows users to create sessions with and chat with designated proxies. In terms of developer
publishing, developers can contribute to the repository
[Chattable Agent](#chattable), allowing users to create sessions with these proxies. The opposite llm-chat-playground is
responsible for multi-user management, session management, token
Auditing, caching, multi-agent sessions, etc., developers only need to focus on the internal logic of the agent (the
chain of thought).

It is built using the following technologies:

- 🧠 Langchain: Building applications with LLMs through composability
- 🔥 AutoGen (planned): Developing LLM applications with multiple agents
- ⚡️ FastAPI: A modern, fast web framework for building high-performance APIs.
- 🗄 SQLAlchemy: A powerful SQL toolset and object-relational mapping (ORM) library for Python.
- 🐍 Python 3.11: a programming language for backend development.

## Features

1. 🤝 multi-user support: Supports multiple users, allowing them to create sessions with agents.
2. 📇 session creation: Users can create a session with a specific agent to personalize the conversation (by adjusting
   the parameters of the current session or the parameters of the agent or agent of the current session).
3. 💬 chat logs: Users can chat with agents in a session, and the framework supports storing and reading historical chat
   logs.
4. 🤖 [Chattable Agent](#chattable) Contribution: Developers can contribute [Chattable Agent] (#chattable) to the
   repository to provide users with more choices.
5. 🔒 large model call caching: Calls to large models use caching to improve performance and efficiency.
6. 📊 session-based token metering (planned): Token usage in each session will be tracked to provide more accurate
   metering for resource management and billing.
7. 📂 Chattable serialization (planned): The planned feature will enable serialization of Chattable objects for better
   storage and management.
8. 🔥 multi-agent sessions (planned): Framework-supported multi-agent sessions that bring multiple agents into a session,
   and these agents can talk to each other to solve tasks.

## Advantages

- 🚀 simplify development: Developers can focus on building [Chattable Agent](#chattable) and its capabilities without
  worrying about complex trade-offs for user management, session management, and chat log storage.
- ⚙️ Quick Release: Product ideas can go online quickly
- 🌟 user experience: session management, auditing, caching and other capabilities support the basic user experience.

## Quick start

To start using the llm-chat-playground backend service, follow these steps:

1. 📥 clone repositories from [GitHub](https://github.com/ClayCheung/llm-chat-playground).
2. ⚙️ use `pip install -r requirements.txt` to install the required dependencies.
3. 🛠 configure necessary settings, such as database connections and API keys.
4. ▶️ use `python main.py` to run the application.
5. 🌐 access the back end API endpoint to interact with the application.

    ```shell
    curl --location '127.0.0.1:8080/CreateSession' \
    --header 'Content-Type: application/json' \
    --data '{
        "user_id": 1,
        "agent": {
            "id": "simple_openai_agent"
        }
    }'
    ```

    ```shell
    curl --location '127.0.0.1:8080/ListSessions' \
    --header 'Content-Type: application/json' \
    --data '{
      "user_id": 1
    }'
    ```

    ```shell
    curl --location '127.0.0.1:8080/SendMessage' \
    --header 'Content-Type: application/json' \
    --data '{
      "session_id": "b36a53ea-b37d-4ea4-9c56-47a4195eb88f",
      "content": "What was the first thing I said?"
    }'
    ```

## Concept

### Chattable

Loose interfaces mean you can implement chattable agents in a variety of ways, such as langchain, autogen, xagent, or
custom implementations

```python
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
```

### Current Chattable agents

| agent id            | 介绍                            | 仓库连接                                                                                   |
|---------------------|-------------------------------|----------------------------------------------------------------------------------------|
| fake_echo_agent     | a fake echo proxy for testing | https://github.com/ClayCheung/llm-chat-playground/blob/main/chains/fake_echo_agent     |
| simple_openai_agent | a simple openAI agent         | https://github.com/ClayCheung/llm-chat-playground/blob/main/chains/simple_openai_agent |

## Roadmap

- [ ] Added implementation of Chattable proxy
- [ ] Use redis llm to call cache, currently in memory cache
- [ ] Support session token metering
- [ ] Support multi-agent sessions
- [ ] Automatic summary of chat records
- [ ] Chattable or Session Serialization

## License

LLM chat application back end based on [MIT license](https://opensource.org/licenses/MIT)
See the [LICENSE](https://github.com/ClayCheung/llm-chat-playground/blob/main/LICENSE) file for more details