from queue import PriorityQueue


class Node:

    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None


    def __str__(self):
        return str(self.value)


class BinaryTree:
    def __init__(self, root_value):
        self.root = Node(root_value)

    def insert_left(self, parent_node, new_value):
        if parent_node.left_child is None:
            parent_node.left_child = Node(new_value)
        else:
            new_node = Node(new_value)
            new_node.left_child = parent_node.left_child
            parent_node.left_child = new_node

    def insert_right(self, parent_node, new_value):
        if parent_node.right_child is None:
            parent_node.right_child = Node(new_value)
        else:
            new_node = Node(new_value)
            new_node.right_child = parent_node.right_child
            parent_node.right_child = new_node



    def bfs(self):
        queue = []
        visited = []

        queue.append(self.root)

        while queue:
            node = queue.pop(0)
            visited.append(node)

            if node.left_child:
                queue.append(node.left_child)
            if node.right_child:
                queue.append(node.right_child)

        return visited




    def dfs(self, node=None, visited=None):
        if node is None:
            node = self.root
        if visited is None:
            visited = []

        visited.append(node)

        if node.left_child and node.left_child not in visited:
            self.dfs(node.left_child, visited)
        if node.right_child and node.right_child not in visited:
            self.dfs(node.right_child, visited)

        return visited




    def astar(self, target):
        open_set = PriorityQueue()
        open_set.put((0, self.root))

        closed_set = set()
        came_from = {}
        g_score = {self.root: 0}
        f_score = {self.root: self.heuristic(self.root, target)}

        while not open_set.empty():
            current_node = open_set.get()[1]

            if current_node == target:
                path = []
                while current_node is not self.root:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(self.root)
                path.reverse()
                return path

            closed_set.add(current_node)

            for neighbor in self.get_neighbors(current_node):
                tentative_g_score = g_score[current_node] + self.distance(current_node, neighbor)

                if neighbor in closed_set:
                    continue

                if neighbor not in [n[1] for n in open_set.queue]:
                    open_set.put((f_score[neighbor], neighbor))
                elif tentative_g_score >= g_score[neighbor]:
                    continue

                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, target)

        return None

    def get_neighbors(self, node):
        neighbors = []
        if node.left_child:
            neighbors.append(node.left_child)
        if node.right_child:
            neighbors.append(node.right_child)
        return neighbors

    def distance(self, node1, node2):
        return 1

    def heuristic(self, node, target):
        return abs(node.value - target.value)
