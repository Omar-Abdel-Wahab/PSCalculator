from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from database import Database
import concurrent.futures as cf
import threading
import datetime
import ast

database_name = 'configurations.db'


def initialize_database():
    """Create/ Connect to the database and fetch the required data"""
    db = Database(database_name)
    i, m, u, p = db.fetch_needed_data()

    return i, m, u, p


def from_thread_result_to_dictionary(returned_result):
    """Turn the result returned from a thread into a dictionary"""
    keys = []
    values = []

    for returned_result_item in returned_result:
        keys.append(returned_result_item[0])
        values.append(returned_result_item[1])

    dictionary = dict(zip(keys, values))
    return dictionary


def create_machines_tuple(value):
    """Create a tuple of machines numbers"""
    tuple_values = []

    for j in range(1, value + 1):
        tuple_values.append(j)

    return tuple(tuple_values)


with cf.ThreadPoolExecutor() as executor:
    returned = executor.submit(initialize_database)
    returned_items = returned.result()[0]
    returned_machines = returned.result()[1][0]
    returned_users = returned.result()[2]
    returned_prices = returned.result()[3]
    arguments = [returned_items, returned_users, returned_prices]
    returned_machines_result = executor.submit(create_machines_tuple, returned_machines)
    returned_results = executor.map(from_thread_result_to_dictionary, arguments)
    returned_results = list(returned_results)
    # print(returned_machines)

items = returned_results[0]
users = returned_results[1]
prices = returned_results[2]
machines = returned_machines_result.result()

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


added_items_frames = []
added_item_comboboxes = []
added_item_quantity_spinboxes = []


def add_item():
    """Add another beverage or so to be calculated along with the main beverage and the time in which the customers
    played"""

    item_add_button.pack_forget()
    playstation_frame.pack_forget()
    pending_operations_frame.pack_forget()

    added_items_frame = Frame(calculation_frame)
    added_items_frames.append(added_items_frame)
    added_item_name_label = Label(added_items_frame, text='المشروب/ المأكول')

    added_item_name_var = StringVar()
    added_item_combobox = ttk.Combobox(added_items_frame, textvariable=added_item_name_var)
    added_item_comboboxes.append(added_item_combobox)
    added_item_combobox["values"] = tuple(items.keys())

    added_item_quantity_label = Label(added_items_frame, text='الكمية')
    added_item_quantity_spinbox = Spinbox(added_items_frame, from_=0, to=20, font=Font(size=11))
    added_item_quantity_spinboxes.append(added_item_quantity_spinbox)

    def select_added_item_quantity(event):
        added_item_quantity_spinbox.selection_range(0, END)

    added_item_quantity_spinbox.bind("<FocusIn>", select_added_item_quantity)

    added_item_name_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_item_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_item_quantity_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
    added_item_quantity_spinbox.pack(side=RIGHT, padx=10, pady=5, expand=True)

    added_items_frame.pack()
    item_add_button.pack(padx=10, pady=20)
    playstation_frame.pack()
    pending_operations_frame.pack(pady=40)


def reset():
    """Reset the main window back to its normal form"""
    for frame in added_items_frames:
        frame.destroy()
    added_item_comboboxes.clear()
    added_item_quantity_spinboxes.clear()
    hour_end_spinbox.delete(0, END)
    hour_end_spinbox.insert(0, '1')
    hour_start_spinbox.delete(0, END)
    hour_start_spinbox.insert(0, '1')
    minute_end_spinbox.delete(0, END)
    minute_end_spinbox.insert(0, '0')
    minute_start_spinbox.delete(0, END)
    minute_start_spinbox.insert(0, '0')
    item_combobox.set('')
    item_quantity_spinbox.delete(0, END)
    item_quantity_spinbox.insert(0, '0')
    playstation_numbers_combobox.set('1')
    playstation_prices_combobox.set('Single-20')
    playstation_calculate_label.config(text='0.0')
    playstation_pending_calculation_label.config(text='0.0')


def calculate_using_threads():
    """Calculate the time, beverages and food for a customer"""
    hour_end = int(hour_end_spinbox.get())
    minute_end = int(minute_end_spinbox.get())
    hour_start = int(hour_start_spinbox.get())
    minute_start = int(minute_start_spinbox.get())
    main_item = item_combobox.get()
    main_quantity = int(item_quantity_spinbox.get())
    machine_number = int(playstation_numbers_combobox.get())
    pending_calculation = float(playstation_pending_calculation_label.cget('text'))
    extra_items = []
    extra_quantities = []
    for added_item in added_item_comboboxes:
        extra_items.append(added_item.get())
    for added_item_quantity in added_item_quantity_spinboxes:
        extra_quantities.append(added_item_quantity.get())
    price_name = playstation_prices_combobox.get()
    start_time = datetime.time(hour_start, minute_start)
    end_time = datetime.time(hour_end, minute_end)
    time_difference = datetime.datetime.combine(datetime.date.today(), end_time) - \
                      datetime.datetime.combine(datetime.date.today(), start_time)
    total_time = time_difference.total_seconds() / 3600
    total_items = 0
    total_items_string = ''
    if main_item != '':
        total_items += main_quantity * items[main_item]
        total_items_string += main_item + ', '
    for index in range(len(extra_items)):
        if extra_items[index] != '':
            total_items += int(extra_quantities[index]) * items[extra_items[index]]
            total_items_string += extra_items[index] + ', '
    if total_items_string != '':
        total_items_string = total_items_string[:-2]
    total = total_time * prices[price_name] + total_items + pending_calculation
    playstation_pending_calculation_label.config(text='0.0')
    playstation_calculate_label.configure(text=str(total))
    today = datetime.datetime.today()
    db = Database(database_name)
    db.insert_into_calculations(today.day, today.month, today.year, start_time.hour, start_time.minute,
                                end_time.hour, end_time.minute, total_items_string, machine_number,
                                total - pending_calculation)
    # print(today.year, today.month, today.day, today.hour, today.minute)


def calculate():
    """Call calculate_using_threads()"""
    # This is done in such matter because adding a callback to the button using the threading module
    # will incur a Runtime exception of "threads can only start once".
    # For some reason, concurrent.futures doesn't work here. So, the threading module will be used instead.
    threading.Thread(target=calculate_using_threads).start()


def bring_records_to_file_using_threads():
    """Bring calculations records of a certain date and save to a file"""
    username = username_entry.get()
    password = password_entry.get()
    day = int(day_entry.get())
    month = int(month_entry.get())
    year = int(year_entry.get())
    today = datetime.date(year, month, day)
    if username in users:
        if password == users[username]:
            db = Database(database_name)
            data = db.fetch_calculations(day, month, year)
            # print(data)
            # print(today)
            save_to_file(today, data)


def save_to_file(today, data):
    today_str = today.strftime("%d-%b-%Y") + '.txt'
    with open(today_str, 'w', encoding='utf-8') as f:
        total_of_today = 0
        for datum in data:
            start = datetime.time(datum[3], datum[4])
            end = datetime.time(datum[5], datum[6])
            time_difference = datetime.datetime.combine(today, end) - datetime.datetime.combine(today, start)
            item = datum[7]
            machine_number = datum[8]
            price = datum[9]
            total_of_today += price
            f.write(f"Start: {start}\n")
            f.write(f"End: {end}\n")
            f.write(f"Difference: {time_difference}\n")
            f.write(f"Item(s): {item}\n")
            f.write(f"Machine: {machine_number}\n")
            f.write(f"Price: {price}\n")
            f.write("\n----------------\n\n")
        f.write(f"Total is: {total_of_today}\n")


def bring_records_to_file():
    """Call bring_records_to_file_using_threads()"""
    # This is done in such matter because adding a callback to the button using the threading module
    # will incur a Runtime exception of "threads can only start once".
    # For some reason, concurrent.futures doesn't work here. So, the threading module will be used instead.
    threading.Thread(target=bring_records_to_file_using_threads).start()


def select_day_entry(event):
    day_entry.selection_range(0, END)


def select_month_entry(event):
    month_entry.selection_range(0, END)


def select_year_entry(event):
    year_entry.selection_range(0, END)


def select_hour_end(event):
    hour_end_spinbox.selection_range(0, END)


def select_minute_end(event):
    minute_end_spinbox.selection_range(0, END)


def select_hour_start(event):
    hour_start_spinbox.selection_range(0, END)


def select_minute_start(event):
    minute_start_spinbox.selection_range(0, END)


def select_item_quantity(event):
    item_quantity_spinbox.selection_range(0, END)


def select_playstation_number(event):
    playstation_numbers_combobox.selection_range(0, END)


def select_price_name(event):
    playstation_prices_combobox.selection_range(0, END)


def add_to_listbox():
    machine_number = playstation_numbers_combobox.get()
    all_listbox_items = pending_operations_listbox.get(0, END)
    all_dictionaries = []
    for listbox_item in all_listbox_items:
        all_dictionaries.append(ast.literal_eval(listbox_item))

    for dictionary in all_dictionaries:
        if dictionary['machine'] == machine_number:
            return
    hour_end = hour_end_spinbox.get()
    minute_end = minute_end_spinbox.get()
    hour_start = hour_start_spinbox.get()
    minute_start = minute_start_spinbox.get()
    main_item = item_combobox.get()
    main_quantity = item_quantity_spinbox.get()
    calculation = playstation_calculate_label.cget('text')
    extra_items = []
    extra_quantities = []
    for added_item in added_item_comboboxes:
        extra_items.append(added_item.get())
    for added_item_quantity in added_item_quantity_spinboxes:
        extra_quantities.append(added_item_quantity.get())
    price_name = playstation_prices_combobox.get()
    pending_dictionary = {'machine': machine_number, 'he': hour_end, 'me': minute_end, 'hs': hour_start,
                          'ms': minute_start, 'mi': main_item, 'mq': main_quantity, 'ei': extra_items,
                          'eq': extra_quantities, 'pn': price_name, 'ca': calculation}
    pending_operations_listbox.insert(END, pending_dictionary)
    playstation_calculate_label.config(text='0.0')


def delete_from_listbox():
    try:
        index = pending_operations_listbox.curselection()[0]
        pending_operations_listbox.delete(index)
    except IndexError:
        pass


def select_listbox_item(event):
    global selected_listbox_item
    try:
        index = pending_operations_listbox.curselection()[0]
    except IndexError:
        pass
    except UnboundLocalError:
        pass
    reset()
    selected_listbox_item = pending_operations_listbox.get(index)
    selected_listbox_item = ast.literal_eval(selected_listbox_item)
    minute_start_spinbox.delete(0, END)
    minute_start_spinbox.insert(0, selected_listbox_item['ms'])
    minute_end_spinbox.delete(0, END)
    minute_end_spinbox.insert(0, selected_listbox_item['me'])
    hour_start_spinbox.delete(0, END)
    hour_start_spinbox.insert(0, selected_listbox_item['hs'])
    hour_end_spinbox.delete(0, END)
    hour_end_spinbox.insert(0, selected_listbox_item['he'])
    item_combobox.delete(0, END)
    item_combobox.insert(0, selected_listbox_item['mi'])
    item_quantity_spinbox.delete(0, END)
    item_quantity_spinbox.insert(0, selected_listbox_item['mq'])
    playstation_numbers_combobox.delete(0, END)
    playstation_numbers_combobox.insert(0, selected_listbox_item['machine'])
    playstation_prices_combobox.delete(0, END)
    playstation_prices_combobox.insert(0, selected_listbox_item['pn'])
    playstation_pending_calculation_label.config(text=selected_listbox_item['ca'])
    extra_items = selected_listbox_item['ei']
    extra_quantities = selected_listbox_item['eq']

    for index in range(len(extra_items)):
        add_item()
        added_item_comboboxes[index].insert(0, extra_items[index])
        added_item_quantity_spinboxes[index].delete(0, END)
        added_item_quantity_spinboxes[index].insert(0, extra_quantities[index])


center(root)
root.iconbitmap('res/images/newplaystationicon.ico')

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

hour_end_spinbox.bind("<FocusIn>", select_hour_end)
minute_end_spinbox.bind("<FocusIn>", select_minute_end)
hour_start_spinbox.bind("<FocusIn>", select_hour_start)
minute_start_spinbox.bind("<FocusIn>", select_minute_start)

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
item_combobox["values"] = tuple(items.keys())
item_quantity_label = Label(items_frame, text='الكمية')

item_quantity_spinbox = Spinbox(items_frame, from_=0, to=20, font=Font(size=11))
item_quantity_spinbox.bind("<FocusIn>", select_item_quantity)

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
playstation_numbers_combobox = ttk.Combobox(playstation_frame, textvariable=playstation_number_var)
playstation_numbers_combobox["values"] = machines
playstation_numbers_combobox.current(0)
playstation_numbers_combobox.bind("<FocusIn>", select_playstation_number)
playstation_price_var = StringVar()
playstation_prices_combobox = ttk.Combobox(playstation_frame, textvariable=playstation_price_var)
playstation_prices_combobox["values"] = tuple(prices.keys())
playstation_prices_combobox.current(0)
playstation_prices_combobox.bind("<FocusIn>", select_price_name)
playstation_calculate_button = Button(playstation_frame, text='حساب', command=calculate)
playstation_calculate_label = Label(playstation_frame, text='0.0')
playstation_reset_button = Button(playstation_frame, text='Reset', command=reset)
playstation_pending_label = Label(playstation_frame, text=': حساب معلق')
playstation_pending_calculation_label = Label(playstation_frame, text='0.0')

# Packing the labels, combobox, button and the container frame
playstation_number_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_numbers_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_prices_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_calculate_button.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_calculate_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_reset_button.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_pending_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_pending_calculation_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
playstation_frame.pack()

# 5) A) Create the first part of pending_calculations frame by creating the necessary buttons (Add, Edit, Delete) #

pending_operations_frame = Frame(calculation_frame)

# Creating a Frame for Pending Operations buttons
pending_buttons_frame = Frame(pending_operations_frame)

# Creating the three buttons (Add a pending operation, Edit, Delete)
pending_add_button = Button(pending_buttons_frame, text='إضافة حساب معلق', command=add_to_listbox)
pending_delete_button = Button(pending_buttons_frame, text='مسح حساب معلق', command=delete_from_listbox)

# Packing the buttons and the container frame
pending_add_button.pack(padx=80, pady=5)
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
pending_operations_listbox.bind('<<ListboxSelect>>', select_listbox_item)

# Packing the listbox, scrollbar and the container frame
scrollbar.pack(side=RIGHT)
pending_operations_listbox.pack(side=RIGHT)

pending_operations_ls_frame.pack(side=RIGHT)

pending_operations_frame.pack(pady=40)

# Create the saved_calculations layout #

# Create the frames for the widgets
username_frame = Frame(saved_calculations_frame)
password_frame = Frame(saved_calculations_frame)
date_frame = Frame(saved_calculations_frame)

username_label = Label(username_frame, text='المستخدم')
username_var = StringVar()
username_entry = Entry(username_frame, textvariable=username_var)

password_label = Label(password_frame, text='كلمة السر')
password_var = StringVar()
password_entry = Entry(password_frame, textvariable=password_var, show='*')

date_of_today = datetime.datetime.today()
day_label = Label(date_frame, text='اليوم')
day_var = StringVar()
day_var.set(str(date_of_today.day))
day_entry = Entry(date_frame, textvariable=day_var)
day_entry.bind("<FocusIn>", select_day_entry)

month_label = Label(date_frame, text='الشهر')
month_var = StringVar()
month_var.set(str(date_of_today.month))
month_entry = Entry(date_frame, textvariable=month_var)
month_entry.bind("<FocusIn>", select_month_entry)

year_label = Label(date_frame, text='السنة')
year_var = StringVar()
year_var.set(str(date_of_today.year))
year_entry = Entry(date_frame, textvariable=year_var)
year_entry.bind("<FocusIn>", select_year_entry)

records_button = Button(saved_calculations_frame, text='جلب سجلات اليوم', command=bring_records_to_file)

# Packing the labels, entries, button and containing frames
username_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
username_entry.pack(side=RIGHT, padx=10, pady=5, expand=True)

username_frame.pack(pady=(20, 0))

password_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
password_entry.pack(side=RIGHT, padx=10, pady=5, expand=True)

password_frame.pack(pady=(20, 20))

year_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
year_entry.pack(side=RIGHT, padx=10, pady=5, expand=True)

month_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
month_entry.pack(side=RIGHT, padx=10, pady=5, expand=True)

day_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
day_entry.pack(side=RIGHT, padx=10, pady=5, expand=True)

date_frame.pack(pady=40)

records_button.pack(pady=40)

# Finally, show the GUI using mainloop method #

# Keep the root window running
root.mainloop()
