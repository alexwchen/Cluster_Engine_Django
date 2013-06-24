from numpy import *
from scipy.io import loadmat
import copy
import matplotlib
import pylab



'''
    Messages from variable nodes to factor nodes
'''
#Calculate the outgoing messages from c to every factor - Modified
def set_outgoing_c_to_theta(N,K,from_c_var,sum_c,from_f_fac,from_theta_fac,normalize):

    #outgoing messages to theta
    for i in range(N-1):
        for j in range(i+1,N):
            for k in range(K):
                from_c_var[i].theta_jk_fac[j,k,:] = sum_c[:,i] - from_theta_fac[i][j].c_i_var[:,k];
                from_c_var[j].theta_jk_fac[i,k,:] = sum_c[:,j] - from_theta_fac[i][j].c_j_var[:,k];
                if normalize==1:
                    from_c_var[i].theta_jk_fac[j,k,:] = from_c_var[i].theta_jk_fac[j,k,:] - max(from_c_var[i].theta_jk_fac[j,k,:]);
                    from_c_var[j].theta_jk_fac[i,k,:] = from_c_var[j].theta_jk_fac[i,k,:] - max(from_c_var[j].theta_jk_fac[i,k,:]);
    return;

#Modified
def set_outgoing_c_to_f(N,K,from_c_var,sum_c,from_f_fac,from_theta_fac,normalize):

    #outgoing messages to f
    for i in range(N):
        for k in range(K):
            from_c_var[i].f_fac[:,k] = sum_c[:,i] - from_f_fac[k].c_var[:,i];
            if normalize==1:
                from_c_var[i].f_fac[:,k] = from_c_var[i].f_fac[:,k] - max(from_c_var[i].f_fac[:,k]);

    return;

#Modified
def set_outgoing_c(N,K,from_c_var,sum_c,from_f_fac,from_theta_fac,normalize):

    #outgoing messages to theta
    for i in range(N-1):
        for j in range(i+1,N):
            for k in range(K):
                from_c_var[i].theta_jk_fac[j,k,:] = sum_c[:,i] - from_theta_fac[i][j].c_i_var[:,k];
                from_c_var[j].theta_jk_fac[i,k,:] = sum_c[:,j] - from_theta_fac[i][j].c_j_var[:,k];
                if normalize==1:
                    from_c_var[i].theta_jk_fac[j,k,:] = from_c_var[i].theta_jk_fac[j,k,:] - max(from_c_var[i].theta_jk_fac[j,k,:]);
                    from_c_var[j].theta_jk_fac[i,k,:] = from_c_var[j].theta_jk_fac[i,k,:] - max(from_c_var[j].theta_jk_fac[i,k,:]);

    #outgoing messages to f
    for i in range(N):
        for k in range(K):
            from_c_var[i].f_fac[:,k] = sum_c[:,i] - from_f_fac[k].c_var[:,i];
            if normalize==1:
                from_c_var[i].f_fac[:,k] = from_c_var[i].f_fac[:,k] - max(from_c_var[i].f_fac[:,k]);

    return;

#-----------------------

#Calculate the outgoing message from n to every factor
#Modified
def set_outgoing_n_to_f(N,K,from_n_var,sum_n,from_f_fac,from_theta_fac,normalize):
    #outgoing messages to all f_k
    for k in range(K):
        from_n_var[k].f_fac = sum_n[:,k] - from_f_fac[k].N_var;
        if normalize==1:
            from_n_var[k].f_fac = from_n_var[k].f_fac - max(from_n_var[k].f_fac);
    return;

#Modified
def set_outgoing_n_to_theta(N,K,from_n_var,sum_n,from_f_fac,from_theta_fac,normalize):

    #outgoing messages to theta
    #for j in range(N):
    #	for i in range(j):
    #		for k in range(K):
    #			from_n[k].theta_ij[i,j,:] = sum_n[:,k] - from_theta[i][j].N[:,k];

    #we send to N(N-1) theta nodes though we only care about half of them
    for i in range(N-1):
        for j in range(i+1,N):
            for k in range(K):
                from_n_var[k].theta_ij_fac[i,j,:] = sum_n[:,k] - from_theta_fac[i][j].N_var[:,k];
                if normalize==1:
                    from_n_var[k].theta_ij_fac[i,j,:] = from_n_var[k].theta_ij_fac[i,j,:] - max(from_n_var[k].theta_ij_fac[i,j,:]);

    return;

#Outgoing messages for all n variable nodes. - Modified
def set_outgoing_n(N,K,from_n_var,sum_n,from_f_fac,from_theta_fac,normalize): 

    #we send to N(N-1) theta nodes though we only care about half of them
    for i in range(N-1):
        for j in range(i+1,N):
            for k in range(K):
                from_n_var[k].theta_ij_fac[i,j,:] = sum_n[:,k] - from_theta_fac[i][j].N_var[:,k];
                if normalize==1:
                    from_n_var[k].theta_ij_fac[i,j,:] = from_n_var[k].theta_ij_fac[i,j,:] - max(from_n_var[k].theta_ij_fac[i,j,:]);

    #outgoing messages to all f_k
    for k in range(K):
        from_n_var[k].f_fac = sum_n[:,k] - from_f_fac[k].N_var;
        if normalize==1:
            from_n_var[k].f_fac = from_n_var[k].f_fac - max(from_n_var[k].f_fac);
    return;


#---------------------------

#calculate the sum of all messages into every c node - Modified
def sum_incoming_c(N,K,from_f_fac,from_theta_fac):
    sum_c = zeros((K,N));

    #compute sum for the values from theta_ijk
    #Old method - traverse pariwise nodes
    #for j in range(N):
    #	for i in range(j):
    #		sum_c[:,i] = sum_c[:,i] + from_theta[i][j].c_i.sum(axis=1);
    #		sum_c[:,j] = sum_c[:,j] + from_theta[i][j].c_j.sum(axis=1);

    #new method - traverse all, divide by 2
    for i in range(N-1):
        for j in range(i+1,N):
            sum_c[:,i] = sum_c[:,i] + from_theta_fac[i][j].c_i_var.sum(axis=1);
            sum_c[:,j] = sum_c[:,j] + from_theta_fac[i][j].c_j_var.sum(axis=1);

    #--------------------------


    #compute sum of incoming messages from f_k to
    for k in range(K):
        for i in range(N):#OPTIMIZE THIS LOOP
            sum_c[:,i] = sum_c[:,i]+from_f_fac[k].c_var[:,i];

    return sum_c,argmax(sum_c,axis=0);



#Calculate the sum of all messages into every N node - Modified
def sum_incoming_n(N,K,from_f_fac,from_theta_fac):
    sum_n = zeros((N+1,K));
    #New one - goes through all

    for i in range(N-1):
        for j in range(i+1,N):
            for k in range(K):
                sum_n[:,k] = sum_n[:,k] + from_theta_fac[i][j].N_var[:,k];

    #Divide by 2 to make 	
    sum_n = sum_n/2;

    #--------------------------

    #compute the message from f
    for k in range(K):
        sum_n[:,k] = sum_n[:,k] + from_f_fac[k].N_var;

    return sum_n,argmax(sum_n,axis=0);