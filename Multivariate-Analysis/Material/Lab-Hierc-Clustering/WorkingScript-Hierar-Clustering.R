#Retrieve the data saved AFTER the profiling practice...... this means data already cleaned

#setwd("D:/karina/docencia/areferenciesPPT/DadesPractiques/CREDSCO")
dd <- read.csv("credscoClean.csv", sep=";",dec=".",stringsAsFactors = TRUE)
names(dd)
dim(dd)
summary(dd)
attach(dd)

#set a list of numerical variables
names(dd)

dcon <- data.frame (Antiguedad.Trabajo,Plazo,Edad,Gastos,Ingresos,Patrimonio,Cargas.patrimoniales,Importe.solicitado,Precio.del.bien.financiado,Estalvi, RatiFin)
dim(dcon)

#
# CLUSTERING
#
# HIERARCHICAL CLUSTERING
help("dist")
d  <- dist(dcon[1:50,])
help("hclust")
h1 <- hclust(d,method="ward.D") 
plot(h1)

d  <- dist(dcon)
?dist
h1 <- hclust(d,method="ward.D")  
plot(h1)

# BUT WE ONLY NEED WHERE THERE ARE THE LEAPS OF THE HEIGHT

# WHERE ARE THER THE LEAPS? WHERE WILL YOU CUT THE DENDOGRAM?, HOW MANY CLASSES WILL YOU OBTAIN?

nc = 3

c1 <- cutree(h1,nc)

c1[1:20]

nc = 5

c5 <- cutree(h1,nc)

c5[1:20]


table(c1)
table(c5)
table(c1,c5)


cdg <- aggregate(as.data.frame(dcon),list(c1),mean)
cdg



# LETS SEE THE PARTITION VISUALLY


plot(Edad,Estalvi,col=c1,main="Clustering of credit data in 3 classes")
legend("topright",c("class1","class2","class3"),pch=1,col=c(1:3))

plot(RatiFin,Estalvi,col=c1,main="Clustering of credit data in 3 classes")
legend("topright",c("class1","class2","class3"),pch=1,col=c(1:3), cex=0.6)

plot(Antiguedad.Trabajo,Estalvi,col=c1,main="Clustering of credit data in 3 classes")
legend("topright",c("class1","class2","class3"),pch=1,col=c(1:3), cex=0.6)
plot(Patrimonio, Ingresos,col=c1,main="Clustering of credit data in 3 classes")
legend("topright",c("class1","class2","class3"),pch=1,col=c(1:3), cex=0.6)
plot(Patrimonio, Antiguedad.Trabajo,col=c1,main="Clustering of credit data in 3 classes")
legend("topright",c("class1","class2","class3"),pch=1,col=c(1:3), cex=0.6)

pairs(dcon[,1:7], col=c1)

#move to Gower mixed distance to deal 
#simoultaneously with numerical and qualitative data

library(cluster)

#dissimilarity matrix

actives<-c(2:16)
dissimMatrix <- daisy(dd[,actives], metric = "gower", stand=TRUE)

distMatrix<-dissimMatrix^2

h1 <- hclust(distMatrix,method="ward.D")  
plot(h1)
c2 <- cutree(h1,4)

#class sizes 
table(c2)

names(dd)
#ratiFin
boxplot(dd[,16]~c2, horizontal=TRUE)

#plazo
boxplot(dd[,4]~c2, horizontal=TRUE)

#gastos
boxplot(dd[,9]~c2, horizontal=TRUE)

pairs(dcon[,1:7], col=c2)

plot(RatiFin,Estalvi,col=c2,main="Clustering of credit data in 4 classes")
legend("topright",levels(as.factor(c2)),pch=1,col=c(1:4), cex=0.6)

cdg <- aggregate(as.data.frame(dcon),list(c2),mean)
cdg

plot(Edad, Gastos, col= c2)
points(cdg[,4],cdg[,5],pch=16,col="orange")
text(cdg[,4],cdg[,5], labels=cdg[,1], pos=2, font=2, cex=0.7, col="orange")

potencials<-c(3,4,6,7,10,11)
pairs(dcon[,potencials],col=c2)

#Profiling plots
