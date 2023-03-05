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
        ttk.Button(task_frame, text="Delete Task", command=self.delete_task).grid(row=4, column=1, padx=5)

        # Timer frame
        timer_frame = ttk.Frame(self)
        timer_frame.pack(padx=10, pady=10)

        self.timer_var = tk.StringVar(value="00:00:00")
        self.timer_label = ttk.Label(timer_frame, textvariable=self.timer_var, font=("Helvetica",    50))
        self.timer_label.pack()

        # Create the timer buttons
        self.start_btn = ttk.Button(timer_frame, text="Start", command=self.start_timer)
        self.start_btn.pack(side="left", padx=5)
        self.pause_btn = ttk.Button(timer_frame, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(timer_frame, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # Load tasks from file
        self.load_tasks()

        # Update the task list box
        self.update_task_list()

    def load_tasks(self):
        """Load saved tasks from file"""
        try:
            with open("tasks.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    task_name, total_seconds_str = row
                    total_seconds = int(total_seconds_str)
                    self.tasks[task_name] = Task(task_name)
                    self.tasks[task_name].total_time = timedelta(seconds=total_seconds)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        """Save tasks to file"""
        with open("tasks.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for task in self.tasks.values():
                writer.writerow([task.name, task.total_time.total_seconds()])

    def update_task_list(self):
        """Update the task list box with the current task names"""
        self.task_listbox.delete(0, tk.END)
        self.task_list = list(self.tasks.keys())
        self.task_list.sort()
        for task_name in self.task_list:
            self.task_listbox.insert(tk.END, task_name)

    def create_task(self):
        """Create a new task with the name in the task_name_entry box"""

        task_name = self.task_name_var.get()

        if not task_name:
            messagebox.showerror("Error", "Please enter a task name")
            return

        # Create the task object
        task = Task(task_name)

        # Add the task to the task list and combo box
        self.tasks[task.name] = task
        self.task_list.append(task.name)
        self.task_combo["values"] = self.task_list

        # Clear the task name entry box
        self.task_name_var.set("")

        # Select the new task in the combo box
        self.task_combo.set(task.name)

    def create_task_from_entry(self):
        """Create a new task with the name in the task_name_entry box"""

        task_name = self.task_name_var.get()

        if task_name in self.tasks:
            messagebox.showerror("Error", "Task already exists")
            return

        # Create the task object
        task = Task(task_name)

        # Add the task to the task list and combo box
        self.tasks[task.name] = task
        self.task_list.append(task.name)
        self.task_combo["values"] = self.task_list

        # Clear the task name entry box
        self.task_name_var.set("")

        # Select the new task in the combo box
        self.task_combo.set(task.name)

    def delete_task(self):
        """Delete the selected task"""

        task_name = self.task_var.get()

        if not task_name:
            messagebox.showerror("Error", "Please select a task to delete")
            return

        # Confirm task deletion with user
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the task '{task_name}'?")

        if confirm:
            # Delete the task from the task list and combo box
            del self.tasks[task_name]
            self.task_list.remove(task_name)
            self.task_combo["values"] = self.task_list

            # Clear the task selection and reset the timer
            self.task_var.set("")
            self.reset_timer()

    def start_timer(self):
        """Start the timer for the current task"""

        # Check if a task is selected
        task_name = self.task_var.get()
        if not task_name:
            messagebox.showerror("Error", "Please select a task")
            return

        # Check if the timer is already running
        if self.start_time:
            messagebox.showerror("Error", "Timer is already running")
            return

        # Start the timer
        self.current_task = self.tasks[task_name]
        self.current_task.start()
        self.start_time = datetime.now()

        # Configure the UI
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="enabled")
        self.stop_btn.config(state="enabled")

    def create_task_from_entry(self):
        """Create a new task with the name in the task_name_entry box"""
        task_name = self.task_name_var.get()

        if not task_name:
            messagebox.showerror("Error", "Please enter a task name")
            return

        # Create the task object
        task = Task(task_name)

        # Add the task to the tasks dictionary
        if task_name in self.tasks:
            messagebox.showerror("Error", f"A task with the name '{task_name}' already exists.")
        else:
            self.tasks[task_name] = task
            self.update_task_list()
            self.task_name_var.set("")
            self.task_combo.set(task_name)
            messagebox.showinfo("Task Created", f"The task '{task_name}' has been created.")

    def delete_task(self):
        """Delete the currently selected task"""

        task_name = self.task_var.get()

        if not task_name:
            messagebox.showerror("Error", "Please select a task to delete")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the task '{task_name}'?")

        if confirm:
            del self.tasks[task_name]
            self.update_task_list()
            self.task_combo.set("")
            messagebox.showinfo("Task Deleted", f"The task '{task_name}' has been deleted.")

    def start_timer(self):
        """Start the task timer"""

        # Get the selected task
        task_name = self.task_var.get()

        if not task_name:
            messagebox.showerror("Error", "Please select a task to start")
            return

        # Stop the current task if there is one
        if self.current_task:
            self.current_task.stop()
            self.elapsed_time += datetime.now() - self.start_time
            self.start_time = None
            self.timer_var.set(str(self.elapsed_time).split(".")[0])

        # Start the selected task
        self.current_task = self.tasks[task_name]
        self.current_task.start()

        # Update the UI
        self.start_btn.configure(state="disabled")
        self.pause_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")
        self.start_time = datetime.now()

    def pause_timer(self):
        """Pause the task timer"""

        # Stop the current task
        self.current_task.stop()
        self.elapsed_time += datetime.now() - self.start_time
        self.start_time = None

        # Update the UI
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        self.pause_btn.configure(text="Resume", command=self.resume_timer)
        self.stop_btn.configure(state="disabled")
    def stop_timer(self):
        """Stop the task timer"""

        # Stop the current task
        self.current_task.stop()
        self.elapsed_time += datetime.now() - self.start_time
        self.start_time = None

        # Update the task total time
        self.current_task.total_time += self.elapsed_time

        # Update the UI
        self.start_btn.configure(state="normal")
        self.pause_btn.configure(state="disabled")
        self.stop_btn.configure(state="disabled")
        self.timer_var.set("00:00:00")

        # Reset the elapsed time
        self.elapsed_time = timedelta(seconds=0)

        # Save the tasks
        self.save_tasks()

        # Update the task list
        self.update_task_list()

    # def create_task(self):
    #     """Create a new task with the name selected in the task combo box"""
    #     task_name = self.task_var.get()
    #     if task_name not in self.tasks:
    #         self.tasks[task_name] = Task(task_name)
    #     self.update_task_list()
    #
    # def create_task_from_entry(self):
    #     """Create a new task with the name entered in the task name entry box"""
    #     task_name = self.task_name_var.get()
    #     if task_name and task_name not in self.tasks:
    #         self.tasks[task_name] = Task(task_name)
    #     self.update_task_list()
    #
    # def delete_task(self):
    #     """Delete the selected task from the task list"""
    #     task_name = self.task_listbox.get(tk.ACTIVE)
    #     if task_name in self.tasks:
    #         del self.tasks[task_name]
    #         self.update_task_list()
    #
    # def start_timer(self):
    #     """Start the timer for the selected task"""
    #     task_name = self.task_var.get()
    #     if task_name and task_name in self.tasks:
    #         self.current_task = self.tasks[task_name]
    #         self.start_time = datetime.now()
    #         self.start_btn.config(state="disabled")
    #         self.pause_btn.config(state="normal")
    #         self.stop_btn.config(state="normal")
    #         self.task_combo.config(state="disabled")
    #         self.task_name_entry.config(state="disabled")
    #         self.current_task.start()
    #         self.update_timer()
    #
    # def pause_timer(self):
    #     """Pause the timer for the selected task"""
    #     self.current_task.stop()
    #     self.start_btn.config(state="normal")
    #     self.pause_btn.config(state="disabled")
    #     self.stop_btn.config(state="normal")
    #     self.task_combo.config(state="readonly")
    #     self.task_name_entry.config(state="normal")
    #
    # def stop_timer(self):
    #     """Stop the timer for the selected task"""
    #     self.current_task.stop()
    #     self.elapsed_time += datetime.now() - self.start_time
    #     self.start_time = None
    #     self.start_btn.config(stat.grid(row=0, column=0)
