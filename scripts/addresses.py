# STEP 4


import os
import pandas as pd
from tqdm import tqdm
import networkx as nx

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=SyntaxWarning)

from utils import get_stamp


base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir, 
                                        "..", 
                                        "data"))

os.makedirs(data_dir, exist_ok=True)
print('data_dir:', data_dir)


def ipparse(s):
    try:
        if 'ipv4' in s.lower(): # 'ipv4://149.202.71.189:9735'
            s = s.split('://')[1].split(':')[0]
        elif 'ipv6' in s.lower(): # 'ipv6://[2001:470:5f:5f::232]:9735'
            s = s.split('[')[1].split(']')[0]
        if len(s) > 5\
            and '127.0.0.1' not in s\
            and '127.0.1.1' not in s\
            and '0.0.0.0' not in s\
            and 'tor' not in s\
            and 'onion' not in s\
            and 'UNKNOWN' not in s:
            return s
    except:
        pass 


addresses = os.path.join(data_dir, "addresses.csv")
graphs = pd.read_csv(os.path.join(data_dir, 'shapes.csv'), 
                            parse_dates=True, index_col=1)

if os.path.exists(addresses):
    results = pd.read_csv(addresses, dtype=str)
else:
    results = pd.DataFrame()

timestamps = set(results.timestamp) if 'timestamp' in results else set()
for item in tqdm(graphs.file_name):
    timestamp = get_stamp(item)
    if not timestamp in timestamps:
        g = nx.read_gml(os.path.join(data_dir, item))
        a = [(n, ipparse(g.nodes[n]['addresses']), timestamp) 
                    for n in g.nodes if 'addresses' in g.nodes[n]]
        a = [i for i in a if i[1]]
        a = pd.DataFrame(a, columns=['node', 'address', 'timestamp'])
        results = pd.concat([results, a])
        timestamps.add(timestamp)
        results.to_csv(addresses, index=False)

results.drop_duplicates(subset='node', inplace=True)
results.to_csv(addresses, index=False)