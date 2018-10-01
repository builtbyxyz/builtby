import requests
from bs4 import BeautifulSoup


def get_rss_items(rss_url):
    """Returns the HTML elements in the RSS feed

    Arguments:
        rss_url (str): URL to RSS feed

    Returns:
        items (list of div elements)
    """
    response = requests.get(rss_url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('item')  # each item is a different permit
    return items
