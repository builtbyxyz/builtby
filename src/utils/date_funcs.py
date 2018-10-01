import datetime


def get_last_date(data, k='published_date', as_type='string'):
    """Extracts the date field for each item in a dict and returns the most
    recent date.

    Arguments:
        data (list of dict or JSON)
        k (str): name of key to check, default 'published_date'
    Return:
        last_date (str): format MM/DD/YYYY
    """
    assert as_type in ['string', 'datetime']
    dates = []
    for item in data:
        date_item = datetime.datetime.strptime(item[k], '%m/%d/%Y')
        dates.append(date_item)
    last_date = max(dates)
    if as_type == 'string':
        return last_date.strftime('%m/%d/%Y')
    elif as_type == 'datetime':
        return last_date
    else:
        print("'as_type' should be either 'string' or 'datetime'.")
        raise
