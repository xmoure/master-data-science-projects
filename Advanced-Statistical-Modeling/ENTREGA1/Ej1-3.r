
####################  1.3 Garriga   ##############################

#####	prior distribution and prior predictive distribution
#no clear upper limit, use Poisson

prior1 <- c(alpha =  0.01, beta =0.001)
prior2 <- c(alpha =  6.25, beta =2.25)
prior3 <- c(alpha =  1, beta =0)

plot(function(x)dgamma(x, prior1[1], prior1[2]), xlim=c(0,10),ylim=c(0,1), ylab="", xlab = expression(lambda), col='blue') # Lambda is number of happenings
plot(function(x)dgamma(x, prior2[1], prior2[2]), xlim=c(0,10), ylab="", add = T, col='red')
plot(function(x)dgamma(x, prior3[1], prior3[2]), xlim=c(0,10), ylab="", add = T, col='green')
title("prior distribution") #Translate info plot to observable space?
legend("topright", c("Bru", "Claudia", "Carles"), col=c("blue", "red", "green"), lty=c(1, 1, 1))

###### data

y <- c(3, 2, 0, 8, 2, 4, 6, 1) 
n <- length(y)
n
y

####### standardaized likelihood function  

sd.like <- function(th) {
 (th^sum(y)*exp(-n*th))/integrate(function(th)(th^sum(y)*exp(-n*th)), lower = 0, upper = 10)$value
} #Standarized Likelyhood


par(mfrow=c(1, 1))
plot(function(x)sd.like(x), xlim=c(0,10), ylab="", xlab = expression(lambda))
 plot(function(x)dgamma(x, prior2[1], prior2[2]), xlim=c(0,10), add=T, lty=2)
 legend("topright", c("prior", "likelihood"), lty = c(2,1))



#########  posterior distribution


posterior1 <- c(a = prior1[1] + sum(y), b = prior1[2] +  n)
posterior2 <- c(a = prior2[1] + sum(y), b = prior2[2] +  n)
posterior3 <- c(a = prior3[1] + sum(y), b = prior3[2] + n)

# prior, likelihood and posterior

plot(function(x)dgamma(x, posterior1[1], posterior1[2]), xlim=c(0,10),ylim=c(0,1), col='blue')
 plot(function(x)dgamma(x, posterior2[1], posterior2[2]), xlim=c(0,10),ylim=c(0,1), add=T, col='red')
 plot(function(x)sd.like(x), xlim=c(0,10), ylab="", xlab = expression(lambda), add=T, col='green')
 plot(function(x)dgamma(x, posterior3[1], posterior3[2]), xlim=c(0,10),ylim=c(0,1), add=T, col='green')
 legend("topright", c("Bru", "Claudia", "Carles"), col=c("blue", "red", "green"), lty=c(1, 1, 1))



#  Confidence
 ##set.seed(123)  # for reproducibility
 M <- 100000
 
 
 y <- c(3, 2, 0, 8, 2, 4, 6, 1) 
 n <- length(y)

 posterior1 <- c(a = 0.01 + sum(y), b = 0.001 + n)
 posterior2 <- c(a = 6.25 + sum(y), b = 2.5 + n)
 posterior3 <- c(a = 1 + sum(y), b = 0 + n)
 #1
 posterior1.sim <- rgamma(M, posterior1[1], posterior1[2])
 pre.posterior1.sim <- rpois(M,posterior1.sim)
 table(pre.posterior1.sim)
 
 interval1 <- quantile(pre.posterior1.sim, probs = c(0.05, 0.95))
 print(interval1)
 
 #2
 posterior2.sim <- rgamma(M, posterior2[1], posterior2[2])
 pre.posterior2.sim <- rpois(M,posterior2.sim)
 table(pre.posterior2.sim)
 
 interval2 <- quantile(pre.posterior2.sim, probs = c(0.05, 0.95))
 print(interval2)
 
 
 #3
 posterior3.sim <- rgamma(M, posterior3[1], posterior3[2])
 pre.posterior3.sim <- rpois(M,posterior3.sim)
 table(pre.posterior3.sim)
 
 interval3 <- quantile(pre.posterior3.sim, probs = c(0.05, 0.95))
 print(interval3)

 
 # Output the 90% credible intervals
 list(Bru = interval1, Claudia = interval2, Carles = interval3)
 
 
 