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