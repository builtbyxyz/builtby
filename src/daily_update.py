"""Check RSS feed daily and add new projects to database

1. Load existing mongodb.
2. Get last published date.
3. Make request to RSS feed to get list of links.
4. Parse links to check published date.
5. Remove project links that are older than last published .
6. Package approved projects and format as JSON or dict.
7. Add these projects to the database.
"""
import plac
import datetime

from utils.mongo_funcs import load_collection
from utils.date_funcs import get_last_date
from utils.request_funcs import get_rss_items
from utils.soup_funcs import get_specific_elem
from utils.project_funcs import (create_project_obj, package_project,
                                 load_project)


"""
USAGE:
    `python daily_scrape.py`
"""


def get_newly_published_data():
    """
    """
    new_projects_data = load_collection('builtby', 'new_projects',
                                        to_json=True)
    last_run_date = get_last_date(new_projects_data, as_type='datetime')
    print(f"Most recent published date from database: {last_run_date}")
    base_url = "http://www.seattle.gov/DPD/aboutus/news/events/DesignReview/"
    rss_url = "{}upcomingreviews/RSS.aspx".format(base_url)
    project_links = get_rss_items(rss_url)

    print(f"Found {len(project_links)} items.")

    new_proj_idxs = []
    for idx, proj in enumerate(project_links):
        pub_date = get_specific_elem(proj, 'pubdate')
        pub_date_as_dt = datetime.datetime.strptime(pub_date,
                                                    '%m/%d/%Y %H:%M:%S %p')
        if pub_date_as_dt > last_run_date:
            new_proj_idxs.append((idx))

    print(f"Found {len(new_proj_idxs)} newly published items")

    new_pub_projs = [project_links[idx] for idx in new_proj_idxs]
    return new_pub_projs


def project_pipeline(project_object):
    project_object = create_project_obj(project_object)
    project_object = package_project(project_object)
    #   add latlon
    #   parse proposal page
    #   add project image if available
    load_project(project_object)


def main():
    new_pub_projects = get_newly_published_data()
    for proj in new_pub_projects:
        project_pipeline(proj)


if __name__ == "__main__":
    plac.call(main)
