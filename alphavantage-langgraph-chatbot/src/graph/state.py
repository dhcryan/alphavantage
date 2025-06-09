class GraphState:
    def __init__(self):
        self.current_node = None
        self.transitions = {}

    def set_current_node(self, node):
        self.current_node = node

    def add_transition(self, from_node, to_node):
        if from_node not in self.transitions:
            self.transitions[from_node] = []
        self.transitions[from_node].append(to_node)

    def get_next_nodes(self):
        return self.transitions.get(self.current_node, [])

    def reset(self):
        self.current_node = None
        self.transitions = {}