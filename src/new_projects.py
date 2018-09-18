import datetime
import requests
from bs4 import BeautifulSoup

import json
import plac

from utils.geo import get_latlon
from utils.pdf import download_and_convert_pdf


def get_rss_items(rss_url):
    """Returns the HTML elements in the RSS feed
    """
    response = requests.get(rss_url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    # each item is a different permit
    items = soup.select('item')
    return items


def create_project_obj(elem):
    """Creates a project JSON object when given an HTML element
    Arguments:
        elem (html element)
    Returns:
        project (dict)
    """
    # get todays date in MM/DD/YYYY format as string
    today = datetime.datetime.now().strftime('%m/%d/%Y')

    project = {}  # create empty dictionary
    link = elem.select_one('link').text.strip()
    published_date = elem.select_one('pubdate').text.split()[0]
    title = elem.select_one('title').text.strip()
    project_review_date = title.split(' - ')[0]
    review_desc = elem.select_one('description').text.strip()

    # parse review_desc
    review_board = review_desc.split(' - ')[0]
    meeting_details = review_desc.split(' - ')[1]

    # build project dict
    project = {
        'title': title,
        'published_date': published_date,
        'project_review_date': project_review_date,
        'design_review_link': link,
        'review_board': review_board,
        'meeting_details': meeting_details,
        'found_date': today
    }

    return project


def add_lat_lon(project):
    """Uses Google Map's API to get the latitude and longitude values
    """
    project_address = project['address']
    print(f"Getting latitude and longitude for {project_address} ...")

    if 'latitude' not in project.keys():
        full_address = project['address'] + ' Seattle, WA'
        lat, lon = get_latlon(full_address)

        project['latitude'] = lat
        project['longitude'] = lon
    return project


def parse_propasal_page(project):
    """Parses the content specific to each project
    """
    project_name = project['title']
    print(f"Parsing design proposal info for {project_name} ...")

    url = project['design_review_link']
    baseurl = url.split('/Detail')[0]
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.content
        soup = BeautifulSoup(html, 'html.parser')
        description = soup.select_one(
            'div#dvDataFound p span#lblDescription').text
        address = soup.select_one('span#lblAddress').text

        # check for design proposal and report PDFs
        design_proposal = soup.select_one('a#hypProposal')
        if design_proposal is not None:
            design_proposal_link = design_proposal['href']
            project['design_proposal_link'] = design_proposal_link

        report = soup.select_one('a#hypProposal')
        if report is not None:
            report_link = report['href']
            project['report_link'] = report_link

        # check for past reviews
        past_reviews = soup.select_one('a#hypPastReviews')
        if past_reviews is not None:
            past_reviews_link = baseurl + past_reviews['href'].lstrip('..')
            project['past_reviews_link'] = past_reviews_link

        project_num = soup.select_one('div span#lblProject').text
        project['address'] = address
        project['description'] = description
        project['project_num'] = project_num

    return project


def create_new_projects():
    """Creates a JSON file in the data dir with the upcoming design review
    meetings
    """
    base_url = "http://www.seattle.gov/DPD/aboutus/news/events/DesignReview/"
    rss_url = "{}upcomingreviews/RSS.aspx".format(base_url)

    # get rss html items
    items = get_rss_items(rss_url)

    upcoming_projects = []  # container for list of dictionaries
    # create project objects
    for item in items:
        project = create_project_obj(item)
        upcoming_projects.append(project)

    # print to console the number of projects found
    num_projects = len(upcoming_projects)
    print(f"Found {num_projects} project(s).")

    # add design proposal information to project object
    for project in upcoming_projects:
        project = parse_propasal_page(project)

    # add latitude and longitude data to project object
    for project in upcoming_projects:
        project = add_lat_lon(project)

    return upcoming_projects


def update_new_projects(path_to_exist):
    """Adds new items to an existing JSON file
    """
    base_url = "http://www.seattle.gov/DPD/aboutus/news/events/DesignReview/"
    rss_url = "{}upcomingreviews/RSS.aspx".format(base_url)

    # get rss html items
    items = get_rss_items(rss_url)

    with open(path_to_exist, 'r') as f:
        new_projects = json.load(f)

    last_pub_date = new_projects['meta']['last_pub_date']

    newly_published_projects = []  # container for list of dictionaries

    # create project objects
    for item in items:
        project = create_project_obj(item)
        if project['published_date'] > last_pub_date:
            newly_published_projects.append(project)

    # print to console the number of projects found
    num_projects = len(newly_published_projects)
    print(f"Found {num_projects} project(s).")

    # add design proposal information to project object
    for project in newly_published_projects:
        project = parse_propasal_page(project)

    # add latitude and longitude data to project object
    for project in newly_published_projects:
        project = add_lat_lon(project)

    combined = new_projects['data']
    combined.extend(newly_published_projects)
    return combined


def get_last_date(data, k='published_date'):
    """Extracts the date field for each item in the dict and returns the most
    recent date.
    """
    dates = []
    for item in data:
        date_item = datetime.datetime.strptime(item[k], '%m/%d/%Y')
        dates.append(date_item)
    last_date = max(dates)
    return last_date.strftime('%m/%d/%Y')


def package_data(projects_list, path):
    """Creates meta data object and saves the new projects under the 'data' key
    """
    last_run_date = datetime.datetime.now().strftime('%m/%d/%Y')
    last_pub_date = get_last_date(projects_list, k='published_date')

    new_projects_db = {}
    new_projects_db['meta'] = {
        'last_pub_date': last_pub_date,
        'last_run_date': last_run_date}

    new_projects_db['data'] = projects_list

    with open(path, 'w') as f:
        json.dump(new_projects_db, f, indent=4)


def resolve_geo_attr(path):
    with open(path, 'r') as f:
        new_projects = json.load(f)

    projects = new_projects['data']

    for project in projects:
        if project['latitude'] is None:
            full_address = project['address'] + ' Seattle, WA'
            print(f"Attempting to retrieve lat and lon for {full_address}")
            lat, lon = get_latlon(full_address)

            project['latitude'] = lat
            project['longitude'] = lon

    return projects


def get_project_image(path):
    with open(path, 'r') as f:
        new_projects = json.load(f)

    projects = new_projects['data']

    for project in projects:
        dp_pdf_link = project['design_proposal_link']
        project_address = project['address']
        if dp_pdf_link is not None:
            if 'dpimage_url' not in project.keys():
                if dp_pdf_link.split('.')[-1] is 'pdf':
                    try:
                        print(f"Obtaining image for {project_address}")
                        png_fname = download_and_convert_pdf(dp_pdf_link)

                        s3_url = "https://s3-us-west-2.amazonaws.com/builtby/"

                        project['dpimage_url'] = s3_url + png_fname
                    except Exception as exc:
                        print(f"Encountered error with {project_address}")
                        print(exc)
    return projects


@plac.annotations(
    path=("Path for new JSON file", "positional"),
    new=("Create new JSON file; provide path to existing file", "flag", "n"),
    update=("Update an existing JSON file; provide path to existing file",
            "flag", "u"),
    resolve_geo=("Add lat lon info to projects where missing", "flag", None),
    get_images=("Get image from design proposal cover", "flag", None))
def main(path, new=False, update=False, resolve_geo=False, get_images=False):
    """Creates or updates a JSON file with projects from an RSS feed."""
    if new:  # if new JSON file
        new_projects = create_new_projects()
        package_data(new_projects, path)
    if update:
        new_projects = update_new_projects(path)
        package_data(new_projects, path)
    if resolve_geo:
        projects = resolve_geo_attr(path)
        package_data(projects, path)
    if get_images:
        projects = get_project_image(path)
        package_data(projects, path)


if __name__ == "__main__":
    plac.call(main)
