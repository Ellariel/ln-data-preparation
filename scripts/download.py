# STEP 0

import os
import requests
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

base_dir = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(base_dir, 
                                        "..", 
                                        "data"))

os.makedirs(data_dir, exist_ok=True)
print('data_dir:', data_dir)

dates = ['20201014', '20201102', '20201203',
        '20210104', '20210908', '20220823', '20230924']

files = [f'https://storage.googleapis.com/lnresearch/gossip-{f}.gsp.bz2' 
         for f in dates]

for f in tqdm(files):
    file_name = os.path.join(data_dir, os.path.basename(f))
    if not os.path.exists(file_name):
        print(f"downloading {f}")
        r = requests.get(f)
        r.raise_for_status()
        with open(file_name, "wb") as file:
            file.write(r.content)
    else:
        print(f"{f} is already there.")
