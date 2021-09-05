import pytest
from src.priority_queue import IndexedPQ

@pytest.fixture
def pq_max_size():
    return 5


@pytest.fixture
def pq_type():
    return "max"


@pytest.fixture
def pq_data():
    return [(0, 4), (2, 7), (1, 6), (4, 10), (3, 5)]


@pytest.fixture
def pq_data_sorted():
    return [(4, 10), (2, 7), (1, 6), (3, 5), (0, 4)]

@pytest.fixture
def pq_altered_data():
    return [(0, 1), (2, 2), (1, 45), (3, 59), (4, -12)]

@pytest.fixture
def pq_altered_data_sorted():
    return [(3, 59), (1, 45), (2, 2), (0, 1), (4, -12)]

@pytest.fixture
def pq(pq_max_size, pq_type):
    return IndexedPQ(pq_max_size, pq_type)


def test_insertions_and_deletions(pq, pq_data, pq_data_sorted):
    
    assert pq.isEmpty

    for i, key in pq_data:
        pq.insert(i, key)
    
    for i, key in pq_data_sorted:
        deleted_i, deleted_key = pq.delete()
        assert deleted_i == i and deleted_key == key, "Sorting failed"

    raised_empty_pq_error = False
    try:
        pq.delete()
    except IndexError:
        raised_empty_pq_error = True
    
    assert raised_empty_pq_error


def test_mutations(pq, pq_data, pq_altered_data, pq_altered_data_sorted):

    assert pq.isEmpty

    for i, key in pq_data:
        pq.insert(i, key)

    increased = False
    decreased = False

    for i, key in pq_altered_data:
        if key > pq.key[i]:
            pq.increaseKey(i, key)
            increased = True
        elif key < pq.key[i]:
            pq.decreaseKey(i, key)
            decreased = True
    
    assert increased and decreased

    for i, key in pq_altered_data_sorted:
        deleted_i, deleted_key = pq.delete()
        assert deleted_i == i and deleted_key == key, "Sorting failed"

    raised_empty_pq_error = False
    try:
        pq.delete()
    except IndexError:
        raised_empty_pq_error = True
    
    assert raised_empty_pq_error