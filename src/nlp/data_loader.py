import json
import numpy as np


def load_data(path, attr_name, ent_label, qty=None, random=True, include=None):
    """Load data from json file and transform to training data schema
    
    Arguments:
        path (str)
        qty (int): number of orgs to get
        random (bool): randomly select orgs
        include (list): list of words to include

    
    Returns:
        training_data (list of tuples)
    """
    
    training_data = []  # container
    
    with open(path, 'r') as f:
        all_orgs = json.load(f)
    
    if qty is None:  # return all companies
        qty = len(all_orgs)

    if random:
        total_qty = len(all_orgs)
        arr_selection = np.random.choice(total_qty, qty, replace=False)
        select_data = [all_orgs[idx][attr_name] for idx in arr_selection]
    else:  # select from top
        select_data = [org[attr_name] for org in all_orgs[:qty]]
    
    if include is not None:
        assert type(include) is list
        filtered_data = []
        for org_name in select_data:
            for word in org_name.split():
                if word in include:
                    filtered_data.append(org_name)
                    break
    else: filtered_data = select_data

    # Package orgs
    print(f"Packaging {len(filtered_data)} organizations")
    for text in filtered_data:
        # package into schema and load into container
        ent_dict = {'entities': [(0, len(text), ent_label)]}
        training_data.append((text, ent_dict))
        
    return training_data


def load_org_data(path, qty=None, random=True):
    attr_name = 'legal_name'
    training_data = load_data(path, attr_name, "ORG", qty, random, 
        include=["ARCHITECT", "ARCHITECTS", "LLC", "PLLC", "INC", "DESIGN"])
    return training_data


def load_loc_data(path, qty=None, random=True):
    all_attrs = ["address", "city", "state", "zipcode"]

    qtys = [qty // 4, qty // 4, qty // 4, qty - 3 * (qty // 4)]

    training_data = []

    for idx, attr_name in enumerate(all_attrs):
        subset_data = load_data(path, attr_name, "LOC", qtys[idx], random)
        training_data.extend(subset_data)

    return training_data


def augment_org_data(org_name):
    """
    """

    # capitalize name of company
    org_name = reformat_org_name(org_name)

    aug_data = []  

    aug_text = [
        f"The architect who designed this building was {org_name}.",
        f"{org_name} was the architect",
        f"{org_name} designed this building",
        f"The architect, {org_name}, designed this building",
        f"Architect: {org_name}",
        f"Engineer: {org_name}",
        f"Developer: {org_name}",
        f"Owner: {org_name}"
    ]

    for text in aug_text:
        begin = text.find(org_name)
        last = begin + len(org_name) - 1
        ent_dict = {'entities': [(begin, last, 'ORG')]}
        aug_data.append((text, ent_dict))

    # text = f'The architect who designed this building was {org_name}.'
    # begin = text.find(org_name)
    # last = B + len(org_name)
    # ent_dict = {'entities': [begin, last, ent_label)]}
    # aug_data.append((text, ent_dict))

    # text = f'{org_name} was the architect'
    # begin = text.find(org_name)
    # last = B + len(org_name)
    # ent_dict = {'entities': [(begin, last, ent_label)]}
    # aug_data.append((text, ent_dict))

    # text = f'{org_name} designed this building'
    # begin = text.find(org_name)
    # last = B + len(org_name)
    # ent_dict = {'entities': [(begin, last, ent_label)]}
    # aug_data.append((text, ent_dict))

    # text = f'The architect, {org_name}, designed this building'
    # begin = text.find(org_name)
    # last = B + len(org_name)
    # ent_dict = {'entities': [(begin, last, ent_label)]}
    # aug_data.append((text, ent_dict))

    print(f"Added {len(aug_data)} augmented data items.")
    return aug_data


def augment_org_w_loc(org_name, loc):
    """
    """

    # capitalize name of company
    org_name = reformat_org_name(org_name)

    aug_data = []  

    aug_text = [
        f'{org_name} designed the building located in {loc}',
        f'The building at {loc} was designed by {org_name}'
    ]

    for text in aug_text:

        entities = []
        for ent_obj, ent_label in [(org_name, 'ORG'), (loc, 'LOC')]:
            begin = text.find(ent_obj)
            last = begin + len(ent_obj) - 1
            ent = (begin, last, ent_label)
            entities.append(ent)
        ent_dict = {'entities': entities}
        aug_data.append((text, ent_dict))

    print(f"Added {len(aug_data)} augmented data items.")
    return aug_data


def reformat_org_name(org_name):
    # capitalize name of company
    reformat_name = []
    for word in org_name.split():
        if word not in ['LLC', 'PLLC']:
            reformat_name.append(word.capitalize())
        else:
            reformat_name.append(word)

    formatted = " ".join(reformat_name)
    # print(f"Changed {org_name} to {formatted} for augmented data.")
    return formatted