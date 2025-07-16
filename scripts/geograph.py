# STEP 6


import os, sys
import json
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


graphs = pd.read_csv(os.path.join(data_dir, 'shapes.csv'), 
                            parse_dates=True)
addresses = os.path.join(data_dir, "addresses.csv")
geojson = os.path.join(data_dir, "geo.json")

if os.path.exists(geojson):
    with open(geojson, 'r') as f:
        geojson = json.load(f)
else:
    geojson = {}

if os.path.exists(addresses):
    addresses = pd.read_csv(addresses, dtype=str)
    addresses.set_index('node', inplace=True)
else:
    addresses = pd.DataFrame()

geographs = os.path.join(data_dir, "shapes.geo.csv.tmp")
if os.path.exists(geographs):
    results = pd.read_csv(geographs, dtype=str)
else:
    results = pd.DataFrame()

if len(addresses) < 1 or len(geojson) < 1:
    print('There is some issues with data files..')
    sys.exit()

timestamps = set(results.timestamp) if 'timestamp' in results else set()
for item in tqdm(graphs.file_name):
    timestamp = get_stamp(item)
    if not timestamp in timestamps:
        g = nx.read_gml(os.path.join(data_dir, item))
        fname = f"{timestamp}.gml.geo"
        encoded = 0
        for n in g.nodes:
            try:
                ip = addresses.loc[n]['address']
                geo = geojson[ip]
                g.nodes[n]['geojson'] = geo
                encoded += 1
            except:
                pass
        nx.write_gml(g, os.path.join(data_dir, fname))
        a = pd.DataFrame([(timestamp, encoded, fname)], 
                columns=['timestamp', 'geocoded_nodes', 'file_name'])
        results = pd.concat([results, a])
        timestamps.add(timestamp)     

results.to_csv(geographs, index=False)


pd.concat([graphs[['timestamp', 'datetime', 'nodes', 'channels', 'degree', 'diameter']],
                   results[['geocoded_nodes', 'file_name']]], axis=1)\
                   .to_csv(os.path.join(data_dir, "shapes.geo.csv"), index=False)
