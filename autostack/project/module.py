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


class Module(BaseModel):
    name: str
    description: str
    attributes: List[Attribute] = None
    summary: Optional[str] = None
    created: Optional[bool] = False

    @property
    def serialize(self):
        # exclude={"entity_name"}采用这个可以去除一些属性
        return self.model_dump(exclude={"summary", "created"})

    @staticmethod
    def get_schema():
        return {
            "name": "模块名称",
            "description": "模块描述",
            "attributes": [Attribute.get_schema()]
        }


if __name__ == "__main__":
    print(Module.get_schema())


