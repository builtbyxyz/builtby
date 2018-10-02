import json


def load_json(path):
    """Load existing json file for new_projects
    """
    with open(path, 'r') as f:
        new_projects = json.load(f)

    return new_projects


def write_to_json(data, path):
    """Write to list of dictionaries to a JSON file
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
