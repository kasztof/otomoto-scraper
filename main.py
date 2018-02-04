import os
from collections import defaultdict
from urllib.request import urlopen
import statistics

import collections

import xlsxwriter as xlsxwriter
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.chart import BarChart

# CARS = 'https://www.otomoto.pl/osobowe/skoda/octavia/?page='
MAXIMUM_MILEAGE = 2000000


def get_car_url(mark, model):
    return 'https://www.otomoto.pl/osobowe/' + mark + '/' + model + '/?page='


def merge_dictionaries(dict1, dict2):
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


def merge_list_of_dictionaries(dict_list):
    for i in range(1, len(dict_list)):
        dict_list[0] = merge_dictionaries(dict_list[0], dict_list[i])
    return dict_list[0]


def number_of_values_in_dict(dictionary):
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
        mileage = get_number(mlg.span.string)
        if mileage < MAXIMUM_MILEAGE:
            result_dict[yrs.span.string].append(mileage)

    return result_dict


def get_number(string):
    result = ""
    for char in string:
        if char.isdigit():
            result += char
    return int(result)


def get_data_from_pages(path, mark, model, start_page, end_page):
    list_of_pages = []
    for page_number in range(start_page, end_page + 1):
        print(page_number)
        list_of_pages.append(get_mileages_and_years(get_car_url(mark, model) + str(page_number)))

    data_set = merge_list_of_dictionaries(list_of_pages)
    save_to_excel(path, data_set, mark, model)
    return data_set


def dict_with_avg_of_values(dictionary):
    result = {}
    for key, val in dictionary.items():
        avg = statistics.mean(val)
        result[key] = avg

    return result


def dict_with_median_of_values(dictionary):
    result = {}
    for key, val in dictionary.items():
        median = statistics.median(val)
        result[key] = median

    return result


def dict_with_median_and_avg_of_values(dictionary):
    result = defaultdict(list)
    for key, val in dictionary.items():
        median = statistics.median(val)
        avg = statistics.mean(val)
        result[key].append(median)
        result[key].append(avg)

    return result


def save_to_excel(path, data, mark, model):
    to_save = collections.OrderedDict(sorted(dict_with_median_and_avg_of_values(data).items()))
    if os.path.exists(path + '/data.xlsx'):
        workbook = openpyxl.load_workbook(path + '/data.xlsx')
    else:
        wb = xlsxwriter.Workbook(path + '/data.xlsx')
        wb.close()
        workbook = openpyxl.load_workbook(path + '/data.xlsx')

    print(mark + "_" + model)
    print(workbook.sheetnames)

    if (mark + '_' + model) not in workbook.sheetnames:
        workbook.create_sheet(mark + '_' + model)
        sheet = workbook[mark + '_' + model]
    else:
        sheet = workbook[mark + '_' + model]

    sheet['B1'] = 'median'
    sheet['C1'] = 'average'

    for key, value in to_save.items():
        sheet.append([key, *value])

    chart = BarChart()
    chart.type = "col"
    chart.y_axis.title = 'Mileage'
    chart.x_axis.title = 'Year of prod.'

    data = openpyxl.chart.Reference(sheet, min_col=2, max_col=3, min_row=1, max_row=len(to_save))
    cats = openpyxl.chart.Reference(sheet, min_col=1, min_row=1, max_row=len(to_save))

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    sheet.add_chart(chart, "E2")

    workbook.save(path + '/data.xlsx')
