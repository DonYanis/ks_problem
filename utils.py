class Node:
    def __init__(self, state, parent=None, actions=[], path_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.path_cost = path_cost
        self.depth = depth
    
    def __str__(self):
        return f'{self.state.__str__()}'

class State:
    def __init__(self, objects_array, weight, value):
        self.objects_array = objects_array
        self.weight = weight
        self.value = value

    def __str__(self):
        return f'weight : {self.weight} , value : {self.value} , state : {self.objects_array}'

class Object:
    def __init__(self, id, weight, value):
        self.id = id
        self.weight = weight
        self.value = value
    def __str__(self) -> str:
        return self.id

    def __str__(self):
        return f'weight : {self.weight} , value : {self.value}'


def succ(state, action, OBJECTS, MAX_WEIGHT):

    if len(state.objects_array) != len(action):
        raise ValueError('invalide state or action')
    
    current_object = OBJECTS[action.index(1)] 
    
    if state.weight + current_object.weight > MAX_WEIGHT : 
        return 0

    new_state = []
    for e1, e2 in zip(state.objects_array, action):
        result = e1+e2
        if 0 <= result <= 1 :
            new_state.append(result)
        else : 
            return 0

    return State(
        new_state, 
        state.weight + current_object.weight,
        state.value + current_object.value
    )

def successors(node, OBJECTS, MAX_WEIGHT):
    return [succ(node.state, action, OBJECTS, MAX_WEIGHT) for action in node.actions if succ(node.state, action, OBJECTS, MAX_WEIGHT) != 0]

def test_goal(node, OBJECTS, MAX_WEIGHT):
    return len(successors(node, OBJECTS, MAX_WEIGHT)) == 0

def create_node_actions(state) :
    actions = []
    for i in range(len(state.objects_array)) :
        action = [0]*len(state.objects_array)
        if state.objects_array[i] == 0 : 
            action[i] = 1
            actions.append(action)
    return actions

def heuristic(nodes, heu, lmbda=1):
    
    if heu == 'w':
        return max(nodes, key= lambda e: e.state.weight)
    
    elif heu == 'v':
        return max(nodes, key= lambda e: e.state.value)

    elif heu == 'vwratio':
        return max(nodes, key= lambda e: e.state.value / e.state.weight)
    
    elif heu == 'linear':
        return max(nodes, key= lambda e: e.state.value - lmbda * e.state.weight)
    
    else :
        raise ValueError('invalide heuristic')

def search_bfs(init_state, actions, OBJECTS, MAX_WEIGHT):
    #create list
    nodes = [ Node(init_state, actions=actions) ]
    #search loop
    while True:
        #check if no solutions
        if len(nodes)==0:
            return False
        
        #get element from node list
        node = nodes.pop(0)

        #check gaol state
        if test_goal(node, OBJECTS, MAX_WEIGHT):
            return node
        
        #generate successors
        for successor_state in successors(node, OBJECTS, MAX_WEIGHT):
            #create actions : 
            actions = create_node_actions(successor_state)
            #create node :
            n = Node(state=successor_state, parent=node, actions=actions, depth=node.depth+1)
            #add node to list
            nodes.append(n)

def search_dfs(init_state, actions, OBJECTS, MAX_WEIGHT):
    #create list
    nodes = [ Node(init_state, actions=actions) ]
    #search loop
    while True:
        #check if no solutions
        if len(nodes)==0:
            return False
        
        #get element from node list
        node = nodes.pop()

        #check gaol state
        if test_goal(node, OBJECTS, MAX_WEIGHT):
            return node
        
        #generate successors
        for successor_state in successors(node, OBJECTS, MAX_WEIGHT):
            #create actions : 
            actions = create_node_actions(successor_state)
            #create node :
            n = Node(state=successor_state, parent=node, actions=actions, depth=node.depth+1)
            #add node to list
            nodes.append(n)

def search_heu(init_state, actions, OBJECTS, MAX_WEIGHT, heu):
    #create list
    nodes = [ Node(init_state, actions=actions) ]
    #search loop
    while True:
        #check if no solutions
        if len(nodes)==0:
            return False

        node = nodes.pop()
        #check gaol state
        if test_goal(node, OBJECTS, MAX_WEIGHT):
            return node
        #generate successors
        temp = []
        for successor_state in successors(node, OBJECTS, MAX_WEIGHT):
            #create actions : 
            actions = create_node_actions(successor_state)
            #create node :
            n = Node(state=successor_state, parent=node, actions=actions, depth=node.depth+1)
            #add node to list
            temp.append(n)
        nodes.append(heuristic(temp,heu))
