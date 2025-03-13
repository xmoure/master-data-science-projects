from sklearn.datasets import make_swiss_roll
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np


def generate_data(test_size, n_samples, noise, random_state):

    X, t = make_swiss_roll(n_samples=n_samples, noise=noise, random_state=random_state)

    # threshold based on the mean of t
    threshold = np.mean(t)
    y = np.where(t < threshold, -1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = generate_data(test_size=0.5, n_samples=1000, noise=0.2, random_state=42)

num_train_points = X_train.shape[0]
num_test_points = X_test.shape[0]

print(f"Number of points in the training data: {num_train_points}")
print(f"Number of points in the test data: {num_test_points}")


#Save training data
np.savetxt('train_data.txt', np.hstack((X_train, y_train.reshape(-1, 1))), fmt='%0.8f')

# Save testing data
np.savetxt('test_data.txt', np.hstack((X_test, y_test.reshape(-1, 1))), fmt='%0.8f')


clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma=10))
clf.fit(X_train, y_train)

# Evaluate the classifier on the test data
accuracy = clf.score(X_test, y_test)
print(f"Test set accuracy: {accuracy:.2f}")

