from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
import pandas as pd

iris = fetch_ucirepo(id=53)

X = iris.data.features
y = iris.data.targets

class_counts = y.value_counts()

y_binary = (y == 'Iris-virginica').astype(float) * 2 - 1
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=42, stratify=y_binary)

train_data = pd.concat([X_train, y_train], axis=1)
train_data.to_csv('train_iris.txt', sep=' ', header=False, index=False)

# Export test data to test_iris.txt
test_data = pd.concat([X_test, y_test], axis=1)
test_data.to_csv('test_iris.txt', sep=' ', header=False, index=False)

