import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


class TimeTracker(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.tasks = {}
        self.current_task = None
        self.elapsed_time = timedelta()
        self.timer_running = False
        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.task_label = tk.Label(self, text="Task:")
        self.task_combo = ttk.Combobox(self)
        self.task_combo.bind("<<ComboboxSelected>>", self.on_task_selected)
        self.start_btn = tk.Button(self, text="Start", command=self.start_timer, state="disabled")
        self.pause_btn = tk.Button(self, text="Pause", command=self.pause_timer, state="disabled")
        self.stop_btn = tk.Button(self, text="Stop", command=self.stop_timer, state="disabled")
        self.time_label = tk.Label(self, text="00:00:00")

        # Create layout
        task_layout = tk.Frame(self)
        self.task_label.pack(side="left")
        self.task_combo.pack(side="left")
        task_layout.pack(pady=5)

        button_layout = tk.Frame(self)
        self.start_btn.pack(side="left", padx=5)
        self.pause_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)
        button_layout.pack(pady=5)

        self.time_label.pack(pady=5)

        # Set timer
        self.timer_interval = 1000  # milliseconds
        self.last_update = datetime.now()

    def on_task_selected(self, event):
        self.current_task = self.task_combo.get()
        if self.current_task:
            self.start_btn.config(state="normal")
        else:
            self.start_btn.config(state="disabled")

    def start_timer(self):
        self.timer_running = True
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.last_update = datetime.now()

    def pause_timer(self):
        self.timer_running = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="normal")
        self.elapsed_time += datetime.now() - self.last_update

    def stop_timer(self):
        self.timer_running = False
        self.pause_btn.config(state="disabled")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="disabled")
        self.task_combo.set("")
        self.elapsed_time += datetime.now() - self.last_update

        # Save time data
        if self.current_task:
            print(f"Task: {self.current_task}, Time: {self.elapsed_time}")

        # Reset elapsed time and timer state
        self.elapsed_time = timedelta()
        self.current_task = None

    def update_time_label(self):
        try:
            if self.timer_running:
                now = datetime.now()
                self.elapsed_time += now - self.last_update
                self.last_update = now
            self.time_label.config(text=str(self.elapsed_time)[:8])
        except Exception as e:
            print(f"Error updating time label: {e}")
        finally:
            self.time_label.after(self.timer_interval, self.update_time_label)

    def populate_task_combo(self, tasks):
        self.task_combo["values"] = tasks

    def run(self):
        # Create GUI
        self.master.title("Time Tracker")
        self.master.resizable(False, False)
        self.pack()

        # Populate task combo
        tasks = ["Task 1", "Task 2", "Task 3"]
        self.populate_task_combo(tasks)
