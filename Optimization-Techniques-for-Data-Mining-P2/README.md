# OTDM
## Lab assignment 2: Support vector machine

### 1. Implementation over generated dataset

#### 1.1. Generating the dataset

Two datasets were generated, one of 8000 rows for training, and one of 2000 rows for testing, and both using `seed = 1234`, and was done with the following commands:

```shell
./gensvmdat train_data.txt 8000 1234

./gensvmdat test_data.txt 2000 1234
```

Then it was necessary to delete the character `*` present in some lines of the dataset, which was done with the following commands:

```shell
sed -i 's/\*//' train_data.txt

sed -i 's/\*//' test_data.txt
```

#### 1.2 Primal

###### Implementation

The problem is defined as: 

![primal.png](images%2Fprimal.png)

So to do it in `AMPL` it was needed to implement the following files:

- [primal.mod](primal.mod): implements the primal as an optimization problem.

```AMPL
# Parameters

param m_train;
param m_test;
param n; 

param nu;

param y_train {1..m_train};
param A_train {1..m_train, 1..n};

param y_test {1..m_test};
param A_test {1..m_test, 1..n}; 


# Variables

var w {1..n}; 
var gamma;
var s {1..m_train}; 

# Problem

minimize primal:
    0.5 * sum{j in 1..n}(w[j]^2)
    + nu * sum{i in 1..m_train}(s[i]);

subject to primal_c1 {i in 1..m_train}:
    -y_train[i]*sum{j in 1..n}(A_train[i,j]*w[j] + gamma) -s[i] + 1 <= 0;

subject to primal_c2 {i in 1..m_train}:
    -s[i] <= 0;
```
- [dataset.dat](data%2Fdataset.dat): it reads the train and test files and loads them, also it sets the values for the parameters like `m` 
(number of rows), `n` (number of columns) and `nu` (tradeoff).

```AMPL
param m_train := 8000;
param m_test := 2000;
param n := 4;

param nu := 30;

read {i in 1..m_train}(
A_train[i,1], A_train[i,2], A_train[i,3], A_train[i,4], y_train[i]
) < data/train_data.txt;

read {i in 1..m_test}(
A_test[i,1], A_test[i,2], A_test[i,3], A_test[i,4], y_test[i]
) < data/test_data.txt;
```

- [primal.run](primal.run): is an script that executes the model over the generated dataset, it sets `cplex` as the solver
 and after solving it calculates the train and test accuracies using the calculated variables (`w` and `gamma`) .
```AMPL
reset;

option solver cplex;

model primal.mod

data ./data/dataset.dat;

solve;

display w, gamma;

print "Train accuracy";

param y_pred_tr {1..m_train};
let {i in {1..m_train}} y_pred_tr[i] :=
    if sum{j in {1..n}}(A_train[i,j]*w[j] + gamma) > 0 then 1 else -1;

param correct_tr = sum{i in {1..m_train}}(
    if y_pred_tr[i] = y_train[i] then 1 else 0
);

param accuracy_tr = correct_tr / m_train;

display accuracy_tr;

print "Test accuracy";

param y_pred_te {1..m_test};
let {i in {1..m_test}} y_pred_te[i] :=
    if sum{j in {1..n}}(A_test[i,j]*w[j] + gamma) > 0 then 1 else -1;

param correct_te = sum{i in {1..m_test}}(
    if y_pred_te[i] = y_test[i] then 1 else 0
);

param accuracy_te = correct_te / m_test;

display accuracy_te;
```

###### Results

To execute the code the following command was executed on `AMPL IDE`:

```AMPL
include primal.run;
```

And the output is the following:

```
CPLEX 22.1.1.0: optimal solution; objective 72426.20237
26 separable QP barrier iterations
No basis.
w [*] :=
1  5.1156
2  4.98397
3  5.04391
4  5.00287
;

gamma = -2.52409

Train accuracy
accuracy_tr = 0.94175

Test accuracy
accuracy_te = 0.933
```


### 2. Application to other datasets

#### 2.1 Iris dataset

##### 2.1.1 Implementation

The selected dataset to test the implemented code was the Iris dataset, that can be found on the following [link](https://archive.ics.uci.edu/dataset/53/iris0), 
or it can also be directly imported to `Python`, which it was done.

The dataset consists on a group of instances that describe a type of plant and
each entry has 4 numerical features:

- sepal length
- sepal width
- petal length
- petal width 


And its target variable, which has 3 levels are:
- Iris Setosa
- Iris Versicolour
- Iris Virginica

To convert this dataset into a suitable input por `AMPL` and into a suitable problem for our implemented code, the dataset 
had to be transformed into a binary problem and to do so, [dataGen.py](iris_data%2FdataGen.py) was implemented. The new decided
problem was to classify if the plant is `Iris Virginica` or not.

There first the dataset was imported, then the target variable values were converted into 1 and -1 (if it is `Iris Virginica` 
or not respectively). With that, the dataset was split into train and test (80-20) using stratify to get the target balanced on each split.
And finally these were exported into [train_iris.txt](iris_data%2Ftrain_iris.txt) 
and [test_iris.txt](iris_data%2Ftest_iris.txt).

To execute the `AMPL` implemented code with this dataset it was needed to create new `.dat` and `.run` files:

- [dataset.dat](iris_data%2Fdataset.dat): where the only changes where over the `m` sizes and the filenames where the data is imported,
this because this dataset `n` was the same as the generated one previously.
```AMPL
param m_train := 120;
param m_test := 30;
param n := 4;

param nu := 1;

read {i in 1..m_train}(
A_train[i,1], A_train[i,2], A_train[i,3], A_train[i,4], y_train[i]
) < iris_data/train_iris.txt;

read {i in 1..m_test}(
A_test[i,1], A_test[i,2], A_test[i,3], A_test[i,4], y_test[i]
) < iris_data/test_iris.txt;
```
- [primal_iris.run](primal_iris.run): the only change was the `data` command parameter, changing the `.dat` file.

```AMPL
reset;

option solver cplex;

model primal.mod

data ./iris_data/dataset.dat;

solve;

display w, gamma;

print "Train accuracy";

param y_pred_tr {1..m_train};
let {i in {1..m_train}} y_pred_tr[i] :=
    if sum{j in {1..n}}(A_train[i,j]*w[j] + gamma) > 0 then 1 else -1;

param correct_tr = sum{i in {1..m_train}}(
    if y_pred_tr[i] = y_train[i] then 1 else 0
);

param accuracy_tr = correct_tr / m_train;

display accuracy_tr;

print "Test accuracy";

param y_pred_te {1..m_test};
let {i in {1..m_test}} y_pred_te[i] :=
    if sum{j in {1..n}}(A_test[i,j]*w[j] + gamma) > 0 then 1 else -1;

param correct_te = sum{i in {1..m_test}}(
    if y_pred_te[i] = y_test[i] then 1 else 0
);

param accuracy_te = correct_te / m_test;

display accuracy_te;
```

##### 2.1.2 Results

###### Primal:

To execute the code the following command was executed on `AMPL IDE`:

```AMPL
include primal_iris.run;
```

And the output is the following:

```
CPLEX 22.1.1.0: optimal solution; objective 13.51679642
15 separable QP barrier iterations
No basis.
w [*] :=
1  -0.687044
2  -0.937784
3 2.12455
4 1.56317
;
gamma = -1.51585
Train accuracy
accuracy_tr = 0.983333
Test accuracy
accuracy_te = 1
```
