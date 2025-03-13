param m_train;
param m_test;
param n; 

param nu;

param y_train {1..m_train};
param A_train {1..m_train, 1..n};

param y_test {1..m_test};
param A_test {1..m_test, 1..n}; 

var lambda {1..m_train} >=0 ,  <=nu;  # lagrange multipliers

maximize svm_dual:
	sum{i in 1..m_train} lambda[i]
	-1/2*sum{i in 1..m_train, j in 1..m_train}lambda[i]*y_train[i]*lambda[j]*y_train[j]*(sum{k in 1..n}A_train[i,k]*A_train[j,k]);

subject to dual_constraint:
	sum{i in 1..m_train}lambda[i]*y_train[i] =0;
