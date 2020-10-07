FILE_NAME = "things.txt"
POPULATION_SIZE = 100
RUCKSACK_VOLUME = 250
BORDER = 0.3
ITERATIONS = 1000
MUTATION_CHANCE = 0.05

import random





class Thing:
    def __init__(self, cost, weight):
        self.cost = cost
        self.weight = weight

    def __repr__(self):
        return f"Thing: cost={self.cost}; weight={self.weight}"


class Solution:
    all_things = []
    def __init__(self, vector=[], total_cost=0, total_weight=0):
        self.vector = vector
        self.total_cost = total_cost
        self.total_weight = total_weight

    def __repr__(self):
        return f"Solution: vector={self.vector}; total_cost={self.total_cost}; total_weight={self.total_weight}"

    @classmethod
    def create_array_things(cls, file_name):
        with open(file_name) as f:
            for line in f:
                cost, weight = line.split()
                thing = Thing(int(cost), int(weight))
                cls.all_things.append(thing)
        print("Created all things")


    def find_total_cost(self):
        self.total_cost = 0
        for idx in range(len(self.vector)):
            if self.vector[idx] == 1:
                c = Solution.all_things[idx].cost
                self.total_cost += c


    def find_total_weight(self):
        self.total_weight = 0
        for idx in range(len(self.vector)):
            if self.vector[idx] == 1:
                w = Solution.all_things[idx].weight
                self.total_weight += w


    def mutation(self):
        idx1 = random.randint(0, len(self.vector)-1)
        idx2 = random.randint(0, len(self.vector)-1)
        while idx1 == idx2:
            idx2 = random.randint(0, len(self.vector)-1)

        self.vector[idx1], self.vector[idx2] = self.vector[idx2], self.vector[idx1]
        self.find_total_cost()
        self.find_total_weight()
        
        # If mutation is bad get changes back
        if self.total_weight > RUCKSACK_VOLUME:
            self.vector[idx1], self.vector[idx2] = self.vector[idx2], self.vector[idx1]
            self.find_total_cost()
            self.find_total_weight()

    # My local upgrade is in putting 1 to random place and checking if it fits
    def local_upgrade(self):
        idx = random.randint(0, len(self.vector)-1)
        if self.vector[idx] == 0:
            if self.total_weight + Solution.all_things[idx].weight <= RUCKSACK_VOLUME:
                self.vector[idx] = 1
                self.total_weight += Solution.all_things[idx].weight
                self.total_cost += Solution.all_things[idx].cost
            



# This works    
# Solution.create_array_things(FILE_NAME)
# print(Solution.all_things)

####### population generation
def generate_population(amount):
    population = []
    for number in range(amount):
        vector = [0 for _ in range(len(Solution.all_things))]
        vector[number] = 1
        vector[random.randint(0, len(vector)-1)] = 1
        s = Solution(vector)
        s.find_total_cost()
        s.find_total_weight()
        population.append(s)

    print(f"Population of {amount} generated")
    return population

# Find out the solution with least cost
# Returns index, total_cost of least solution
def find_least_solution(population):
    least_cost = None
    least_sol_idx = None 
    for idx in range(len(population)):
        if least_cost is None:
            least_cost = population[idx].total_cost
            least_sol_idx = idx
            continue
        
        if population[idx].total_cost < least_cost:
            least_cost = population[idx].total_cost
            least_sol_idx = idx

    return least_sol_idx, least_cost

def find_best_solution(population):
    best_cost = None
    best_sol_idx = None 
    for idx in range(len(population)):
        if best_cost is None:
            best_cost = population[idx].total_cost
            best_sol_idx = idx
            continue
        
        if population[idx].total_cost > best_cost:
            best_cost = population[idx].total_cost
            best_sol_idx = idx

    return best_sol_idx, best_cost


# Cross two solutions and get new
# Returns a new solution
def cross_solutions(s1, s2, border=BORDER):
    new_s1_vector = s1.vector[:int(border*len(s1.vector))] + s2.vector[int(border*len(s2.vector)):]
    new_s2_vector = s2.vector[:int(border*len(s2.vector))] + s1.vector[int(border*len(s1.vector)):]
    
    new_s1 = Solution(new_s1_vector)
    new_s1.find_total_cost()
    new_s1.find_total_weight()

    new_s2 = Solution(new_s2_vector)
    new_s2.find_total_cost()
    new_s2.find_total_weight()

    if new_s1.total_weight > RUCKSACK_VOLUME and new_s2.total_weight > RUCKSACK_VOLUME:
        return None
    elif new_s2.total_weight > RUCKSACK_VOLUME:
        return new_s1
    elif new_s1.total_weight > RUCKSACK_VOLUME:
        return new_s2
    elif new_s1.total_cost >= new_s2.total_cost:
        return new_s1
    elif new_s2.total_cost > new_s1.total_cost:
        return new_s2

# Random from 0 to 1
def random_number():
    return random.random()



def genetic_algorithm():

    # Create all things
    Solution.create_array_things(FILE_NAME)
    # Generate population
    population = generate_population(POPULATION_SIZE)
    # print(population)

    for iteration in range(ITERATIONS):
        # Let's cross best and random solutions
        best_idx, best_cost = find_best_solution(population)
        rand_idx = random.randint(0, len(population)-1)

        if (iteration+1)%20 == 0:
            print(f"Iteration {iteration+1}: Cost={best_cost}")
        
        while rand_idx == best_idx:
            rand_idx = random.randint(0, len(population)-1)

        best_sol = population[best_idx]
        rand_sol = population[rand_idx]

        new_sol = cross_solutions(best_sol, rand_sol)
        if new_sol is not None:
            if random_number() < MUTATION_CHANCE: 
                new_sol.mutation()

            new_sol.local_upgrade()

            population.append(new_sol)
            least_sol_idx, least_cost = find_least_solution(population)
            population.pop(least_sol_idx)

        

    # All iterations completed
    best_idx, best_cost = find_best_solution(population)
    best_sol = population[best_idx]
    print(best_sol)


genetic_algorithm()


