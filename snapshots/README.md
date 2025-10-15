## Description

This dataset contains 336 geolocated Lightning Network topology snapshots covering the years 2019–2023.
The snapshots were reconstructed from Decker’s publicly available gossip message data, accessible at [https://github.com/lnresearch/topology](https://github.com/lnresearch/topology) (last snapshot accessed on *2023-09-24*).

All files are bundled in a single archive: `snapshots.geo.zip`.
Each snapshot is stored in *GML* format and named using the pattern `YYYYMMDD.gml.geo` (e.g., `20190120.gml.geo`), where the filename corresponds to the snapshot date.
Snapshots can be loaded directly using the standard `nx.read_gml()` function from the *NetworkX* library.

The archive also includes `shapes.geo.csv`, which provides metadata for each snapshot, including:

* Unix timestamp and corresponding datetime
* Number of nodes and channels
* Average node degree
* Approximated graph diameter
* Number of geocoded nodes
* Associated snapshot filename

*Example:*

```python
timestamp,datetime,nodes,channels,degree,diameter,geocoded_nodes,file_name
1547942400,2019-01-20,1137,3240,5.699208443271768,7,771,20190120.gml.geo
1548028800,2019-01-21,1222,3760,6.153846153846154,7,826,20190121.gml.geo
```

A working demonstration of how to load and analyze the data is provided in the `example.ipynb` notebook.

*Note:* The archive also contains `scripts.zip`, which includes the reconstruction scripts for archival purposes only. It is recommended to use the actively maintained version available at: [https://github.com/ellariel/ln-data-preparation](https://github.com/ellariel/ln-data-preparation)

If you use this dataset, please cite it appropriately, along with the original Decker topology datasets.

## Sources and References

* Decker, C. (2020). *Lightning Network Research – Topology Datasets.*
  DOI: [10.5281/zenodo.4088530](https://doi.org/10.5281/zenodo.4088530)
  URL: [https://github.com/lnresearch/topology](https://github.com/lnresearch/topology)

* IPinfo Developer API (used for geolocation): [https://ipinfo.io](https://ipinfo.io)
