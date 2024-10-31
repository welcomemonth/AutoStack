import os
from pathlib import Path
from typing import Dict, Iterable, List, Literal, Optional

from pydantic import BaseModel, model_validator
from segmapy.configs.llm_config import LLMConfig, LLMType
from segmapy.utils.yaml_model import YamlModel
from segmapy.const import CONFIG_ROOT

class Config(YamlModel):
    """Configurations for BaseAPI"""

    # Key Parameters
    llm: LLMConfig

    # Global Proxy. Will be used if llm.proxy is not set
    proxy: str = ""



    @classmethod
    def default(cls):
        """Load default config
        - Priority: env < default_config_paths
        - Inside default_config_paths, the latter one overwrites the former one
        """
        default_config_paths: List[Path] = [
            CONFIG_ROOT / "config/config.yaml",
            CONFIG_ROOT / "config.yaml",
        ]

        dicts = [dict(os.environ)]
        dicts += [Config.read_yaml(path) for path in default_config_paths]
        final = merge_dict(dicts)
        return Config(**final)

    @classmethod
    def from_llm_config(cls, llm_config: dict):
        """user config llm
        example:
        llm_config = {"api_type": "xxx", "api_key": "xxx", "model": "xxx"}
        gpt4 = Config.from_llm_config(llm_config)
        A = Role(name="A", profile="Democratic candidate", goal="Win the election", actions=[a1], watch=[a2], config=gpt4)
        """
        llm_config = LLMConfig.model_validate(llm_config)
        dicts = [dict(os.environ)]
        dicts += [{"llm": llm_config}]
        final = merge_dict(dicts)
        return Config(**final)


def merge_dict(dicts: Iterable[Dict]) -> Dict:
    """Merge multiple dicts into one, with the latter dict overwriting the former"""
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result


config = Config.default()
