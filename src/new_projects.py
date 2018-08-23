import datetime
import requests
from bs4 import BeautifulSoup
from utils import get_latlon
import json


def build_new_projects():
    """Creates a JSON file in the data dir with the upcoming design review
    meetings
    """
    today = datetime.datetime.now().strftime('%m/%d/%Y')

    rss_url = 'http://www.seattle.gov/DPD/aboutus/news/events/DesignReview/upcomingreviews/RSS.aspx'
    response = requests.get(rss_url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('item')

    upcoming_projects = []  # container for list of dictionaries

    for item in items:
        project = {}
        link = item.select_one('link').text.strip()
        published_date = item.select_one('pubdate').text.split()[0]
        title = item.select_one('title').text.strip()
        project_review_date = title.split(' - ')[0]
        review_desc = item.select_one('description').text.strip()

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
        upcoming_projects.append(project)

    for project in upcoming_projects:
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

    for project in upcoming_projects:
        if 'latitude' not in project.keys():
            full_address = project['address'] + ' Seattle, WA'
            lat, lon = get_latlon(full_address)
        project['latitude'] = lat
        project['longitude'] = lon

    return upcoming_projects


if __name__ == "__main__":
    new_projects = build_new_projects()

    with open('../data/new_projects.json', 'w') as f:
        js = json.dumps(new_projects)
        f.write(js)
