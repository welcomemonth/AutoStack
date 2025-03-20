import os
from openai import OpenAI
from typing import Optional, Union
from dotenv import load_dotenv
from autostack.common.const import ROOT
from .schema import Message
from autostack.common.logs import logger

load_dotenv(ROOT / "autostack" / "env" / "llm.env")


class LLM:
    def __init__(self, api_key: Optional[str] = None, 
                 base_url: Optional[str] = None, 
                 system_prompt: Optional[str] = None,
                 model: Optional[str] = None
                 ):
        
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.system_prompt = system_prompt or os.getenv("LLM_SYSTEM_PROMPT", "You are a helpful assistant.")
        self.model = model or os.getenv("LLM_MODEL", "gpt-4o")
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def completion(self, messages: Union[str, Message, list[dict], list[Message], list[str]]):
        logger.info(f"LLM completion with messages: \n{messages}")
        resp = self.client.chat.completions.create(
            model=self.model, 
            messages=self.format_msg(messages),
            timeout=600
        )
        result = resp.choices[0].message.content
        # # 适配 deepseek
        # if "<think>" in result:
        #     logger.info(f"LLM completion response: {result.split('</think>')[0].split('<think>')[1]}")
        #     result = result.split("</think>")[1]
        #     # logger.info(f"LLM completion response: {result}")
        return result

    def format_msg(self, messages: Union[str, Message, list[dict], list[Message], list[str]]) -> list[dict]:
        """convert messages to list[dict]."""

        if not isinstance(messages, list):
            messages = [messages]

        processed_messages = []
        for msg in messages:
            if isinstance(msg, str):
                processed_messages.append({"role": "user", "content": msg})
            elif isinstance(msg, dict):
                assert set(msg.keys()) == {"role", "content"}
                processed_messages.append(msg)
            elif isinstance(msg, Message):
                processed_messages.append(msg.to_dict())
            else:
                raise ValueError(
                    f"Only support message type are: str, Message, dict, but got {type(messages).__name__}!"
                )
        # add system prompt
        processed_messages.insert(0, {"role": "system", "content": self.system_prompt})
        return processed_messages

