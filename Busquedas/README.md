This google life of mine
=========

#### Description  

- Copy this files to the folder where you download Search information of Takeout
- Run the following commands on terminal:
- for frecuency visualization
- ls *.json | ./trends.py | ./graficaHoras.py 
- for topic finding with LDA and NMF
- ls *.json | ./get_querys.py | ./clustering_LDA.py 
- For clustering with kmeans and finding the number of clusters
- ls *.json | ./get_querys.py | ./clustering.py