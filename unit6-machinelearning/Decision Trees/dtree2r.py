import sys
import time
import math
import random
from matplotlib import pyplot as plt

#Node class to create the tree
class Node:
    def __init__(self, name, name_index, depth, is_feature, is_leaf, children, is_start, outcome):
        self.name = name
        self.name_index = name_index
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
    if feature == None:
        head.children.append(Node('Randomly Selected', -1, head.depth+1, False, True, [], False, dataset[0][-1]))
        return head
    #print(feature)
    feature_node = Node(feature[0], feature[1], head.depth+1, True, False, [], False, None)
    head.children.append(feature_node)
    new_datasets = reduce_dataset(feature, dataset)
    for new_dataset in new_datasets:
        if find_entropy(new_dataset) == 0:
            feature_node.children.append(Node(new_dataset[0][feature[1]], feature[1], feature_node.depth+1, False, True, [], False, new_dataset[0][-1]))
        else:
            #print(new_dataset)
            new_node = Node(new_dataset[0][feature[1]], feature[1], feature_node.depth+1, False, False, [], False, None)
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
    best_feature, ig = max(ig_values, key=lambda x: x[1])
    if ig == 0:
        return None
    else:
        return best_feature

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

#given a set of data, check if they all have the same classification
#return type: boolean
def all_same_classification(TRAINING):
    classification = TRAINING[0][-1]
    for data_value in TRAINING:
        if data_value[-1] != classification:
            return True
    return False

#given a set of data, delete any rows that contain a ?
#return type: new dataset
def drop_missing_data(dataset):
    new_dataset = list()
    for data_value in dataset:
        if '?' not in data_value:
            new_dataset.append(data_value)
    return new_dataset

#given a fully created decision tree and a data value, return the classification of that data value according to the tree
#return type: outcome
def classify(data_value, head):
    current = head.children[0]
    while current.is_leaf != True:
        if current.is_feature:
            found_child = False
            for child in current.children:
                if child.name == data_value[current.name_index]:
                    current = child
                    found_child = True
                    break
                #randomly pick way in tree to go
            if not found_child:
                current = random.choice(current.children)
        else:
            current = current.children[0]
    return current.outcome

#given a list of features, data to extract a training set from, a test set, and other logistic info, creating a learning curve
#return type: [(size, accuracy), ...]
def create_learning_curve(features, dataset, TEST, min_train_size, max_train_size, train_step):
    accuracies = list()
    for SIZE in range(min_train_size, max_train_size, train_step):
        print(SIZE)
        TRAINING = random.sample(dataset, SIZE)
        while not all_same_classification(TRAINING):
            TRAINING = random.sample(dataset, SIZE)
        head = generate_tree(features, TRAINING, Node('Start', -1, -1, False, False, [], True, None))
        num_correct = 0
        for test_value in TEST:
            if classify(test_value, head) == test_value[-1]:
                num_correct += 1
        accuracies.append((SIZE, num_correct/len(TEST)))
    return accuracies

#given a list of features and a dataset, create a new dataset where the ? are replaced with the most frequent value for that specific classification
#return type: dataset
def replace_missing(features, dataset):
    frequency_dict = dict()
    for data_value in dataset:
        if data_value[-1] not in frequency_dict.keys():
            frequency_dict[data_value[-1]] = dict()
            for feature_name, index in features:
                frequency_dict[data_value[-1]][feature_name] = dict()
        for count, feature in enumerate(features):
            if data_value[count] == '?':
                continue
            if data_value[count] not in frequency_dict[data_value[-1]][feature[0]].keys():
                frequency_dict[data_value[-1]][feature[0]][data_value[count]] = 1
            else:
                frequency_dict[data_value[-1]][feature[0]][data_value[count]] += 1
    print(frequency_dict)
    new_dataset = list()
    for data_value in dataset:
        while '?' in data_value:
            classification = data_value[-1]
            feature_index = data_value.index('?')
            feature = features[feature_index][0]
            value_list = [(key, value) for key, value in frequency_dict[classification][feature].items()]
            new_value = max(value_list, key=lambda x: x[1])[0]
            data_value = list(data_value)
            data_value[feature_index] = new_value
            data_value = tuple(data_value)
        new_dataset.append(data_value)
    return new_dataset


#get command line arguments
filename = sys.argv[1]
test_size = int(sys.argv[2])
min_train_size = int(sys.argv[3])
max_train_size = int(sys.argv[4])
train_step = int(sys.argv[5])

#read in values from csv and store in features and dataset variables
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

#randomly select test set
random.shuffle(dataset)
TEST = dataset[-test_size:]

#create curve
start = time.perf_counter()
accuracies = create_learning_curve(features, dataset, TEST, min_train_size, max_train_size, train_step)
end = time.perf_counter()
print(f'Time: {end - start}')

#create graph
x_values = [item[0] for item in accuracies]
y_values = [item[1] for item in accuracies]
plt.scatter(x_values, y_values)
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy")
plt.show()
