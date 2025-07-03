# STEP 2

import os
import pandas as pd
from glob import glob
from tqdm import tqdm
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from utils import read_shape, get_stamp



def filter_holes(df):
    flag = True
    df = df.copy()
    for idx, item in list(df.iterrows())[1:]:
        pitem = df.iloc[idx - 1]
        check_1 = (len(str(item['nodes'])) > len(str(pitem['nodes']))) or\
                (len(str(item['edges'])) > len(str(pitem['edges'])))
        check_2 = (len(str(item['nodes'])) < len(str(pitem['nodes']))) or\
                (len(str(item['edges'])) < len(str(pitem['edges'])))
        if check_1:
            flag = True
        if check_2:
            flag = False
        df.loc[idx, 'keep'] = flag
    return df

base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir, 
                                        "..", 
                                        "data"))

os.makedirs(data_dir, exist_ok=True)
print('data_dir:', data_dir)

# manual fix
fix = pd.read_csv(os.path.join(data_dir, 'fix.txt'), 
                  header=None, dtype=str)[0].to_list()

filelist = [i for i in glob(data_dir + "/*.gml.tmp")]
filelist = [i for i in filelist if get_stamp(i) not in fix]
timestamps = [get_stamp(i) for i in filelist]
shapes = [read_shape(i) for i in tqdm(filelist)]
df = pd.concat([pd.Series(timestamps), 
           pd.DataFrame(shapes), 
           pd.Series(filelist)], axis=1)
df.columns = ['datetime', 'nodes', 'edges', 'file_name']
df['datetime'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))

while True:
    df = filter_holes(df)
    done = not (df['keep'] == False).any()
    df = df[df['keep'] == True].reset_index(drop=True)
    if done:
        break  

df.index = pd.DatetimeIndex(pd.to_datetime(df['datetime']))
df = df[df.index >= '20.01.2019']
df['file_name'] = df['file_name'].apply(lambda x: os.path.split(x)[1])
df['datetime'] = pd.to_datetime(df.index)
df['timestamp'] = df['datetime'].apply(lambda x:  int(x.timestamp()))
df = df[['timestamp', 'datetime', 'nodes', 'edges', 'file_name']]

df.to_csv(os.path.join(data_dir, 'shapes.csv.tmp'), index=False)