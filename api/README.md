# REST API
The data collected can be queried by running this API.
___

## Usage
1. Clone this repo.
```bash
git clone https://github.com/mnguyenngo/builtby.git
```
2. Go to `rest-api` directory.
```bash
cd builtby/rest-api
```
3. Build the [virtual environment](https://virtualenv.pypa.io/en/stable/)
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
4. Run the `api.py`
```bash
python api.py
```
5. Deactivate virtual environment
```bash
deactivate
```

## Querying from the API
In new terminal window:
```bash
curl http://localhost:5000/
# Warning: there are over 3500 documents
```

With Python:
```python
requests.get('http://localhost:5000/').json()
```


#### Supported Arguments
The following examples can be passed as part of the parameters of a GET request:

example | description
--- | ---
'$q': 'northshore' | general search; searches all fields for the word `northshore`; not case-sensitive
$limit': 50  | limit the output to 50 objects
'permitclass': 'Multifamily' | only return objects with a `permitclass` attribute equal to `Multifamily`
'$where': ('estprojectcost > 5000000') | return objects where `estprojectcost` is greater than 5000000

#### Endpoints

description | route
--- | ---
Permit_LandUse |  `/permits/landuse`
Permit_Building |  `/permits/building`
Permit_Electrical |  `/permits/electrical`
Permit_Trade |  `/permits/trade`
NewProjectsList |  `/new`
Companies |  `/companies`


## API Authentication

Basic HTTP authorization was implemented but is not turned on.

[Tutorial Reference](http://polyglot.ninja/securing-rest-apis-basic-http-authentication-python-flask/)
