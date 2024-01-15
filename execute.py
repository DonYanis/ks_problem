import json
import sys

from utils import search_heu, search_bfs, search_dfs, create_node_actions, Object, State
from utils2 import search_vwratio, search_upperbound

approaches = ['formalization 1 : graph with multiple children', 'formalization 2 : binary graph']
methods = [
    ['uninformed BFS ', 'uninformed DFS', 'value heuristic', 'weight heuristic', 'value weight ratio heuristic'],
    ['Upper bound heuristic', 'value weight ratio heuristic']
]

def execute(approach, method, dataset_path):

    #read data set : 
    try:
        with open(dataset_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f'The file {dataset_path} was not found.')
        sys.exit(1) 
    except json.JSONDecodeError:
        print(f'There was an error decoding JSON in {dataset_path}.')
        sys.exit(1) 
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        sys.exit(1) 

    OBJECTS = [] 

    for e in data['objects'] : 
        OBJECTS.append(Object(e['id'],e['weight'],e['value']))

    MAX_WEIGHT = data['maxweight']

    #exuction : 
    if approach == 1 : 
        init_state = State([0]*len(OBJECTS),0,0)
        actions = create_node_actions(init_state)
        if method == 1:
            node = search_bfs(init_state, actions, OBJECTS, MAX_WEIGHT)
        elif method == 2:
            node = search_dfs(init_state, actions, OBJECTS, MAX_WEIGHT)
        elif method == 3:
            node = search_heu(init_state, actions, OBJECTS, MAX_WEIGHT,'v')
        elif method == 4:
            node = search_heu(init_state, actions, OBJECTS, MAX_WEIGHT,'w')
        elif method == 5:
            node = search_heu(init_state, actions, OBJECTS, MAX_WEIGHT,'vwratio')
        objects = [o.id for i,o in enumerate(OBJECTS) if node.state.objects_array[i]==1]

    elif approach == 2 : 
        if method == 2:
            sorted_obj = sorted(OBJECTS, key=lambda obj: obj.value / obj.weight, reverse=True)
            node = search_vwratio(sorted_obj, MAX_WEIGHT)
            objects = sorted([o.id for i,o in enumerate(sorted_obj) if node.state.objects_array[i]==1])

        elif method == 1:
            node = search_upperbound(OBJECTS, MAX_WEIGHT)
            objects = [o.id for i,o in enumerate(OBJECTS) if node.state.objects_array[i]==1]


    print(f'\napproach : {approaches[approach-1]}\nmethod : {methods[approach-1][method-1]}\nobjects : {len(OBJECTS)}\nmax weight : {MAX_WEIGHT}')
    print(f'solution : \n\ttotal value : {node.state.value}\n\ttotal weight : {node.state.weight}')
    print(f'objects in knapsack : {objects}')