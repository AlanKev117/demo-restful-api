import sys
import pathlib

# Prepare static imports
PROJECT_DIR = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(PROJECT_DIR)

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from src.priority_queue import IndexedPQ

app = Flask(__name__)
api = Api(app)
MAX_PQ_SIZE = 2**16
PQ = IndexedPQ(MAX_PQ_SIZE)


def abort_if_pq_empty():
    if PQ.isEmpty():
        abort(404, message="Priority queue is empty.")


parser = reqparse.RequestParser()
parser.add_argument('key')


class HelloWorld(Resource):
    def get(self):
        return "Hello, World"


class PriorityQueueKey(Resource):
    """A set of methods that involve retrieving or mutating specific
    items from the PQ.

    Methods:
        get: to retrieve a key from the PQ by its index
        post: to store a key into an index
        put: to alter the key of an index
    """

    def get(self, index):
        abort_if_pq_empty()
        return {"index": index, "key": PQ.key[index]}

    def post(self, index):
        args = parser.parse_args()
        key = int(args["key"])

        try:
            PQ.insert(index, key)
        except AssertionError:
            abort(400, "Index is not an int")
        except IndexError:
            abort(400, "Invalid index to insert to")

        return {"index": index, "key": key}, 201

    def put(self, index):
        abort_if_pq_empty()
        args = parser.parse_args()
        key = int(args['key'])
        try:
            if key > PQ.key[index]:
                PQ.increaseKey(index, key)
            elif key < PQ.key[index]:
                PQ.decreaseKey(index, key)
        except:
            abort(400, message="Index not storing a key yet")
        return {"index": index, "key": key}, 201


class PriorityQueue(Resource):
    """A set of methods that involve retrieving or poping the
    highest priority item in the PQ.

    Methods:
        get: retreives the content of the PQ and its highest priority item
        delete: pops out the highest priority key from the PQ
    """

    def get(self):
        abort_if_pq_empty()
        res = {"highest": {}, "content": []}
        for heap_index, index in enumerate(PQ.pq):
            if index is not None:
                key = PQ.key[index]
                if heap_index == 1:
                    res["highest"] = {"index": index, "key": key}
                res["content"].append({"index": index, "key": key})
        return res

    def delete(self):
        abort_if_pq_empty()
        index, key = PQ.delete()
        return {"index": index, "key": key}

# Endpoints
api.add_resource(HelloWorld, "/")
api.add_resource(PriorityQueue, '/queue')
api.add_resource(PriorityQueueKey, '/queue/<int:index>')


if __name__ == '__main__':
    app.run(debug=False)
