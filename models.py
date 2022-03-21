class Node:
    def __init__(self, doc_id, freq=None):
        self.freq = freq
        self.doc = doc_id
        self.next_val = None


class HeadNode:
    def __init__(self, head=None):
        self.head = head
