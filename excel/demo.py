import xlrd
import os
import pandas as pd

if __name__ == '__main__':

    file_list = os.listdir(r"./raw_data")
    count = 0
    for idx, i in enumerate(file_list):
        if idx % 4 == 0:
            print(file_list[idx])
            df = pd.read_excel("./raw_data/" + file_list[idx], sheet_name=0)
            print(file_list[idx + 1])
            df1 = pd.read_excel("./raw_data/" + file_list[idx + 1], sheet_name=0)
            print(file_list[idx + 2])
            df2 = pd.read_excel("./raw_data/" + file_list[idx + 2], sheet_name=0)
            print(file_list[idx + 3])
            df3 = pd.read_excel("./raw_data/" + file_list[idx + 3], sheet_name=0)
            res = df.append(df1).append(df2).append(df3)
            res.to_excel("./final/" + file_list[idx].split('.')[0][:-1] + ".xlsx", index=False)
            print(res.shape)
            print("=================")

