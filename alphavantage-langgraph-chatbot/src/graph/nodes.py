class Node:
    def __init__(self, id, data=None):
        self.id = id
        self.data = data
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def __repr__(self):
        return f"Node(id={self.id}, data={self.data})"

    def get_edges(self):
        return self.edges

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)