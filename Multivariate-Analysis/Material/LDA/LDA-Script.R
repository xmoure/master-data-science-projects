# install.packages("MASS")
library(MASS)
# https://little-book-of-r-for-multivariate-analysis.readthedocs.io/en/latest/src/multivariateanalysis.html
wine<-read.table("wine.csv", sep=",")
names(wine)
# names(wine)<-c("cultivarId", "alcohol", "MalicAcid", "Ash", "AlcalinityAsh",
#                "Magnesium", "totalPhenols", "Flavanoids","NonflavanoidsPhenols","Proanthocyanins",
#                "ColorIntensity","Hue","RatioDilutedWines","Proline")

## there is a logical error: there is no train and test data. We need to do it

wine.lda <- lda(wine$V1 ~ wine$V2 + wine$V3 + wine$V4 + wine$V5 + wine$V6 + wine$V7 + wine$V8 + wine$V9 + wine$V10 + wine$V11 + wine$V12 + wine$V13 + wine$V14)
#or
wine2.lda<-lda(win2$V1~ ., data=wine)
wine.lda

#coefficients of the LDA
wine.lda$scaling[,2]
wine.lda$scaling[,1]
wine.lda$scaling[,1:2]

#we pass the test data in wine[2:14] in this case is all the database without the target
wine.lda.values <- predict(wine.lda, wine[2:14])

wine[,15]<- wine.lda.values$x[,2]
wine.lda.values$x[,2]
wine[,16]<- wine.lda.values$x[,1]
wine.lda.values$x[,1]
names(wine)[15]<-"LDA2"
names(wine)[16]<-"LDA1"

wine.lda.values
## porbabilities about the memberships of the quality
## for wine number 1 this one was classify almost by 100%



calcWithinGroupsVariance <- function(variable,groupvariable)
{
  # find out how many values the group variable can take
  groupvariable2 <- as.factor(groupvariable[[1]])
  levels <- levels(groupvariable2)
  numlevels <- length(levels)
  # get the mean and standard deviation for each group:
  numtotal <- 0
  denomtotal <- 0
  for (i in 1:numlevels)
  {
    leveli <- levels[i]
    levelidata <- variable[groupvariable==leveli,]
    levelilength <- length(levelidata)
    # get the standard deviation for group i:
    sdi <- sd(levelidata)
    numi <- (levelilength - 1)*(sdi * sdi)
    denomi <- levelilength
    numtotal <- numtotal + numi
    denomtotal <- denomtotal + denomi
  }
  # calculate the within-groups variance
  Vw <- numtotal / (denomtotal - numlevels)
  return(Vw)
}


groupStandardise <- function(variables, groupvariable)
{
  # find out how many variables we have
  variables <- as.data.frame(variables)
  numvariables <- length(variables)
  # find the variable names
  variablenames <- colnames(variables)
  # calculate the group-standardised version of each variable
  for (i in 1:numvariables)
  {
    variablei <- variables[i]
    variablei_name <- variablenames[i]
    variablei_Vw <- calcWithinGroupsVariance(variablei, groupvariable)
    variablei_mean <- mean(as.matrix(variablei))  
    variablei_new <- (variablei - variablei_mean)/(sqrt(variablei_Vw))
    data_length <- nrow(variablei)
    if (i == 1) { variables_new <- data.frame(row.names=seq(1,data_length)) }
    variables_new[`variablei_name`] <- variablei_new
  }
  return(variables_new)
}


#if features are normalized, then results are more understandable
groupstandardisedconcentrations <- groupStandardise(wine[2:14], wine[1])

calcBetweenGroupsVariance <- function(variable,groupvariable)
{
  # find out how many values the group variable can take
  groupvariable2 <- as.factor(groupvariable[[1]])
  levels <- levels(groupvariable2)
  numlevels <- length(levels)
  # calculate the overall grand mean:
  grandmean <- mean(as.matrix(variable) )         
  # get the mean and standard deviation for each group:
  numtotal <- 0
  denomtotal <- 0
  for (i in 1:numlevels)
  {
    leveli <- levels[i]
    levelidata <- variable[groupvariable==leveli,]
    levelilength <- length(levelidata)
    # get the mean and standard deviation for group i:
    meani <- mean( as.matrix(levelidata) )
    sdi <- sd(levelidata)
    numi <- levelilength * ((meani - grandmean)^2)
    denomi <- levelilength
    numtotal <- numtotal + numi
    denomtotal <- denomtotal + denomi
  }
  # calculate the between-groups variance
  Vb <- numtotal / (numlevels - 1)
  Vb <- Vb[[1]]
  return(Vb)
}



calcSeparations <- function(variables,groupvariable)
{
  # find out how many variables we have
  variables <- as.data.frame(variables)
  numvariables <- length(variables)
  # find the variable names
  variablenames <- colnames(variables)
  # calculate the separation for each variable
  for (i in 1:numvariables)
  {
    variablei <- variables[i]
    variablename <- variablenames[i]
    Vw <- calcWithinGroupsVariance(variablei, groupvariable)
    Vb <- calcBetweenGroupsVariance(variablei, groupvariable)
    sep <- Vb/Vw
    print(paste("variable",variablename,"Vw=",Vw,"Vb=",Vb,"separation=",sep))
  }
}

# Separation between the LDA axis (ratio of within & between distance)
calcSeparations(wine.lda.values$x,wine[1])

#total separation (sum of both)

help("predict.lda")

hist(wine.lda.values$x[,2])
hist(wine.lda.values$x[,1])
# multiple histogram between the Discriminant function and the output feature
par("mar")
par(mar=c(1,1,1,1))
par(mar=c(5.1,4.1,4.1,2.1))
par(mar=c(3,2.5,1.5,1))


ldahist(data = wine.lda.values$x[,1], g=wine$V1, ymax=1)


ldahist(data = wine.lda.values$x[,2], g=wine$V1)

#plot  of LDA axis and observations 
plot(wine.lda.values$x[,1],wine.lda.values$x[,2]) # make a scatterplot

plot(wine[,16],wine[,15])
text(wine.lda.values$x[,1],wine.lda.values$x[,2],wine$V1,cex=0.7,pos=4,col=wine$V1)#  "red") # add labels

plot(wine[,16],wine[,15], type="n")
text(wine.lda.values$x[,1],wine.lda.values$x[,2],wine$V1,cex=0.7,pos=4,col="red") # add labels


wine.lda$scaling[,2]
wine.lda$scaling[,1]

# Use the rules to classification task
par(mfrow=c(1,2))
ldahist(data = wine[,15], g=wine$V1)
ldahist(data = wine[,16], g=wine$V1)

n<-dim(wine)[1]
for(i in 1:n){
  if(wine[i,15]<0){wine[i,17]<-2
  }else{if (wine[i,16]<0){wine[i,17]<-1 
  }else{
    wine[i,17]<-3
  }
  }
}


#matriu de confusio
table(wine[,1])
MC<-table(wine[,1], wine[,17])
MC


#accuracy
accuracy<-sum(diag(MC))/dim(wine)[1]
accuracy

#compute missclassification rate
MR<-1-accuracy
MR

# Looking for middle points around medians to use them for classification task


printMeanAndSdByGroup <- function(variables,groupvariable)
{
  # find the names of the variables
  variablenames <- c(names(groupvariable),names(as.data.frame(variables)))
  # within each group, find the mean of each variable
  groupvariable <- groupvariable[,1] # ensures groupvariable is not a list
  means <- aggregate(as.matrix(variables) ~ groupvariable, FUN = mean)
  names(means) <- variablenames
  print(paste("Means:"))
  print(means)
  # within each group, find the standard deviation of each variable:
  sds <- aggregate(as.matrix(variables) ~ groupvariable, FUN = sd)
  names(sds) <- variablenames
  print(paste("Standard deviations:"))
  print(sds)
  # within each group, find the number of samples:
  samplesizes <- aggregate(as.matrix(variables) ~ groupvariable, FUN = length)
  names(samplesizes) <- variablenames
  print(paste("Sample sizes:"))
  print(samplesizes)
}

#Medians(Statistics) of the Discriminant functions by groups
printMeanAndSdByGroup(wine.lda.values$x,wine[1])


plot(wine[,2],wine[,3], col=wine[,1])
plot(wine[,5],wine[,7], col=wine[,1])
