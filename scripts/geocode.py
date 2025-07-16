# STEP 5


import os, sys
import argparse
import json
import requests
import pandas as pd
from tqdm import tqdm


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=SyntaxWarning)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', default=None, type=str)
    parser.add_argument('--proxy', default=None, type=str)
    args = parser.parse_args()
else:
     sys.exit()


base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir, 
                                        "..", 
                                        "data"))

os.makedirs(data_dir, exist_ok=True)
print('data_dir:', data_dir)


def get_proxy():
    from swiftshadow import QuickProxy
    return QuickProxy().as_requests_dict()


proxy = get_proxy() if args.proxy else None
print('key:', args.key)
print('proxy:', proxy)

addresses = pd.read_csv(os.path.join(data_dir, 
                            "addresses.csv"), dtype=str)
addresses = set(addresses.address)

geojson_file = os.path.join(data_dir, "geo.json")
if os.path.exists(geojson_file):
    with open(geojson_file, 'r') as f:
        geojson = json.load(f)
        print('ready:', len(geojson))
else:
    geojson = {}

def flush(data):
    with open(geojson_file, 'w') as f:
        json.dump(data, f)

def get_ip(loc, token=None, proxies=None):
    url = f'https://ipinfo.io/{loc}/json'
    if token:
        url += f'?token={token}'
    r = requests.get(url, proxies=proxies)
    if r.ok:
        print(f"ok: {url}")
        return r.json()
    else:
        print(r.text)

test = get_ip('8.8.8.8', token=args.key, proxies=proxy)
if not test:
    print(test)
    sys.exit(0)

counter = 0
for item in tqdm(addresses):
    if not item in geojson and 'UNKNOWN' not in item:
        g = get_ip(item, token=args.key, proxies=proxy)
        if g:
            counter += 1
            geojson[item] = g
            if counter >= 500:
                counter = 0
                flush(geojson)
                if args.proxy:
                    proxy = get_proxy()

flush(geojson)
