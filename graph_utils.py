# graph_utils.py

import os
import pickle

import osmnx as ox

from config import CACHE_FILE

# exported graph structures
adj_list = {}
node_coords = {}
G = None


def load_graph():
    """Load graph from cache or download from OSM."""
    global G, adj_list, node_coords

    if os.path.exists(CACHE_FILE):
        print(f"📦 Found cache: {CACHE_FILE}. Loading...")
        with open(CACHE_FILE, "rb") as f:
            data = pickle.load(f)
        G = data["G"]
        adj_list = data["adj_list"]
        node_coords = data["node_coords"]
        print("✅ Map Loaded!")
        return

    print("⏳ Downloading Map... (Takes ~60s)")
    G = ox.graph_from_point(
        (33.6938, 73.0652), dist=18000, network_type="drive"
    )

    print("⚙️ Processing Data...")
    for u, v, data in G.edges(data=True):
        if u not in adj_list:
            adj_list[u] = []
        if v not in adj_list:
            adj_list[v] = []

        if u not in node_coords:
            node_coords[u] = (G.nodes[u]["y"], G.nodes[u]["x"])
        if v not in node_coords:
            node_coords[v] = (G.nodes[v]["y"], G.nodes[v]["x"])

        length = data.get("length", 50)
        hw_type = data.get("highway", "unclassified")
        if isinstance(hw_type, list):
            hw_type = hw_type[0]

        adj_list[u].append({"neighbor": v, "length": length, "type": hw_type})

    with open(CACHE_FILE, "wb") as f:
        pickle.dump(
            {"G": G, "adj_list": adj_list, "node_coords": node_coords}, f
        )

    print("✅ System Ready!")
