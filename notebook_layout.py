from tkinter import Frame
from tkinter import ttk


def create_notebook(root):

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

    return calculation_frame, saved_calculations_frame
