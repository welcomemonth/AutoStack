class Project:
    def __init__(self, project_name, project_manager):
        self.project_name = project_name  # 项目名称
        self.project_manager = project_manager  # 项目经理
        self.tasks = []  # 用于存储任务
        self.team_members = []  # 用于存储项目团队成员

    def add_task(self, task_name, task_description, assignee, status='Not Started'):
        """添加任务"""
        task = {
            'task_name': task_name,
            'task_description': task_description,
            'assignee': assignee,
            'status': status
        }
        self.tasks.append(task)

    def update_task_status(self, task_name, status):
        """更新任务状态"""
        for task in self.tasks:
            if task['task_name'] == task_name:
                task['status'] = status
                print(f"Task '{task_name}' status updated to {status}.")
                return
        print(f"Task '{task_name}' not found.")

    def add_team_member(self, member_name, role):
        """添加团队成员"""
        member = {'member_name': member_name, 'role': role}
        self.team_members.append(member)

    def remove_team_member(self, member_name):
        """移除团队成员"""
        self.team_members = [member for member in self.team_members if member['member_name'] != member_name]

    def project_summary(self):
        """打印项目概览"""
        print(f"Project Name: {self.project_name}")
        print(f"Project Manager: {self.project_manager}")
        print(f"Start Date: {self.start_date}")
        print(f"End Date: {self.end_date}")
        print("\nTasks:")
        for task in self.tasks:
            print(f"  Task: {task['task_name']}, Assigned to: {task['assignee']}, Status: {task['status']}")
        print("\nTeam Members:")
        for member in self.team_members:
            print(f"  {member['member_name']} ({member['role']})")

# 示例使用
project = Project("AI Project", "Alice")

# 添加团队成员
project.add_team_member("Bob", "Developer")
project.add_team_member("Charlie", "Tester")

# 添加任务
project.add_task("Design Architecture", "Design the system architecture.", "Bob")
project.add_task("Implement Feature X", "Develop Feature X.", "Charlie")

# 更新任务状态
project.update_task_status("Design Architecture", "In Progress")

# 打印项目概览
project.project_summary()

# 移除团队成员
project.remove_team_member("Charlie")

# 打印项目概览
project.project_summary()
