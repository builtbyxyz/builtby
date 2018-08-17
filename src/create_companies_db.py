"""
FIELDS OF INTEREST
------------------
business_lic_num
legal_name
trade_name
address
city
state
zip
NAICS_id
NAICS_name
business_lic_renewal_date
phone
"""
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
import csv


def read_html(path):
    with open(path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    tr_list = soup.select('tr')
    return tr_list


def get_part_one(tr):
    divs = tr.select('div')
    span_list = divs[0].select('span')
    if len(span_list) > 0:
        return [elem.text for elem in span_list]
    else:
        return None


def get_part_two(tr):
    divs = tr.select('div')
    link = divs[0].select_one('a')
    text = link.text
    text_list = text.split(',')
    num = text_list[0]
    name = text_list[1].strip()
    if link is not None:
        return num, name
    else:
        return None


def get_part_three(tr):
    divs = tr.select('div')
    span = divs[1].select('span')
    if len(span) > 0:
        span_list = span[0].text.split('\xa0')
        return span_list
    else:
        return None


def get_city_state_zip(tr):
    part_one = get_part_one(tr)
    city_state_zip = part_one[4]
    return city_state_zip


def parse_companies_html(tr, service_type=None):
    obj = {}
    obj['service_type'] = service_type

    part_one = get_part_one(tr)
    part_two = get_part_two(tr)
    part_three = get_part_three(tr)

    if part_one is not None:
        business_lic_num = part_one[0]
        legal_name = part_one[1]
        trade_name = part_one[2]
        address = part_one[3]

    city_state_zip = get_city_state_zip(tr).split()
    # if not in Canada
    if 'BC' not in city_state_zip:
        zipcode = city_state_zip[-1]
        state = city_state_zip[-2]
        city = " ".join(city_state_zip[:-2])
        city = city.rstrip(",")
    else:  # if in Canada
        city = city_state_zip[0]
        state = city_state_zip[1]
        zipcode = city_state_zip[2:]

    if part_two is not None:
        NAICS_id, NAICS_name = part_two

    if part_three is not None:
        business_lic_renewal_date = part_three[-4]
        phone = part_three[-1]

    attr_list = ['business_lic_num',
                 'legal_name',
                 'trade_name',
                 'address',
                 'city',
                 'state',
                 'zipcode',
                 'business_lic_renewal_date',
                 'phone',
                 'NAICS_id',
                 'NAICS_name']

    for attr in attr_list:
        try:
            obj[attr] = eval(attr)
        except(NameError):
            pass

    return obj


def build_data_dict(tr_list, service_type=None):
    data = []
    for tr in tr_list:
        data.append(parse_companies_html(tr, service_type))

    return data


def write_to_json(path, data):
    with open(path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)


def write_to_mongodb(dbname, coll, data, delete_existing=True):
    mc = MongoClient('localhost', 27017)
    db = mc[dbname]
    if delete_existing:
        db.drop_collection(coll)
    collection = db[coll]
    collection.insert_many(data)


if __name__ == "__main__":
    with open('../src/company_fnames.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        rows = [row for row in csvreader]
        fname_dict = {}
        for row in rows:
            fname_dict[row[0].split('.')[0]] = row[1]

    for idx, name in enumerate(fname_dict.keys()):
        tr_list = read_html(f'../private_data/seattle/{name}.html')
        data = build_data_dict(tr_list, fname_dict[name])

        write_to_json(path=f'../private_data/seattle/json/{name}.json',
                      data=data)
        write_to_mongodb('builtby', 'companies_20180816', data,
                         delete_existing=(idx == 0))
