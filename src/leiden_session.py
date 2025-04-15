# leiden_session.py
import pandas as pd
import networkx as nx
import igraph as ig
from leidenalg import find_partition, RBConfigurationVertexPartition

def build_bipartite_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        obj_node = f"obj_{row['object_id']}"
        user_node = f"user_{row['participant_id']}"
        G.add_node(obj_node, bipartite=0)
        G.add_node(user_node, bipartite=1)
        if G.has_edge(obj_node, user_node):
            G[obj_node][user_node]['weight'] += 1
        else:
            G.add_edge(obj_node, user_node, weight=1)
    return G

def leiden_community_detection(nx_graph, resolution=1.0):
    nodes = list(nx_graph.nodes())
    edges = list(nx_graph.edges(data=True))
    ig_graph = ig.Graph()
    ig_graph.add_vertices(nodes)
    ig_graph.add_edges([(u, v) for u, v, _ in edges])
    ig_graph.vs["name"] = nodes
    if 'weight' in nx_graph.edges[next(iter(nx_graph.edges))]:
        weights = [d['weight'] for _, _, d in edges]
        ig_graph.es['weight'] = weights
    partition = find_partition(
        ig_graph,
        RBConfigurationVertexPartition,
        resolution_parameter=resolution,
        weights=ig_graph.es['weight'] if 'weight' in ig_graph.edge_attributes() else None
    )
    return partition

def map_communities_to_dataframe(partition, df, event_id):
    ig_graph = partition.graph
    node_community = {ig_graph.vs[i]['name']: comm for i, comm in enumerate(partition.membership)}

    rows = []
    for idx, row in df.iterrows():
        obj_node = f"obj_{row['object_id']}"
        user_node = f"user_{row['participant_id']}"
        comm_id = node_community.get(obj_node, node_community.get(user_node, -1))
        rows.append({
            'event_id': event_id,
            'row_index': idx,
            'session_id': f"{event_id}_sess_{comm_id}",
            'session_type': 'leiden'
        })

    return pd.DataFrame(rows).set_index('row_index')
