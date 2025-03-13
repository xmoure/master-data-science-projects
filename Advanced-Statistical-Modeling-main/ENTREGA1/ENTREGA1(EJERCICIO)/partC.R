# Observed data
x <- c(3, 2, 0, 8, 2, 4, 6, 1)

# Calculate the parameters of the posterior Gamma distributions
a_post_bru <- 0.01 + sum(x)
b_post_bru <- 0.001 + length(x)
a_post_claudia <- 6.25 + sum(x)
b_post_claudia <- 2.5 + length(x)

# Calculate the pdf of the posterior Gamma distributions
pdf_post_bru <- dgamma(mu, shape = a_post_bru, rate = b_post_bru)
pdf_post_claudia <- dgamma(mu, shape = a_post_claudia, rate = b_post_claudia)

# The posterior for Carles is proportional to the likelihood
# Normalize to obtain a proper distribution
pdf_post_carles <- likelihood_values / sum(likelihood_values)

# Create dataframe
data_post <- data.frame(
  mu = mu,
  pdf_post_bru = pdf_post_bru,
  pdf_post_claudia = pdf_post_claudia,
  pdf_post_carles = pdf_post_carles
)

# Plot the three posterior distributions
ggplot(data_post, aes(x = mu)) +
  geom_line(aes(y = pdf_post_bru, color = "Bru's Posterior")) +
  geom_line(aes(y = pdf_post_claudia, color = "Clàudia's Posterior")) +
  geom_line(aes(y = pdf_post_carles, color = "Carles' Posterior")) +
  labs(y = "Density", title = "Posterior Distributions") +
  theme_minimal() +
  scale_color_manual(values = c("red", "blue", "green"))


# Function to calculate the 90% credible interval
credible_interval <- function(alpha, beta) {
  lower <- qgamma(0.05, shape = alpha, rate = beta)
  upper <- qgamma(0.95, shape = alpha, rate = beta)
  return(c(lower, upper))
}

# Calculate the 90% credible interval for each posterior
ci_bru <- credible_interval(a_post_bru, b_post_bru)
ci_claudia <- credible_interval(a_post_claudia, b_post_claudia)
ci_carles <- quantile(mu, probs = c(0.05, 0.95), type = 7)

print(ci_bru)
print(ci_claudia)
print(ci_carles)