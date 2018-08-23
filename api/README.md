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

## API Authentication

Basic HTTP authorization is currently being used.

[Tutorial Reference](http://polyglot.ninja/securing-rest-apis-basic-http-authentication-python-flask/)
