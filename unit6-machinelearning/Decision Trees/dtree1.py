import sys
import time
import math

#Node class to create the tree
class Node:
    def __init__(self, name, depth, is_feature, is_leaf, children, is_start, outcome):
        self.name = name
        self.depth = depth
        self.is_feature = is_feature
        self.is_leaf = is_leaf
        self.children = children
        self.is_start = is_start
        self.outcome = outcome

#main recursive function
#return type: Node
def generate_tree(features, dataset, head):
    feature = choose_feature(features, dataset)
    #print(feature)
    feature_node = Node(feature[0], head.depth+1, True, False, [], False, None)
    head.children.append(feature_node)
    new_datasets = reduce_dataset(feature, dataset)
    for new_dataset in new_datasets:
        if find_entropy(new_dataset) == 0:
            feature_node.children.append(Node(new_dataset[0][feature[1]], feature_node.depth+1, False, True, [], False, new_dataset[0][-1]))
        else:
            #print(new_dataset)
            new_node = Node(new_dataset[0][feature[1]], feature_node.depth+1, False, False, [], False, None)
            feature_node.children.append(new_node)
            generate_tree(features, new_dataset, new_node)
    return head

#given a dataset, find the overall entropy of the dataset
#return type: float
def find_entropy(dataset):
    num_data = len(dataset)
    count_values = dict()
    for data_value in dataset:
        if data_value[-1] not in count_values.keys():
            count_values[data_value[-1]] = 1
        else:
            count_values[data_value[-1]] += 1
    final_sum = 0
    for poss_value in count_values.keys():
        final_sum += ((count_values[poss_value]/num_data) *math.log(count_values[poss_value]/num_data, 2))
    return final_sum * -1

#given a feature and the dataset, find the information gain of that feature
#return type: float
def find_information_gain(feature, dataset):
    num_data = len(dataset)
    curr_entropy = find_entropy(dataset)
    poss_values = set()
    for data_value in dataset:
        poss_values.add(data_value[feature[1]])
    new_entropy = 0
    for poss_value in poss_values:
        new_dataset = split_dataset(feature, poss_value, dataset)
        curr_len = len(new_dataset)
        new_entropy += ((curr_len/num_data)*find_entropy(new_dataset))
    return curr_entropy - new_entropy

#based on the selected feature, split the dataset into multiple datasets based on each value for the feature, return list of these new datasets
#return type: [(name of dataset, list of dataset values)]
def reduce_dataset(feature, dataset):
    poss_values = set()
    for data_value in dataset:
        poss_values.add(data_value[feature[1]])
    new_datasets = list()
    for poss_value in poss_values:
        new_datasets.append(split_dataset(feature, poss_value, dataset))
    return new_datasets

#given a feature, a value for that feature, and the entire dataset, create a new dataset where for the given feature, the value is always the given value
#return type: [(data_value)]
def split_dataset(feature, value, dataset):
    position = feature[1]
    name = feature[0]
    new_dataset = []
    for data_value in dataset:
        if data_value[position] == value:
            new_dataset.append(data_value)
    return new_dataset

#select the feature with the most information gain
#return type: (name, index in list of features)
def choose_feature(features, dataset):
    ig_values = list()
    for feature in features:
        ig_values.append((feature, find_information_gain(feature, dataset)))
    return max(ig_values, key=lambda x: x[1])[0]

#sorting key to sort alphabetically
def sort_alphabetical(node):
    return node.name

#given a fully created decision tree, output the tree, nicely formatted, to a text file
#return type: None
def output_tree(head):
    f = open("treeout.txt", "w")
    stack = list()
    stack.append(head)
    while stack:
        curr_node = stack.pop()
        if curr_node.depth == -1:
            for child in sorted(curr_node.children, key=sort_alphabetical, reverse=True):
                stack.append(child)
            continue
        to_print = '  ' * curr_node.depth
        to_print += '* '
        to_print += curr_node.name
        if curr_node.is_feature == True:
            to_print += '?'
        if curr_node.is_leaf == True:
            to_print += ' --> '
            to_print += curr_node.outcome
        f.write(to_print +'\n')
        for child in sorted(curr_node.children, key=sort_alphabetical, reverse=True):
            stack.append(child)
    f.close()


#read in values from csv and store in features and dataset variables
filename = sys.argv[1]
features = list()
dataset = list()
with open(filename) as csv:
    for count, line in enumerate(csv):
        line = line.strip()
        values = line.split(',')
        if count == 0:
            features = [(values[i], i) for i in range(len(values)-1)]
        else:
            dataset.append(tuple(values))

#generate tree and output
start = time.perf_counter()
head = generate_tree(features, dataset, Node('Start', -1, False, False, [], False, None))
output_tree(head)
end = time.perf_counter()
print(end - start)