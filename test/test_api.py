import pytest
import requests


@pytest.fixture
def api_base_address():
    return "http://localhost:5000"


@pytest.fixture
def pq_data():
    return [(0, 4), (1, 7)]


@pytest.fixture
def pq_get_data():
    return {"highest": {"index": 1, "key": 7}, "content": [
        {"index": 1, "key": 7}, {"index": 0, "key": 4}
    ]}


@pytest.fixture
def pq_endpoint(api_base_address):
    return f"{api_base_address}/queue"


@pytest.fixture
def pq_index_endpoint(api_base_address):
    return f"{api_base_address}/queue/0"


def test_hello_world(api_base_address):
    res = requests.get(api_base_address)
    assert res.status_code == 200
    data = res.json()
    assert data == "Hello, World"


def test_404_scenarios(pq_endpoint, pq_index_endpoint):

    res = requests.get(pq_endpoint)
    assert res.status_code == 404
    res = requests.delete(pq_endpoint)
    assert res.status_code == 404

    res = requests.get(pq_index_endpoint)
    assert res.status_code == 404
    res = requests.put(pq_index_endpoint, data={"key": "10"})
    assert res.status_code == 404


def test_pq_operations(api_base_address, pq_endpoint, pq_data, pq_get_data):

    # Testint post requests to pq indices
    for index, key in pq_data:
        pq_index_endpoint = f"{api_base_address}/queue/{index}"
        res = requests.post(pq_index_endpoint, data={"key": key})
        assert res.status_code == 201
        assert res.json() == {"index": index, "key": key}

    # Testing get request to pq
    res = requests.get(pq_endpoint)
    assert res.status_code == 200
    assert res.json() == pq_get_data

    # Testing put and get request to pq index
    index, key = 1, 99
    pq_index_endpoint = f"{api_base_address}/queue/{index}"
    res = requests.put(pq_index_endpoint, data={"key": key})
    assert res.status_code == 201
    assert res.json() == {"index": index, "key": key}
    res = requests.get(pq_index_endpoint)
    assert res.status_code == 200
    assert res.json() == {"index": index, "key": key}

    # Testing delete request to pq to get highest priority item
    res = requests.delete(pq_endpoint)
    assert res.status_code == 200
    assert res.json() == {"index": index, "key": key}


