import sys
import math
import csv
import os
import argparse
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from constants import DATA_FILE, HOUSES_COL, T0_LABEL, SELECTED_FEATURES

class Train:
    def __init__(self, data, iterations, lr, visu):
        data.insert(0, T0_LABEL, np.ones(data.shape[0]))
        self.selected_features = [HOUSES_COL] + [T0_LABEL] + SELECTED_FEATURES
        self.data = data.loc[:, self.selected_features]
        self.data = self.data.dropna()
        self.lr = lr
        self.visu = visu
        self.iterations = iterations
        self.predictions = {}
        self.houses = self.data.loc[:, HOUSES_COL]
        self.houses_set = self.data.loc[:, HOUSES_COL].unique()
        

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self):
        std_deviations, means, x = self.ft_standardize(self.data.loc[:, self.selected_features[2:]])
        x.insert(0, T0_LABEL, self.data.loc[:, T0_LABEL])
        self.predictions['standard'] = {'std': list(std_deviations), 'mean': list(means)}
        self.predictions['houses'] = {}
        m = x.shape[0]
        for house in self.houses_set:
            cost = []
            thetas = np.zeros((x.shape[1]))
            y = self.is_from_house(house)
            for i in range(self.iterations):
                z = np.dot(x, thetas)
                h = self.sigmoid(z)
                j = (1 / m) * (np.dot(-y.T, np.log(h)) - np.dot((1 - y).T, np.log(1 - h)))
                cost.append(j)
                gradient = np.dot(x.T, (h - y)) / y.size
                thetas -= self.lr * gradient
            self.predictions['houses'][house] = list(thetas)
            if self.visu:
                plt.plot(cost ,label=house)
        if self.visu:
            plt.legend()
            plt.show()
        with open(DATA_FILE, 'w+') as json_file:  
            json.dump(self.predictions,  json_file)

    def is_from_house(self, house):
        return np.where(self.houses == house, 1, 0)

    def ft_standardize(self, matrix):
        return [matrix.std(), matrix.mean(), ((matrix - matrix.mean()) / matrix.std())]



if __name__ == '__main__':
    args = argparse.ArgumentParser("Statistic description of your data file")
    args.add_argument("file", help="File to descripte", type=str)
    args.add_argument("-i", "--iter", help="The number of iterations to go through the regression", default=10000, type=int)
    args.add_argument("-l", "--learning", help="The learning rate to use during the regression", default=0.01, type=float)
    args.add_argument("-v", "--visu", help="Activate visualization of cost evolution", default=False, action="store_true")
    args = args.parse_args()

    if os.path.isfile(args.file):
        try:
            df = pd.read_csv(args.file, sep=',')
            Train(df, args.iter, args.learning, args.visu).train()
        except Exception as e:
            sys.stderr.write('Le fichier n\'est pas bien formaté ou n\'existe pas\n')
            sys.exit(1)
    else:
        sys.stderr.write("Invalid input\n")
        sys.exit(1)