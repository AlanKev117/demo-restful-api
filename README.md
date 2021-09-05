# demo-restful-api

A simple two-endpoint RESTful API to apply to Wizeline's Golang Bootcamp

---

## How it works

The root endpoint `/` simply allows GET requests, so it returns the string `Hello, World`.

The second endpoint of the API, `/queue`, consists of an implementation 
of a max priority queue that can be consulted and altered 
via HTTP requests as shown below:

|Description| Endpoint  | Method  | Data  | JSON Response  |
|---|---|---|---|---|
|Retrieves the content of the PQ and highlights the item with highest priority|  http://localhost:5000/queue |  GET | -  | `{"highest": {"index": int, "key": int}, "content": [{"index": int, "key": int}, ...]}`  |
|Pops out the highest priority item from PQ |  http://localhost:5000/queue |  DELETE | -  |  `{"index": int, "key": int}` |
|Retrieves the key stored at `:index` in the PQ| http://localhost:5000/queue/:index  |  GET | -  |  `{"index": int, "key": int}` |
|Stores a key into `:index` in the PQ| http://localhost:5000/queue/:index  | POST  | `key:int`  |  `{"index": int, "key": int}` |
|Alters a key stored at `:index` in the PQ| http://localhost:5000/queue/:index  |  PUT | `key:int`  |  `{"index": int, "key": int}` |

## Requirements

This API runs on Python 3.7 given that it needs `flask-restful` to operate. Make sure to
have this version installed.

## Instalation

It is recommended to create a virtual environment for this project's dependencies not to
interfere with global ones:

```bash
# Creates virtual env
python3.7 -m venv env
# Activates enviroment
source env/bin/activate
```

Next, install dependencies:

```bash
pip install -r requirements.txt
```

Then, run the API:

```bash
python3.7 src/api.py
```

To run the tests, run the following commands:

```bash
# Unit test for Priority Queue
pytest test/test_pq.py
# Unit test for API
pytest test/test_api.py
```

Make sure to disable the virtual environment once you finish playing around with the API

```bash
deactivate
```
