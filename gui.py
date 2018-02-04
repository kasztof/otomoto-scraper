import tkinter as tk
from tkinter import filedialog

from main import get_data_from_pages

master = tk.Tk()


def say_hi():
    print("hi there, everyone!")


def delete_default_text(event):
    event.widget.delete(0, "end")


def browse_button():
    filename = filedialog.askdirectory()
    print(filename)
    return filename


def get_data():
    mark = car_mark.get()
    model = car_model.get()
    first = int(first_page.get())
    last = int(last_page.get())
    path = browse_button()
    get_data_from_pages(path, mark, model, first, last)

first_page = tk.Entry(master)
last_page = tk.Entry(master)
first_page.insert(0, 'start page')
last_page.insert(0, 'end page')
first_page.bind("<Button-1>", delete_default_text)
last_page.bind("<Button-1>", delete_default_text)

car_mark = tk.Entry(master)
car_model = tk.Entry(master)
car_mark.insert(0, 'mark')
car_model.insert(0, 'model')
car_mark.bind("<Button-1>", delete_default_text)
car_model.bind("<Button-1>", delete_default_text)

tk.Button(master, text="Get data", command=get_data).pack(side="bottom")
# tk.Button(master, text="Choose directory for xlsx file...", command=browse_button).pack(side="bottom")

car_mark.pack(side="top")
car_model.pack(side="top")

first_page.pack(side="left")
last_page.pack(side="right")


master.mainloop()