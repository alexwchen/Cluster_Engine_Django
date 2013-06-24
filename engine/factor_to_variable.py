from numpy import *
from scipy.io import loadmat
from copy import *
import matplotlib
import pylab

'''
	Messages from factor nodes to variable nodes
'''


def set_outgoing_f_to_n(similarity, N, K, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var, normalize,
                        damping_factor):
    #setup and create the M index matrix
    M = zeros((K, N), dtype=int8);
    diff = zeros((N, 1));

    #Optimize - using 1st and second max
    for k in range(K):
        for i in range(N):
            diff[i] = from_c_var[i].f_fac[k, k] - max(delete(from_c_var[i].f_fac[:, k], k));
        temp = argsort(diff, axis=0);
        M[k, :] = transpose(temp[::-1])


    #collect messages from c variable nodes in an easier data structure
    msg_from_c = zeros((K, K, N));
    for k in range(K):
        for i in range(N):
            msg_from_c[k, :, i] = from_c_var[i].f_fac[:, k];

    for k in range(K):
        #Need to look at all the messages from f_k to N_k and all c
        for i in range(N):

            #Messages to

            #0th message
            #removing the kth element
            #delete(....,(k),axis=0)
            #delete the row along the current k, find the maximum along
            #that axis, and take the sum. This is for all incoming messages from


            #optimization - take the sum along the columns and then subtract for every k.

            #damping
            old_msg_n = deepcopy(from_f_fac[k].N_var);

            from_f_fac[k].N_var[0] = sum(delete(msg_from_c[k, :, :], (k), axis=0).max(axis=0));

            #Nth message- All nodes in cluster K
            from_f_fac[k].N_var[N] = sum(msg_from_c[k, k, :]);


            #try and think of the operations only once
            for n in range(1, N):
                # transpose(ARRAY[k,:,[*first n indices taken from M*]])
                # apply same formula as above

                #OPTIMIZE HERE-> Opportunities!!!

                #Fetch it once -> reorder it and then do the cumsum over the reordering
                #M is indexed from 0
                in_k = transpose(msg_from_c[k, :, M[k, 0:(n)]]);
                not_in_k = transpose(msg_from_c[k, :, M[k, (n):]]);
                from_f_fac[k].N_var[n] = sum(in_k[k, :]) + sum(delete(not_in_k, (k), axis=0).max(axis=0));

            if normalize == 1:
                from_f_fac[k].N_var = from_f_fac[k].N_var - max(from_f_fac[k].N_var);
                from_f_fac[k].N_var = (damping_factor * old_msg_n) + ((1 - damping_factor) * from_f_fac[k].N_var);

    return;


def set_outgoing_f_to_c(similarity, N, K, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var, normalize,
                        damping_factor):
    #setup and create the M index matrix
    M = zeros((K, N), dtype=int8);
    diff = zeros((N, 1));

    #Optimize - using 1st and second max
    for k in range(K):
        for i in range(N):
            diff[i] = from_c_var[i].f_fac[k, k] - max(delete(from_c_var[i].f_fac[:, k], k));
        temp = argsort(diff, axis=0);
        M[k, :] = transpose(temp[::-1])


    #collect messages from c variable nodes in an easier data structure
    msg_from_c = zeros((K, K, N));
    for k in range(K):
        for i in range(N):
            msg_from_c[k, :, i] = from_c_var[i].f_fac[:, k];

    for k in range(K):
        #Need to look at all the messages from f_k to N_k and all c
        for i in range(N):

            #Messages to

            #0th message
            #removing the kth element
            #delete(....,(k),axis=0)
            #delete the row along the current k, find the maximum along
            #that axis, and take the sum. This is for all incoming messages from


            #optimization - take the sum along the columns and then subtract for every k.


            #should be N-1 but its N because we index ctr for the last one at the end
            message_to_c_k = zeros((N, 1));
            message_to_c_not_k = zeros((N, 1));
            ctr = 0;

            #try and think of the operations only once
            for n in range(1, N):
                # transpose(ARRAY[k,:,[*first n indices taken from M*]])
                # apply same formula as above

                #OPTIMIZE HERE-> Opportunities!!!

                #Fetch it once -> reorder it and then do the cumsum over the reordering
                #M is indexed from 0

                #For the messages to the c nodes, we need to keep track of the following

                pos_i = where(M[k, :] == i);
                M_no_i = delete(M[k, :], pos_i, axis=0);

                in_k = transpose(msg_from_c[k, :, M_no_i[0:(n - 1)]]);
                not_in_k = transpose(msg_from_c[k, :, M_no_i[(n - 1):]]);
                message_to_c_k[ctr] = from_n_var[k].f_fac[n] + sum(in_k[k, :]) + sum(
                    delete(not_in_k, (k), axis=0).max(axis=0));

                in_k = transpose(msg_from_c[k, :, M_no_i[0:n]]);
                not_in_k = transpose(msg_from_c[k, :, M_no_i[(n):]]);
                message_to_c_not_k[ctr] = from_n_var[k].f_fac[n] + sum(in_k[k, :]) + sum(
                    delete(not_in_k, (k), axis=0).max(axis=0));

                ctr = ctr + 1;


            #Need to set the last message in message_to_c(not k and k)
            #in the case where it is k - consider Nth one
            in_k = transpose(msg_from_c[k, :, M_no_i[:]]);
            message_to_c_k[ctr] = from_n_var[k].f_fac[N] + sum(in_k[k, :]);

            #in the case where it is not k - consider 0th one
            not_in_k = transpose(msg_from_c[k, :, M_no_i[:]]);
            message_to_c_not_k[ctr] = from_n_var[k].f_fac[0] + sum(delete(not_in_k, (k), axis=0).max(axis=0));

            #Set the message from f_k to c_i
            old_msg_c = deepcopy(from_f_fac[k].c_var[:, i]);
            from_f_fac[k].c_var[:, i] = max(message_to_c_not_k);
            from_f_fac[k].c_var[k, i] = max(message_to_c_k);

            if normalize == 1:
                from_f_fac[k].c_var[:, i] = from_f_fac[k].c_var[:, i] - max(from_f_fac[k].c_var[:, i]);
                from_f_fac[k].c_var[:, i] = (damping_factor * old_msg_c) + (
                    (1 - damping_factor) * from_f_fac[k].c_var[:, i]);

    return;


# Functions that control factor->variable messages
def set_outgoing_f(similarity, N, K, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var, normalize,
                   damping_factor):
    #setup and create the M index matrix
    M = zeros((K, N), dtype=int8);
    diff = zeros((N, 1));

    #Optimize - using 1st and second max
    for k in range(K):
        for i in range(N):
            diff[i] = from_c_var[i].f_fac[k, k] - max(delete(from_c_var[i].f_fac[:, k], k));
        temp = argsort(diff, axis=0);
        M[k, :] = transpose(temp[::-1])


    #collect messages from c variable nodes in an easier data structure
    msg_from_c = zeros((K, K, N));
    for k in range(K):
        for i in range(N):
            msg_from_c[k, :, i] = from_c_var[i].f_fac[:, k];

    for k in range(K):
        #Need to look at all the messages from f_k to N_k and all c
        for i in range(N):

            #Messages to

            #0th message
            #removing the kth element
            #delete(....,(k),axis=0)
            #delete the row along the current k, find the maximum along
            #that axis, and take the sum. This is for all incoming messages from


            #optimization - take the sum along the columns and then subtract for every k.

            #damping
            old_msg_n = deepcopy(from_f_fac[k].N_var);

            from_f_fac[k].N_var[0] = sum(delete(msg_from_c[k, :, :], (k), axis=0).max(axis=0));

            #Nth message- All nodes in cluster K
            from_f_fac[k].N_var[N] = sum(msg_from_c[k, k, :]);

            #should be N-1 but its N because we index ctr for the last one at the end
            message_to_c_k = zeros((N, 1));
            message_to_c_not_k = zeros((N, 1));
            ctr = 0;

            #try and think of the operations only once
            for n in range(1, N):
                # transpose(ARRAY[k,:,[*first n indices taken from M*]])
                # apply same formula as above

                #OPTIMIZE HERE-> Opportunities!!!

                #Fetch it once -> reorder it and then do the cumsum over the reordering
                #M is indexed from 0
                in_k = transpose(msg_from_c[k, :, M[k, 0:(n)]]);
                not_in_k = transpose(msg_from_c[k, :, M[k, (n):]]);
                from_f_fac[k].N_var[n] = sum(in_k[k, :]) + sum(delete(not_in_k, (k), axis=0).max(axis=0));

                #For the messages to the c nodes, we need to keep track of the following

                pos_i = where(M[k, :] == i);
                M_no_i = delete(M[k, :], pos_i, axis=0);

                in_k = transpose(msg_from_c[k, :, M_no_i[0:(n - 1)]]);
                not_in_k = transpose(msg_from_c[k, :, M_no_i[(n - 1):]]);
                message_to_c_k[ctr] = from_n_var[k].f_fac[n] + sum(in_k[k, :]) + sum(
                    delete(not_in_k, (k), axis=0).max(axis=0));

                in_k = transpose(msg_from_c[k, :, M_no_i[0:n]]);
                not_in_k = transpose(msg_from_c[k, :, M_no_i[(n):]]);
                message_to_c_not_k[ctr] = from_n_var[k].f_fac[n] + sum(in_k[k, :]) + sum(
                    delete(not_in_k, (k), axis=0).max(axis=0));

                ctr = ctr + 1;

            if normalize == 1:
                from_f_fac[k].N_var = from_f_fac[k].N_var - max(from_f_fac[k].N_var);
                from_f_fac[k].N_var = (damping_factor * old_msg_n) + ((1 - damping_factor) * from_f_fac[k].N_var);

            #Need to set the last message in message_to_c(not k and k)
            #in the case where it is k - consider Nth one
            in_k = transpose(msg_from_c[k, :, M_no_i[:]]);
            message_to_c_k[ctr] = from_n_var[k].f_fac[N] + sum(in_k[k, :]);

            #in the case where it is not k - consider 0th one
            not_in_k = transpose(msg_from_c[k, :, M_no_i[:]]);
            message_to_c_not_k[ctr] = from_n_var[k].f_fac[0] + sum(delete(not_in_k, (k), axis=0).max(axis=0));

            #Set the message from f_k to c_i
            old_msg_c = deepcopy(from_f_fac[k].c_var[:, i]);
            from_f_fac[k].c_var[:, i] = max(message_to_c_not_k);
            from_f_fac[k].c_var[k, i] = max(message_to_c_k);

            if normalize == 1:
                from_f_fac[k].c_var[:, i] = from_f_fac[k].c_var[:, i] - max(from_f_fac[k].c_var[:, i]);
                from_f_fac[k].c_var[:, i] = (damping_factor * old_msg_c) + (
                    (1 - damping_factor) * from_f_fac[k].c_var[:, i]);

    return;


#----------------------------------

#Calculate the outgoing messages from theta to n - Modified
def set_outgoing_theta_to_n(similarity, N, K, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var, normalize,
                            damping_factor):
    #outgoing messages to N
    for i in range(N - 1):
        for j in range(i + 1, N):
            for k in range(K):
                #POSSIBILITIES FOR OPTIMIZATION

                #For the message from theta_ijk to N_k variable node
                #Need to construct a message of size N+1
                #Need to reference:
                # from_c[i].theta_jk[j,k,:] - message from c_i to theta_ij for k
                # from_c[j].theta_jk[i,k,:] - message from c_j to theta_ij for k

                #Create copies of the message from
                mu_ci = deepcopy(from_c_var[i].theta_jk_fac[j, k, :]);
                mu_cj = deepcopy(from_c_var[j].theta_jk_fac[i, k, :]);

                #From these messages, we need 4 entities
                # 1. message in position k from c_i and c_j
                k_c_i = mu_ci[k];
                k_c_j = mu_cj[k];


                # 2. maximal message not in position k from c_i and c_j
                mu_ci[k] = -inf;
                mu_cj[k] = -inf;
                max_c_i = amax(mu_ci);
                max_c_j = amax(mu_cj);

                # 3. similarity between i and j
                sim = similarity[i, j];

                # 4. max of the sum of them
                max_both = max((mu_cj + mu_ci));

                #Set up outgoing message to N

                #damping
                old_msg_n = deepcopy(from_theta_fac[i][j].N_var[:, k]);

                #Corner cases
                #Fixed
                from_theta_fac[i][j].N_var[0, k] = max_c_j + max_c_i;
                from_theta_fac[i][j].N_var[1, k] = max(k_c_i + max_c_j, max_c_i + k_c_j, max_c_i + max_c_j);
                from_theta_fac[i][j].N_var[N - 1, k] = max((sim / (N - 1)) + k_c_i + k_c_j, k_c_i + max_c_j,
                                                           max_c_i + k_c_j);
                from_theta_fac[i][j].N_var[N, k] = (sim / N) + k_c_i + k_c_j;

                #Remaining messages
                for m in range(2, N - 1):
                    from_theta_fac[i][j].N_var[m, k] = max((sim / m) + k_c_i + k_c_j, k_c_i + max_c_j, max_c_i + k_c_j,
                                                           max_c_i + max_c_j);

                if normalize == 1:
                    from_theta_fac[i][j].N_var[:, k] = from_theta_fac[i][j].N_var[:, k] - max(
                        from_theta_fac[i][j].N_var[:, k]);
                    from_theta_fac[i][j].N_var[:, k] = (damping_factor * old_msg_n) + (
                        (1 - damping_factor) * from_theta_fac[i][j].N_var[:, k]);
    return;

#Calculate the outgoing messages from theta to c - Modified
def set_outgoing_theta_to_c(similarity, N, K, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var, normalize,
                            damping_factor):
    #outgoing messages to N
    for i in range(N - 1):
        for j in range(i + 1, N):
            for k in range(K):
                #POSSIBILITIES FOR OPTIMIZATION

                #Create copies of the message from
                mu_ci = deepcopy(from_c_var[i].theta_jk_fac[j, k, :]);
                mu_cj = deepcopy(from_c_var[j].theta_jk_fac[i, k, :]);

                #From these messages, we need 4 entities
                # 1. message in position k from c_i and c_j
                k_c_i = mu_ci[k];
                k_c_j = mu_cj[k];


                # 2. maximal message not in position k from c_i and c_j
                mu_ci[k] = -inf;
                mu_cj[k] = -inf;
                max_c_i = amax(mu_ci);
                max_c_j = amax(mu_cj);

                # 3. similarity between i and j
                sim = similarity[i, j];

                # 4. max of the sum of them
                max_both = max((mu_cj + mu_ci));

                #For the message from theta_ijk to c_i variable node
                #Need to construct a message of size N+1
                #Need to reference:
                # from_n[k].theta_ij[i,j,:] - message from N_k to theta_ijk
                # one of the two, depending on who the message is being sent to
                # from_c[j].theta_jk[i,k,:] - message from c_j to theta_ij for k
                # OR from_c[i].theta_jk[j,k,:] - message from c_i to theta_ij for k
                mu_n = deepcopy(from_n_var[k].theta_ij_fac[i, j, :]);

                #Messages will be symmetric in nature for c_i and c_j
                #initialize vector of similaritie
                max_N_0N = amax(mu_n[1:N]);
                max_N_NN = amax(mu_n[0:N - 1]);

                #RECHECK
                divisor = cumsum(ones((N - 1, 1))) + 1;
                normalized = similarity[i, j] / divisor;
                max_N_01 = amax(mu_n[2:N + 1] + normalized);

                old_msg_c_i = deepcopy(from_theta_fac[i][j].c_i_var[:, k]);
                old_msg_c_j = deepcopy(from_theta_fac[i][j].c_j_var[:, k]);

                from_theta_fac[i][j].c_i_var[:, k] = max(k_c_j + max_N_0N, max_c_j + max_N_NN);
                from_theta_fac[i][j].c_j_var[:, k] = max(k_c_i + max_N_0N, max_c_i + max_N_NN);

                from_theta_fac[i][j].c_i_var[k, k] = max(k_c_j + max_N_01, max_c_j + max_N_0N);
                from_theta_fac[i][j].c_j_var[k, k] = max(k_c_i + max_N_01, max_c_i + max_N_0N);

                if normalize == 1:
                    from_theta_fac[i][j].c_i_var[:, k] = from_theta_fac[i][j].c_i_var[:, k] - max(
                        from_theta_fac[i][j].c_i_var[:, k]);
                    from_theta_fac[i][j].c_j_var[:, k] = from_theta_fac[i][j].c_j_var[:, k] - max(
                        from_theta_fac[i][j].c_j_var[:, k]);
                    from_theta_fac[i][j].c_i_var[:, k] = (damping_factor * old_msg_c_i) + (
                        (1 - damping_factor) * from_theta_fac[i][j].c_i_var[:, k]);
                    from_theta_fac[i][j].c_j_var[:, k] = (damping_factor * old_msg_c_j) + (
                        (1 - damping_factor) * from_theta_fac[i][j].c_j_var[:, k]);
    return;


#Calculate the outgoing messages from theta - Modified
def set_outgoing_theta(similarity, N, K, from_c_var, sum_c, from_f_fac, from_theta_fac, from_n_var, normalize,
                       damping_factor):
    #outgoing messages to N
    for i in range(N - 1):
        for j in range(i + 1, N):
            for k in range(K):
                #POSSIBILITIES FOR OPTIMIZATION

                #For the message from theta_ijk to N_k variable node
                #Need to construct a message of size N+1
                #Need to reference:
                # from_c[i].theta_jk[j,k,:] - message from c_i to theta_ij for k
                # from_c[j].theta_jk[i,k,:] - message from c_j to theta_ij for k

                #Create copies of the message from
                mu_ci = deepcopy(from_c_var[i].theta_jk_fac[j, k, :]);
                mu_cj = deepcopy(from_c_var[j].theta_jk_fac[i, k, :]);

                #From these messages, we need 4 entities
                # 1. message in position k from c_i and c_j
                k_c_i = mu_ci[k];
                k_c_j = mu_cj[k];


                # 2. maximal message not in position k from c_i and c_j
                mu_ci[k] = -inf;
                mu_cj[k] = -inf;
                max_c_i = amax(mu_ci);
                max_c_j = amax(mu_cj);

                # 3. similarity between i and j
                sim = similarity[i, j];

                # 4. max of the sum of them
                max_both = max((mu_cj + mu_ci));

                #Set up outgoing message to N

                #damping
                old_msg_n = deepcopy(from_theta_fac[i][j].N_var[:, k]);

                #Corner cases
                #Fixed
                from_theta_fac[i][j].N_var[0, k] = max_c_j + max_c_i;
                from_theta_fac[i][j].N_var[1, k] = max(k_c_i + max_c_j, max_c_i + k_c_j, max_c_i + max_c_j);
                from_theta_fac[i][j].N_var[N - 1, k] = max((sim / (N - 1)) + k_c_i + k_c_j, k_c_i + max_c_j,
                                                           max_c_i + k_c_j);
                from_theta_fac[i][j].N_var[N, k] = (sim / N) + k_c_i + k_c_j;

                #Remaining messages
                for m in range(2, N - 1):
                    from_theta_fac[i][j].N_var[m, k] = max((sim / m) + k_c_i + k_c_j, k_c_i + max_c_j, max_c_i + k_c_j,
                                                           max_c_i + max_c_j);

                if normalize == 1:
                    from_theta_fac[i][j].N_var[:, k] = from_theta_fac[i][j].N_var[:, k] - max(
                        from_theta_fac[i][j].N_var[:, k]);
                    from_theta_fac[i][j].N_var[:, k] = (damping_factor * old_msg_n) + (
                        (1 - damping_factor) * from_theta_fac[i][j].N_var[:, k]);

                #For the message from theta_ijk to N_k variable node
                #Need to construct a message of size N+1
                #Need to reference:
                # from_n[k].theta_ij[i,j,:] - message from N_k to theta_ijk
                # one of the two, depending on who the message is being sent to
                # from_c[j].theta_jk[i,k,:] - message from c_j to theta_ij for k
                # OR from_c[i].theta_jk[j,k,:] - message from c_i to theta_ij for k
                mu_n = deepcopy(from_n_var[k].theta_ij_fac[i, j, :]);

                #Messages will be symmetric in nature for c_i and c_j
                #initialize vector of similaritie
                max_N_0N = amax(mu_n[1:N]);
                max_N_NN = amax(mu_n[0:N - 1]);

                #RECHECK
                divisor = cumsum(ones((N - 1, 1))) + 1;
                normalized = similarity[i, j] / divisor;
                max_N_01 = amax(mu_n[2:N + 1] + normalized);

                old_msg_c_i = deepcopy(from_theta_fac[i][j].c_i_var[:, k]);
                old_msg_c_j = deepcopy(from_theta_fac[i][j].c_j_var[:, k]);

                from_theta_fac[i][j].c_i_var[:, k] = max(k_c_j + max_N_0N, max_c_j + max_N_NN);
                from_theta_fac[i][j].c_j_var[:, k] = max(k_c_i + max_N_0N, max_c_i + max_N_NN);

                from_theta_fac[i][j].c_i_var[k, k] = max(k_c_j + max_N_01, max_c_j + max_N_0N);
                from_theta_fac[i][j].c_j_var[k, k] = max(k_c_i + max_N_01, max_c_i + max_N_0N);

                if normalize == 1:
                    from_theta_fac[i][j].c_i_var[:, k] = from_theta_fac[i][j].c_i_var[:, k] - max(
                        from_theta_fac[i][j].c_i_var[:, k]);
                    from_theta_fac[i][j].c_j_var[:, k] = from_theta_fac[i][j].c_j_var[:, k] - max(
                        from_theta_fac[i][j].c_j_var[:, k]);
                    from_theta_fac[i][j].c_i_var[:, k] = (damping_factor * old_msg_c_i) + (
                        (1 - damping_factor) * from_theta_fac[i][j].c_i_var[:, k]);
                    from_theta_fac[i][j].c_j_var[:, k] = (damping_factor * old_msg_c_j) + (
                        (1 - damping_factor) * from_theta_fac[i][j].c_j_var[:, k]);
    return;
