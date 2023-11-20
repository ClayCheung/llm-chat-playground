# llm-chat-playground

`llm-chat-playground` 是一款为`基于 LLM 代理的聊天应用`提供发布和使用便利的平台。从用户体验角度来看，其功能类似于 poe.com 的聊天机器人平台，
用户可通过该平台创建与特定代理的会话并实现对话交流。从开发人员发布角度出发，开发人员可向仓库贡献他们的 [Chattable代理](#chattable)，
从而使用户能够使用与这些代理创建会话。而`llm-chat-playground` 则承担了多用户管理、会话管理、token 审计、缓存管理以及多代理会话支持等相关任务，
开发人员只需专注于实现代理的内部逻辑（即思维链的构建）。

它使用以下技术构建：

- 🧠 Langchain：通过可组合性使用LLM构建应用程序
- 🔥 AutoGen（计划中）: 使用多个代理开发LLM应用程序
- ⚡️ FastAPI：用于构建高性能 API 的现代、快速的 Web 框架。
- 🗄 SQLAlchemy：用于 Python 的强大 SQL 工具集和对象关系映射（ORM）库。
- 🐍 Python 3.11：用于后端开发的编程语言。

## 主要功能

1. 🤝 多用户支持：支持多个用户，允许他们与代理创建会话。
2. 📇 会话创建：用户可以与特定代理创建会话，进行个性化对话（通过调整当前会话的参数或当前会话的代理或代理的参数）。
3. 💬 聊天记录：用户可以在会话中与代理进行聊天，并且由框架支持存储和读取历史聊天记录。
4. 🤖[Chattable 代理](#chattable) 贡献：开发者可以向仓库贡献 [Chattable 代理](#chattable)，为用户提供更多选择。
5. 🔒 大模型调用缓存：对大模型的调用使用缓存，以提高性能和效率。
6. 📊 基于会话的 token 计量（计划中）：将跟踪每个会话中的 token 使用量，为资源管理和计费提供更精确的计量。
7. 📂 Chattable 序列化（计划中）：计划中的功能，将实现 Chattable 对象的序列化，以便更好地存储和管理。
8. 🔥 多 Agent 会话（计划中）：框架支持的多 agent 会话，将多个 agent 引入一个会话，这些 agent 可以相互交谈以解决任务。

## 优点

- 🚀 简化开发：开发者可以专注于构建 [Chattable 代理](#chattable) 及其功能，无需担心用户管理、会话管理和聊天记录存储的复杂性。
- ⚙️ 快速发布：产品构想可以快速上线
- 🌟 用户体验：会话管理、审计、缓存等能力支撑了基本的用户使用体验。

## 快速入门

要开始使用 LLM 聊天应用后端，请按照以下步骤操作：

1. 📥 从 [GitHub](https://github.com/ClayCheung/llm-chat-playground) 克隆仓库。
2. ⚙️ 使用 `pip install -r requirements.txt` 安装所需的依赖项。
3. 🛠 配置必要的设置，如数据库连接和 API 密钥。
4. ▶️ 使用 `python main.py` 运行应用程序。
5. 🌐 访问后端 API 端点与应用程序进行交互。
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

## 概念

### Chattable

- 松散的接口意味着你可以使用各种方式来实现 chattable agent, 诸如 langchain, autogen, xagent, agents 或者自定义实现等等

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

目前已有的 Chattable 代理

| agent id            | 介绍                  | 仓库连接                                                                                   |
|---------------------|---------------------|----------------------------------------------------------------------------------------|
| fake_echo_agent     | 一个用于测试的假的 echo 代理   | https://github.com/ClayCheung/llm-chat-playground/blob/main/chains/fake_echo_agent     |
| simple_openai_agent | 一个最简易的 openai agent | https://github.com/ClayCheung/llm-chat-playground/blob/main/chains/simple_openai_agent |

## Roadmap

- [ ] 增加 Chattable 代理的实现
- [ ] 使用 redis llm 调用缓存，目前是 in memory cache
- [ ] 支持会话的 token 计量
- [ ] 支持多 agents 的会话
- [ ] 聊天记录的自动汇总
- [ ] Chattable or Session 序列化

## 许可证

LLM 聊天应用后端基于 [MIT 许可证](https://opensource.org/licenses/MIT)
。请参阅 [LICENSE](https://github.com/ClayCheung/llm-chat-playground/blob/main/LICENSE) 文件以获取更多详细信息。
