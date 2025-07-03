# STEP 3

import os
from glob import glob
import networkx as nx
import pandas as pd
from tqdm import tqdm
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")

from utils import get_stamp, set_seed, read_shape



base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir, 
                                        "..", 
                                        "data"))

os.makedirs(data_dir, exist_ok=True)
print('data_dir:', data_dir)


def proccess_graph(source_file, results_file, seed=13):
    set_seed(seed)
    g = nx.read_gml(source_file).to_undirected()
    zero_capacity_edges = [e for e in g.edges 
                                if int(g.edges[e].get('htlc_maximum_msat', 0)) < 1]
    g.remove_edges_from(zero_capacity_edges)
    zero_degree_nodes = [n[0] for n in g.degree 
                                if int(n[1]) < 1]
    g.remove_nodes_from(zero_degree_nodes)
    nx.write_gml(g, results_file)


graphs = pd.read_csv(os.path.join(data_dir, 'shapes.csv.tmp'), parse_dates=True, index_col=0)

for f in tqdm(graphs.file_name):
    source_file = os.path.join(data_dir, f)
    results_file = os.path.join(data_dir, f"{get_stamp(f)}.gml")
    if not os.path.exists(results_file):
        proccess_graph(source_file, results_file)
    
# update shapes
filelist = [i for i in glob(data_dir + "/*.gml")]
timestamps = [get_stamp(i) for i in filelist]
shapes = [read_shape(i) for i in tqdm(filelist)]
df = pd.concat([pd.Series(timestamps), 
           pd.DataFrame(shapes), 
           pd.Series(filelist)], axis=1)
df.columns = ['datetime', 'nodes', 'edges', 'file_name']
df['datetime'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y%m%d'))
df.index = pd.DatetimeIndex(pd.to_datetime(df['datetime']))
df = df[df.index >= '20.01.2019']
df['file_name'] = df['file_name'].apply(lambda x: os.path.split(x)[1])
df['datetime'] = pd.to_datetime(df.index)
df['timestamp'] = df['datetime'].apply(lambda x:  int(x.timestamp()))
df = df[['timestamp', 'datetime', 'nodes', 'edges', 'file_name']]

df.to_csv(os.path.join(data_dir, 'shapes.csv'), index=False)