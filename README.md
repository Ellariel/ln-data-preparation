### Scripts for the paper "Geolocated Lightning Network topology snapshots: A dataset covering 2019–2023".

These are the scripts associated with a data paper on the Lightning Network snapshots reconstruction and geolocation. The folder contains several scripts representing a complete pipline. All figures from the paper can also be reproduced using `misc/validation.ipynb`.

Scripts must be executed in the sequence specified in the table bellow. Input data, temporary data and final data must be stored in the `data` folder until the scripts are finished.


| Stage     |Scripts           |
|:----------|:-----------------|
| 1. Data acquisition | 1. `download.py` |
| 2. Network graph reconstruction | 2. `slice.py` |
| 3. Pre-processing and consistency control | 3. `shapes.py` <br/> 4. `clean.py` |
| 4. Geolocation | 5. `addresses.py` <br/> 6. `geocode.py` <br/> 7. `geograph.py` |


#### Citation

```python
Danila Valko and Jorge Marx Gómez (2025). Geolocated Lightning Network topology snapshots: A dataset covering 2019–2023.
```

```python
@misc{ValkoMarxGomez2025,
title={Geolocated Lightning Network topology snapshots: A dataset covering 2019–2023}, 
author={Danila Valko and Jorge {Marx Gómez}},
year={2025},
journal = {},
month = {},
volume = {},
pages = {},
doi = {},
}
```


#### Sources and References

- The NetworkX library was used to represent and store network graphs, see Hagberg, A. A., Schult, D. A., & Swart, P. J. (2008). Exploring network structure, dynamics, and function using NetworkX. In G. Varoquaux, T. Vaught, & J. Millman (Eds.), *Proceedings of the 7th Python in Science Conference (SciPy2008)* (pp. 11–15). Pasadena, CA, USA. https://networkx.org/documentation/stable/index.html
- Lightning Network gossip messages data and related algorithms comes from Decker, C. (2020). Lightning Network Research - Topology Datasets. https://github.com/lnresearch/topology
- The IPinfo developer API was used to geocode the nodes. https://ipinfo.io



