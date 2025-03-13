from sklearn.preprocessing import StandardScaler
from sklearn import datasets
import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt



np.random.seed(42)  # For reproducibility


def genIris():
    iris = datasets.load_iris()
    iris_data = iris.data

    # Select a sample of 25 rows
    sample_indices = np.random.choice(iris_data.shape[0], 25, replace=False)
    iris_sample = iris_data[sample_indices]
    iris_sample_normalized = (iris_sample - np.mean(iris_sample, axis=0)) / np.std(iris_sample, axis=0)
    iris_sample_df = pd.DataFrame(iris_sample_normalized)
    iris_sample_df.to_csv('data/iris_data.txt', sep=' ', header=False, index=False)

     # Save to iris.dat
    with open('data/iris.dat', 'w') as dat_file:
        # Write the parameters for m and n
        dat_file.write(f'param m := {len(iris_sample_normalized)};\n')
        dat_file.write(f'param n := {iris_sample_normalized.shape[1]};\n\n')

        # Write the data for matrix A
        dat_file.write('param A :')
        for j in range(1, iris_sample_normalized.shape[1] + 1):
            dat_file.write(f' {j}')
        dat_file.write(' :=\n')

        for i, sample in enumerate(iris_sample_normalized, start=1):
            dat_file.write(f'{i}')
            for feature in sample:
                dat_file.write(f' {feature}')
            dat_file.write('\n')
        dat_file.write(';\n')


def save_moon_dat(moon_data):
    # Save to moon.dat
    with open('data/moon.dat', 'w') as dat_file:
        # Write the parameters for m (number of points) and n (number of features)
        m, n = moon_data.shape
        dat_file.write(f'param m := {m};\n')
        dat_file.write(f'param n := {n};\n\n')

        # Write the data for matrix A
        dat_file.write('param A :')
        for j in range(1, n + 1):
            dat_file.write(f' {j}')
        dat_file.write(' :=\n')

        for i, sample in enumerate(moon_data, start=1):
            dat_file.write(f'{i}')
            for feature in sample:
                dat_file.write(f' {feature}')
            dat_file.write('\n')
        dat_file.write(';\n')

def genMoons():
    # Generate moon dataset with 25 samples
    moon_data, _ = datasets.make_moons(n_samples=25, noise=0.05, random_state=42)
    moon_data_normalized = (moon_data - np.mean(moon_data, axis=0)) / np.std(moon_data, axis=0)
    moon_data_df = pd.DataFrame(moon_data_normalized)
    moon_data_df.to_csv('data/moon_data.txt', sep=' ', header=False, index=False)

    # Save the data to a .dat file for AMPL
    save_moon_dat(moon_data_normalized)


def genBlobs():
    # Generate sample data using make_blobs
    n_samples = 500  # Number of data points
    n_features = 2   # Number of features
    centers = 3      # Number of centers or clusters

    X, _ = make_blobs(n_samples=n_samples, n_features=n_features, centers=centers, cluster_std=2 , random_state=42)

    # Normalize the data
    X_normalized = StandardScaler().fit_transform(X)

     # Plot the generated blobs
    plt.scatter(X_normalized[:, 0], X_normalized[:, 1], s=50)
    plt.title('Generated Blobs')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.show()

    # Save to blob_data.txt
    pd.DataFrame(X_normalized).to_csv('data/blob_data.txt', sep=' ', header=False, index=False)

    # Save to blob.dat
    with open('data/blob.dat', 'w') as dat_file:
        m, n = X_normalized.shape
        dat_file.write(f'param m := {m};\n')
        dat_file.write(f'param n := {n};\n\n')
        dat_file.write('param A :')
        for j in range(1, n + 1):
            dat_file.write(f' {j}')
        dat_file.write(' :=\n')
        for i, sample in enumerate(X_normalized, start=1):
            dat_file.write(f'{i}')
            for feature in sample:
                dat_file.write(f' {feature}')
            dat_file.write('\n')
        dat_file.write(';\n')




if __name__ == "__main__":
    genIris()
    genMoons()
    genBlobs()
