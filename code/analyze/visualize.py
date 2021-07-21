import json
import pandas as pd
import os
import shutil
import numpy as np
import itertools
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy import sparse
# from analyze.connect_db import MysqlController

ALL_2020 = "./data/matrix/kdc/"
ALL_2020_DATA = os.listdir(ALL_2020)


def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

def set_barplot_data(indexes, dataframe):
    dataframes = []
    x = dataframe.columns[1:]

    for idx in indexes:
        title = sgd1.loc[idx]["index"]
        y = dataframe.loc[idx].values[1:]
        info = ("code", "value", pd.DataFrame({"code": x, "value": y}), title)
        dataframes.append(info)
    return dataframes

def draw_barplot(indexes, dataframe):
    fig, axs = plt.subplots(ncols=len(indexes))
    dataframes = set_barplot_data(indexes, dataframe)
    for idx, dataframe in enumerate(dataframes):
        x = dataframe[0]
        y = dataframe[1]
        data = dataframe[2]
        title = dataframe[3]

        if type(axs) == np.ndarray:
            chart = sns.barplot(x=x, y=y, data=data, ax=axs[idx])
            axs[idx].set_title(title)
        else:
            chart = sns.barplot(x=x, y=y, data=data)
            axs.set_title(title)
        # 바 차트위에 수치 작성    
        for idx, row in data.iterrows():
            chart.text(row.name, row.value, str(round(row.value, 2)) + f"({row.name})", ha="center")
        
    plt.show()


set_config()

sgd_data = pd.read_pickle(ALL_2020 + ALL_2020_DATA[0])

sgd1 = sgd_data['isbn1_sgd'].reset_index()
sgd2 = sgd_data['isbn2_sgd'].reset_index()
sgd3 = sgd_data['isbn3_sgd'].reset_index()

indexes = [10, 11]
draw_barplot(indexes, sgd1)
draw_barplot(indexes, sgd2)
draw_barplot(indexes, sgd3)

