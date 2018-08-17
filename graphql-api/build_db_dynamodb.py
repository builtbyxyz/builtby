"""
"""
import pymongo
import pandas as pd
import boto3
from decimal import Decimal


def build_db():
    mc = pymongo.MongoClient()

    # seattle_land is the database name
    db = mc['seattle_land']

    # land_use is the collection for raw data
    coll = db['land_use']

    # convert collection to pandas dataframe
    df = pd.DataFrame(list(coll.find()))
    commercial = df[df['permitclass'] == 'Commercial']

    dynamodb = boto3.resource('dynamodb')

    # delete existing table
    table = dynamodb.Table('builtby_commercial')
    print(table.item_count)
    if table.item_count > 0:
        table.delete()

    # create new dynamo table
    table = dynamodb.create_table(
        TableName='builtby_commercial',
        KeySchema=[
            {
                'AttributeName': 'permit_num',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'permit_num_alpha',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'permit_num',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'permit_num_alpha',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # create empty container for data
    data = []
    for idx, row in commercial.iterrows():
        row_dict = {}

        row_dict['applied_date'] = row['applieddate']
        row_dict['expires_date'] = row['expiresdate']
        row_dict['issued_date'] = row['issueddate']

        row_dict['description'] = row['description']
        row_dict['est_cost'] = Decimal(row['estprojectcost'])

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

        data.append(row_dict)

    with table.batch_writer() as batch:
        for item in data:
            batch.put_item(
                Item=item
            )


if __name__ == '__main__':
    build_db()
