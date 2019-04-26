import pandas as pd
import seaborn as sns
import argparse
import matplotlib.pyplot as plt
from describe import get_data

if __name__ == '__main__':
    args = argparse.ArgumentParser("programms that describes the indicated csv file")
    args.add_argument("file", help="The file to describe", type=str)
    args = args.parse_args()
    df = pd.read_csv(args.file, sep=',')
    sns.set(style="ticks", color_codes=True)
    df.pop('Index')
    sns.pairplot(df.dropna(), hue = "Hogwarts House")
    plt.tight_layout()
    plt.savefig('pair_plot.pdf')