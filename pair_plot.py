import pandas as pd
import seaborn as sns
import argparse
import matplotlib.pyplot as plt
import sys
import os
from describe import get_data
from constants import HOUSES_COL

if __name__ == '__main__':
    args = argparse.ArgumentParser("programms that describes the indicated csv file")
    args.add_argument("file", help="The file to describe", type=str)
    args = args.parse_args()
    try:
        if (not os.path.isfile(args.file)):
            raise("Invalid File")
        df = pd.read_csv(args.file, sep=',')
        sns.set(style="ticks", color_codes=True)
        df.pop('Index')
        if not df.loc[:, HOUSES_COL].isnull().values.any():
            sns.pairplot(df.dropna(), hue =HOUSES_COL)
        else:
            df.pop(HOUSES_COL)
            sns.pairplot(df.dropna())
        plt.tight_layout()
        plt.savefig('pair_plot.pdf')
    except:
        sys.stderr.write("Le fichier n'est pas correctement formaté ou n'existe pas\n")
        sys.exit(1)