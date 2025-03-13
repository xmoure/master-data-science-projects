import pandas as pd
import matplotlib.pyplot as plt

# Function to load blob data from a text file
def load_blob_data(file_path):
    return pd.read_csv(file_path, sep=' ', header=None)

# Function to read cluster assignments from a text file
def read_cluster_assignments(file_path):
    with open(file_path, 'r') as file:
        clusters = [line.split().index('1') + 1 for line in file]
    return clusters

# Load the blob data
sampled_iris_data = load_blob_data('../data/iris_data.txt')

# Read the cluster assignments
cluster_assignments = read_cluster_assignments('../output/output_iris.txt')

# Remap the cluster assignments
unique_clusters = sorted(set(cluster_assignments))
cluster_mapping = {k: v for v, k in enumerate(unique_clusters)}
mapped_clusters = [cluster_mapping[cluster] for cluster in cluster_assignments]

sampled_iris_data['Cluster'] = mapped_clusters

plt.figure(figsize=(10, 6))

# Define colors for each cluster
colors = ['red', 'green', 'blue']

# Plot each cluster with a different color and label
for i, color in enumerate(colors):
    plt.scatter(sampled_iris_data[sampled_iris_data['Cluster'] == i].iloc[:, 0],
                sampled_iris_data[sampled_iris_data['Cluster'] == i].iloc[:, 1],
                c=color, label=f'Cluster {i+1}', marker='o')

plt.title('Iris Data Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
# Save the figure
plt.savefig('../output/iris_clusters.png', format='png', dpi=300)

plt.show()
