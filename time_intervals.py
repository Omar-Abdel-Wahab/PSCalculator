from tkinter import Label, Frame, Spinbox, RIGHT, X
from tkinter.font import Font


def create_time_intervals(calculation_frame):

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