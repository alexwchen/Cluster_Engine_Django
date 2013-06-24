from django.conf.urls import patterns, url

urlpatterns = patterns('engine.views',
    url(r'^$', 'display_cluster_engine'),
    #url(r'^upload/', 'process_upload_file'),
    url(r'^get_parameter_given_algorithm_or_dataset_name/', 'get_parameter_given_algorithm_or_dataset_name'),
    url(r'^get_machine_learning_result_given_algorithm_and_dataset/', 'get_machine_learning_result_given_algorithm_and_dataset'),
    url(r'^user_uploaded_dataset/', 'user_uploaded_dataset'),

    url(r'^list/$', 'list', name='list'),

)
