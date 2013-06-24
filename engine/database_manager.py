from engine.models import list_object 
from engine.models import object_object 
from engine.models import parameter_object 

def retrieve_interface_data():
    m_list = list_object.objects.get(title='algorithm_list')
    algorithms = object_object.objects.filter(master_list=m_list)
    
    m_list = list_object.objects.get(title='dataset_list')
    datasets = object_object.objects.filter(master_list=m_list)

    return algorithms, datasets

def retrieve_algorithm_parameter_given_algo_or_data_name(name):
    para_dict = {}
    obj = object_object.objects.get(title=name)
    obj_params = parameter_object.objects.filter(master_object=obj)

    for para in obj_params:
        para_dict[para.title] = para.default
    
    return para_dict
