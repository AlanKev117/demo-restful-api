class IndexedPQ:
    """An abstraction of an indexed priority queue, tweaked to behave as either
    a maximum or a minimum one. Original code taken from: 

    https://gist.github.com/mkhoshpa/21cf58141a166a692a22a74eeecbe3c4#file-indexedminpq-py

    Attributes:
        N: the max capacity of the PQ
        key: actual priority values
        pq: heap representation of the PQ as an array
        qp: contains the index of each key
        total: the amount of current items saved in the PQ
        q_type: defines whether the PQ is a max or a min one
        compare: comparator defined by q_type
    """

    def __init__(self, N, q_type="max"):
        """Inits an empty PQ
        Args:
            N: max size of the PQ
            q_type: the type of the PQ ("max" or "min")
        Raises:
            AssertionError: if q_type is not either "max" or "min"
        """

        def is_bigger(a, b):
            return a > b

        def is_less(a, b):
            return a < b

        assert q_type in ("min", "max"), "Wrong PQ type"

        self.N = N
        self.q_type = q_type
        self.key = [None for i in range(self.N)]
        self.pq = [None for i in range(self.N+1)]
        self.qp = [None for i in range(self.N)]
        self.total = 0
        self.compare = is_bigger if q_type == "max" else is_less

    def insert(self, i, key):
        """Inserts a key to the PQ
        Args:
            i: index to store the key at
            key: priority value to be stored
        Raises:
            AssertionError: if type of i is not int
            IndexError: if trying to insert to an invalid index
        """
        assert type(i) is int
        if i >= self.N:
            raise IndexError('index is out of the range of IndexedMinPQ.')
        if self.key[i] is not None:
            raise IndexError('index is already in the IndexedMinPQ.')
        self.total += 1
        self.key[i] = key
        self.pq[self.total] = i
        self.qp[i] = self.total
        self.__swim(self.total)

    def __swim(self, i):
        parent_i = i//2

        while parent_i > 0:
            key = self.key[self.pq[i]]
            parent_key = self.key[self.pq[parent_i]]
            if self.compare(parent_key, key):
                break
            self.pq[i], self.pq[parent_i] = self.pq[parent_i], self.pq[i]
            self.qp[self.pq[i]], self.qp[self.pq[parent_i]
                                         ] = self.qp[self.pq[parent_i]], self.qp[self.pq[i]]
            i = parent_i
            parent_i = i // 2

    def delete(self):
        """Deletes the higest priority key from the PQ
        Raises:
            IndexError: when trying to delete from empty PQ
        """
        if not self.isEmpty():
            key_out = self.key[self.pq[1]]
            index_out = self.pq[1]
            self.key[self.pq[1]] = None
            self.qp[self.pq[1]] = None
            self.pq[1] = self.pq[self.total]
            self.qp[self.pq[1]] = 1
            self.pq[self.total] = None
            self.total -= 1
            self.__sink(1)
            return index_out, key_out
        raise IndexError('IndexedMinPQ is Empty')

    def __sink(self, i):
        child_i = i * 2
        if child_i <= self.total:
            key = self.key[self.pq[i]]
            child_key = self.key[self.pq[child_i]]
            other_child = child_i + 1
            if other_child <= self.total:
                other_child_key = self.key[self.pq[other_child]]
                if self.compare(other_child_key, child_key):
                    child_i = other_child
                    child_key = other_child_key
            if self.compare(child_key, key):
                self.pq[i], self.pq[child_i] = self.pq[child_i], self.pq[i]
                self.qp[self.pq[i]], self.qp[self.pq[child_i]
                                             ] = self.qp[self.pq[child_i]], self.qp[self.pq[i]]
                self.__sink(child_i)

    def isEmpty(self):
        return self.total == 0

    def decreaseKey(self, i, key):
        """Replaces a key value at an index to a lower one.
        Args:
            i: index whose key to alter
            key: lower priority value to be stored
        Raises:
            IndexError: if index to alter is not valid
        """
        if i < 0 or i > self.N:
            raise IndexError('index i is not in the range')
        if self.key[i] is None:
            raise IndexError('index i is not in the IndexedMinPQ')
        assert type(i) is int
        assert key < self.key[i]
        self.key[i] = key

        if self.q_type == "min":
            self.__swim(self.qp[i])
        else:
            self.__sink(self.qp[i])

    def increaseKey(self, i, key):
        """Replaces a key value at an index to a higher one.
        Args:
            i: index whose key to alter
            key: higher priority value to be stored
        Raises:
            IndexError: if index to alter is not valid
        """
        if i < 0 or i > self.N:
            raise IndexError('index i is not in the range')
        if self.key[i] is None:
            raise IndexError('index i is not in the IndexedMinPQ')
        assert type(i) is int
        assert key > self.key[i]
        self.key[i] = key

        if self.q_type == "min":
            self.__sink(self.qp[i])
        else:
            self.__swim(self.qp[i])
