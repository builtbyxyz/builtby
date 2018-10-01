from bs4 import BeautifulSoup


def get_specific_elem(html, elem_name):
    """
    """
    content = html.select_one(elem_name).text
    # return content without extra whitespace on each side
    return content.strip()
