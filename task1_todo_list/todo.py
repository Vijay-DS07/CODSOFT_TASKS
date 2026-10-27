"""To-Do List application (CodSoft Python Internship - Task 1).

Command-line app to create, update, and track to-do items.
Tasks are saved to todo_data.json so they persist between runs.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo_data.json")


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def show_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet.")
        return
    print()
    for t in tasks:
        mark = "x" if t["done"] else " "
        print(f"{t['id']:>3}. [{mark}] {t['title']}")
    print()


def pick_task(tasks):
    """Ask the user for a task ID and return the matching task, or None."""
    try:
        task_id = int(input("Enter task ID: ").strip())
    except ValueError:
        print("Please enter a valid number.")
        return None
    for t in tasks:
        if t["id"] == task_id:
            return t
    print(f"No task with ID {task_id}.")
    return None


def add_task(tasks):
    title = input("Task description: ").strip()
    if not title:
        print("Task cannot be empty.")
        return
    tasks.append({"id": next_id(tasks), "title": title, "done": False})
    save_tasks(tasks)
    print("Task added.")


def update_task(tasks):
    task = pick_task(tasks)
    if task is None:
        return
    new_title = input(f"New description (blank keeps '{task['title']}'): ").strip()
    if new_title:
        task["title"] = new_title
        save_tasks(tasks)
        print("Task updated.")
    else:
        print("No change made.")


def toggle_done(tasks):
    task = pick_task(tasks)
    if task is None:
        return
    task["done"] = not task["done"]
    save_tasks(tasks)
    status = "completed" if task["done"] else "marked as not done"
    print(f"Task {status}.")


def delete_task(tasks):
    task = pick_task(tasks)
    if task is None:
        return
    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted.")


def main():
    tasks = load_tasks()
    menu = """
========== TO-DO LIST ==========
1. View tasks
2. Add task
3. Update task
4. Mark done / not done
5. Delete task
6. Exit
================================"""
    actions = {
        "2": add_task,
        "3": update_task,
        "4": toggle_done,
        "5": delete_task,
    }
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice == "1":
            show_tasks(tasks)
        elif choice in actions:
            actions[choice](tasks)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
