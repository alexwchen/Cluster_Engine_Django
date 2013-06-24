from django.http import HttpResponse
from django.shortcuts import render_to_response
from engine.models import list_object
from engine.models import object_object
from engine.models import parameter_object


from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from engine.models import Document
from engine.forms import DocumentForm


import database_manager
import algorithm_manager
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django import forms

from django.utils import simplejson
from engine.forms import DocumentForm
import datetime
import scipy
import sklearn
from numpy import *
import os


###########################################
#   Debugging use
#
###########################################

def list(request):

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('engine.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form

    return render_to_response(
        'engine/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )




def display_cluster_engine(request):

    algorithms, datasets = database_manager.retrieve_interface_data()
    upload_file_name = ""

	# Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            # remove whatever is in there
            now = datetime.datetime.now()
            if now.month < 10:
                mth = str(0)+str(now.month)
            else:
                mth = str(now.month)

            if now.day < 10:
                day = str(0)+str(now.day)
            else:
                day = str(now.day)

            path = '/static_media_clustapp/documents/'+str(now.year)+'/'+mth+'/'+day+'/'
            full_path = os.path.realpath('.')
            os.system('rm '+full_path+path+'*')


            # store uploaded file
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            upload_file_name = request.FILES['docfile']

            # debugging use, output the newest file uploaded
            print 'Newest File Uploaded'
            os.system('ls '+full_path+path)



            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('engine.views.display_cluster_engine'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'engine/engine_interface.html',
        {
            'documents': documents,
            'form': form,
            'algorithms':algorithms,
            'datasets': datasets,
            'upload':upload_file_name,

        },
        context_instance=RequestContext(request)
    )

    """
    algorithms, datasets = database_manager.retrieve_interface_data()

    return render_to_response(
            'engine/engine_interface.html',
            {
                'algorithms':algorithms,
                'datasets': datasets,
            }
    )
    """


def get_parameter_given_algorithm_or_dataset_name(request):
    name = request.GET['algo']
    param_dict = {}
    parameters = database_manager.retrieve_algorithm_parameter_given_algo_or_data_name(name)
    json_return = simplejson.dumps(parameters)

    return HttpResponse(json_return)

def user_uploaded_dataset(request):

    algo_name = request.GET['algo']
    data_name = request.GET['data']
    algo_para = request.GET['algo_para'].split(',')

    # get data path and load data
    now = datetime.datetime.now()
    if now.month < 10:
        mth = str(0)+str(now.month)
    else:
        mth = str(now.month)

    if now.day < 10:
        day = str(0)+str(now.day)
    else:
        day = str(now.day)

    path = '/static_media_clustapp/documents/'+str(now.year)+'/'+mth+'/'+day+'/'
    full_path = os.path.realpath('.')
    file_name = full_path+path+data_name
    data_file = scipy.io.loadmat(file_name)

    input_data = data_file['X']
    #correct_label = data_file['y']

    # Calling Algorithms
    clustered_label = {}
    unique_label = {}

    # Calling Algorithms
    if algo_name=="MiniBatchKMeans":
        print 'MiniBatchKMeans'
        n_clust = int(algo_para[0])
        kmean_label = algorithm_manager.call_kmean(n_clust, input_data, True)
        clustered_label = kmean_label

    elif algo_name=="Spectral Clustering":
        print "Spectral Clustering"
        n_clust = int(algo_para[0])
        spectral_label = algorithm_manager.call_spectral(n_clust, 'arpack', input_data, True)
        clustered_label = spectral_label

    elif algo_name=="Affinity Propagation":
        print "Affinity Propagation"
        max_iter_ = int(algo_para[0])
        con_iter = int(algo_para[1])
        affinity_label = algorithm_manager.call_affinity(max_iter_, con_iter, input_data, True)
        clustered_label = affinity_label

    elif algo_name=="Greedy":
        print "Greedy"
        n_clust = int(algo_para[0])
        greedy_label = algorithm_manager.call_greedy(n_clust, input_data, True)
        clustered_label = greedy_label

    elif algo_name=="Message Passing":
        print "Message Passing"
        n_clust = int(algo_para[0])
        mp_label = algorithm_manager.call_mp(n_clust, input_data, True)
        clustered_label = mp_label

    # saving the result in the correct directory
    output_data = {}
    output_data ['y'] = clustered_label
    out_file_name = full_path+path+data_name[:-4] + '_result.mat'
    print output_data
    print out_file_name
    print out_file_name
    print output_data
    data_file = scipy.io.savemat(out_file_name, output_data)

    # return the path
    return_file_name = path+data_name[:-4]  + '_result.mat'
    return HttpResponse(return_file_name)

def get_machine_learning_result_given_algorithm_and_dataset(request):
    algo_name = request.GET['algo']
    data_name = request.GET['data']
    algo_para = request.GET['algo_para'].split(',')
    data_para = request.GET['data_para'].split(',')
    #paras = request.GET['paras']

    print "algo_name: ", algo_name
    print "data_name: ", data_name
    print "algo_para: ", algo_para
    print "data_para: ", data_para

    #print "paras: ", paras


    data_dict = {}
    input_data = None
    n_samples = 1500

    # Generateing Sample Data Algorithm
    from sklearn import cluster, datasets
    if data_name=="Sample Blob":
        n_samp = int(data_para[0])
        ran_st = int(data_para[1])
        blob_dict, X, y = algorithm_manager.generate_blob_sample(n_samp, ran_st)
        data_dict = blob_dict
        input_data = X

    elif data_name=="Sample Circle":
        factor_= float(data_para[0])
        n_samp = int(data_para[1])

        circle_dict,X,y = algorithm_manager.generate_circle_sample(n_samp, factor_)
        data_dict = circle_dict
        input_data = X

    elif data_name=="Sample Moon":
        n_samp = int(data_para[0])
        moon_dict,X,y = algorithm_manager.generate_moon_sample(n_samp)
        data_dict = moon_dict
        input_data = X

    elif data_name=="Breast Cancer":
        # load from text file
        print "in b cancer "
        #os.system('ls '+full_path+path)
        X = loadtxt( os.path.abspath(os.path.dirname(__file__)) + '/bcancer.txt')
        print X
        data_dict = [(0,0)]
        input_data = X


    clustered_label = {}
    unique_label = {}

    # Calling Algorithms
    if algo_name=="MiniBatchKMeans":
        print 'MiniBatchKMeans'
        n_clust = int(algo_para[0])
        kmean_label, unique_label = algorithm_manager.call_kmean(n_clust, input_data, False)
        clustered_label = kmean_label

    elif algo_name=="Spectral Clustering":
        print "Spectral Clustering"
        n_clust = int(algo_para[0])
        spectral_label, unique_label = algorithm_manager.call_spectral(n_clust, 'arpack', input_data, False)
        clustered_label = spectral_label

    elif algo_name=="Affinity Propagation":
        print "Affinity Propagation"
        max_iter_ = int(algo_para[0])
        con_iter = int(algo_para[1])
        affinity_label, unique_label = algorithm_manager.call_affinity(max_iter_, con_iter, input_data, False)
        clustered_label = affinity_label

    elif algo_name=="Greedy":
        print "Greedy"
        n_clust = int(algo_para[0])
        greedy_label, unique_label = algorithm_manager.call_greedy(n_clust, input_data, False)
        clustered_label = greedy_label

    elif algo_name=="Message Passing":
        print "Message Passing"
        n_clust = int(algo_para[0])
        mp_label, unique_label = algorithm_manager.call_mp(n_clust, input_data, False)
        clustered_label = mp_label

    # main return dictionary contain dictionary about everything
    return_dict = {}
    return_dict['original_data_points'] = data_dict
    return_dict['clustered_data_label'] = clustered_label
    return_dict['clustered_data_unique_label'] = unique_label
    json_return = simplejson.dumps(return_dict)


    return HttpResponse(json_return)
