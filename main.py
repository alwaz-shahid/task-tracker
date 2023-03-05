import tkinter as tk
from time_tracker import TimeTracker

root = tk.Tk()
app = TimeTracker(None)
app.pack()
root.mainloop()
