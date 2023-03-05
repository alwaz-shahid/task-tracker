import datetime

tasks = {}

def start_timer(task_name):
    tasks[task_name] = {"start_time": datetime.datetime.now(), "elapsed_time": datetime.timedelta(0)}

def stop_timer(task_name):
    task = tasks.get(task_name)
    if task:
        task["elapsed_time"] += datetime.datetime.now() - task["start_time"]
        print(f"Task: {task_name}, Time: {str(task['elapsed_time'])[:-4]}")
        del tasks[task_name]
    else:
        print(f"No timer found for task {task_name}")

def list_tasks():
    for task_name, task in tasks.items():
        elapsed_time = str(task['elapsed_time'])[:-4]
        print(f"Task: {task_name}, Time: {elapsed_time}")

def main():
    while True:
        command = input("Enter command (start, stop, list, quit): ").lower()
        if command == "quit":
            break
        elif command == "list":
            list_tasks()
        elif command == "start":
            task_name = input("Enter task name: ")
            start_timer(task_name)
        elif command == "stop":
            task_name = input("Enter task name: ")
            stop_timer(task_name)
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
