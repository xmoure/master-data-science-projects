# Observed data
x <- c(3, 2, 0, 8, 2, 4, 6, 1)
mu <- seq(0, 10, 0.01)
# Calculate the likelihood
likelihood <- function(mu) {
  prod(dpois(x, lambda = mu))
}

# Evaluate the likelihood function over the range of mu values
likelihood_values <- sapply(mu, likelihood)

# Normalize the likelihood function
likelihood_values <- likelihood_values / sum(likelihood_values)

# Plot the likelihood function
plot(mu, likelihood_values, type = "l", col = "blue", lwd = 2,
     ylab = "Likelihood", xlab = expression(mu), main = "Likelihood Function")
