from numpy import *
from scipy.io import loadmat
import copy
import matplotlib
import pylab

def start_algo():
    print "Loading input data"
    data = loadmat('/Users/benaneesh/Desktop/clusteringece496/clustapp/engine/sample2.mat')
    
    print "Initializing data from .mat file"
    N = size((data['S'])[0])
    S = data['S']
    K = 5
    DataPoints = data['DataPoints']
    greedyCluster(-S,N,K,DataPoints)
    return
    
#calculate the total cost for any given configuration
def clusterCost(c,k,idxlst,idx):
    netcost = 0
    for k in range(k):
        cluster_similarity = 0
        for a in range(len(idxlst[k])):
            for b in range(len(idxlst[k])):
                cluster_similarity = cluster_similarity + c[idxlst[k][a],idxlst[k][b]] 
        netcost = netcost + (cluster_similarity/len(idxlst[k]))
    return netcost

#calculate thecost of having node placed within cluster
def clusterCost_k(c,cluster,idxlst,node):
    cluster_cost = 0
    for a in range(len(idxlst[cluster])):
        cluster_cost = cluster_cost + c[idxlst[cluster][a],node] 
    cluster_cost =  cluster_cost/len(idxlst[cluster])
    return cluster_cost

def allocateList(upper_lim,arrlist):
    for i in range(upper_lim):
        arrlist.append(0)
    return

def greedyCluster(costmatrix,n,k,datapoints):
    print "Beginning Greedy Cluster"    
    #prm = permutation(n)
    
    #permuting points disabled
    #c = costmatrix[prm][prm]
    c = costmatrix    
    
    idx = []
    allocateList(n,idx)
    
    
    #idx - Put 1st k datapoints in random clusters
    #idxlst - create list of lists containing points in each cluster
    idxlst = [[] for i in range(0,k)]
    for i in range(0,n):
      idx[i]=random.randint(0,k)
      idxlst[idx[i]].append(i)
    
    # Repeatedly process the dataset until convergence
    cvg = 0 
    it = 0
  
  
    netcost = []
    delcost = []
    
    #netcost = zeros((10000,1),int) 
    #delcost = zeros((k,1),int)
    allocateList(100000,netcost)
    allocateList(k,delcost)
    
    #calculate initial netcost 
    netcost[0] = clusterCost(c,k,idxlst,idx)


    while not cvg:
        it = it + 1
        netcost[it] = netcost[it-1]
        idxold = copy.deepcopy(idx)

        for i in range(n):
            for j in range(k):
                delcost[j] = clusterCost_k(c,j,idxlst,i)
            
            mn = min(delcost)
            mni= delcost.index(mn);
            if mni != idx[i]:
                #need to do he swap
                old = idx[i]
                new = mni
                idxlst[old].remove(i)
                idxlst[new].append(i)
                idx[i] = new
                #netcost[it] = netcost[it]+mn-delcost[idx[i]];
                netcost[it] = clusterCost(c,k,idxlst,idx)
        #end of for
        
        if idxold == idx:
            cvg = 1
    #end of while
    

    #plot
    #f = matplotlib.pyplot.figure(1)
    #f.clear()
    #matplotlib.pyplot.subplot(211) 
    #matplotlib.pyplot.scatter(datapoints[:,0],datapoints[:,1],s=100,c=idx)  
    #matplotlib.pyplot.show()

    #matplotlib.pyplot.subplot(212)
    #matplotlib.pyplot.plot(range(1,it+1),netcost[0:it])
    #matplotlib.pyplot.xlabel('Iterations')
    #matplotlib.pyplot.ylabel('Netcost')
    #matplotlib.pyplot.show()

    return idx, it, netcost
    #end of function
    


#TODO
#optimization ideas
#keep cost of cluster to prevent recomputation
