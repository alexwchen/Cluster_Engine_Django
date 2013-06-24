#########################################################################
# File Name: algorithm.py
# Author: Alexander Chen   
#
# Description:
#   Funcions written in this file are mostly related to producing questoins
#   for training and testing the user. 
#
# Class:
#   Quizbot
#
# Functions:
#
# [ Accessing Inernal Word Database ]  
#
# [ Accessing User Preference Database ]  
#
# [ Generating Questions ]  
#
#########################################################################


import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn import metrics

from sklearn.datasets.samples_generator import make_blobs

def call_affinity_propagation(similarity,preference):
    af = AffinityPropagation().fit(similarity, preference)
    examplar_labels = af.cluster_centers_indices_
    all_labels = af.labels_
    num_clusters = len(examplar_labels)
    print examplar_labels 
    print labels
    print num_clusters
    
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
def call_kmean(num_cluster, num_trial, data):
    k_means = KMeans(init='k-means++', n_clusters=num_cluster, n_init=num_trial)
    k_means.fit(data)
    labels = k_means.labels_
    cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(labels)
    print labels
    print cluster_centers
    print k_means_labels_unique

#########################################################################
#   hit wall, try to figure this out later
#########################################################################
from sklearn.cluster import spectral_clustering
def call_spectral(similarity, num_cluster):
    sp = spectral_clustering(n_clusters=num_cluster).fit(similarity)



##############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5)

##############################################################################
# Compute similarities
X_norms = np.sum(X ** 2, axis=1)
S = - X_norms[:, np.newaxis] - X_norms[np.newaxis, :] + 2 * np.dot(X, X.T)
P = 10 * np.median(S)


#call_affinity_propagation(S,P)
#call_kmean(3,10,X)
#call_spectral(S, 3)

