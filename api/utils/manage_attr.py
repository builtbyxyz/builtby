"""
Convert attribute names to be more standardized across different sources

latitude -> latitude
longitude -> longitude
description -> description

link -> design_review_link -> primary_link
issueddate -> published_date
originaladdress1 -> address
permitnum -> project_num
permitclass at originaladdress -> title
"""


def convert_attr(project):
    conversions = {
        'link': 'design_review_link',  # convert to primary_link later
        'issueddate': 'published_date',
        'originaladdress1': 'address',
        'originaladdress': 'address',
        'permitnum': 'project_num'
    }

    for attr in conversions.keys():
        if attr in project:
            project[conversions[attr]] = project[attr]
            del project[attr]

    if 'title' not in project:
        permitclass = project['permitclass']
        if 'address' in project.keys():
            address = project['address']
            project['title'] = f"{permitclass} Permit at {address}"
        # if 'originaladdress1' in project.keys():
        #     address = project['originaladdress1']
        #     project['title'] = f"{permitclass} at {address}"
        # elif 'location_1_address' in project.keys():
        #     address = project['location_1_address']
        #     project['title'] = f"{permitclass} at {address}"
        else:
            project['title'] = f"{permitclass} Permit"

    return project


def attr_conversion_pipeline(data):
    transformed_data = []
    for project in data:
        transformed_project = convert_attr(project)
        transformed_data.append(transformed_project)

    return transformed_data
