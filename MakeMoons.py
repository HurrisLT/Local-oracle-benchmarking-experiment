import glob
import os
import shutil

from sklearn.datasets import make_moons
from pandas import DataFrame
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold

# amount of data rows
n = 100000
# amount of network participants

# monolith gen0\ext0\train.csv
# monolith gen0\ext0\test.csv
# monolith gen0\ext0\outPDT.model
# monolith gen0\ext0\outPLR.model
# monolith gen0\ext0\outRLR.model
# monolith gen0\ext0\outRDT.model

# network gen0\ext0\int0\train.csv
# network gen0\ext0\int0\test.csv

# ensemble gen0\ext0\int0\peer7\part0\train0.csv
# ensemble gen0\ext0\int0\peer7\part0\test0.csv
# ensemble gen0\ext0\int0\peer7\part0\outPDT.csv - row 20000 col 7 saugoti pries vidurkinima


# naudoti situs pavadinimus folderiams
gen_count = 10  # for
ext_count = 5  # split
int_count = 5  # split
peer_count = 10  # split
part_run = 10  # for


def write_json_multiline(df, path, name):
    file = open(path + name,"w")
    file.writelines("[")
    for i in range(len(df)):
        file.writelines("{")
        file.write("\"label\":" + str(df.index[i]) + ",")
        file.write("\"x\":" + str(df.values[i][0]) + ",")
        file.write("\"y\":" + str(df.values[i][1]))
        if len(df) - 1 != i:
            file.writelines("},")
        else:
            file.writelines("}")
    file.writelines("]")
    file.close()

def append_json_multiline(file ,df, last):
    for i in range(len(df)):
        file.writelines("{")
        file.write("\"label\":" + str(df.index[i]) + ",")
        file.write("\"x\":" + str(df.values[i][0]) + ",")
        file.write("\"y\":" + str(df.values[i][1]))
        if len(df) - 1 != i:
            file.writelines("},")
        else:
            if not last:
                file.writelines("},")
            else:
                file.writelines("}")

def generate_data(type_name, iter):
    # using sklearn we generate moon data
    gen_path = './Data/gen' + str(iter)
    X, y = make_moons(n_samples=n, noise=0.15)
    print(y)
    skf = StratifiedKFold(n_splits=ext_count)
    ext_counter = 0
    os.mkdir(gen_path)
    for train_index, test_index in skf.split(X, y):
        # creating test train data sets
        x_train, x_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        # creating folder names and paths
        ext_path = gen_path + "/ext" + str(ext_counter)
        os.mkdir(ext_path)
        os.mkdir(ext_path + '/monolith/')
        os.mkdir(ext_path + '/monolith' + "/json")
        os.mkdir(ext_path + '/monolith' + "/csv")
        df_train = DataFrame(x_train, y_train)
        df_test = DataFrame(x_test, y_test)

        # writing data frames to json and csv formats

        write_json_multiline(df_train, ext_path + '/monolith' + "/json/", "train.json")
        write_json_multiline(df_test, ext_path + '/monolith' + "/json/", "test.json")

        df_train.to_csv(ext_path + '/monolith' + "/csv/" + "train.csv", sep=',', header=False, index=True)
        df_test.to_csv(ext_path + '/monolith' + "/csv/" + "test.csv", sep=',', header=False, index=True)
        int_counter = 0
        # be stratified ir shuffle true, dar galima ma=inti int count iki 5
        skf = KFold(n_splits=int_count, shuffle=True)
        for train_spit_index, test_spit_index in skf.split(x_train, y_train):
            peer_path = "peer" + str(part_run)
            x_split_train, x_split_test = X[train_spit_index], X[test_spit_index]
            y_split_train, y_split_test = y[train_spit_index], y[test_spit_index]
            df_train_temp = DataFrame(x_split_train, y_split_train)
            df_test_temp = DataFrame(x_split_test, y_split_test)
            int_path = "int" + str(int_counter)
            full_test_data_path = ext_path + "/" + int_path + "/" + peer_path + '/fulltestdata'
            os.mkdir(ext_path + "/" + int_path)
            os.mkdir(ext_path + "/" + int_path + "/" + peer_path)
            os.mkdir(ext_path + "/" + int_path + "/" + peer_path + '/outputs/')
            os.mkdir(full_test_data_path)
            os.mkdir(full_test_data_path +"/csv")
            os.mkdir(full_test_data_path +"/json")
            filefulltest = open(full_test_data_path + "/json/fulltest.json", "a")
            filefulltest.writelines("[")
            int_counter = int_counter + 1
            skf = StratifiedKFold(n_splits=part_run)
            part_counter = 0
            # train data part
            for unused_split_index, int_split_index in skf.split(x_split_train, y_split_train):
                part_path = "part" + str(part_counter)
                full_split_path = ext_path + "/" + int_path + "/" + peer_path + "/" + part_path
                os.mkdir(full_split_path)
                os.mkdir(full_split_path + "/json")
                os.mkdir(full_split_path + "/csv")
                df_part_train = df_train_temp.take(int_split_index)
                write_json_multiline(df_part_train,  full_split_path + "/json/", "train.json")
                df_part_train.to_csv(full_split_path + "/csv/" + "/train.csv", sep=',', header=False, index=True)
                part_counter = part_counter + 1
            #test data part
            part_counter = 0

            for unused_split_index, int_split_index in skf.split(x_split_test, y_split_test):
                part_path = "part" + str(part_counter)
                full_split_path = ext_path + "/" + int_path + "/" + peer_path + "/" + part_path
                df_part_test = df_test_temp.take(int_split_index)
                write_json_multiline(df_part_test, full_split_path + "/json/", "test.json")
                last = False
                if part_counter == part_run - 1:
                    last = True
                append_json_multiline(filefulltest,df_part_test, last)
                df_part_test.to_csv(full_split_path + "/csv/" + "/test.csv", sep=',', header=False, index=True)
                df_part_test.to_csv(full_test_data_path + "/csv/"+ "/fulltest.csv", sep=',', header=False, index=True, mode="a")
                part_counter = part_counter + 1

            filefulltest.writelines("]")
            filefulltest.close()
        ext_counter = ext_counter + 1

# main program
dir_path = '/home/vdledger/PycharmProjects/MakeMoonsGeneration/Data'
shutil.rmtree(dir_path)
os.mkdir('./Data')
for i in range(gen_count):
    generate_data('moons', i)
