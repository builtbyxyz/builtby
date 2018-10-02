import plac

from utils.mongo_funcs import (load_collection, write_collection,
                               delete_collection)
# from utils.date_funcs import get_last_date
from utils.request_funcs import get_rss_items
from utils.json_funcs import load_json, write_to_json
from utils.project_funcs import (create_project_obj, package_project,
                                 save_project, resolve_geo_attr_mongo)


def create_new_projects_db(dbname='builtby', coll='new_projects',
                           overwrite=False):
    """Creates a new collection and loads the collection with projects

    Returns:
        None
    """
    if overwrite:
        delete_collection(dbname, coll)

    base_url = "http://www.seattle.gov/DPD/aboutus/news/events/DesignReview/"
    rss_url = "{}upcomingreviews/RSS.aspx".format(base_url)

    # get rss html items
    items = get_rss_items(rss_url)
    print(f"Found {len(items)} items.")

    # upcoming_projects = []  # container for list of dictionaries
    # create project objects
    for item in items:
        project = create_project_obj(item)
        document = package_project(project)  # send project through pipeline
        save_project(document)


@plac.annotations(
    new=("Create new collection", "flag", "n"),
    overwrite=("Overwrite the existing collection", "flag", "o"),
    to_json=("Convert mongo collection to json", "flag", None),
    to_mongo=("Convert json to mongo", "option", None),
    resolve_geo=("Resolve missing lat and lon info", "flag", None)
    )
def main(new=False, overwrite=False, to_json=False, to_mongo=None,
         resolve_geo=False):
    """Creates or updates a JSON file with projects from an RSS feed."""
    if new:
        create_new_projects_db(dbname='builtby', coll='new_projects',
                               overwrite=overwrite)
    elif to_json:
        projects = load_collection(dbname='builtby', coll='new_projects',
                                   to_json=to_json)
        for project in projects:
            if '_id' in project:
                del project['_id']
        path = "../data/new_projects_1.json"
        write_to_json(projects, path)
    elif to_mongo is not None:  # convert json file at path to mongo
        path = to_mongo
        projects = load_json(path)
        write_collection(dbname='builtby', coll='new_projects', data=projects,
                         delete_existing=True)
    elif resolve_geo:
        projects = load_collection(dbname='builtby', coll='new_projects')
        resolve_geo_attr_mongo(projects)
    else:
        print("Hello world!")


if __name__ == "__main__":
    plac.call(main)
