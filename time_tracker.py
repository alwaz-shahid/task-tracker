import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class TimeTracker(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.tasks = {}
        self.current_task = None
        self.init_ui()

    def init_ui(self):
        # Set window size
        self.master.geometry("500x400")

        # Create widgets
        self.task_label = tk.Label(self, text="Task:")
        self.task_entry = tk.Entry(self)
        self.task_entry.bind("<Return>", self.add_task)
        self.task_list = tk.Listbox(self, selectmode="SINGLE", height=10, width=40)
        self.task_list.bind("<<ListboxSelect>>", self.on_task_selected)
        self.start_btn = tk.Button(self, text="Start", command=self.start_timer, state="disabled")
        self.pause_btn = tk.Button(self, text="Pause", command=self.pause_timer, state="disabled")
        self.stop_btn = tk.Button(self, text="Stop", command=self.stop_timer, state="disabled")
        self.time_label = tk.Label(self, text="00:00:00", font=("Arial", 36))

        # Create layout
        task_layout = tk.Frame(self)
        self.task_label.pack(side="left")
        self.task_entry.pack(side="left")
        task_layout.pack(pady=5)

        task_list_layout = tk.Frame(self)
        self.task_list.pack(side="left")
        task_list_layout.pack(pady=5)

        button_layout = tk.Frame(self)
        self.start_btn.pack(side="left", padx=5)
        self.pause_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)
        button_layout.pack(pady=5)

        self.time_label.pack(pady=20)

        # Set timer
        self.timer_interval = 1000  # milliseconds
        self.last_update = datetime.now()

    def add_task(self, event):
        task_name = self.task_entry.get()
        if task_name:
            self.tasks[task_name] = {"elapsed_time": timedelta(), "running": False}
            self.task_list.insert("end", task_name)
            self.task_entry.delete(0, "end")

    def on_task_selected(self, event):
        selected_task = self.task_list.get(self.task_list.curselection())
        self.current_task = selected_task
        if self.tasks[selected_task]["running"]:
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")

    def start_timer(self):
        self.tasks[self.current_task]["running"] = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.last_update = datetime.now()

    def pause_timer(self):
        self.tasks[self.current_task]["running"] = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.tasks[self.current_task]["elapsed_time"] += datetime.now() - self.last_update

    def stop_timer(self):
        self.tasks[self.current_task]["running"] = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.task_list.selection_clear(0, "end")
        self.tasks[self.current.task]["elapsed_time"] += datetime.now() - self.last_update
        self.task_list.selection_clear(0, "end")
        self.current_task = None

    def update_timer(self):
        if self.current_task is not None and self.tasks[self.current_task]["running"]:
            elapsed_time = self.tasks[self.current_task]["elapsed_time"] + (datetime.now() - self.last_update)
        else:
            elapsed_time = timedelta()

        self.time_label.configure(text=str(elapsed_time))

        self.after(self.timer_interval, self.update_timer)

    # Add the following method to create a new task with a unique name
    def create_new_task(self):
        i = 1
        task_name = f"Task {i}"
        while task_name in self.tasks:
            i += 1
            task_name = f"Task {i}"
        self.tasks[task_name] = {"elapsed_time": timedelta(), "running": False}
        self.task_list.insert("end", task_name)

    # Add the following method to remove the currently selected task
    def remove_task(self):
        if self.current_task is not None:
            self.tasks.pop(self.current_task)
            self.task_list.delete(self.task_list.curselection())
            self.current_task = None

    # Modify the add_task method to check for existing task names and create a new task with a unique name if needed
    def add_task(self, event):
        task_name = self.task_entry.get()
        if task_name:
            if task_name in self.tasks:
                task_name = f"{task_name} (1)"
                while task_name in self.tasks:
                    task_name = f"{task_name[:-3]}{int(task_name[-2]) + 1})"
            self.tasks[task_name] = {"elapsed_time": timedelta(), "running": False}
            self.task_list.insert("end", task_name)
            self.task_entry.delete(0, "end")

    # Modify the on_task_selected method to enable/disable buttons based on the selected task's state
    def on_task_selected(self, event):
        selected_task = self.task_list.get(self.task_list.curselection())
        self.current_task = selected_task
        if self.tasks[selected_task]["running"]:
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")

    # Modify the start_timer method to create a new task with a unique name if no task is currently selected
    def start_timer(self):
        if self.current_task is None:
            self.create_new_task()
            self.current_task = self.task_list.get("end")
            self.task_list.selection_clear(0, "end")
            self.task_list.select_set(self.task_list.size() - 1)

        self.tasks[self.current_task]["running"] = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.last_update = datetime.now()

    # Add the following method to stop all running tasks
    def stop_all(self):
        for task_name in self.tasks:
            self.tasks[task_name]["running"] = False
            self.tasks[task_name]["elapsed_time"] += datetime.now() - self.last_update

        self.current_task = None
        self.task_list.selection_clear(0, "end")
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")

    # Modify the init_ui method to include new widgets and rearrange the layout
    def init_ui(self):
        # Set window size
        self.master.geometry("500x400")

        # Create widgets
        self.task_label = tk.Label(self, text="Task:")
        self.task_entry = tk.Entry(self)
        self.task_entry.bind("<Return>", self.add_task)
        self.task_list = tk.Listbox(self, selectmode="SINGLE", height=10, width=40)
        self.task_list.bind("<<ListboxSelect>>", self.on_task_selected)
        self.start_btn = tk.Button(self, text="Start", command=self.start_timer, state="disabled")
        self.pause_btn = tk.Button(self, text="Pause", command=self.pause_timer, state="disabled")
        self.stop_btn = tk.Button(self, text="Stop", command=self.stop_timer, state="disabled")
        self.time_label = tk.Label(self, text="00:00:00", font=("Arial", 36))

        # Create layout
        task_layout = tk.Frame(self)
        self.task_label.pack(side="left")
        self.task_entry.pack(side="left")
        task_layout.pack(pady=5)

        task_list_layout = tk.Frame(self)
        self.task_list.pack(side="left")
        task_list_layout.pack(pady=5)

        button_layout = tk.Frame(self)
        self.start_btn.pack(side="left", padx=5)
        self.pause_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)
        button_layout.pack(pady=5)

        self.time_label.pack(pady=20)

        # Set timer
        self.timer_interval = 1000  # milliseconds
        self.last_update = datetime.now()

        # Create task-specific widgets
        self.task_name_label = tk.Label(self, text="Task Name:")
        self.task_name_entry = tk.Entry(self)
        self.task_time_label = tk.Label(self, text="00:00:00", font=("Arial", 24))
        self.task_start_btn = tk.Button(self, text="Start", command=self.start_timer, state="disabled")
        self.task_pause_btn = tk.Button(self, text="Pause", command=self.pause_timer, state="disabled")
        self.task_stop_btn = tk.Button(self, text="Stop", command=self.stop_timer, state="disabled")

        # Create task-specific layout
        task_name_layout = tk.Frame(self)
        self.task_name_label.pack(side="left")
        self.task_name_entry.pack(side="left")
        task_name_layout.pack(pady=5)

        task_time_layout = tk.Frame(self)
        self.task_time_label.pack()
        task_time_layout.pack(pady=10)

        task_button_layout = tk.Frame(self)
        self.task_start_btn.pack(side="left", padx=5)
        self.task_pause_btn.pack(side="left", padx=5)
        self.task_stop_btn.pack(side="left", padx=5)
        task_button_layout.pack(pady=5)

        # Hide task-specific widgets initially
        self.task_name_label.pack_forget()
        self.task_name_entry.pack_forget()
        self.task_time_label.pack_forget()
        self.task_start_btn.pack_forget()
        self.task_pause_btn.pack_forget()
        self.task_stop_btn.pack_forget()

    # Modify the add_task method to include a task name parameter
    def add_task(self, event=None, task_name=None):
        if task_name is None:
            task_name = self.task_entry.get()

        if task_name:
            self.tasks[task_name] = {"elapsed_time": timedelta(), "running": False}
            self.task_list.insert("end", task_name, " - 00:00:00")
            self.task_entry.delete(0, "end")

    def on_task_selected(self, event=None):
        selected_task = self.task_list.get(self.task_list.curselection())
        self.current_task = selected_task
        if self.tasks[selected_task]["running"]:
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")
        self.update_time_label()

    def start_timer(self):
        self.tasks[self.current_task]["running"] = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.last_update = datetime.now()

    def pause_timer(self):
        self.tasks[self.current_task]["running"] = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.tasks[self.current_task]["elapsed_time"] += datetime.now() - self.last_update
        self.update_time_label()

    def stop_timer(self):
        self.tasks[self.current_task]["running"] = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.task_list.selection_clear(0, "end")
        self.tasks[self.current_task]["elapsed_time"] += datetime.now() - self.last_update
        self.update_time_label()

    def update_time_label(self):
        if self.current_task:
            time_str = str(self.tasks[self.current_task]["elapsed_time"])
        else:
            time_str = "00:00:00"
        self.time_label.config(text=time_str)

    def delete_task(self):
        selected_task = self.task_list.get(self.task_list.curselection())
        self.task_list.delete(self.task_list.curselection())
        del self.tasks[selected_task]
        self.current_task = None
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.update_time_label()



