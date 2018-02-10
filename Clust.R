library(readr)
Ligs_26pops <- read_delim("Desktop/temp/Ligs_26pops.txt", 
                            "\t", escape_double = FALSE, trim_ws = TRUE)
View(Ligs_26pops)

vars.to.use <- colnames(Ligs_26pops)[-1]
pmatrix <- scale(Ligs_26pops[,vars.to.use])
d <- dist(pmatrix, method="euclidean")
pfit <- hclust(d, method="ward")
plot(pfit, labels=Ligs_26pops$X1)

rect.hclust(pfit, k=3)
library(fpc)
kbest.p<-3
cboot.hclust <- clusterboot(pmatrix, B=1000, clustermethod=hclustCBI, method="ward", k=kbest.p)
groups<-cboot.hclust$result$partition

print_clusters <- function(labels, k) {             
  for(i in 1:k) {
    print(paste("cluster", i))
    print(Ligs_26pops[labels==i,c("X1")])
  }
}

print_clusters (groups, kbest.p)

cboot.hclust$bootmean
cboot.hclust$bootbrd


### last lines only work on mac R.. is bug in latest fpc i think

