from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from database import Database
import concurrent.futures as cf

# Connect or create the database #


def initialize_database():
    db = Database('configurations.db')
    i, m, u, p = db.fetch_needed_data()

    return i, m, u, p


with cf.ThreadPoolExecutor() as executor:
    returned = executor.submit(initialize_database)

items = returned.result()[0]
items_names = []
items_prices = []

for item in items:
    items_names.append(item[0])
    items_prices.append(item[1])

items = dict(zip(items_names, items_prices))

machines = returned.result()[1][0]
users = returned.result()[2]
prices = returned.result()[3]

print(items)
print(machines)
print(users)
print(prices)

# First, create the main window (root) that will hold all components, adjust properties and center it #

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


def add_item():
    """Add another beverage or so to be calculated along with the main beverage and the time in which the customers
    played"""

    item_add_button.pack_forget()
    playstation_frame.pack_forget()
    pending_operations_frame.pack_forget()

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
    pending_operations_frame.pack(pady=40)


center(root)

# 1) Creating the Notebook which will carry the tabs (Calculation, Saved_Calculation) #

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

# 2) Create the time_intervals layout #

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

# Packing the labels, spinboxes and the container frame
start_label.pack(side=RIGHT, padx=5, pady=48, anchor='n', expand=True)

minute_start_label.pack()
minute_start_spinbox.pack()
hour_start_label.pack()
hour_start_spinbox.pack()

minute_start_frame.pack(side=RIGHT, padx=5, pady=30, anchor='n', expand=True)
hour_start_frame.pack(side=RIGHT, padx=5, pady=30, anchor='n', expand=True)

end_label.pack(side=RIGHT, padx=5, pady=48, anchor='n', expand=True)

minute_end_label.pack()
minute_end_spinbox.pack()
hour_end_label.pack()
hour_end_spinbox.pack()

minute_end_frame.pack(side=RIGHT, padx=5, pady=30, anchor='n', expand=True)
hour_end_frame.pack(side=RIGHT, padx=5, pady=30, anchor='n', expand=True)

time_frame.pack(anchor='e', fill=X)

# 3) Create the items_frame (for beverages and food) #

# Creating a Frame for items
items_frame = Frame(calculation_frame)

# Creating item labels, combobox, spinbox and "Add Extra" button
item_name_label = Label(items_frame, text='المشروب/ المأكول')
item_name_var = StringVar()
item_combobox = ttk.Combobox(items_frame, textvariable=item_name_var)
item_quantity_label = Label(items_frame, text='الكمية')
item_quantity_spinbox = Spinbox(items_frame, from_=0, font=Font(size=11))
item_add_button = Button(calculation_frame, text='إضافة مشروب/ مأكول أخر', command=add_item)

# Packing the labels, spinboxes and the container frame
item_name_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
item_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
item_quantity_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
item_quantity_spinbox.pack(side=RIGHT, padx=10, pady=5, expand=True)
items_frame.pack()

item_add_button.pack(padx=10, pady=20)

# 4) Create the playstation_frame which will hold the PS number, and Calculation button #

# Creating a Frame for Playstation machines
playstation_frame = Frame(calculation_frame)

# Creating a Label and Combobox for Playstation machines and a Calculate button
playstation_number_label = Label(playstation_frame, text='الجهاز')
playstation_number_var = StringVar()
playstation_combobox = ttk.Combobox(playstation_frame, textvariable=playstation_number_var)
playstation_calculate_button = Button(playstation_frame, text='حساب')
playstation_calculate_label = Label(playstation_frame, text='الحساب هنا')

# Packing the labels, combobox, button and the container frame
playstation_number_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_calculate_button.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_calculate_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_frame.pack()

# 5) A) Create the first part of pending_calculations frame by creating the necessary buttons (Add, Edit, Delete) #

pending_operations_frame = Frame(calculation_frame)

# Creating a Frame for Pending Operations buttons
pending_buttons_frame = Frame(pending_operations_frame)

# Creating the three buttons (Add a pending operation, Edit, Delete)
pending_add_button = Button(pending_buttons_frame, text='إضافة حساب معلق')
pending_edit_button = Button(pending_buttons_frame, text='تعديل حساب معلق')
pending_delete_button = Button(pending_buttons_frame, text='مسح حساب معلق')

# Packing the buttons and the container frame
pending_add_button.pack(padx=80, pady=5)
pending_edit_button.pack(padx=80, pady=5)
pending_delete_button.pack(padx=80, pady=5)

pending_buttons_frame.pack(side=RIGHT, pady=40, anchor='e')

# 5) B) Create the second part of pending_calculations frame by creating a Listbox to hold pending operations #

# Creating a Frame to hold the listbox and the scrollbar
pending_operations_ls_frame = Frame(pending_operations_frame)

# Creating the Pending Operations Listbox
pending_operations_listbox = Listbox(pending_operations_ls_frame, height=40, width=100, border=0)

# Creating a scrollbar for pending ops
scrollbar = Scrollbar(pending_operations_ls_frame)

# Set scroll to listbox
pending_operations_listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=pending_operations_listbox.yview)

# Bind select [Note: needs a callback here passed as a second argument]
pending_operations_listbox.bind('<<ListboxSelect>>')

# Packing the listbox, scrollbar and the container frame
scrollbar.pack(side=RIGHT)
pending_operations_listbox.pack(side=RIGHT)

pending_operations_ls_frame.pack(side=RIGHT)

pending_operations_frame.pack(pady=40)

# Finally, show the GUI using mainloop method #

# Keep the root window running
root.mainloop()
