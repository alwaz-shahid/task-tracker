import tkinter as tk
from time_tracker import TimeTracker

root = tk.Tk()
app = TimeTracker(root)
app.pack()
root.mainloop()
