import tkinter as tk
from main import get_data_from_pages

master = tk.Tk()


def say_hi():
    print("hi there, everyone!")


def delete_default_text(event):
    event.widget.delete(0, "end")


def get_data(event):
    first = int(first_page.get())
    last = int(last_page.get())
    get_data_from_pages(first, last)

first_page = tk.Entry(master)
last_page = tk.Entry(master)
first_page.insert(0, 'start page')
last_page.insert(0, 'end page')
first_page.bind("<Button-1>", delete_default_text)
last_page.bind("<Button-1>", delete_default_text)

get_data_button = tk.Button(master)
get_data_button['text'] = 'Get data'
get_data_button.bind("<Button-1>", get_data)
get_data_button.pack(side='bottom')
# tk.Button(master, text="Get data", command=get_data).pack(side="bottom")

first_page.pack(side="left")
last_page.pack(side="right")


master.mainloop()