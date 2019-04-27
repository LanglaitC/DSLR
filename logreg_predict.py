import json
import argparse
import sys
import os
import pandas as pd
import numpy as np
from constants import SELECTED_FEATURES, T0_LABEL, PREDICTION_FILE, HOUSES_COL
import csv

def prediction(thetas, data):
    house = None
    score = None
    for key, value in thetas.items():
        tmp = np.dot(thetas[key], data)
        if (score is None or tmp > score):
            score = tmp
            house = key
    return house

def ft_standardize(matrix, mean, std):
    return (matrix - mean) / std

if __name__ == '__main__':
    args = argparse.ArgumentParser("Predict houses from data")
    args.add_argument("file", help="File to descripte", type=str)
    args = args.parse_args()
    if os.path.isfile(args.file):
        try:
            df = pd.read_csv(args.file, sep=',')
            json_file = open('data.json')
            data_json = json.load(json_file)
            theta_dic = data_json['houses']
            std_devs = data_json['standard']['std']
            means = data_json['standard']['mean']
        except Exception as e:
            sys.stderr.write("Le fichier de data m'existe pas ou n'est pas formaté correctement\n")
            sys.exit(1)
    else:
        sys.stderr.write("Le fichier de data m'existe pas ou n'est pas formaté correctement\n")
        sys.exit(1)
    df.loc[:, SELECTED_FEATURES] = ft_standardize(df.loc[: , SELECTED_FEATURES], means, std_devs)
    df = df.loc[:, SELECTED_FEATURES]
    df.insert(1, T0_LABEL, np.ones(df.shape[0]))
    df = df.dropna()
    predictions = []
    for index, row in df.iterrows():
        predictions.append((index, prediction(theta_dic, row)))
    with open(PREDICTION_FILE, 'w+') as fd:
        writer = csv.writer(fd)
        writer.writerow(['Index', HOUSES_COL])
        for each in predictions:
            writer.writerow([each[0], each[1]])