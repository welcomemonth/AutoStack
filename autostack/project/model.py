import os
from typing import List, Optional, Union
from pathlib import Path
from pydantic import BaseModel
from autostack.prompt import prompt_handle
from autostack.utils import singleton, parse_code_block, tree
from autostack.const import DEFAULT_WORKSPACE_ROOT
from autostack.llm import LLM
from autostack.logs import logger
from autostack.template_handler import NestModuleTemplateHandler, NestProjectTemplateHandler


# class Module(BaseModel):
#     entity_name: str
#     description: str
#     attributes: List[Attribute] = None
#
#     @property
#     def serialize(self):
#         # exclude={"entity_name"}采用这个可以去除一些属性
#         return self.model_dump()
