import pickle
import numpy as np
import pandas as pd

RANDOM_STATE = 34

dir_data = 'data/'


def correct_preds(sub):
    sub.loc[sub['views'] < 500, 'views'] = 500

    all_dupls = pd.read_csv(dir_data+'accurate_preds.csv')

    for i in all_dupls['document_id_test']:
        sub.loc[sub['document_id'] == i, ['views', 'depth', 'full_reads_percent']
                ] = all_dupls.loc[all_dupls['document_id_test'] == i, ['views', 'depth', 'full_reads_percent']].to_numpy().flatten()

    return sub


def encode_cols(t, mapping, dir_data='data/', as_type=np.int32):
    encoders = load_pickle(dir_data+"encs.pcl")

    for (col, enc) in mapping:
        t[col] = encoders[enc].transform(t[col]).astype(as_type) + 1


def p(*args):
    for a in args:
        print(a, "\n ~")


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        obj = pickle.load(f)
    return obj


def save_pickle(file_name, data):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)


def select_cols(df, names):
    if not isinstance(names, list):
        names = [names]
    new_cols = []
    for col in df.columns:
        for name in names:
            if col.startswith(name):
                new_cols.append(col)
    return new_cols


def flat_cols(df, pre='k', columns=True):

    def f(se):
        return [
            pre + '_' + '_'.join(map(str, col)) if type(col) is tuple else pre + '_' +
            str(col) for col in se.to_numpy()
        ]

    if columns:
        df.columns = f(df.columns)
    else:
        df.index = f(df.index)


def mem(df):
    memory = df.memory_usage().sum() / 1024**2
    print(f'Память: {round(memory)} Мб')


def reduce_mem(df):
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if str(col_type)[:5] == "float":
            c_min = df[col].min()
            c_max = df[col].max()
            if c_min > np.finfo("f2").min and c_max < np.finfo("f2").max:
                # np.float16 не принимает бывает
                df[col] = df[col].astype(np.float32)
            elif c_min > np.finfo("f4").min and c_max < np.finfo("f4").max:
                df[col] = df[col].astype(np.float32)
            else:
                df[col] = df[col].astype(np.float64)
        elif str(col_type)[:3] == "int":
            c_min = df[col].min()
            c_max = df[col].max()
            if c_min > np.iinfo("i1").min and c_max < np.iinfo("i1").max:
                df[col] = df[col].astype(np.int8)
            elif c_min > np.iinfo("i2").min and c_max < np.iinfo("i2").max:
                df[col] = df[col].astype(np.int16)
            elif c_min > np.iinfo("i4").min and c_max < np.iinfo("i4").max:
                df[col] = df[col].astype(np.int32)
            elif c_min > np.iinfo("i8").min and c_max < np.iinfo("i8").max:
                df[col] = df[col].astype(np.int64)
        # elif col == "timestamp":
        #     df[col] = pd.to_datetime(df[col])
        # elif str(col_type)[:8] != "datetime":
        #     df[col] = df[col].astype("category")
    end_mem = df.memory_usage().sum() / 1024**2
    print(f'Память ДО: {round(start_mem,1)} Мб')
    print(f'Память ПОСЛЕ: {round(end_mem,1)} Мб')
    print('Уменьшилось на', round(start_mem - end_mem, 2), 'Мб (минус',
          round(100 * (start_mem - end_mem) / start_mem, 1), '%)')
    return
