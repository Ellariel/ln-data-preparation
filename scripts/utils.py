import os
import random
import numpy as np
import networkx as nx
from tqdm import tqdm
from lntopo.common import DatasetFile
from lntopo.parser import ChannelAnnouncement, ChannelUpdate, NodeAnnouncement



def set_seed(seed=13):
    random.seed(seed)
    np.random.seed(seed)


def read_shape_and_degree(fname):
    g = nx.read_gml(fname)
    return len(g.nodes), len(g.edges), np.mean(list(dict(g.degree).values()))


def get_stamp(s):
    s = os.path.split(s)[1].split('.g')[0]
    if '-' in s:
        s = s.split('-')[1]
    return s


def restore_graph(datafile, timestamp, verbose=True):
    """Restore reconstructs the network topology at a specific time in the past.
    Restore replays gossip messages from a dataset and reconstructs
    the network as it would have looked like at the specified
    timestamp in the past.
    """
    cutoff = timestamp - 2 * 7 * 24 * 3600
    channels = {}
    nodes = {}
    
    dataset = DatasetFile().convert(datafile, 0, 0)
    for m in tqdm(dataset, desc="Replaying gossip messages", disable=not verbose):
        if isinstance(m, ChannelAnnouncement):

            channels[f"{m.short_channel_id}/0"] = {
                "source": m.node_ids[0].hex(),
                "destination": m.node_ids[1].hex(),
                "timestamp": 0,
                "features": m.features.hex(),
            }

            channels[f"{m.short_channel_id}/1"] = {
                "source": m.node_ids[1].hex(),
                "destination": m.node_ids[0].hex(),
                "timestamp": 0,
                "features": m.features.hex(),
            }

        elif isinstance(m, ChannelUpdate):
            scid = f"{m.short_channel_id}/{m.direction}"
            chan = channels.get(scid, None)
            ts = m.timestamp

            if ts > timestamp:
                # Skip this update, it's in the future.
                continue

            if ts < cutoff:
                # Skip updates that cannot possibly keep this channel alive
                continue

            if chan is None:
                continue
                #raise ValueError(
                #    f"Could not find channel with short_channel_id {scid}"
                #)

            if chan["timestamp"] > ts:
                # Skip this update, it's outdated.
                continue

            chan["timestamp"] = ts
            chan["fee_base_msat"] = m.fee_base_msat
            chan["fee_proportional_millionths"] = m.fee_proportional_millionths
            chan["htlc_minimim_msat"] = m.htlc_minimum_msat
            if m.htlc_maximum_msat:
                chan["htlc_maximum_msat"] = m.htlc_maximum_msat
            chan["cltv_expiry_delta"] = m.cltv_expiry_delta
            
        elif isinstance(m, NodeAnnouncement):
            node_id = m.node_id.hex()

            old = nodes.get(node_id, None)
            if old is not None and old["timestamp"] > m.timestamp:
                continue

            alias = m.alias.replace(b'\x00', b'').decode('ASCII', 'ignore')
            nodes[node_id] = {
                "id": node_id,
                "timestamp": m.timestamp,
                "features": m.features.hex(),
                "rgb_color": m.rgb_color.hex(),
                "alias": alias,
                "addresses": ",".join([str(a) for a in m.addresses]),
                "out_degree": 0,
                "in_degree": 0,
            }

    # Cleanup pass: drop channels that haven't seen an update in 2 weeks
    todelete = []
    for scid, chan in tqdm(channels.items(), desc="Pruning outdated channels", disable=not verbose):
        if chan["timestamp"] < cutoff:
            todelete.append(scid)
        else:
            node = nodes.get(chan["source"], None)
            if node is None:
                continue
            else:
                node["out_degree"] += 1
            node = nodes.get(chan["destination"], None)
            if node is None:
                continue
            else:
                node["in_degree"] += 1

    for scid in todelete:
        del channels[scid]

    nodes = [n for n in nodes.values() if n["in_degree"] > 0 or n['out_degree'] > 0]

    #if len(channels) == 0:
    #    print(
    #        "ERROR: no channels are left after pruning, make sure to select a"
    #        "timestamp that is covered by the dataset."
    #    )
    #    return

    g = nx.DiGraph()
    for n in nodes:
        g.add_node(n["id"], **n)

    for scid, c in channels.items():
        g.add_edge(c["source"], c["destination"], scid=scid, **c)

    return g

