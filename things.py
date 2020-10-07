from random import randint


NUM_THINGS = 100
MIN_COST = 2
MAX_COST = 30
MIN_WEIGHT = 1
MAX_WEIGHT = 25

"""
Generates a file containing things
Rule:
cost1 weight1
cost2 weight2
...
"""
def generate_things(file_name):
    with open(file_name, "w") as f:
        for _ in range(NUM_THINGS):
            cost = randint(MIN_COST, MAX_COST)
            weight = randint(MIN_WEIGHT, MAX_WEIGHT)
            f.write(f"{cost} {weight}\n")

    print(f"Generated {NUM_THINGS} things to file {file_name}")


generate_things("things.txt")
