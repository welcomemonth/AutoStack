import os
from typing import List, Optional, Union
from pydantic import BaseModel


class Attribute(BaseModel):
    """
    {
        "name": "id",
        "type": "String",
        "required": True,
        "comment": "用户ID"
    }
    """
    name: str
    type: str
    required: bool
    comment: str

    @staticmethod
    def get_schema():
        return {
            "name": "属性名称",
            "type": "属性类型",
            "required": "属性是否必须",
            "comment": "属性注释",
        }

    @property
    def serialize(self):
        return self.model_dump()


class Entity(BaseModel):
    name: str
    description: str
    attributes: List[Attribute] = None

    @property
    def serialize(self):
        # exclude={"entity_name"}采用这个可以去除一些属性
        return self.model_dump(exclude={})

    @staticmethod
    def get_schema():
        return {
            "name": "实体名称",
            "description": "实体描述",
            "attributes": [Attribute.get_schema()]
        }


# 项目内置接口类
class ModuleApi(BaseModel):
    name: str
    description: Union[str, None] = None
    # 参数
    params: List[str] = []
    return_type: str

    @staticmethod
    def get_schema():
        return {
            "name": "接口名称",
            "description": "接口描述",
            "params": ["参数1", "参数2"],
            "return_type": "返回类型"
        }


class Module(BaseModel):
    name: str
    description: Union[str, None] = None
    entity: Entity
    created: Optional[bool] = False  # 模块是否已经创建
    # 模块接口列表
    apis: List[ModuleApi] = []

    @staticmethod
    def get_schema():
        return {
            "name": "模块名称",
            "description": "模块描述",
            "apis": [ModuleApi.get_schema()],
            "entities": [Entity.get_schema()]
        }

    @property
    def serialize(self):
        return self.model_dump(exclude={"created"})


if __name__ == "__main__":
    print(Module.get_schema())


