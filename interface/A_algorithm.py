"""Check out the amazing original code at:
https://codes-sources.commentcamarche.net/source/54225-mise-en-evidence-de-l-algorithme-a-star-graphiquement
by Mints
"""

from math import sqrt


class Node():
    """Each cell of the game is represented by a node object which contains:
         - its position on the grid
         - its G-cost : distance between it and its ascendant + G-cost of its
           ascendant
         - its H cost : distance between it and the final node
         - its F-cost : sum of G and H
    """

    def __init__(self, cell_pos):
        self.column, self.row = cell_pos
        self.costF = 0
        self.costG = 0
        self.costH = 0
        self.parent = self


def A_algorithm(grid, begin_cell, dest_cell, cardinal=4):
    """Main while loop :
        - The best node of the open list is put in the closed list and we call
          the function that will look for its neighbors
        - when the best node corresponds to the final node, the loop is ended
          to returns the computed path
        - if the final node is not reached and if the list of nodes to be
          explore is empty: there is no solution
    """

    global openned_list, closed_list, current_node, final_node

    if begin_cell == dest_cell:
        return []

    first_node = Node(begin_cell)
    final_node = Node(dest_cell)

    openned_list = []
    closed_list = []

    # Initialization of current_node with first_node
    current_node = first_node
    current_node.costH = distance(current_node, final_node)
    current_node.costF = current_node.costH
    # Put it in openned list
    openned_list.append(current_node)

    while (not (current_node.row == final_node.row
                and current_node.column == final_node.column)
           and openned_list != []):
        # Choose best node as current_node
        current_node = best_node()
        add_closed_list(current_node)

        # Search current_node neighbor's
        add_neighbors(grid, cardinal=cardinal)

    # Reached final node
    if (current_node.row == final_node.row
            and current_node.column == final_node.column):
        road = return_path()

    # Didn't reach final node and no node left
    elif openned_list == []:
        road = []

    return road


def best_node():
    """Function that returns the best node of the open list according to
    its F cost"""
    cost = 5000000
    node = None
    for n in openned_list:
        if n.costF < cost:
            cost = n.costF
            node = n
    return node


def add_closed_list(node):
    "Adds a node to the closed list and removes it from the open list"""
    global openned_list, closed_list

    closed_list.append(node)
    openned_list.remove(node)


def add_neighbors(grid, cardinal=4):
    """Function that searches all possible neighbors to the current_node."""

    global openned_list, closed_list, current_node

    if cardinal == 8:
        # 8 movements allowed in the matrix
        deplacements = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                        (1, 0), (1, -1), (0, -1), (-1, -1)]
    elif cardinal == 4:
        deplacements = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for direction in deplacements:
        next_cell = (current_node.column + direction[1],
                     current_node.row + direction[0])

        cell = grid.get(next_cell, None)

        # Check if neighbor is accessible
        if cell is not None and cell.active:
            # Create node at neighbor coordinates
            temp_node = Node(next_cell)
            # current_node is parent of temp_node
            temp_node.parent = current_node
            # Check if temp_node neighbor is not already in closed list
            if not already_in_list(temp_node, closed_list):
                # Compute its costs
                temp_node.costG = (temp_node.parent.costG
                                   + distance(temp_node, temp_node.parent))
                temp_node.costH = distance(temp_node, final_node)
                temp_node.costF = temp_node.costG + temp_node.costH

                n = already_in_list(temp_node, openned_list)

                # If temp_node already in openned list
                if n is not False:
                    # Compare its G cost with the n node from openned list
                    if temp_node.costG < n.costG:
                        # If <, replace n costs by temp_node
                        n.parent = current_node
                        n.costG = temp_node.costG
                        n.costH = temp_node.costH
                        n.costF = temp_node.costF
                    # if >, keep previous n

                # Add node in openned list if not present
                else:
                    openned_list.append(temp_node)


def distance(node1, node2):
    """Compute the distance between two nodes."""
    a = node2.row - node1.row
    b = node2.column - node1.column

    return sqrt((a*a) + (b*b))


def already_in_list(node, liste):
    """Functions that seach if a node is already present in the openned list.
    """
    for n in liste:
        if n.row == node.row and n.column == node.column:
            return n
    return False


def return_path():
    """The goal is reached, this function goes up the path from ascending to
    starting from the last chosen current node and return the path."""

    chemin = []
    n = closed_list[-1]
    chemin.append(n)
    n = n.parent

    while n.parent != n:
        chemin.append(n)

        n = n.parent

    chemin.append(n)

    output = []

    for node in chemin:
        output.append((node.column, node.row))

    output.reverse()  # set the path in the correct order
    output.pop(0)  # remove standing cell

    return output
