

# setting working directory

setwd("  ")


# instaling the library R2jags

#install.packages('R2jags')
library(R2jags)


x <- c(1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5)
y <- c(25, 31, 27, 28, 36, 35, NA, 34)

# Removing NA
not_na <- !is.na(y)
x <- x[not_na]
y <- y[not_na]
data_list <- list(x=x, y=y, n=length(y))

plot(x, y, pch=19, xlab="Fertilizer level", ylab="Yield")

n <- length(y)

par(mfrow=c(1,1))



#####  Bayesian Model  #####

regression <- "
model {
 for (i in 1:n) {
   y[i]~ dnorm(b0+b1*x[i], tau)
 }
 b0 ~ dnorm(0, 1.0E-7)
 b1 ~ dnorm(0, 1.0E-7)
 sigma ~ dunif(0, 100000)
 tau <- pow(sigma, -2)
}
"

### discarded "Burn", save "Iter", chains "Chain"

Iter <- 10000
Burn <- 1000
Chain <- 2
Thin <- 1

data <- list(y=y, x=x, n=n)

parameters <- c("b0", "b1", "sigma")

potatoes.model  <-jags(data, inits=NULL, parameters.to.save=parameters,
                    model=textConnection(regression),
                    n.iter=(Iter*Thin+Burn), n.burnin=Burn, n.thin=Thin, n.chains=Chain)

traceplot(potatoes.model, mfrow = c(length(parameters),1), varname = parameters)

print(potatoes.model)

attach.jags(potatoes.model)
b0 <- b0
b1 <- b1
sigma <- sigma
detach.jags()



par(mfrow=c(2,2))

plot(density(b0, adjust = 1.5), main = expression(paste(pi,"(",beta[0],"|y)")), xlab= "" )
plot(density(b1, adjust = 1.5), main = expression(paste(pi,"(",beta[1],"|y)")), xlab= ""  )
plot(density(sigma, adjust = 1.5), main = expression(paste(pi,"(",sigma,"|y)")), xlab= "" )


# Calculate the 95% credible intervals for b0, b1, and sigma
CI_b0 <- quantile(b0, c(0.025, 0.975))
CI_b1 <- quantile(b1, c(0.025, 0.975))
CI_sigma <- quantile(sigma, c(0.025, 0.975))

# Print the 95% credible intervals
print(CI_b0)
print(CI_b1)
print(CI_sigma)

# prediction

M <- length(b0)
y.x4 <- rnorm(M, b0+b1*4, sigma)

par(mfrow=c(2,1))
plot(density(y.x4))


quantile(y.x4, c(0.025,0.975))

summary(y.x4)