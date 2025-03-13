# Load necessary libraries
library(ggplot2)
library(MASS)  # for truehist

# Given data
y <- c(3, 2, 0, 8, 2, 4, 6, 1)
n <- length(y)

# Posterior parameters calculated previously
posterior1 <- c(a = 0.01 + sum(y), b = 0.001 + n)
posterior2 <- c(a = 6.25 + sum(y), b = 2.5 + n)

# Posterior Predictive for Bru and Claudia using Negative Binomial Distribution
# size parameter for Negative Binomial is the shape parameter of the Gamma posterior
# mu parameter for Negative Binomial is the mean of the Gamma posterior, which is shape/rate

# Bru
size_bru <- posterior1[1]
mu_bru <- posterior1[1] / posterior1[2]
prob_bru <- size_bru / (size_bru + mu_bru)
CI_bru <- qnbinom(c(0.05, 0.95), size = size_bru, mu = mu_bru)

# Claudia
size_claudia <- posterior2[1]
mu_claudia <- posterior2[1] / posterior2[2]
prob_claudia <- size_claudia / (size_claudia + mu_claudia)
CI_claudia <- qnbinom(c(0.05, 0.95), size = size_claudia, mu = mu_claudia)

# Simulation for Carles' Predictive Posterior
set.seed(123)  # for reproducibility
n_sims <- 10000
lambda_samples_carles <- rgamma(n_sims, shape = sum(y) + 1, rate = n)  # Assuming a flat prior leads to a shape parameter of sum(y)+1 and a rate of n
y_new_samples_carles <- rpois(n_sims, lambda = lambda_samples_carles)
CI_carles <- quantile(y_new_samples_carles, probs = c(0.05, 0.95))

# Output the 90% credible intervals
list(Bru = CI_bru, Claudia = CI_claudia, Carles = CI_carles)

