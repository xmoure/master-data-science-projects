# Load necessary library
library(ggplot2)

# Define the data and the number of data points
y <- c(3, 2, 0, 8, 2, 4, 6, 1)
n <- length(y)

# Define the prior parameters
prior1 <- c(alpha =  0.01, beta = 0.001)
prior2 <- c(alpha =  6.25, beta = 2.5)
prior3 <- c(alpha =  1, beta = 0)  # Note: This flat prior is improper and won't work with dgamma

# Calculate the posterior parameters for Bru and Claudia
posterior1 <- c(a = prior1[1] + sum(y), b = prior1[2] + n)
posterior2 <- c(a = prior2[1] + sum(y), b = prior2[2] + n)

# Define the standardized likelihood function
sd.like <- function(th) {
  (th^sum(y)*exp(-n*th))/integrate(function(th)(th^sum(y)*exp(-n*th)), lower = 0, upper = 10)$value
}

# For Carles, calculate the unnormalized posterior
# This function defines the unnormalized posterior distribution for 
# Carles based on the likelihood of a Poisson distribution.
carles_posterior_unnormalized <- function(th) {
  th^sum(y) * exp(-n*th)
}

# Normalize Carles' posterior
normalization_constant_carles <- integrate(carles_posterior_unnormalized, lower = 0, upper = 10)$value
carles_posterior <- function(th) {
  carles_posterior_unnormalized(th) / normalization_constant_carles
}

# Define a sequence of x values for plotting
x_vals <- seq(0, 10, 0.1)

# Evaluate the posterior distributions and the standardized likelihood at the x values
bru_posterior_vals <- dgamma(x_vals, shape = posterior1[1], rate = posterior1[2])
claudia_posterior_vals <- dgamma(x_vals, shape = posterior2[1], rate = posterior2[2])
carles_posterior_vals <- sapply(x_vals, carles_posterior)
sd_like_vals <- sapply(x_vals, sd.like)

# Create a data frame for plotting
plot_data <- data.frame(
  x_vals,
  bru_posterior_vals,
  claudia_posterior_vals,
  carles_posterior_vals,
  sd_like_vals
)

# Plot the posterior distributions and the standardized likelihood
ggplot(plot_data, aes(x = x_vals)) +
  geom_line(aes(y = bru_posterior_vals, color = 'Bru')) +
  geom_line(aes(y = claudia_posterior_vals, color = 'Claudia')) +
  geom_line(aes(y = carles_posterior_vals, color = 'Carles')) +
  geom_line(aes(y = sd_like_vals, color = 'Standardized Likelihood'), linetype = "dashed") +
  scale_color_manual(
    values = c('Bru' = 'blue', 'Claudia' = 'red', 'Carles' = 'green', 'Standardized Likelihood' = 'orange'),
    breaks = c('Bru', 'Claudia', 'Carles', 'Standardized Likelihood')
  ) +
  labs(title = "Posterior Distributions and Standardized Likelihood", x = expression(lambda), y = "Density") +
  theme_minimal()

