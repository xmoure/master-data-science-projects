library(dplyr)
library(reshape2)
library(tidyr)
library(ggplot2)
library(stats)
library(cluster)
library(mclust)
library(factoextra)
library(dendextend)
library(NbClust)
library(colorspace)
library(patchwork)

#https://archive.ics.uci.edu/ml/datasets/Wine
data <- read.table("wine.data", header=FALSE, sep=",", as.is = TRUE)

names <- c('Cultivar','Alcohol','Malic_acid' , 'Ash', 'Alcalinity_ash', 'Magnesium', 'Total_phenols','Flavanoids', 'Nonflavanoid_phenols', 'Proanthocyanins', 'Color_intensity', 'Hue','OD280_OD315_diluted_wines','Proline')
colnames(data) <- names
summary(data)

cultivar <- data$Cultivar
data <- data[,-1]
dim(data)

###Scale or not????

##Clustering Ward.D with Euclidean distance
distancia<-dist(data,"euclidean")
fit<-hclust(distancia, "ward.D")
plot(fit, main="H.Clustering with euclidean distance and method WARD")
rect.hclust(fit, k=4, border=6)

###or
#library(FactoMineR)
#distance<-get_dist (data,"manhattan")
#fviz_dist(distance, gradient = list(low = "#00AFBB", mid = "white",high = "#FC4E07")) 
#fit2<-HCPC(data)



####Inspecting Height
fit$height
plot(fit)
rect.hclust(fit, h=608.940284,border="red")
plot(fit)
rect.hclust(fit, h= 6118.584596,border="red")

###############
fviz_dend(x = fit, k = 6, cex = 0.6)+ geom_hline(yintercept = 2500, linetype = "dashed") + labs(title = "Hierar.Clustering",subtitle = "Euclidean Distance - Method Ward - K=6")

###### Selection of K with quality clustering KPIs by using NbClust

indices <- c("kl","ch","hartigan","cindex","db","silhouette","ball","dunn","sdindex")

particiones <- vector()
for(i in 1:length(indices)){
  print(indices[i])
  sel_k<-NbClust(data,diss=distancia,distance=NULL,min.nc=2,max.nc=6,method="ward.D",index=indices[i])
  particiones[i]<-max(sel_k$Best.partition)
}

names(particiones) <- indices
particiones


#Labelling of Clustering Results
# Decision on k=6 (just for final-user requirements)
k <- 6
cut_k <- cutree(fit,k)
cut_k

###### Selection of K by using silhoutte
sil = silhouette (cut_k,distancia) # or use your cluster vector
windows() # RStudio sometimes does not display silhouette plots correctly
plot(sil)

#Interpreting Clustering  

data <- cbind(data,clusters=cut_k)
head(data)
data$clusters <- as.factor(data$clusters)
str(data)

centroides <- data.frame(data%>%dplyr::group_by(clusters)%>%dplyr::summarise(Proline=mean(Proline),Alcohol=mean(Alcohol),Flavanoids=mean(Flavanoids),Color_intensity=mean(Color_intensity), Magnesium=mean(Magnesium)))

centroides

#Visualization clusters versus features

centroides_melt <- centroides %>% melt(id.vars="clusters", variable.name="variable", value.name="valor")
centroides_melt

pallete <- rainbow_hcl(length(unique(centroides_melt$variable)))
c <- 1

myplots <- vector('list', length(unique(centroides_melt$variable)))
myplots

for(v in unique(centroides_melt$variable)){
  message(v)  
  d <- centroides_melt%>%filter(variable==v)%>%select(clusters,valor)
  
  myplots[[c]] <- local({
    c <- c
    g <- ggplot(d, aes(x=clusters,y=valor, group=1)) +
           geom_line(color=pallete[c]) +
           geom_point(color=pallete[c]) +
           ggtitle("Visualización de centroides", subtitle = paste("Variable",v))
    print(g)
  })
  c <- c+1
}

myplots

#(myplots[[1]]+myplots[[2]]+myplots[[3]])/(myplots[[4]]+myplots[[5]])

####Other methods
####daisy: Dissimilarity Matrix Calculation
####Compute all the pairwise dissimilarities (distances) between observations in the data set. The original variables may be of mixed types.
#### In that case, or whenever metric = "gower" is set, a generalization of Gower's formula is used.


###Agnes:Agglomerative Nesting (Hierarchical Clustering)
### Computes agglomerative hierarchical clustering of the dataset.
###   agnes(x, diss = inherits(x, "dist"), metric = "euclidean",
      stand = FALSE, method = "average", par.method,
      keep.diss = n < 100, keep.data = !diss, trace.lev = 0)

#### mona: MONothetic Analysis Clustering of Binary Variables
#### Returns a list representing a divisive hierarchical clustering of a dataset with binary variables only.
#### mona(x, trace.lev = 0)

