import random
import copy
import math

NUM_CUSTOMERS = 50 
NUM_VEHICLES = 10
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000

customers = [(random.randint(0,100), random.randint(0,100)) for i in range(NUM_CUSTOMERS)]
depot = (0,0)

# Route class to represent a gene 
class Route:
  def __init__(self):
    self.route = []
    self.load = 0
    self.distance = 0
  
  def add_customer(self, customer):
    self.route.append(customer)
    self.load += customer[0]
    self.distance += math.sqrt((customer[1] - depot[1])**2 + (customer[0] - depot[0])**2)
      
  def fitness(self):
    return 1/self.distance
  
# Generate initial population  
population = [Route() for i in range(POPULATION_SIZE)]
for route in population:
  while len(route.route) < NUM_CUSTOMERS//NUM_VEHICLES:
    random_customer = random.choice(customers)
    if route.load + random_customer[0] <= 100:  
      route.add_customer(random_customer)
      customers.remove(random_customer)

# Genetic algorithm     
for generation in range(MAX_GENERATIONS):

  # Evaluate fitness
  for route in population:
    route.fitness()
    
  # Select parents  
  parents = random.choices(population, weights=[r.fitness() for r in population], k=POPULATION_SIZE)
  
  # Breed new generation
  children = []
  while len(children) < POPULATION_SIZE:
    child1, child2 = random.sample(parents, 2)
    child = breed(child1, child2)
    children.append(child)

  # Replace population  
  population = children
 
# Print best route  
fitnesses = [route.fitness() for route in population]
best_route = population[fitnesses.index(max(fitnesses))]
print(best_route.route)