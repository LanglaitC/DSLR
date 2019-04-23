from describe import get_data
import matplotlib.pyplot as plt
import argparse
from constants import HOUSES_INDEX

def create_histogram(houses, value, title, graph_num):
    plt.subplot(7, 2, graph_num)
    plt.title(title)
    houses_dict = {}
    houses_set = []
    houses_value = []
    for i in range(len(houses)):
        if value[i] != None:
            if houses[i] not in houses_dict:
                houses_value.append([value[i]])
                houses_dict[houses[i]] = len(houses_dict)
                houses_set.append(houses[i])
            else:
                houses_value[houses_dict[houses[i]]].append(value[i])
    plt.hist(houses_value, label=houses_set)

if __name__ == '__main__':
    args = argparse.ArgumentParser("Buid histogram from csv file")
    args.add_argument("file", help="The file to analyze")
    args = args.parse_args()
    full_data, data = get_data(args.file)
    i = 0
    for value in data.values():
        if value["numerical"] and value["label"] != "Index":
            i += 1
            create_histogram(data[HOUSES_INDEX]["value"], value["value"], value["label"], i)
    #plt.legend()
    plt.show()