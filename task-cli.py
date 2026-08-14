import argparse

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
add = subparsers.add_parser("add", help="Add a task")
update = subparsers.add_parser("update", help="Update a task according (ID)")
delete = subparsers.add_parser("delete", help="Delete a task (ID)")
mark_in_progress = subparsers.add_parser("mark-in-progress", help="Marks a task as in-progress")
mark_done = subparsers.add_parser("mark-done", help="Marks a task as done")
lists = subparsers.add_parser("list", help="List all tasks")


add.add_argument("task", type=str, help="Task Description")\




args = parser.parse_args()

print(args.add)