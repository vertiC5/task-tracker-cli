import argparse
import json
import os
import sys


class Task:
    def __init__(self, task):
        self.id = self._id_counter()
        self.task_name = task
        self.status = "todo"
        self.createdAt = "test"
        self.updatedAt = "test"

    @staticmethod
    def _id_counter():
        counter_path = "counter.txt"
        if os.path.exists(counter_path) and os.path.getsize(counter_path) > 0:
            with open(counter_path, 'r') as file:
                current_id = int(file.read())
                if current_id:
                    return current_id + 1
                else:
                    return 0
        else:
            with open(counter_path, 'w') as file:
                file.write("0")
            return 0

def add_func(arg):
    json_path = "tasks.json"
    new_task = Task(arg.task)

    if os.path.exists(json_path) and os.path.getsize(json_path) > 2:
        with open(json_path, 'r') as file:
            tasks = json.load(file)

    else:
        tasks = []
    new_task = Task(arg.task)
    tasks.append(new_task)
    print(vars(new_task))

    with open(json_path, 'w') as file:
        json.dump(tasks, file, default=vars)

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
add = subparsers.add_parser("add", help="Add a task")
update = subparsers.add_parser("update", help="Update a task according (ID)")
delete = subparsers.add_parser("delete", help="Delete a task (ID)")
mark_in_progress = subparsers.add_parser("mark-in-progress", help="Marks a task as in-progress")
mark_done = subparsers.add_parser("mark-done", help="Marks a task as done")
lists = subparsers.add_parser("list", help="List all tasks")

add.add_argument("task", type=str, help="Task Description")
add.set_defaults(func=add_func)

args = parser.parse_args()
args.func(args)
