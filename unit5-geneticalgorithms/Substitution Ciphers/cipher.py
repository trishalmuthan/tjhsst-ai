import time
import random
import sys
from math import log

#Given a string cipher alphabet, return a dictionary of letter:sub letter
def create_cipher_dict(cipher_alphabet):
    cipher_dict = dict()
    for count, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        cipher_dict[letter] = cipher_alphabet[count]
    return cipher_dict

def create_inv_cipher_dict(cipher_alphabet):
    cipher_dict = dict()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for count, letter in enumerate(cipher_alphabet):
        cipher_dict[letter] = alphabet[count]
    return cipher_dict

#Given a block of text and cipher alphabet, return the encrypted text
def encode(text, cipher_alphabet):
    cipher_dict = create_cipher_dict(cipher_alphabet)
    return ''.join(cipher_dict[letter] if letter in cipher_dict.keys() else letter for letter in text.upper())

#Given an encrypted text and cipher alphabet, return the decrypted text
def decode(encrypted_text, cipher_alphabet):
    inv_cipher_dict = create_inv_cipher_dict(cipher_alphabet)
    return ''.join(inv_cipher_dict[letter] if letter in inv_cipher_dict.keys() else letter for letter in encrypted_text.upper())

#Given an n, encoded text block, and cipher alphabet, return fitness value, decoded text
def fitness(n, encoded_text, cipher_alphabet):
    #decode given encoded_text
    decoded_text = decode(encoded_text, cipher_alphabet)
    #split encoded_text into n-grams
    final_sum = 0
    n_gram_list = list()
    for i in range(0, len(decoded_text)-n+1):
        pot_ngram = decoded_text[i:i+n]
        if pot_ngram.isalpha() and pot_ngram in freq_dict.keys():#for every n-gram, if it the ngram is fully alphabet, take log of frequency and sum
            final_sum += log(freq_dict[pot_ngram], 2)
    return final_sum, decoded_text

#Given encoded text do hill climbing and print out decoded text
def basic_hill_climbing(encoded_text):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(alphabet)
    cipher_alphabet = ''.join(alphabet)
    cur_fitness, cur_decoded_message = fitness(3, encoded_text, cipher_alphabet)
    on_same = 0
    while True:
        ind_1 = random.randint(0, 25)
        ind_2 = random.randint(0, 25)
        cipher_alphabet = list(cipher_alphabet)
        cipher_alphabet[ind_1], cipher_alphabet[ind_2] = cipher_alphabet[ind_2], cipher_alphabet[ind_1]
        cipher_alphabet = ''.join(cipher_alphabet)
        new_fitness, new_decoded_message = fitness(3, encoded_text, cipher_alphabet)
        if new_fitness > cur_fitness:
            cur_fitness = new_fitness
            cur_decoded_message = new_decoded_message
            on_same = 0
        else:
            on_same += 1
        if on_same > 40000:
            print(cur_decoded_message)
            return

#Return list of n permutations of alphabet
def generate_population(n):
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    perms = set()
    while len(perms) < n:
        random.shuffle(alphabet)
        perms.add(''.join(alphabet))
    return list(perms)

def sort_old_fitness(cipher_alphabet):
    if cipher_alphabet in strategy_fitnesses.keys():
        return strategy_fitnesses[cipher_alphabet]
    else:
        fitness_score, decoded = fitness(4, text, cipher_alphabet)
        strategy_fitnesses[cipher_alphabet] = fitness_score
        return fitness_score

def sort_new_fitness(cipher_alphabet):
    return strategy_fitnesses[cipher_alphabet]

def selection(old_generation):
    new_gen = set() #new generation set
    old_generation.sort(key=sort_old_fitness, reverse=True) #sort the old generation according to fitness
    for i in range(NUM_CLONES):#add some of the old generation directly to the new generation
        new_gen.add(old_generation[i])
    while len(new_gen) < POPULATION_SIZE: #while new generation is not filled up
        all_participants = random.sample(old_generation, 2*TOURNAMENT_SIZE)#randomly get 2*tourneysize strategies
        tourney1 = all_participants[:len(all_participants)//2]#split all participants into two tourneys
        tourney2 = all_participants[len(all_participants)//2:]
        tourney1.sort(key=sort_new_fitness, reverse=True)#sort both of them by fitness
        tourney2.sort(key=sort_new_fitness, reverse=True)
        winner1, winner2 = run_tournament(tourney1, tourney2)#run the tournament and get winners
        parents = [winner1, winner2]
        random.shuffle(parents)#randomize which parent is which winner
        parent1, parent2 = parents[0], parents[1]
        child = breed(parent1, parent2)#breed the parents and get the child
        if random.random() < MUTATION_RATE:#mutate maybe
            child = mutate(child)
        new_gen.add(child)#add to new generation
    return list(new_gen)#return list form of new generation

def mutate(child):
    ind_1 = random.randint(0, 25)
    ind_2 = random.randint(0, 25)
    child = list(child)
    child[ind_1], child[ind_2] = child[ind_2], child[ind_1]#swap two random indices
    child = ''.join(child)
    return child

def breed(parent1, parent2):
    child = [None] * len(parent1)
    crossover_letters = random.sample(parent1, CROSSOVER_LOCATIONS)
    crossover_indices = [parent1.index(letter) for letter in crossover_letters]
    for index in crossover_indices:
        child[index] = parent1[index]
    for letter in parent2:
        if letter not in child:
            child[child.index(None)] = letter
    return ''.join(child)

def run_tournament(sorted_tourney1, sorted_tourney2):
    for count, cipher in enumerate(sorted_tourney1):
        if random.random() <= TOURNAMENT_WIN_PROBABILITY:
            winner1 = cipher
            break
        if count == len(sorted_tourney1)-1:
            winner1 = cipher
            break
    for count, cipher in enumerate(sorted_tourney2):
        if random.random() <= TOURNAMENT_WIN_PROBABILITY:
            winner2 = cipher
            break
        if count == len(sorted_tourney2)-1:
            winner2 = cipher
            break
    return winner1, winner2
    
def simulate():
    population = generate_population(POPULATION_SIZE)
    for i in range(500):
        population = selection(population)
        population.sort(key=sort_old_fitness, reverse=True)
        best = population[0]
        #print(i)
        print(decode(text, best))

POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 25
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

#start = time.perf_counter()

#text = """NU XTZEIMYTNEVZ INUHU YM, ZML SPYVI NXILNFFZ XNFF IVPU N API VNTD. NU PI ILTWU MLI, P XNW YM N FMWY JNZ
#JPIVMLI LUPWY NWZ MC IVNI YFZEV IVNI ITNDPIPMWNFFZ CMFFMJU 'D' NI NFF. PUW'I IVNI ULTETPUPWY? P CMLWD
#IVPU ULTETPUPWY, NWZJNZ! NW NLIVMT JVM NFUM CMLWD IVPU ULTETPUPWY, FMWY NYM, NXILNFFZ FMUI SNWZ SMWIVU
#JTPIPWY N AMMH - N CLFF CPXIPMWNF UIMTZ - JPIVMLI IVNI YFZEV NI NFF. NSNRPWY, TPYVI?"""
text = sys.argv[1]
strategy_fitnesses = dict()
freq_dict = dict()
with open('ngrams.txt') as f:
    for line in f:
        split_line = line.split()
        freq_dict[split_line[0]] = int(split_line[1])
simulate()
#end = time.perf_counter()
#print(end-start)