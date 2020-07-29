from tkinter import *
from tkinter import ttk

# Creating the root window, and adding some properties
root = Tk()
root.title("PS Calculator")
root.geometry("800x600")


def center(window):
    """Center a Tkinter window"""
    window.update_idletasks()

    # Find the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Find new (x, y) coordinates
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width/2 - 5 * size[0] / 9
    y = screen_height/2 - 3 * size[1] / 5

    # Apply new coordinates
    window.geometry("+%d+%d" % (x, y))


center(root)

# Making a style to make the tabs right-aligned
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='ne')

# Setting the style to the notebook, and making it resizable with the parent window
notebook = ttk.Notebook(root, style='lefttab.TNotebook')
notebook.pack(fill="both", expand=1, pady=15, padx=15)

# Creating the tabs to be inserted in the notebook
calculation_frame = Frame(notebook, width=600, height=800)
saved_calculations_frame = Frame(notebook, width=600, height=800)

# Packing the tabs
calculation_frame.pack(fill="both", expand=1)
saved_calculations_frame.pack(fill="both", expand=1)

# Adding the tabs to the notebook
notebook.add(saved_calculations_frame, text="الدفتر")
notebook.add(calculation_frame, text="الحساب")

# Selecting the "Calculation_frame"
notebook.select(1)

# Creating Labels
start_label = Label(calculation_frame, text='البداية')
end_label = Label(calculation_frame, text='النهاية')

# Creating Spinboxes
hour_end_spinbox = Spinbox(calculation_frame, from_=1, to=12)
minute_end_spinbox = Spinbox(calculation_frame, from_=1, to=59)
hour_start_spinbox = Spinbox(calculation_frame, from_=1, to=12)
minute_start_spinbox = Spinbox(calculation_frame, from_=1, to=59)

# Packing the labels and spinboxes
start_label.pack(side=RIGHT, padx=5, pady=10, anchor='n', expand=True)
minute_start_spinbox.pack(side=RIGHT, padx=5, pady=10, anchor='n', expand=True)
hour_start_spinbox.pack(side=RIGHT, padx=5, pady=10, anchor='n', expand=True)
end_label.pack(side=RIGHT, padx=5, pady=10, anchor='n', expand=True)
minute_end_spinbox.pack(side=RIGHT, padx=5, pady=10, anchor='n', expand=True)
hour_end_spinbox.pack(side=RIGHT, padx=5, pady=10, anchor='n', expand=True)

# Keep the root window running
root.mainloop()
