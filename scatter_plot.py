from describe import get_data
import matplotlib.pyplot as plt
import argparse
from constants import HOUSES_INDEX 
import sys
import os

def get_all_houses(houses, value):
    houses_dict = {}
    houses_set = []
    houses_value = []
    for i in range(len(houses)):
        if houses[i] not in houses_dict:
            houses_value.append([value[i]])
            houses_dict[houses[i]] = len(houses_dict)
            houses_set.append(houses[i])
        else:
            houses_value[houses_dict[houses[i]]].append(value[i])
    return [houses_set, houses_value]

def create_scatter_plot(data_index, data):
    houses = data[HOUSES_INDEX]["value"]
    num_graph = 0
    houses_label, y = get_all_houses(houses, data[data_index]["value"])
    for index, value in data.items():
        if value["numerical"] and index != data_index and value["label"] != "Index":
            num_graph += 1
            plt.subplot(6, 2, num_graph)
            plt.ylabel(data[data_index]["label"])
            plt.title(value["label"])
            houses_label, x = get_all_houses(houses, value["value"])
            for j in range(len(x)):
                for i in range(len(x)):
                    if x[i] == None or y[i] == None:
                        del x[i]
                        del y[i]
                if houses_label[j]:
                    plt.scatter(x[j], y[j], label=houses_label[j])
                else:
                    plt.scatter(x[j], y[j])
            if len(x) != 1:
                plt.legend()
    plt.show()

if __name__ == '__main__':
    args = argparse.ArgumentParser("Buid histogram from csv file")
    args.add_argument("file", help="The file to analyze")
    args = args.parse_args()
    try:
        plt.rc('font', size=6)
        if not os.path.isfile(args.file):
            raise("Invalid File")
        full_data, data = get_data(args.file)
        for index, value in data.items():
            if value["numerical"] and value["label"] != "Index":
                create_scatter_plot(index, data)
    except:
        sys.stderr.write("Le fichier n'est pas correctement formaté ou n'existe pas\n")
        sys.exit(1)
