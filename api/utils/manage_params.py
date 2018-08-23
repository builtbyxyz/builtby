import yaml


def manage_params(args):
    """Adds arguments passed by user to base parameters for use with Socrata
    API

    Arguments:
        args (dict): sparse dict of possible arguments that could be passed

    Returns:
        params (dict): trimmed parameter dict to be passed with GET request
    """
    # Socrata API
    with open("secret/builtby-socrata.yaml", 'r') as f:
        try:
            socrata_api_credentials = yaml.load(f)
        except yaml.YAMLError as exc:
            print(exc)

    socrata_app_token = socrata_api_credentials['app_token']

    # base params
    params = {
        '$$app_token': socrata_app_token
    }
    # remove null attributes
    args = {k: v for k, v in args.items() if v is not None}
    # add args to params
    params.update(args)  # inplace

    return params
