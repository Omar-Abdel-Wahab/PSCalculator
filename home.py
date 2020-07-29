from tkinter import *
from tkinter import ttk
from tkinter.font import Font

# Creating the root window, and adding some properties
root = Tk()
root.title("PS Calculator")
root.geometry("1024x768")


def center(window):
    """Center a Tkinter window"""
    window.update_idletasks()

    # Find the screen resolution
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Find new (x, y) coordinates
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width/2 - 7 * size[0] / 13
    y = screen_height/2 - 6 * size[1] / 11

    # Apply new coordinates
    window.geometry("+%d+%d" % (x, y))


center(root)


def add_item():
    added_item_name_label = Label(items_frame, text='المشروب/ المأكول')
    added_item_name_var = StringVar()
    added_item_combobox = ttk.Combobox(items_frame, textvariable=item_name_var)
    added_item_quantity_label = Label(items_frame, text='الكمية')
    added_item_quantity_spinbox = Spinbox(items_frame, from_=0, font=Font(size=11))


# Making a style to make the tabs right-aligned
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='ne')

# Setting the style to the notebook, and making it resizable with the parent window
notebook = ttk.Notebook(root, style='lefttab.TNotebook')
notebook.pack(fill="both", expand=1, pady=30, padx=15)

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

# Creating Frames for hours and minutes
time_frame = Frame(calculation_frame)
hour_start_frame = Frame(time_frame)
minute_start_frame = Frame(time_frame)
hour_end_frame = Frame(time_frame)
minute_end_frame = Frame(time_frame)

# Creating Labels for hours and minutes
hour_start_label = Label(hour_start_frame, text='الساعة')
minute_start_label = Label(minute_start_frame, text='الدقيقة')
hour_end_label = Label(hour_end_frame, text='الساعة')
minute_end_label = Label(minute_end_frame, text='الدقيقة')

# Creating Labels for start and end
start_label = Label(time_frame, text='البداية')
end_label = Label(time_frame, text='النهاية')

# Creating Spinboxes
hour_end_spinbox = Spinbox(hour_end_frame, from_=1, to=12, font=Font(size=11))
minute_end_spinbox = Spinbox(minute_end_frame, from_=0, to=59, font=Font(size=11))
hour_start_spinbox = Spinbox(hour_start_frame, from_=1, to=12, font=Font(size=11))
minute_start_spinbox = Spinbox(minute_start_frame, from_=0, to=59, font=Font(size=11))

# Packing the labels and spinboxes
start_label.pack(side=RIGHT, padx=5, pady=58, anchor='n', expand=True)

minute_start_label.pack()
minute_start_spinbox.pack()
hour_start_label.pack()
hour_start_spinbox.pack()

minute_start_frame.pack(side=RIGHT, padx=5, pady=40, anchor='n', expand=True)
hour_start_frame.pack(side=RIGHT, padx=5, pady=40, anchor='n', expand=True)

end_label.pack(side=RIGHT, padx=5, pady=58, anchor='n', expand=True)

minute_end_label.pack()
minute_end_spinbox.pack()
hour_end_label.pack()
hour_end_spinbox.pack()

minute_end_frame.pack(side=RIGHT, padx=5, pady=40, anchor='n', expand=True)
hour_end_frame.pack(side=RIGHT, padx=5, pady=40, anchor='n', expand=True)

time_frame.pack(anchor='e', fill=X)

# Creating a Frame for items
items_frame = Frame(calculation_frame)

# Creating item labels, combobox, spinbox and "Add Extra" button
item_name_label = Label(items_frame, text='المشروب/ المأكول')
item_name_var = StringVar()
item_combobox = ttk.Combobox(items_frame, textvariable=item_name_var)
item_quantity_label = Label(items_frame, text='الكمية')
item_quantity_spinbox = Spinbox(items_frame, from_=0, font=Font(size=11))
item_add_button = Button(items_frame, text='إضافة مشروب/ مأكول أخر', command=add_item)

# Packing the labels and spinboxes
item_name_label.pack(side=RIGHT, padx=10, expand=True)
item_combobox.pack(side=RIGHT, padx=10, expand=True)
item_quantity_label.pack(side=RIGHT, padx=10, expand=True)
item_quantity_spinbox.pack(side=RIGHT, padx=10, expand=True)
item_add_button.pack(side=RIGHT, padx=10, expand=True)

items_frame.pack()

# Keep the root window running
root.mainloop()
