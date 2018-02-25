import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

from main import get_mileages_and_years, get_car_url, merge_list_of_dictionaries, save_to_xlsx

MASTER = tk.Tk()
PROGRESS_BAR_LENGTH = 300
PROGRESS_BAR_STEPS = 100


def delete_default_text(event):
    event.widget.delete(0, "end")


def browse_button():
    filename = filedialog.askdirectory()
    return filename


def get_data_from_pages(path, mark, model, start_page, end_page):
    list_of_pages = []
    one_step = PROGRESS_BAR_STEPS / (end_page - start_page + 1)
    for page_number in range(start_page, end_page + 1):
        list_of_pages.append(get_mileages_and_years(get_car_url(mark, model) + str(page_number)))
        progress['value'] += one_step
        MASTER.update_idletasks()

    data_set = merge_list_of_dictionaries(list_of_pages)
    save_to_xlsx(path, data_set, mark, model, end_page - start_page + 1)
    progress['value'] = 0
    return data_set


def get_data():
    mark = car_mark.get()
    model = car_model.get()
    first = int(first_page.get())
    last = int(last_page.get())
    progress.pack(side="bottom")
    path = browse_button()
    get_data_from_pages(path, mark, model, first, last)
    messagebox.showinfo("Info", "Data download and saved in specified location.")


first_page = tk.Entry(MASTER)
last_page = tk.Entry(MASTER)
first_page.insert(0, 'start page')
last_page.insert(0, 'end page')
first_page.bind("<Button-1>", delete_default_text)
last_page.bind("<Button-1>", delete_default_text)

car_mark = tk.Entry(MASTER)
car_model = tk.Entry(MASTER)
car_mark.insert(0, 'mark')
car_model.insert(0, 'model')
car_mark.bind("<Button-1>", delete_default_text)
car_model.bind("<Button-1>", delete_default_text)

progress = Progressbar(MASTER, orient=tk.HORIZONTAL, length=PROGRESS_BAR_LENGTH)

tk.Button(MASTER, text="Get data", command=get_data).pack(side="bottom")

car_mark.pack(side="top")
car_model.pack(side="top")

first_page.pack(side="left")
last_page.pack(side="right")


MASTER.mainloop()
