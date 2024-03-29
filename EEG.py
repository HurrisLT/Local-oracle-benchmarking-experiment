import glob
import os
import shutil

import pandas
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
gen_count = 1
ext_count = 5  # split
int_count = 5  # split
peer_count = 3# split
part_run = 3  # for


# write function asummes Labal will be last element in data set if any other column apears last Label should be replaced by it
def write_json_multiline(df, path, name):
    file = open(path + name,"w")
    file.writelines("[")
    for i in range(len(df)):
        file.writelines("{")
        for col in df.columns:
            if col != "A15_B3of3":
                file.write("\"" + col.lower() + "\":" + str(df[col].iloc[i]) + ",")
            else:
                file.write("\"" + col.lower() + "\":" + str(df[col].iloc[i]))
        if len(df) - 1 != i:
            file.writelines("},")
        else:
            file.writelines("}")
    file.writelines("]")
    file.close()
# append function asummes Labal will be last element in data set if any other column apears last Label should be replaced by it
def append_json_multiline(file ,df, last):
    for i in range(len(df)):
        file.writelines("{")
        for col in df.columns:
            if col != "A15_B3of3":
                file.write("\"" + col.lower() + "\":" + str(df[col].iloc[i]) + ",")
            else:
                file.write("\"" + col.lower() + "\":" + str(df[col].iloc[i]))
        if len(df) - 1 != i:
            file.writelines("},")
        else:
            if not last:
                file.writelines("},")
            else:
                file.writelines("}")

def generate_data(type_name, iter, EEG_DF_gen):
    # using sklearn we generate moon data

    #EEG_DF = EEG_DF.drop("id", axis=1)
    #EEG_DF = EEG_DF.rename(columns={"y": "Label"})
    X = EEG_DF_gen
    y = EEG_DF_gen["Label"].to_numpy()

    # data normalization using z-score

    gen_path = './Data/gen' + str(iter)
    skf = StratifiedKFold(n_splits=ext_count)
    ext_counter = 0
    #os.mkdir(gen_path)
    for train_index, test_index in skf.split(X, y):
        # creating test train data sets
        data_train = X.iloc[train_index]
        data_test = X.iloc[test_index]
        y_train = data_train["Label"].to_numpy()

        # creating folder names and paths

        ext_path = gen_path + "/ext" + str(ext_counter)
        #os.mkdir(ext_path)
        #os.mkdir(ext_path + '/monolith/')
        #os.mkdir(ext_path + '/monolith' + "/json")
        #os.mkdir(ext_path + '/monolith' + "/csv")
        df_train = data_train
        df_test = data_test

        # writing data frames to json and csv formats

        #write_json_multiline(df_train, ext_path + '/monolith' + "/json/", "train.json")
        #write_json_multiline(df_test, ext_path + '/monolith' + "/json/", "test.json")

        #df_train.to_csv(ext_path + '/monolith' + "/csv/" + "train.csv", sep=',', header=False, index=False)
        #df_test.to_csv(ext_path + '/monolith' + "/csv/" + "test.csv", sep=',', header=False, index=False)
        int_counter = 0
        # be stratified ir shuffle true, dar galima ma=inti int count iki 5
        skf = KFold(n_splits=int_count, shuffle=True)
        for train_spit_index, test_spit_index in skf.split(data_train, y_train):

            peer_path = "peer" + str(part_run)

            data_train_split = X.iloc[train_spit_index]
            print(data_train_split)
            y_train_split = data_train_split["Label"].to_numpy()
            data_test_split = X.iloc[test_spit_index]
            y_test_split =  data_test_split["Label"].to_numpy()

            df_train_temp = data_train_split
            df_test_temp =  data_test_split
            int_path = "int" + str(int_counter)
            full_test_data_path = ext_path + "/" + int_path + "/" + peer_path + '/fulltestdata'
            #os.mkdir(ext_path + "/" + int_path)
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
            for unused_split_index, int_split_index in skf.split(data_train_split, y_train_split):
                part_path = "part" + str(part_counter)
                full_split_path = ext_path + "/" + int_path + "/" + peer_path + "/" + part_path
                os.mkdir(full_split_path)
                os.mkdir(full_split_path + "/json")
                os.mkdir(full_split_path + "/csv")
                df_part_train = df_train_temp.take(int_split_index)
                write_json_multiline(df_part_train,  full_split_path + "/json/", "train.json")
                df_part_train.to_csv(full_split_path + "/csv/" + "/train.csv", sep=',', header=False, index=False)
                part_counter = part_counter + 1
            #test data part
            part_counter = 0

            for unused_split_index, int_split_index in skf.split(data_test_split, y_test_split):
                part_path = "part" + str(part_counter)
                full_split_path = ext_path + "/" + int_path + "/" + peer_path + "/" + part_path
                df_part_test = df_test_temp.take(int_split_index)
                write_json_multiline(df_part_test, full_split_path + "/json/", "test.json")
                last = False
                if part_counter == part_run - 1:
                    last = True
                append_json_multiline(filefulltest,df_part_test, last)
                df_part_test.to_csv(full_split_path + "/csv/" + "/test.csv", sep=',', header=False, index=False)
                df_part_test.to_csv(full_test_data_path + "/csv/"+ "/fulltest.csv", sep=',', header=False, index=False, mode="a")
                part_counter = part_counter + 1

            filefulltest.writelines("]")
            filefulltest.close()
        ext_counter = ext_counter + 1

# main program
dir_path = './Data'
#shutil.rmtree(dir_path)
#os.mkdir('./Data')
EEG_DF = pandas.read_csv('./UnmodifiedData/creditA.csv', index_col=False)
#generate_data('AdultInc', 0, EEG_DF)
skf = StratifiedKFold(n_splits=gen_count)

for col in EEG_DF.columns:
    y = EEG_DF["Label"].to_numpy()
iter = 0
for train_index, test_index in skf.split(EEG_DF, y):
    if iter == 0:
        EEG_DF_gen = EEG_DF.iloc[test_index]
        generate_data('creaditA', iter, EEG_DF_gen)
        break
    iter = iter + 1
