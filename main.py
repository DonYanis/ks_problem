from execute import execute

#approach
approach = 0
while True:

    choice = input("Choose between:\n1 for 'approach 1 : multiple children graph'\n2 for 'approach 2 : binary graph'\n")

    if choice in ['1', '2']:
        approach = int(choice)
        break   
    else:
        print("Invalid choice.")

#method
method = 0
while True:
    if approach == 1 : 
        choice = input("Choose a method of resolving:\n1 : BFS\n2 : DFS\n3 : value heuristic\n4 : weight heuristic\n5 : value/weight heuristic\n")
        if choice in ['1', '2', '3', '4', '5']:
            method = int(choice)
            break  

    elif approach == 2 :
        choice = input("Choose a method of resolving:\n1 : upper bound heuristic\n2 : value/weight heuristic\n")
        if choice in ['1', '2']:
            method = int(choice)
            break   
    else:
        print("Invalid choice.")

#dataset
dataset = 0
dataset_path = ''
while True:
 
    choice = input("Choose a dataset:\n1 : data0.json (20 objects)\n2 : data1.json (320 objects)\n3 : data2.json (640 objects)\n4 : type an other dataset name\n")

    if choice in ['1', '2', '3', '4']:
        dataset = int(choice)
        break   
    else:
        print("Invalid choice.")


if dataset == 1 :
    dataset_path = 'data/data0.json'
elif dataset == 2 : 
    dataset_path = 'data/data1.json'
elif dataset == 3 : 
    dataset_path = 'data/data2.json'
elif dataset == 4 : 
    dataset_path = input("enter dataset path with JSON extension : \n")


execute(approach, method, dataset_path)