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
3. Run the `api.py`
```bash
python api.py
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
