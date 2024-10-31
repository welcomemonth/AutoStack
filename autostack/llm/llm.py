import litellm
from typing import Optional, Union

from segmapy.configs.config import config
from segmapy.configs.llm_config import LLMConfig
from segmapy.llm.schema import Message

class LLM:
    
    llmconfig: LLMConfig = config.llm
    system_prompt = "You are a helpful assistant."

    def completion(self, messages: Union[str, Message, list[dict], list[Message], list[str]]):
        return litellm.completion(
            model=self.llmconfig.model, 
            messages=self.format_msg(messages), 
            api_base=self.llmconfig.base_url,
        )

    def format_msg(self, messages: Union[str, Message, list[dict], list[Message], list[str]]) -> list[dict]:
        """convert messages to list[dict]."""

        if not isinstance(messages, list):
            messages = [messages]

        processed_messages = []
        for msg in messages:
            if isinstance(msg, str):
                processed_messages.append({"role": "user", "content": msg})
            elif isinstance(msg, dict):
                assert set(msg.keys()) == set(["role", "content"])
                processed_messages.append(msg)
            elif isinstance(msg, Message):
                processed_messages.append(msg.to_dict())
            else:
                raise ValueError(
                    f"Only support message type are: str, Message, dict, but got {type(messages).__name__}!"
                )
        return processed_messages


if __name__ == "__main__":
    llm = LLM()
    print(llm.format_msg("hello"))
    print(llm.format_msg(Message(content="hello")))
    print(llm.format_msg([Message(content="hello"), Message(content="world")]))
    print(llm.format_msg([{"role": "user", "content": "hello"}, {"role": "system", "content": "world"}]))
    print(llm.format_msg(["hello", "world"]))
    print(llm.format_msg([{"role": "user", "content": "hello"}, "world"]))
    print(llm.format_msg([Message(content="hello"), "world"]))
    print(llm.format_msg([Message(content="hello"), {"role": "system", "content": "world"}]))
    print(llm.completion("介绍一下你自己").choices[0].message.content)
