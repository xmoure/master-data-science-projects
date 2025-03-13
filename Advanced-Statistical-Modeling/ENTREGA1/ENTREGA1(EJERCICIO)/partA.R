library(ggplot2)

# Define the parameters for the Gamma distributions

prior_bru <- c(alpha = 0.01 , beta = 0.001)
prior_claudia <- c(alpha = 6.25 , beta = 2.5)

# Create a sequence of mu values instead of simulating values
mu <- seq(0, 10, 0.01)

# Calculate the pdf (probability density functions) of the Gamma distributions at 
# each value of mu
pdf_bru <- dgamma(mu, shape = prior_bru[1], rate = prior_bru[2])
pdf_claudia <- dgamma(mu, shape = prior_claudia[1], rate = prior_claudia[2])

# Create a dataframe for plotting
data <- data.frame(
  mu = mu,
  pdf_bru = pdf_bru,
  pdf_claudia = pdf_claudia,
  flat_prior = rep(1, length(mu))
)

# Plot the three prior distributions
ggplot(data, aes(x = mu)) +
  geom_line(aes(y = pdf_bru, color = "Bru's Prior")) +
  geom_line(aes(y = pdf_claudia, color = "Clàudia's Prior")) +
  geom_line(aes(y = flat_prior, color = "Carles' Prior")) +
  labs(x =  expression(lambda),y = "Density", title = "Prior Distributions") +
  theme_minimal() +
  scale_color_manual(values = c("red", "blue", "green"))
