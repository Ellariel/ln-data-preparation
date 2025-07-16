# STEP 1

import os
import ray
import networkx as nx
from glob import glob
from itertools import batched
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from utils import get_stamp


base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir, 
                                        "..", 
                                        "data"))

os.makedirs(data_dir, exist_ok=True)
print('data_dir:', data_dir)

num_cpu = 20
twoweeks = 130

ray.init(num_cpus=num_cpu)

@ray.remote
def proccess_timestamp(file_path, timestamp):
    from scripts.utils import restore_graph
    g = restore_graph(file_path, timestamp.timestamp(), verbose=False)
    if len(g.nodes) >= 0 and len(g.edges) >= 0:
        nx.write_gml(g, os.path.join(data_dir, f"{timestamp.strftime('%Y%m%d')}.gml.tmp"))
    return {timestamp.strftime('%Y%m%d'): (len(g.nodes), len(g.edges))}


for file_path in sorted(glob(data_dir + "/*.gsp.bz2"), reverse=True):
    print(f'start file: {file_path}')
    time_stamp = datetime.strptime(get_stamp(file_path), '%Y%m%d')
    stop_date = [get_stamp(i) for i in glob(data_dir + "/*.gml.tmp")]
    print(f'already done: {stop_date}')
    planned = []
    for i in range(0, twoweeks):
        ts = time_stamp - timedelta(weeks=2*i)
        if not ts.strftime('%Y%m%d') in stop_date and\
            int(ts.strftime('%Y%m%d')[:4]) > 2018:
                planned.append(ts)

    print(f'planned: {[i.strftime('%d.%m.%Y') for i in planned]}')

    results = []
    for batch in batched(planned, num_cpu):
        print(f"started new batch: {[i.strftime('%d.%m.%Y') for i in batch]}")
        results += ray.get([proccess_timestamp.remote(file_path, i) for i in batch])
        print('done.')

    results = {k: v for i in results for k, v in i.items()}
    print(f'planned: {results}')

