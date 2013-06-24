from numpy import *
from scipy.io import loadmat
from copy import *
import matplotlib
import pylab
import variable_to_factor
import factor_to_variable


#Notes
#Tried default dict of default dict. doesnt work well with classes. So just statically allocate the space instead
#using the line listed below


#Calculate the total cost for any configuration
#c - cost matrix
#k - number of clusters
#idxlst - linked list of clusters. idxlst[k] contains nodes in cluster k
#idx - up to date cluster identity of nodes
def clusterCost(c, k, idxlst, idx):
    netcost = 0
    for k in range(k):
        cluster_similarity = 0
        for a in range(len(idxlst[k])):
            for b in range(len(idxlst[k])):
                cluster_similarity = cluster_similarity + c[idxlst[k][a], idxlst[k][b]]
        if len(idxlst[k]) > 0:
            netcost = netcost + (cluster_similarity / (len(idxlst[k])));
    return netcost

#Plot final results
def plotResults(idx, it, netcost, datapoints):
    f = matplotlib.pyplot.figure(1)
    f.clear()
    matplotlib.pyplot.subplot(211)
    matplotlib.pyplot.scatter(datapoints[:, 0], datapoints[:, 1], s=100, c=idx)

    matplotlib.pyplot.subplot(212);
    matplotlib.pyplot.plot(range(1, it + 1), netcost[0:it]);
    matplotlib.pyplot.xlabel('Iterations');
    matplotlib.pyplot.ylabel('Netcost');
    matplotlib.pyplot.show();

    #print idx
    #print it
    #for i in range(0,it):
    #    print netcost[i]
    return

#Defining classes for different kinds of messages
#NOTE: Keep dimensionality at the end all the time?
#denote the variable, factor -> f_fac and c_var etc.

class f_fac:
    def __init__(self, N, K):
        self.N_var = random.rand(N + 1);
        #self.c_var = random.rand(K,N);
        #self.N_var = zeros((N+1));
        self.c_var = zeros((K, N));


class c_var:
    def __init__(self, N, K):
        #self.theta_jk_fac = random.rand(N,K,K);
        #self.f_fac = random.rand(K,K);
        self.theta_jk_fac = zeros((N, K, K));
        self.f_fac = zeros((K, K));


class n_var:
    def __init__(self, N, K):
        #self.f_fac = random.rand(N+1);
        #self.theta_ij_fac = random.rand(N,N,N+1);
        self.f_fac = zeros((N + 1));
        self.theta_ij_fac = zeros((N, N, N + 1));


class theta_fac:
    def __init__(self, N, K):
        #self.c_i_var = random.rand(K,K);
        #self.c_j_var = random.rand(K,K);
        self.N_var = random.rand(N + 1, K);
        self.c_i_var = zeros((K, K));
        self.c_j_var = zeros((K, K));

    #self.N_var = zeros((N+1,K));


#Cluster - main function for clustering
#c - cost matrix
#n - number of points
#k - number of clusters
#datapoints - the data points in 2d
def cluster(c, n, k, datapoints):
    print "Beginning MP Cluster";

    #make sure you remember the updaet
    from_theta_fac = [[theta_fac(n, k) for j in range(n)] for i in range(n)];
    from_n_var = [n_var(n, k) for j in range(k)];
    from_f_fac = [f_fac(n, k) for j in range(k)];
    from_c_var = [c_var(n, k) for j in range(n)];

    #--------------------------------------------
    #threshold - whats the minimum difference to stop the algorithm at
    threshold = 0.0005;
    maxits = 50;
    objval = zeros((maxits + 1, 1));
    idx = [];
    idxold = [];
    it = 1;
    normalize = 1;
    damping_factor = 0.5;

    num_it_idx_constant = 0;
    THRESHOLD_CVG = 80;

    #loop : while not converged or
    while it <= maxits:
        print "\nIteration " + str(it);
        #Calculate the sum of all incoming messages, while there -> calculate the number of nodes in every cluster
        #and the clustering assignments of every point
        #Checked - Implementation OK
        sum_n, number_in_cluster = variable_to_factor.sum_incoming_n(n, k, from_f_fac, from_theta_fac);
        sum_c, idx = variable_to_factor.sum_incoming_c(n, k, from_f_fac, from_theta_fac);

        if it == 1:
            idxold = idx;
        else:
            if array_equal(idxold, idx):
                num_it_idx_constant = num_it_idx_constant + 1;
            else:
                num_it_idx_constant = 0;
            idxold = idx;

        if num_it_idx_constant == THRESHOLD_CVG:
            break;

        #Calculate the value of the objective function
        idxlst = [[] for i in range(0, k)];
        for i in range(n):
            idxlst[idx[i]].append(i);
        objval[it] = clusterCost(c, k, idxlst, idx);

        print number_in_cluster;
        print idx;
        print objval[it];
        #number_in_cluster is currently not used!

        #Send messages from factor to variable
        factor_to_variable.set_outgoing_theta_to_c(c, n, k, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var,
                                                   normalize, damping_factor);
        factor_to_variable.set_outgoing_theta_to_n(c, n, k, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var,
                                                   normalize, damping_factor);

        factor_to_variable.set_outgoing_f_to_c(c, n, k, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var,
                                               normalize, damping_factor);
        factor_to_variable.set_outgoing_f_to_n(c, n, k, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var,
                                               normalize, damping_factor);


        #Send messages from variable to factor
        variable_to_factor.set_outgoing_c_to_f(n, k, from_c_var, sum_c, from_f_fac, from_theta_fac, normalize);
        variable_to_factor.set_outgoing_c_to_theta(n, k, from_c_var, sum_c, from_f_fac, from_theta_fac, normalize);
        variable_to_factor.set_outgoing_n_to_theta(n, k, from_n_var, sum_n, from_f_fac, from_theta_fac, normalize);
        variable_to_factor.set_outgoing_n_to_f(n, k, from_n_var, sum_n, from_f_fac, from_theta_fac, normalize);

        #Older versions - Not used
        #variable_to_factor.set_outgoing_c(n,k,from_c_var,sum_c,from_f_fac,from_theta_fac,normalize);
        #variable_to_factor.set_outgoing_n(n,k,from_n_var,sum_n,from_f_fac,from_theta_fac,normalize);
        #factor_to_variable.set_outgoing_theta(c,n,k,from_c_var,sum_c,from_f_fac,from_theta_fac,from_n_var,normalize,damping_factor);
        #factor_to_variable.set_outgoing_f(c,n,k,from_c_var,sum_c,from_f_fac,from_theta_fac,from_n_var,normalize,damping_factor);
        it = it + 1;

    print "Done MP Cluster"
    return idx, it

#plot final results
#print idx;
#print number_in_cluster;
#plotResults(idx,it,objval,datapoints);
