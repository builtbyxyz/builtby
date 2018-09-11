import json
import numpy as np


def load_org_data(path, num_orgs=None, random=True):
    """Load data from json file and transform to training data schema
    
    Arguments:
        path (str)
        num_orgs (int): number of organizations to get
    
    Returns:
        training_data (list of tuples)
    """
    
    training_data = []  # container
    
    with open(path, 'r') as f:
        all_orgs = json.load(f)
    
    if num_orgs is None:  # return all companies
        num_orgs = len(all_orgs)
    
    if random:
        total_num_orgs = len(all_orgs)
        arr_selection = np.random.choice(total_num_orgs, num_orgs, replace=False)
        select_orgs = [all_orgs[idx]['legal_name'] for idx in arr_selection]
    else:  # select from top
        select_orgs = all_orgs[:num_orgs]
    
    for org in select_orgs:
        # package into schema and load into container
        ent_dict = {'entities': [(0, len(org), 'ORG')]}
        training_data.append((org, ent_dict))
        
    return training_data