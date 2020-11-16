import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Create a frontier and add the source as its initial node
    frontier = QueueFrontier()
    frontier.add(Node(source, None, None))

    # Create empty explored set
    explored_states = []

    # Searching for a node with target state by removing nodes from the
    # frontier and adding their neighbors to it
    while True:
        # If the forntier is empty, there is no path to between source and
        # target and thus None is returned
        if frontier.empty():
            return None

        # Remove a node from the frontier and jumpt out of the cycle, if it
        # containts the target we are searching for
        target_node = frontier.get_node_with_state(target)
        if not target_node:
            removed = frontier.remove()
        else:
            break

        # Add the state of removed node to the explored states to avoid cycles
        explored_states.add(removed.state)

        # Add neighbors of removed node to the frontier
        for neighbor in neighbors_for_person(removed.state):
            state = neighbor[1]
            action = neighbor[0]
            if state not in explored_states:
                frontier.add(Node(state, removed, action))

        target_node = None

    # Reconstruct the path to the target node
    path = []
    index = target_node
    while True:
        if index.state == source:
            path.reverse()
            return path

        path.append((index.action, index.state))
        index = index.parent


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def print_frontier(frontier):
    for node in frontier.frontier:
        person = people[node.state]['name']
        if not node.action:
            movie = "N/A"
        else:
            movie = movies[node.action]['title']
        if not node.parent:
                parent = "N/A"
        else:
            parent = people[node.parent.state]['name']

        print(f"[S: {person}, A: {movie}, P: {parent}]  ")


def print_path(path, source):
    state = people[source]['name']
    path.reverse()
    for link in path:
        action = movies[link[0]]['title']
        target = people[link[1]]['name']
        print(f"{ state } played in { action } with { target }")
        state = target


def debug():
    load_data("small")
    path = shortest_path('144', '102')
    print(path)


if __name__ == "__main__":
    main()
    # debug()
