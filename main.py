import tkinter as tk
from time_tracker import TimeTracker

# Create the root window
root = tk.Tk()

# Create an instance of the TimeTracker class
app = TimeTracker(master=root)

# Run the application
app.run()

# Start the event loop
root.mainloop()
