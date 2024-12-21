from datetime import datetime
import uuid
from enum import Enum
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
        return self.dict()

    @model_validator(mode='before')
    def check_task_id(cls, values):
        if not values.get('id'):
            values['id'] = uuid.uuid4().hex
        return values


# 定义一个type的枚举类型，有文件和命令两种
class ActionType(Enum):
    FILE = "file"
    COMMAND = "command"


class Action(BaseModel):
    type: ActionType = Field(default=ActionType.FILE)
    content: str
    result: str

    def to_dict(self):
        return {
            "type": self.type.value,
            "content": self.content,
            "result": self.result
        }


class Task(BaseModel):
    task_id: str = ""
    task_desc: str = ""  # 具体的任务描述
    result: list[Action] = ""
    is_success: bool = False
    is_finished: bool = False

    @model_validator(mode='before')
    @classmethod
    def check_task_id(cls, values):
        if not values.get('task_id'):
            values['task_id'] = uuid.uuid4().hex
        return values

    def reset(self, task_desc: str):
        """重置任务，如果任务执行失败，或者根据之前执行的历史需要调整任务"""
        self.task_desc = task_desc
        self.result = []
        self.is_finished = False
        self.is_success = False
        return self

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_desc": self.task_desc,
            "result": [action.to_dict() for action in self.result],
            "is_success": self.is_success,
            "is_finished": self.is_finished
        }

    def get_task_desc(self):
        return {
            "task_id": self.task_id,
            "task_desc": self.task_desc,
        }


class Plan(BaseModel):
    goal: str = ""
    context: str = ""  # FIXME 计划是否需要上下文
    tasks: list[Task] = []
    current_task_id: str = ""

    is_success: bool = False
    is_finished: bool = False
    is_refined: bool = False

    @property
    def current_task(self) -> Task:
        """ 根据current_task_id 在任务列表中查找当前任务 """
        return next((task for task in self.tasks if task.task_id == self.current_task_id), None)

    def add_tasks(self, tasks: list[Task]):
        """
            为计划添加任务
        Args:
            tasks (list[Task]): A list of tasks (may be unordered) to add to the plan.

        Returns:
            None: The method updates the internal state of the plan but does not return anything.
        """
        if not tasks:
            return

        # Topologically sort the new tasks to ensure correct dependency order
        new_tasks = tasks

        if not self.tasks:
            # If there are no existing tasks, set the new tasks as the current tasks
            self.tasks = new_tasks
        else:
            self.tasks.append(*new_tasks)
        self._update_current_task()

    def add_task(self, new_task: Task):
        """
        Append a new task to the end of existing task sequences

        Args:
            new_task (Task): The new task to be appended to the existing task sequence

        Returns:
            None
        """
        self.tasks.append(new_task)
        self._update_current_task()

    def _update_current_task(self):
        current_task_id = ""
        for task in self.tasks:
            if not task.is_finished:
                current_task_id = task.task_id
                break
        self.current_task_id = current_task_id  # all tasks finished

    def finish_current_task(self):
        """Finish current task, set Task.is_finished=True, set current task to next task"""
        if self.current_task_id:
            self.current_task.is_finished = True
            self._update_current_task()  # set to next task

    def get_finished_tasks(self) -> list[Task]:
        """return all finished tasks in correct linearized order

        Returns:
            list[Task]: list of finished tasks
        """
        return [task for task in self.tasks if task.is_finished]

    # 获取未完成的任务列表
    def get_unfinished_tasks(self) -> list[Task]:
        """return all unfinished tasks in correct linearized order"""
        return [task for task in self.tasks if not task.is_finished]


if __name__ == "__main__":
    msg = Message(content="hello")
    print(msg.to_dict())


