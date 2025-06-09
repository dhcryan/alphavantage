class Edge:
    def __init__(self, from_node, to_node, weight=1):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight

    def __repr__(self):
        return f"Edge(from: {self.from_node}, to: {self.to_node}, weight: {self.weight})"

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def get_nodes(self):
        return self.from_node, self.to_node