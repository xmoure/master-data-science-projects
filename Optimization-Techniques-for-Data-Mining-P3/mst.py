import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import time
from scipy.spatial import distance


def find_clusters_with_mst_networkx(data, k):
    # Build a complete graph with nodes representing data points
    G = nx.complete_graph(len(data))

    # Add weights (distances) to the edges
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            # Euclidean distance between data points
            distance = np.linalg.norm(data[i] - data[j])
            G.add_edge(i, j, weight=distance)

    # Compute the minimum spanning tree of the graph
    mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

    # Sort edges by weight in descending order and remove k-1 highest weighted edges
    edges = sorted(mst.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    for i in range(k - 1):
        mst.remove_edge(edges[i][0], edges[i][1])

    # Identify clusters (connected components)
    clusters = list(nx.connected_components(mst))

    return [list(cluster) for cluster in clusters]


def plot_clusters(data, clusters, title, route):
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    plt.figure(figsize=(8, 6))

    for i, cluster in enumerate(clusters):
        points = data[cluster]
        plt.scatter(points[:, 0], points[:, 1], c=colors[i % len(colors)], label=f'Cluster {i + 1}')

    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title(title)
    plt.legend()
    plt.savefig(route)
    plt.show()


def plot_data(data, title, route):
    plt.figure(figsize=(6, 4))
    plt.scatter(data[:, 0], data[:, 1])
    plt.title(title)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.savefig(route)
    plt.show()


def calculate_total_distance(clusters, data):
    total_distance = 0
    for cluster in clusters:
        # Extract the points for this cluster based on the indices
        cluster_points = data[cluster]
        # Find the medoid - the point in the cluster with the smallest sum of distances to other points
        medoid_index = np.argmin(np.sum(distance.cdist(cluster_points, cluster_points), axis=1))
        medoid = cluster_points[medoid_index]
        # Calculate the sum of distances from all points in the cluster to the medoid
        total_distance += np.sum(np.linalg.norm(cluster_points - medoid, axis=1))
    return total_distance



if __name__ == "__main__":

    # Execute with Iris
    k_iris = 3  # Number of clusters
    iris_df = pd.read_csv('data/iris_data.txt', sep=' ', header=None)
    iris_data = iris_df.to_numpy()
    plot_data(iris_data, "Iris Data","images/iris.png")
    start_time = time.time()
    iris_clusters = find_clusters_with_mst_networkx(iris_data, k_iris)
    end_time = time.time() - start_time
    print(f"Iris clustering execution time: {end_time:.6f} seconds")
    plot_clusters(iris_data[:, :2], iris_clusters, "Iris Clusters", "images/iris_cl_mst.png")

    # Execute with moon
    k_moon = 2  # Number of clusters
    moon_df = pd.read_csv('data/moon_data.txt', sep=' ', header=None)
    moon_data = moon_df.to_numpy()
    plot_data(moon_data, "Moon Data","images/moon.png")
    start_time = time.time()
    moon_clusters = find_clusters_with_mst_networkx(moon_data, k_moon)
    end_time = time.time() - start_time
    print(f"Moon clustering execution time: {end_time:.6f} seconds")
    plot_clusters(moon_data[:, :2], moon_clusters, "Moon Clusters", "images/moon_cl_mst.png")


    # Execute with blob
    k_blob = 3  # Number of clusters
    blob_df = pd.read_csv('data/blob_data.txt', sep=' ', header=None)
    blob_data = blob_df.to_numpy()
    plot_data(blob_data, "Blob Data","images/blob.png")
    start_time = time.time()
    blob_clusters = find_clusters_with_mst_networkx(blob_data, k_blob)
    end_time = time.time() - start_time
    print(f"Blob clustering execution time: {end_time:.6f} seconds")
    plot_clusters(blob_data[:, :2], blob_clusters, "Blob Clusters", "images/blob_cl_mst.png")

     # For Iris data
    iris_total_distance = calculate_total_distance(iris_clusters, iris_data)
    print(f"Total distance for Iris data: {iris_total_distance}")

    # For Moon data
    moon_total_distance = calculate_total_distance(moon_clusters, moon_data)
    print(f"Total distance for Moon data: {moon_total_distance}")

    # For Blob data
    blob_total_distance = calculate_total_distance(blob_clusters, blob_data)
    print(f"Total distance for Blob data: {blob_total_distance}")

