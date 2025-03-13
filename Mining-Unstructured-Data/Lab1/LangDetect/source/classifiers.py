from sklearn.naive_bayes import MultinomialNB
from utils import toNumpyArray
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# You may add more classifier methods replicating this function
def applyNaiveBayes(X_train, y_train, X_test):
    trainArray = toNumpyArray(X_train)
    testArray = toNumpyArray(X_test)
    
    clf = MultinomialNB()
    clf.fit(trainArray, y_train)
    y_predict = clf.predict(testArray)
    return y_predict

def apply_linear_svc(X_train, y_train, X_test):
    print("----------------")
    print("Linear support vector classifier")
    print("----------------")
    train_array = toNumpyArray(X_train)
    test_array = toNumpyArray(X_test)
    clf = LinearSVC()
    clf.fit(train_array, y_train)
    y_predict = clf.predict(test_array)
    return y_predict

def apply_multiple_layer_perceptron(X_train, y_train, X_test):
    print("----------------")
    print("Multiple layer perceptron classifier")
    print("----------------")
    train_array = toNumpyArray(X_train)
    test_array = toNumpyArray(X_test)
    clf = MLPClassifier()
    clf.fit(train_array, y_train)
    y_predict = clf.predict(test_array)
    return y_predict

def apply_k_neighbours(X_train, y_train, X_test):
    print("----------------")
    print("K-neighbours classifier")
    print("----------------")
    train_array = toNumpyArray(X_train)
    test_array = toNumpyArray(X_test)
    clf = KNeighborsClassifier()
    clf.fit(train_array, y_train)
    y_predict = clf.predict(test_array)
    return y_predict

def apply_decision_tree(X_train, y_train, X_test):
    print("----------------")
    print("Decision tree classifier")
    print("----------------")
    train_array = toNumpyArray(X_train)
    test_array = toNumpyArray(X_test)
    clf = DecisionTreeClassifier()
    clf.fit(train_array, y_train)
    y_predict = clf.predict(test_array)
    return y_predict


def apply_random_forest(X_train, y_train, X_test):
    print("----------------")
    print("Random forest classifier")
    print("----------------")
    train_array = toNumpyArray(X_train)
    test_array = toNumpyArray(X_test)
    clf = RandomForestClassifier()
    clf.fit(train_array, y_train)
    y_predict = clf.predict(test_array)
    return y_predict
