import csv
from collections import deque

def parse_ntm(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)
    #parsing csv file
    name = lines[0][0]
    states = lines[1]
    tape_symbols = lines[2]
    tape_alphabet = lines[3]
    start_state = lines[4][0]
    accept_state = lines[5][0]
    reject_state = lines[6][0]
    transitions = lines[7:]

    return { #return dict
        "name": name,
        "states": states,
        "tape_symbols": tape_symbols,
        "tape_alphabet": tape_alphabet,
        "start_state": start_state,
        "accept_state": accept_state,
        "reject_state": reject_state,
        "transitions": transitions
    }

def ntm_bfs(ntm, input_string, max_depth=100):
    start_config = ["", ntm["start_state"], input_string, ""]
    tree = [[start_config]]
    queue = deque([start_config])
    depth = 0
    transitions = ntm["transitions"]
    b = 0

    while queue and depth < max_depth:
        next_level = []
        while queue:
            current = queue.popleft()
            left, state, right, _ = current

            if state == ntm["accept_state"]:
               # print(f"String accepted in {depth} transitions!\n")
                return tree, b, depth, 1

            # Get the current head symbol (blank if no symbols left)
            head = right[0] if right else "_"

            # Find applicable transitions
            for t in transitions:
                old_state = t[0]
                old_symbol = t[1]
                new_state = t[2]
                new_symbol = t[3]
                direction = t[4]

               
                if state == old_state and old_symbol == head: #check for match
                    b += 1
                    new_left = left
                    new_right = right[1:] if len(right) > 1 else ""  # Remove the head symbol from the tape

                    #right head movement
                    if direction == "R":
                        
                        new_left += new_symbol
                        new_right = new_right if new_right else ""

                    #left head movement
                    elif direction == "L":
                        
                        holder = new_left[-1] if new_left else "_"
                        new_left = new_left[:-1] if new_left else ""

                        new_right = holder + new_symbol + new_right



                    # Create new configuration and add to next level
                    next_config = [new_left, new_state, new_right, old_state]
                    next_level.append(next_config)

        if not next_level:
           # print(f"String rejected in {depth} transitions.\n")
            return tree, b, depth, 0

        tree.append(next_level)
        queue.extend(next_level)
        depth += 1

    print("Execution stopped after max depth.\n")
    return tree, b, depth, 0

def backtrack(tree, accept_state):
    # Find the accepting configuration
    accept_config = None
    for level in tree:
        for config in level:
            if config[1] == accept_state:
                accept_config = config
                break
        if accept_config:
            break

    if not accept_config:
        return []

    # Backtrack through the tree using the previous state information
    path = []
    current = accept_config

    while current:
        x, y, z, _ = current
        s = [x, y, z]
        path.append(s)
        previous_state = current[3]
        #print(f"Current config: {current}, Previous state: {previous_state}")  # Debug print

        if previous_state is None:
            break  # Reached the start configuration

        found = False
        for level in reversed(tree):
            for config in level:
                if config[1] == previous_state:
                    #print("Match found!")  # Debug print for when a match is found
                    current = config
                    found = True
                    break
            if found:
                tree = tree[:-1]
                break

        if not found:
            break

    path.reverse()
    return path
    

if __name__ == "__main__":
    print("")
    ntm = parse_ntm("NTM_test_files/2x0_DTM - Sheet1.csv")  
    input_str = "0010"  
    tree, branches, depth, accept = ntm_bfs(ntm, input_str, 100)
    nondeterminism = branches / depth if depth > 0 else 1

    #output prints
    print(f'Name of Machine: {ntm["name"]}')
    print(f'Initial String: {input_str}')
    print(f'Depth of Tree: {depth}')

    print(f'Total number of transitions simulated: {branches}')
    print(f"Degree of Nondeterminism: {nondeterminism:.2f}")

    #call backtrack
    path = backtrack(tree, ntm['accept_state'])

    if not path:
        print("No accepting path to display.\n")
    else:
        print("Accepting Path:")
        for i, config in enumerate(path):
            print(f"Step {i}: {config}")
        print("")
