## Topology and Network Dynamics of the Lightning Network: A Comprehensive Analysis

These are the data and scripts associated with the paper on the comprehensive analysis of the network’s topology and its temporal dynamics. The folder contains several scripts and a Dockerfile used to compute various network science metrics. The final results of these calculations are available in `result/metrics.csv` and it is merged with `make_metrics.py`. All figures from the paper can be reproduced using the `make_figures.py` script.

Note that since the raw data is quite large, we did not mirror it here, but it can be directly downloaded from [(Decker, 2020)](https://github.com/lnresearch/topology). Working and temporary data and results are also not stored here, but can be reproduced with the scripts available, see `metrics_*.py`.

The repository includes the following calculated metrics (see `utils.py`):

 **Category**|**Metrics and attributes**                    
-------------|--------------------------
Basic Network Structure|nodes, edges (channels), components, density, diameter, shortest path length, mean degree, degree assortativity
Connectivity & Resilience|bridges, average node connectivity, minimal edge cover, transitivity, average clustering
Function & Dynamics|global efficiency, information centrality, mean betweenness centrality, communicability betweenness centrality, common neighbor centrality, constraint value, effective size, Burt's effective size, closeness vitality
Emergent Patterns|resource allocation index, Jaccard coefficient, preferential attachment, label communities (FLP), lpa communities (ALP)
Other|payment hop distribution and degree distribution approximation parameters, Gini betweenness centrality, node intersection rate, channel intersection rate, Wiener index


### Citation

```python
Valko, D., & Marx Gómez, J. (2025). Topology and Network Dynamics of the Lightning Network: A Comprehensive Analysis
```

```python
@misc{ValkoMarxGómez2025,
title={Topology and Network Dynamics of the Lightning Network: A Comprehensive Analysis}, 
author={Danila Valko and Jorge Marx Gómez},
year={2025},
journal = {},
month = {},
volume = {},
pages = {},
doi = {},
}
```


### Sources and References

- Raw data snapshots of the Lightning Network are obtained from [(Decker, 2020)](https://github.com/lnresearch/topology).
- Native pathfinding algorithms are based on [[Kumble & Roos, 2021]](https://ieeexplore.ieee.org/document/9566199); [[Kumble, Epema & Roos, 2021]](https://arxiv.org/pdf/2107.10070.pdf); see also, [GitHub](https://github.com/SatwikPrabhu/Attacking-Lightning-s-anonymity).


