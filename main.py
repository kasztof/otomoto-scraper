from collections import defaultdict
from urllib.request import urlopen
import statistics

import collections
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.chart import BarChart

CARS = 'https://www.otomoto.pl/osobowe/skoda/octavia/?page='


def add_dictionaries(dict1, dict2):
    result = defaultdict(list)
    for key, value in dict1.items():
        if key in dict2:
            result[key] = [*value, *dict2[key]]
        else:
            result[key] = value

    for key, value in dict2.items():
        if key not in dict1:
            result[key] = value
    return result


def merge_dictionaries(dict1, dict2):
    result = {key: [*value, *dict2[key]] if key in dict2 else value
              for key, value in dict1.items()}
    return result


def merge_list_of_dictionaries(dict_list):
    for i in range(1, len(dict_list)):
        dict_list[0] = add_dictionaries(dict_list[0], dict_list[i])
    return dict_list[0]


def count_values_in_dict(dictionary):
    sum_of_values = 0
    for values in dictionary.values():
        for _ in values:
            sum_of_values += 1
    return sum_of_values


def get_mileages_and_years(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    mileages = soup.find_all(attrs={"data-code": "mileage"})
    years = soup.find_all(attrs={"data-code": "year"})
    result_dict = defaultdict(list)

    for yrs, mlg in list(zip(years, mileages)):
        mileage = int(get_number(mlg.span.string))
        if mileage < 1000000:
            result_dict[yrs.span.string].append(get_number(mlg.span.string))

    return result_dict


def get_number(string):
    result = ""
    for char in string:
        if char.isdigit():
            result += char
    return result


def get_car_data():
    list_of_pages = []
    for page_number in range(2, 50):
        print(page_number)
        list_of_pages.append(get_mileages_and_years(CARS + str(page_number)))

    data_set = merge_list_of_dictionaries(list_of_pages)
    return data_set


def dict_with_avg_of_values(dictionary):
    result = {}
    for key, values in dictionary.items():
        values = [int(i) for i in values]
        avg = statistics.mean(values)
        result[key] = avg

    return result


def dict_with_median_of_values(dictionary):
    result = {}
    for key, values in dictionary.items():
        values = [int(i) for i in values]
        median = statistics.median(values)
        result[key] = median

    return result


def dict_with_median_and_avg_of_values(dictionary):
    result = defaultdict(list)
    for key, values in dictionary.items():
        values = [int(i) for i in values]
        median = statistics.median(values)
        avg = statistics.mean(values)
        result[key].append(median)
        result[key].append(avg)

    return result


DATA = collections.OrderedDict(sorted(dict_with_median_and_avg_of_values(get_car_data()).items()))

workbook = openpyxl.load_workbook('data.xlsx')
if not workbook['skoda_octavia']:
    workbook.create_sheet('skoda_octavia')
print(workbook.active)
sheet = workbook['skoda_octavia']
print(workbook.sheetnames)

i = 1  # no to to wez popraw gosciu
for key, value in DATA.items():
    sheet.append([key, *value])
    # sheet['B' + str(i)] = int(el)
    # sheet['C' + str(i)] = DATA[el]
    # i += 1

chart = BarChart()
chart.type = "col"
chart.y_axis.title = 'Mileage'
chart.x_axis.title = 'Year of prod.'

data = openpyxl.chart.Reference(sheet, min_col=2, max_col=3, min_row=1, max_row=len(DATA))
cats = openpyxl.chart.Reference(sheet, min_col=1, min_row=1, max_row=len(DATA))

chart.add_data(data)
chart.set_categories(cats)
sheet.add_chart(chart, "E2")

workbook.save('data.xlsx')

# plt.rcParams.update({'font.size': 7})
# plt.bar(DATA.keys(), dict_with_avg_of_values(DATA).values(), color='g')
# plt.show()
