library(ggplot2)

x_vals <- seq(0, 20, 0.1)

bru_prior <- dgamma(x_vals, shape = 0.01, rate = 0.001)
claudia_prior <- dgamma(x_vals, shape = 6.25, rate = 2.5)

ggplot(data.frame(x_vals, bru_prior, claudia_prior), aes(x=x_vals)) +
  geom_line(aes(y=bru_prior, color='Bru: Gamma(0.01, 0.001)')) +
  geom_line(aes(y=claudia_prior, color='Claudia: Gamma(6.25, 2.5)')) +
  geom_hline(yintercept = 1, color='blue', linetype='dotted') + # Carles: Flat
  labs(title="Prior Distributions", x="μ", y="Density") +
  theme_minimal()


data <- c(3, 2, 0, 8, 2, 4, 6, 1)

likelihood <- function(mu) {
  prod(dpois(data, mu))
}

likelihood_vals <- sapply(x_vals, likelihood)

# Integrate the likelihood to get the normalization factor
integrated_likelihood <- function(mu) {
  prod(dpois(data, mu))
}


# Calculate the area using the trapezoidal rule
trapezoidal_rule <- function(y_values, x_values) {
  n <- length(y_values)
  area <- sum(0.5 * (y_values[-1] + y_values[-n]) * diff(x_values))
  return(area)
}

total_area <- trapezoidal_rule(likelihood_vals, x_vals)

normalized_likelihood_vals <- likelihood_vals / total_area


ggplot(data.frame(x_vals, normalized_likelihood_vals), aes(x=x_vals, y=normalized_likelihood_vals)) +
  geom_line(color='black') +
  labs(title="Normalized Likelihood Function", x="μ", y="Likelihood") +
  theme_minimal()


sum_data <- sum(data)
n <- length(data)

bru_alpha_post <- 0.01 + sum_data
bru_beta_post <- 0.001 + n
bru_posterior <- dgamma(x_vals, shape=bru_alpha_post, rate=bru_beta_post)

claudia_alpha_post <- 6.25 + sum_data
claudia_beta_post <- 2.5 + n
claudia_posterior <- dgamma(x_vals, shape=claudia_alpha_post, rate=claudia_beta_post)

ggplot(data.frame(x_vals, bru_posterior, claudia_posterior, normalized_likelihood_vals), aes(x=x_vals)) +
  geom_line(aes(y=bru_posterior, color='Bru')) +
  geom_line(aes(y=claudia_posterior, color='Claudia')) +
  geom_line(aes(y=normalized_likelihood_vals, color='Carles (Likelihood)')) +
  labs(title="Posterior Distributions", x="μ", y="Density") +
  theme_minimal()


# bru_ci <- qgamma(c(0.05, 0.95), shape=bru_alpha_post, rate=bru_beta_post)
# claudia_ci <- qgamma(c(0.05, 0.95), shape=claudia_alpha_post, rate=claudia_beta_post)
# 
# print(bru_ci)
# print(claudia_ci)

# d) Calculate a 90% credible interval of the number of accidents for next weekend
# for each of the three Bayesian models

# Define the range of possible number of accidents
x_accidents <- 0:20


# Clàudia
size_claudia <- claudia_alpha_post
prob_claudia <- 1 / (1 + claudia_beta_post)
pred_claudia <- dnbinom(x_accidents, size=size_claudia, prob=prob_claudia)
CI_claudia <- qnbinom(p=c(0.05, 0.95), size=size_claudia, prob=prob_claudia)

# Plotting posterior predictive distributions
plot(x_accidents, pred_bru, type="h", col="blue", lwd=2, xlab="x", ylab="Probability",
     main="Posterior Predictive Distributions")
lines(x_accidents, pred_claudia, type="h", col="red", lwd=2)
legend("topright", legend=c("Bru", "Clàudia"), col=c("blue", "red"), lwd=2)


# Bru
size_bru <- bru_alpha_post
prob_bru <- size_bru / (size_bru + bru_beta_post)
pred_bru <- dnbinom(x_accidents, size=size_bru, prob=prob_bru)
CI_bru <- qnbinom(p=c(0.05, 0.95), size=size_bru, prob=prob_bru)

# Print the 90% credible interval for the number of accidents next weekend
print(CI_bru)


# Printing 90% credible intervals
print(CI_bru)
print(CI_claudia)

# For Carles, the posterior predictive distribution might need to be computed numerically.
