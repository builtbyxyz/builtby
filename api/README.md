# API Documentation

## Startup
1. Clone the repo
2. Go to builtby/api/ directory and activate the virtual environment
```bash
source env/bin/activate
```
3. Run the app
```bash
python app.py
```
3. To deactivate the virtual environment
```bash
deactivate env
```


## Example Query
After running `python app.py` and navigating to `http://127.0.0.1:5000/graphql`, you can run the following query:
```
{
  permits {
    id
    permitnum
    permitclass
    location1 {
      coordinates
    }
  }
}
```
The above query returns data in the following format:
```
{
  "data": {
    "permits": [
      {
        "id": "UGVybWl0OjViNWE0YzNkZWQ0ZjFmMWU1NGEyYjU2Mg==",
        "permitnum": "3031038-LU",
        "permitclass": "Commercial",
        "location1": {
          "coordinates": "[-122.34715996, 47.73307912]"
        }
      },
      {
        "id": "UGVybWl0OjViNWE0YzNkZWQ0ZjFmMWU1NGEyYjU2Mw==",
        "permitnum": "3032223-LU",
        "permitclass": "Multifamily",
        "location1": {
          "coordinates": "[-122.31719727, 47.70999978]"
        }
      },
      {
        "id": "UGVybWl0OjViNWE0YzNkZWQ0ZjFmMWU1NGEyYjU2NA==",
        "permitnum": "3032295-EG",
        "permitclass": "Commercial",
        "location1": {
          "coordinates": "[-122.3017157, 47.61359969]"
        }
      },

      ...

    }
  }
}
```
