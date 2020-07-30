from tkinter import Label, StringVar, Button, Frame, ttk, RIGHT


def create_playstation_layout(calculation_frame):

    # Creating a Frame for Playstation machines
    playstation_frame = Frame(calculation_frame)

    # Creating a Label and Combobox for Playstation machines and a Calculate button
    playstation_number_label = Label(playstation_frame, text='الجهاز')
    playstation_number_var = StringVar()
    playstation_combobox = ttk.Combobox(playstation_frame, textvariable=playstation_number_var)
    playstation_calculate_button = Button(playstation_frame, text='حساب')
    playstation_calculate_label = Label(playstation_frame, text='الحساب هنا')

    # Packing the labels, combobox and button
    playstation_number_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
    playstation_combobox.pack(side=RIGHT, padx=10, pady=5, expand=True)
    playstation_calculate_button.pack(side=RIGHT, padx=10, pady=5, expand=True)
    playstation_calculate_label.pack(side=RIGHT, padx=10, pady=5, expand=True)
    playstation_frame.pack()

    return playstation_frame
