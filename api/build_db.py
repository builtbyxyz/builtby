"""
"""
import pymongo
# import sys
import pandas as pd


def build_db():
    mc = pymongo.MongoClient()

    # seattle_land is the database name
    db = mc['seattle_land']

    # land_use is the collection for raw data
    coll = db['land_use']

    # convert collection to pandas dataframe
    df = pd.DataFrame(list(coll.find()))

    commercial = df[df['permitclass'] == 'Commercial']

    # drop existing collection of the same name if exists
    if 'commercial' in db.collection_names():
        db.drop_collection('commercial')

    # create new collection
    comm_coll = db['commercial']

    for idx, row in commercial.iterrows():
        row_dict = {}

        row_dict['applied_date'] = row['applieddate']
        row_dict['expires_date'] = row['expiresdate']
        row_dict['issued_date'] = row['issueddate']

        row_dict['description'] = row['description']
        row_dict['est_cost'] = float(row['estprojectcost'])

        row_dict['longitude'] = row['longitude']
        row_dict['latitude'] = row['latitude']
        row_dict['address'] = row['location_1_address']
        row_dict['city'] = row['location_1_city']
        row_dict['state'] = row['location_1_state']
        if float(row['location_1_zip']) > 0:
            row_dict['zip'] = int(row['location_1_zip'])
        else:
            row_dict['zip'] = 0

        row_dict['link'] = row['link']

        row_dict['permit_num'] = row['permitnum']
        row_dict['permit_num_digits'] = int(row['permitnum'].split('-')[0])
        row_dict['permit_num_alpha'] = row['permitnum'].split('-')[1]
        row_dict['permit_class'] = row['permitclass']
        row_dict['permit_class_mapped'] = row['permitclassmapped']

        row_dict['contractor'] = row['contractorcompanyname']

        row_dict['status_current'] = row['statuscurrent']

        comm_coll.insert_one(row_dict)


if __name__ == '__main__':
    build_db()
