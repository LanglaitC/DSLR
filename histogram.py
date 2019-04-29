from describe import get_data
import matplotlib.pyplot as plt
import argparse
from constants import HOUSES_INDEX
import sys
import os

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
    plt.legend()

if __name__ == '__main__':
    args = argparse.ArgumentParser("Buid histogram from csv file")
    args.add_argument("file", help="The file to analyze")
    args = args.parse_args()
    try:
        if not os.path.isfile(args.file):
            raise("Invalid File")
        full_data, data = get_data(args.file)
        i = 0
        plt.rc('font', size=6)
        for value in data.values():
            if value["numerical"] and value["label"] != "Index":
                i += 1
                create_histogram(data[HOUSES_INDEX]["value"], value["value"], value["label"], i)
        plt.show()
    except:
        sys.stderr.write("Le fichier n'est pas correctement formaté ou n'existe pas\n")
        sys.exit(1)