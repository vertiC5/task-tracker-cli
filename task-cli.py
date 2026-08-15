import argparse
import os
from dataclasses import dataclass, asdict
import json
from datetime import datetime

@dataclass
class Task:
    task: str
    id: int
    status: str
    createdAt: str
    updatedAt: str

    def __init__(self, task):
        self.task = task
        self.id = self._id_counter()
        self.status = "todo"
        self.createdAt = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.updatedAt = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def _id_counter():
        current_id = 0
        if not os.path.exists('counter.txt') or os.path.getsize('counter.txt') == 0:
            new_id = current_id + 1
            with open('counter.txt', 'w') as f:
                f.write(str(new_id))
                return new_id

        elif os.path.exists('counter.txt') and os.path.getsize('counter.txt') > 0:
            with open('counter.txt', 'r') as f:
                current_id = int(f.read())
            new_id = current_id + 1
            with open('counter.txt', 'w') as f:
                f.write(str(new_id))
            return new_id

        else: #all else fails
            return current_id + 1

def init_func(arg):
    while True:
        msg = input("Are you sure you want to initialize the task tracker? This will delete all existing tasks. (Y/N): ")
        if msg.lower() == "y":
            os.remove("tasks.json") if os.path.exists("tasks.json") else None
            os.remove("counter.txt") if os.path.exists("counter.txt") else None
            print("Task tracker initialized.")
            return None

        elif msg.lower() == "n":
            print("Initialization cancelled.")
            return None
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

def add_func(arg):
    task_list = []
    new_task = Task(arg.task)
    print(new_task)
    if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 2:
        with open("tasks.json", "r") as f:
            task_list = json.load(f)
            task_list.append(asdict(new_task))
    else:
        task_list.append(asdict(new_task))

    with open("tasks.json", "w") as f:
        json.dump(task_list, f, indent=4)
    print(f"Task added successfully. (ID:{new_task.id})")

def update_func(arg):
    try:
        if os.path.exists("tasks.json") and os.path.getsize("tasks.json") > 2:
            with open("tasks.json", "r") as f:
                task_list = json.load(f)
                task_match = next(task for task in task_list if task["id"] == arg.id)
                if task_match:
                    task_match["task"] = arg.task
                    task_match["updatedAt"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    with open("tasks.json", "w") as file:
                        json.dump(task_list, file, indent=4)
                    return
                else:
                    print(f"Task with ID {arg.id} not found.")
        else:
            print("No tasks found. Please add a task first.")
    except StopIteration:
        print(f"Task with ID {arg.id} not found.")

def delete_func(arg):
    try:
        with open("tasks.json", "r") as f:
            task_list = json.load(f)
        task_match = next(task for task in task_list if task["id"] == arg.id)
        if task_match:
            task_list.remove(task_match)
            with open("tasks.json", "w") as f:
                json.dump(task_list, f, indent=4)
            print(f"Task with ID {arg.id} deleted successfully.")
        else:
            print(f"Task with ID {arg.id} not found.")
    except StopIteration:
        print(f"Task with ID {arg.id} not found.")

def mark_in_progress_func(arg):
    try:
        with open("tasks.json", "r") as f:
            task_list = json.load(f)
        task_match = next(task for task in task_list if task["id"] == arg.id)
        if task_match:
            task_match["status"] = "in-progress"
            task_match["updatedAt"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            with open("tasks.json", "w") as f:
                json.dump(task_list, f, indent=4)
        else:
            print(f"Task with ID {arg.id} not found.")
    except StopIteration:
        print(f"Task with ID {arg.id} not found.")

def mark_done_func(arg):
    try:
        with open("tasks.json", "r") as f:
            task_list = json.load(f)
        task_match = next(task for task in task_list if task["id"] == arg.id)
        if task_match:
            task_match["status"] = "done"
            task_match["updatedAt"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            with open("tasks.json", "w") as f:
                json.dump(task_list, f, indent=4)
        else:
            print(f"Task with ID {arg.id} not found.")
    except StopIteration:
        print(f"Task with ID {arg.id} not found.")

def mark_todo_func(arg):
    try:
        with open("tasks.json", "r") as f:
            task_list = json.load(f)
        task_match = next(task for task in task_list if task["id"] == arg.id)
        if task_match:
            task_match["status"] = "todo"
            task_match["updatedAt"] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            with open("tasks.json", "w") as f:
                json.dump(task_list, f, indent=4)
        else:
            print(f"Task with ID {arg.id} not found.")
    except StopIteration:
        print(f"Task with ID {arg.id} not found.")

def list_func(arg):
    with open("tasks.json", "r") as f:
        task_list = json.load(f)
    if arg.status == "todo":
        task_match = [task for task in task_list if task["status"] == "todo"]
    elif arg.status == "in-progress":
        task_match = [task for task in task_list if task["status"] == "in-progress"]
    elif arg.status == "done":
        task_match = [task for task in task_list if task["status"] == "done"]
    else:
        task_match = task_list

    print("ID: Task - status")
    for task in task_match:
        print(f"{task['id']}: {task['task']} - {task['status']} (Created: {task['createdAt']}, Updated: {task['updatedAt']})")

parser = argparse.ArgumentParser(description="Task Tracker CLI")
subparsers = parser.add_subparsers()

# Initialize Command
init = subparsers.add_parser('init', help='Initialize task tracker')
init.set_defaults(func=init_func)

# Add Command
add = subparsers.add_parser('add', help='Add a new task')
add.add_argument('task', type=str, help = 'Task detail to add')
add.set_defaults(func=add_func)

# Update Command
update = subparsers.add_parser('update', help='Update a task by ID')
update.add_argument('id', type=int, help='ID of the task to update')
update.add_argument('task', type=str, help='Updated task detail')
update.set_defaults(func=update_func)

# Delete Command
delete = subparsers.add_parser('delete', help='Delete a task by ID')
delete.add_argument('id', type=int, help='ID of the task to delete')
delete.set_defaults(func=delete_func)

# mark-in-progress command
mark_in_progress = subparsers.add_parser('mark-in-progress', help='Mark a task as in progress by ID')
mark_in_progress.add_argument('id', type=int, help='ID of the task to mark as in progress')
mark_in_progress.set_defaults(func=mark_in_progress_func)

# mark-done command
mark_done = subparsers.add_parser('mark-done', help='Mark a task as done by ID')
mark_done.add_argument('id', type=int, help='ID of the task to mark as done')
mark_done.set_defaults(func=mark_done_func)

# mark-to do command
mark_todo = subparsers.add_parser('mark-todo', help='Mark a task as to do by ID')
mark_todo.add_argument('id', type=int, help='ID of the task to mark as to do')
mark_todo.set_defaults(func=mark_todo_func)

# list command
list_cmd = subparsers.add_parser('list', help='List all tasks')
list_cmd.add_argument("status", nargs='?', type=str, choices=["done", "todo", "in-progress"], help='Filter by status')
list_cmd.set_defaults(func=list_func)

args = parser.parse_args()
args.func(args)

