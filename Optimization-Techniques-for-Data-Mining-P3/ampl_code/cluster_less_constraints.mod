# Number of data points
param m;
# Number of features per data point
param n;

# Parameter to store the data points
param A {1..m, 1..n};

# Distance matrix
param D {i in 1..m, j in 1..m} :=
  sqrt(sum {l in 1..n} (A[i,l] - A[j,l])^2);

# Binary variables indicating if point i belongs to cluster j
var x {1..m, 1..m} binary;

# Objective: Minimize the sum of distances from points to their cluster medians
#minimize TotalDistance: sum {i in 1..m, j in 1..m} (D[i,j] * x[i,j]);
minimize TotalDistance: sum{i in 1..m}(sum{j in 1..m} D[i,j]*x[i,j]);

# Each data point must belong to one and only one cluster
subject to AssignmentConstraint {i in 1..m}:
  sum {j in 1..m} x[i,j] = 1;

# Exactly k clusters must be chosen
subject to ClusterConstraint:
  sum {j in 1..m} x[j,j] = k;

#Formulation with less constraints
subject to c3 {j in 1..m}:
	m*x[j,j] >= sum{i in 1..m} x[i,j];