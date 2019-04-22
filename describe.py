import argparse
import os
import sys
import csv
import math
import pandas

def get_data(file_name):
    try:
        fd = open(file_name, 'r')
        lines = csv.reader(fd, delimiter=',')
        full_data = []
        data = {}
        for index, row in enumerate(lines):
            new_line_data = []
            for col, value in enumerate(row):
                if index == 0:
                    data[col] = { "label": value, "value": [], "numerical": False }
                else:
                    if value.lower() != "nan" and value != '':
                        try:
                            value = None if value == '' else float(value)
                            data[col]["numerical"] = True
                        except ValueError:
                            data[col]["numerical"] = False
                    if value == '':
                        value = None
                    data[col]["value"].append(value)
                    new_line_data.append(value)
                full_data.append(new_line_data)
        return [full_data, data]
    except:
        raise(Exception("CSV file is not a valid one"))

def get_std(values, mean, count):
    squared_diff_sum = 0.0
    for value in values:
        squared_diff_sum += ((value - mean) ** 2)
    return math.sqrt(float(squared_diff_sum / (count - 1))) # Substraction by one to get same result than pandas

def get_metrics(item):
    item["count"] = 0
    item["max_val"] = None
    item["min_val"] = None
    item["sum_val"] = 0
    for index, value in enumerate(item["value"]):
        if value is None:
            value = 0
            item["value"][index] = 0
        item["count"] += 1
        item["max_val"] = value if item["max_val"] is None or item["max_val"] < value else item["max_val"]
        item["min_val"] = value if item["min_val"] is None or item["min_val"] > value else item["min_val"]
        item["sum_val"] += value
    if (item["count"] == 0):
        raise(Exception("Au moins une des colonnes de ce fichier est vide"))
    item["mean"] = item["sum_val"] / item["count"]
    item["value"] = sorted(item["value"])
    item["25%"] = item["value"][math.floor(item["count"] / 4) - 1] + (item["value"][math.floor(item["count"] / 4)] - item["value"][math.floor(item["count"] / 4) - 1]) * (3 / 4)
    item["50%"] = item["value"][math.floor(item["count"] / 2) - 1] + (item["value"][math.floor(item["count"] / 2)] - item["value"][math.floor(item["count"] / 2) - 1]) * (2 / 4)
    item["75%"] = item["value"][math.floor(item["count"] / 4) * 3 - 1] + (item["value"][math.floor(item["count"] / 4) * 3] - item["value"][math.floor(item["count"] / 4) * 3 - 1]) * (1 / 4)
    item["std"] = get_std(item["value"], item["mean"], item["count"])

def print_metrics(data):
    ligns = ['', 'Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']
    keys = ['label', 'count', 'mean', 'std', 'min_val', '25%', '50%', '75%', 'max_val']
    for i in range(len(ligns)):
        print("{:10}".format(ligns[i]), end='')
        for value in data.values():
            if value["numerical"]:
                if i == 0:
                    print(" {:>8} |".format(value[keys[i]]), end='')
                else:
                    len_label = 8 if len(value["label"]) < 8 else len(value["label"])
                    value = "{:.2f}".format(value[keys[i]])
                    print(" {0:>{1}s} |".format(value, len_label), end='')
        print('')

def describe(data):
    for key, value in data.items():
        if value["numerical"] == True:
            get_metrics(data[key])
            value = pandas.Series(data[key]["value"])
            print(data[key]["label"])
            print (pandas.DataFrame.describe(value))
            print("---------------")
    return

if __name__ == "__main__":
    args = argparse.ArgumentParser("programms that describes the indicated csv file")
    args.add_argument("file", help="The file to describe", type=str)
    args = args.parse_args()

    if os.path.isfile(args.file):
        try:
            full_data, data = get_data(args.file)
            describe(data)
            print_metrics(data)
        except Exception as e:
            sys.stderr.write(e.__str__() + "\n")
            sys.exit(1)
    else:
        sys.stderr.write("File is not valid\n")
        sys.exit(1)