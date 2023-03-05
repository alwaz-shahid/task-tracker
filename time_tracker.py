import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime, timedelta
import csv


class Task:
    """Class to represent a task"""

    def __init__(self, name):
        self.name = name
        self.total_time = timedelta(seconds=0)
        self.start_time = None

    def start(self):
        """Start the task timer"""
        self.start_time = datetime.now()

    def stop(self):
        """Stop the task timer and update total time"""
        if self.start_time:
            end_time = datetime.now()
            elapsed_time = end_time - self.start_time
            self.total_time += elapsed_time
            self.start_time = None

    def reset(self):
        """Reset the task timer"""
        self.total_time = timedelta(seconds=0)
        self.start_time = None

    def resume(self):
        """Resume the task timer"""
        self.start_time = datetime.now()


class TimeTracker(tk.Tk):
    """Class to represent the main TimeTracker app"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # Initialize task variables
        self.tasks = {}
        self.current_task = None

        # Initialize timer variables
        self.elapsed_time = timedelta(seconds=0)
        self.start_time = None
        self.timer_label = None

        # Initialize UI elements
        self.start_btn = None
        self.pause_btn = None
        self.stop_btn = None
        self.resume_btn = None
        self.task_name_entry = None
        self.task_listbox = None
        self.task_list = []

        # Create and configure the UI
        self._create_widgets()

    def _create_widgets(self):
        """Create and configure the UI elements"""

        # Task selection frame
        task_frame = ttk.Frame(self)
        task_frame.pack(padx=10, pady=10)

        ttk.Label(task_frame, text="Select or create a task:").grid(row=0, column=0, sticky="w")

        # Create the task combo box
        self.task_var = tk.StringVar(value="")
        self.task_combo = ttk.Combobox(task_frame, textvariable=self.task_var, state="readonly")
        self.task_combo.grid(row=1, column=0, pady=5, sticky="we")

        # Create the new task button
        ttk.Button(task_frame, text="New Task", command=self.create_task).grid(row=1, column=1, padx=5)

        # Create the task name entry box and create task button
        self.task_name_var = tk.StringVar()
        self.task_name_entry = ttk.Entry(task_frame, textvariable=self.task_name_var)
        self.task_name_entry.grid(row=2, column=0, pady=5, sticky="we")
        ttk.Button(task_frame, text="Create Task", command=self.create_task_from_entry).grid(row=2, column=1, padx=5)

        # Create the task list box and delete task button
        self.task_listbox = tk.Listbox(task_frame)
        self.task_listbox.grid(row=3, column=0, columnspan=2, pady=5, sticky="we")
        ttk.Button(task_frame, text="Deletetask", command=self.delete_task).grid(row=4, column=0, pady=5, sticky="we")

        # Timer frame
        timer_frame = ttk.Frame(self)
        timer_frame.pack(padx=10, pady=10)

        # Create the timer label
        self.timer_label = ttk.Label(timer_frame, text="00:00:00", font=("Helvetica", 36))
        self.timer_label.pack()

        # Create the start button
        self.start_btn = ttk.Button(timer_frame, text="Start", command=self.start_timer)
        self.start_btn.pack(side="left", padx=5)

        # Create the pause button
        self.pause_btn = ttk.Button(timer_frame, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_btn.pack(side="left", padx=5)

        # Create the stop button
        self.stop_btn = ttk.Button(timer_frame, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # Create the resume button
        self.resume_btn = ttk.Button(timer_frame, text="Resume", command=self.resume_timer, state="disabled")
        self.resume_btn.pack(side="left", padx=5)

        # Load tasks from CSV file
        self.load_tasks()

    def create_task(self):
        """Create a new task"""
        task_name = simpledialog.askstring("New Task", "Enter a name for the new task:")
        if task_name:
            task = Task(task_name)
            self.tasks[task_name] = task
            self.task_var.set(task_name)
            self.update_task_list()

    def create_task_from_entry(self):
        """Create a new task from the entry box"""
        task_name = self.task_name_var.get()
        if task_name:
            task = Task(task_name)
            self.tasks[task_name] = task
            self.task_var.set(task_name)
            self.task_name_var.set("")
            self.update_task_list()

    def delete_task(self):
        """Delete the selected task"""
        selected_task = self.task_listbox.get(tk.ACTIVE)
        if selected_task:
            del self.tasks[selected_task]
            self.update_task_list()
            self.task_var.set("")
            self.task_name_var.set("")

    def update_task_list(self):
        """Update the task list box"""
        self.task_list = list(self.tasks.keys())
        self.task_list.sort()
        self.task_combo["values"] = self.task_list
        self.task_listbox.delete(0, tk.END)
        for task_name in self.task_list:
            self.task_listbox.insert(tk.END, task_name)

    def start_timer(self):
        """Start the timer"""
        self.start_time = datetime.now()
        self.start_btn["state"] = "disabled"
        self.pause_btn["state"] = "normal"
        self.stop_btn["state"] = "normal"
        self.current_task = self.tasks.get(self.task_var.get())
        if self.current_task:
            self.current_task.start()
        self.update_timer()

    def pause_timer(self):
        """Pause the timer"""
        self.elapsed_time += datetime.now() - self.start_time
        self.start_time = None
        self.pause_btn["state"] = "disabled"
        self.resume_btn["state"] = "normal"

    def stop_timer(self):
        """Stop the timer"""
        # Update the current task
        if self.current_task:
            self.current_task.stop()

        # Update the elapsed time
        self.elapsed_time += datetime.now() - self.start_time

        # Update the UI
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.resume_btn.config(state="disabled")

        # Reset the timer
        self.start_time = None
        self.elapsed_time = timedelta(seconds=0)

        # Update the timer label
        self.update_timer_label()

        # Save the task data
        self.save_tasks()

    def resume_timer(self):
        """Resume the timer"""
        # Update the current task
        if self.current_task:
            self.current_task.resume()

        # Set the start time
        self.start_time = datetime.now()

        # Update the UI
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.resume_btn.config(state="disabled")

        # Update the timer label
        self.update_timer_label()

    def update_timer_label(self):
        """Update the timer label"""
        if self.start_time:
            elapsed_time = self.elapsed_time + datetime.now() - self.start_time
            elapsed_time_str = str(elapsed_time).split(".")[0]
            self.timer_label.config(text=elapsed_time_str)

        self.after(1000, self.update_timer_label)

    def load_tasks(self):
        """Load the task data from a CSV file"""
        try:
            with open("tasks.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    task_name = row[0]
                    task_total_time = timedelta(seconds=int(row[1]))
                    task = Task(task_name)
                    task.total_time = task_total_time
                    self.tasks[task_name] = task
                    self.update_task_list()
        except FileNotFoundError:
            pass

    def save_tasks(self):
        """Save the task data to a CSV file"""
        with open("tasks.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for task in self.tasks.values():
                row = [task.name, int(task.total_time.total_seconds())]
                writer.writerow(row)
