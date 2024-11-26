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
    entity_name: str
    description: str
    attributes: List[Attribute] = None
    summary: Optional[str] = None

    @property
    def serialize(self):
        # exclude={"entity_name"}采用这个可以去除一些属性
        return self.model_dump()


if __name__ == "__main__":
    print(Attribute.get_schema())


