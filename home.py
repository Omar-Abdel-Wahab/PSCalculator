from tkinter import Label, StringVar, Tk, Frame, Spinbox, RIGHT, Button
from tkinter import ttk
from tkinter.font import Font
from time_intervals import create_time_intervals
from notebook_layout import create_notebook
from playstation_layout import create_playstation_layout

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
    """Add another beverage or so to be calculated along with the main beverage and the time in which the customers
    played"""

    item_add_button.pack_forget()
    playstation_frame.pack_forget()
    added_items_frame = Frame(calculation_frame)
    added_item_name_label = Label(added_items_frame, text='المشروب/ المأكول')
    added_item_name_var = StringVar()
    added_item_combobox = ttk.Combobox(added_items_frame, textvariable=added_item_name_var)
    added_item_quantity_label = Label(added_items_frame, text='الكمية')
    added_item_quantity_spinbox = Spinbox(added_items_frame, from_=0, font=Font(size=11))
    added_item_name_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_item_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_item_quantity_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_item_quantity_spinbox.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_items_frame.pack()
    item_add_button.pack(padx=10, pady=20)
    playstation_frame.pack()


calculation_frame, saved_calculations_frame = create_notebook(root)
create_time_intervals(calculation_frame)

# Creating a Frame for items
items_frame = Frame(calculation_frame)

# Creating item labels, combobox, spinbox and "Add Extra" button
item_name_label = Label(items_frame, text='المشروب/ المأكول')
item_name_var = StringVar()
item_combobox = ttk.Combobox(items_frame, textvariable=item_name_var)
item_quantity_label = Label(items_frame, text='الكمية')
item_quantity_spinbox = Spinbox(items_frame, from_=0, font=Font(size=11))
item_add_button = Button(calculation_frame, text='إضافة مشروب/ مأكول أخر', command=add_item)

# Packing the labels and spinboxes
item_name_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
item_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
item_quantity_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
item_quantity_spinbox.pack(side=RIGHT, padx=10, pady=5, expand=True)
items_frame.pack()

item_add_button.pack(padx=10, pady=20)

playstation_frame = create_playstation_layout(calculation_frame)

# Keep the root window running
root.mainloop()
