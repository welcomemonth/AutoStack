from datetime import datetime
import uuid
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    field_serializer,
    field_validator,
    model_serializer,
    model_validator,
)


class SimpleMessage(BaseModel):
    content: str
    role: str


class Message(BaseModel):
    content: str
    role: str = "user"  # system / user / assistant
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))
    id: str = Field(default="", validate_default=True)

    def to_dict(self):
        return self.model_dump()
    
    @field_validator("id", mode="before")
    @classmethod
    def check_id(cls, id: str) -> str:
        return id if id else uuid.uuid4().hex
    

if __name__ == "__main__":
    msg = Message(content="hello")
    print(msg.to_dict())
          

