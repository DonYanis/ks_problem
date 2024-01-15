from utils import Node, State, Object

def succ(state, action, OBJECTS, MAX_WEIGHT):

    if len(state.objects_array) != len(action):
        raise ValueError('invalide state or action')
    if 1 in action : 
        current_object = OBJECTS[action.index(1)] 
    
        if state.weight + current_object.weight > MAX_WEIGHT : 
            return 0
    else :
        current_object = Object('0',0,0)

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

def test_goal_1(node, OBJECTS, MAX_WEIGHT):
    return len(successors(node, OBJECTS, MAX_WEIGHT)) == 0

def search_vwratio(OBJECTS, MAX_WEIGHT):
    
    init_state = State([0]*len(OBJECTS),0,0)
    actions = [[0]*len(OBJECTS),[0]*len(OBJECTS)]
    next_object = 0
    actions[1][next_object] = 1

    #create list
    nodes = [ Node(init_state, actions=actions) ]

    #search loop
    while True:
        #check if no solutions
        if len(nodes)==0:
            return False
       

        node = nodes.pop()

        #check gaol state
        if test_goal_1(node, OBJECTS, MAX_WEIGHT):
            return node
        
        #generate successors
        
        next_object = node.actions[1].index(1) + 1
        actions = [[0] * len(OBJECTS), [0] * len(OBJECTS)] if next_object < len(OBJECTS) else [[1] * len(OBJECTS), [1] * len(OBJECTS)]

        for successor_state in successors(node, OBJECTS, MAX_WEIGHT): 
            if next_object < len(OBJECTS) :
                actions[1][next_object] = 1
            #create node :
            n = Node(state=successor_state, parent=node, actions=actions, path_cost=0, depth=node.depth+1)
            #add node to list

            nodes.append(n)

def test_goal_2(nodes):
    return len(nodes) == 0

def search_upperbound(OBJECTS, MAX_WEIGHT):

    #initialisations
    init_state = State([0]*len(OBJECTS),0,0)
    actions = [[0]*len(OBJECTS),[0]*len(OBJECTS)]
    next_object = 0
    actions[0][next_object] = 1
    nodes = [ Node(init_state, actions=actions) ]
    best_solution = Node(init_state, actions=actions)
    max_value = 0

    #search loop
    while True:


        if test_goal_2(nodes):
            return best_solution
       
        node = nodes.pop()

        if len(successors(node, OBJECTS, MAX_WEIGHT)) and node.state.value > best_solution.state.value:
            best_solution = node
        
        
        next_object = node.actions[0].index(1) + 1
        actions = [[0] * len(OBJECTS), [0] * len(OBJECTS)] if next_object < len(OBJECTS) else [[1] * len(OBJECTS), [1] * len(OBJECTS)]

        for successor_state in successors(node, OBJECTS, MAX_WEIGHT): 
            if next_object < len(OBJECTS) :
                actions[0][next_object] = 1
            
            remaining_values = sum(obj.value for obj in OBJECTS[node.depth+1:])
            
            max_value = successor_state.value + remaining_values 
            if max_value > best_solution.state.value :
                n = Node(state=successor_state, parent=node, actions=actions, path_cost=0, depth=node.depth+1)
                #add node to list

                nodes.append(n)
