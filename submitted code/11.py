import random
import time


time_limit = 8

start_time = time.time()

# my birthday :D
SEED = 110404 # seed for random number generator for reproducibility

random.seed(SEED)


class Truck:
    def __init__(self, idx):
        self.idx = idx
        self.route = [0]
        self.cost = 0

class Solver:

    def __init__(self, file = ""):
        self.read(file)
        self.reset()
        self.prev_truck = -1
    
    def reset(self):
        self.trucks = [Truck(i) for i in range(self.K)]

        self.combinations = [None for _ in range(self.K)]

        self.origin_reqs = [i for i in range(1, self.N+1)]
        self.attemp = 0

    def read(self, file):
        if file == "":
            readline_command = input
        else:
            f = open(file, 'r')
            readline_command = f.readline

        self.N, self.K = map(int, readline_command().split())
        self.distance_matrix = [list(map(int, readline_command().split())) for _ in range(self.N + 1)]

        if file != "":
            f.close()

    def greedy(self):
        while self.reqs:
            combination = self.best_insert_combination()

            truck_idx = combination['truck_idx']
            route_idx = combination['idx']
            req = combination['req']
            cost = combination['cost']

            self.trucks[truck_idx].route.insert(route_idx, req)
            self.reqs.remove(req)
            
            for i in range(self.K):
                if self.combinations[i]['req'] == req or self.combinations[i]['truck_idx'] == truck_idx:
                    self.combinations[i] = None

            self.trucks[truck_idx].cost = cost
        
    
    def best_insert_combination(self):
        for i in range(self.K):

            if self.combinations[i] == None:
                min_cost = float('inf')
                results = []

                for j in range(1, len(self.trucks[i].route)+1):
                    req = min(self.reqs, key=lambda x: self.insert_cost(i, j, x))
                    current_cost = self.insert_cost(i, j, req)

                    if current_cost == min_cost: # if there are multiple minimum cost
                        results.append({
                            'req': req,
                            'idx': j,
                        })

                    if current_cost < min_cost: # if there is a new minimum cost
                        min_cost = current_cost
                        results = []
                        results.append({
                            'req': req,
                            'idx': j,
                        })
                        
                result = random.choice(results)

                route_idx = result['idx']
                req = result['req']

                min_cost = self.insert_cost(i, route_idx, req)

                combination = {
                    'req': req,
                    'truck_idx': i,
                    'idx': route_idx,
                    'cost': min_cost
                }
                self.combinations[i] = combination
        
        return min(self.combinations, key=lambda x: x['cost'])

    def insert_cost(self, truck_idx, route_idx, node):
        if route_idx <= 0: # cannot happend but just in case
            raise ValueError("route_idx cannot be <=0")

        if (len(self.trucks[truck_idx].route) < route_idx): # just in case
            raise ValueError("route_idx cannot be greater than the length of the route")
        

        prev = self.trucks[truck_idx].route[route_idx-1]

        if (len(self.trucks[truck_idx].route) == route_idx): # if the node is inserted at the end of the route
            return self.trucks[truck_idx].cost + self.distance_matrix[prev][node]
        else: # if the node is inserted in the middle of the route
            current = self.trucks[truck_idx].route[route_idx]
            return self.trucks[truck_idx].cost - self.distance_matrix[prev][current] + self.distance_matrix[prev][node] + self.distance_matrix[node][current]

    def route_cost(self, route):
        ret = 0
        for i in range(1, len(route)):
            ret += self.distance_matrix[route[i-1]][route[i]]
        return ret

    def local_search(self):
        random_truck_idx = random.choice([i for i in range(self.K)])

        if self.prev_truck != random_truck_idx:
            self.combinations = [None for _ in range(self.K)]
        
        self.prev_truck = random_truck_idx

        current_truck = self.trucks[random_truck_idx]

        self.reqs.extend(current_truck.route[1:])

        for node_idx in range(1, len(current_truck.route)):
            temp = current_truck.route[:]
            temp.remove(current_truck.route[node_idx])

            if self.route_cost(temp) >= self.route_cost(current_truck.route):
                self.reqs.remove(current_truck.route[node_idx])
            
            if not self.reqs: # if all nodes are removed
                self.attemp += 1
                return
        
        combination = self.best_insert_combination()
        req = combination['req']
        route_idx = combination['idx']
        cost = combination['cost']
        truck_idx = combination['truck_idx']

        max_cost = max([x.cost for x in self.trucks])
        min_cost = min([x.cost for x in self.trucks])

        if cost < max_cost or (cost == max_cost and truck_idx != random_truck_idx):
            for i in range(self.K):
                if self.combinations[i]['req'] == req or self.combinations[i]['truck_idx'] == truck_idx:
                    self.combinations[i] = None
            self.trucks[truck_idx].route.insert(route_idx, req)
            self.trucks[random_truck_idx].route.remove(req)

            self.trucks[truck_idx].cost = cost
            self.trucks[random_truck_idx].cost = self.route_cost(self.trucks[random_truck_idx].route)

            new_max_cost = max([x.cost for x in self.trucks])
            new_min_cost = min([x.cost for x in self.trucks])

            if max_cost == new_max_cost and min_cost == new_min_cost:
                self.attemp += 1
            else:
                self.attemp = 0

            self.reqs.clear()
        else:
            self.reqs.clear()
            self.attemp += 1


    def solve(self):
        if self.N <= 200:
            max_attemp = 5

            max_cost = float('inf')
            for _ in range(20):
                self.reset()
                
                n = min(10, self.N)

                for _ in range(n):
                    self.reqs = random.sample(self.origin_reqs, self.N//n)
                    for j in self.reqs:
                        self.origin_reqs.remove(j)
                    self.greedy()
                
                self.reqs = self.origin_reqs
                self.greedy()

                while True:
                    if self.attemp >= max_attemp:
                        break

                    self.local_search()

                current_max_cost = max([x.cost for x in self.trucks])
                if current_max_cost < max_cost:
                    max_cost = current_max_cost
                    self.best_routes = [x.route for x in self.trucks]
        else:
            n = 10
            for _ in range(n):
                self.reqs = random.sample(self.origin_reqs, self.N//n)
                for j in self.reqs:
                    self.origin_reqs.remove(j)
                self.greedy()
            
            self.reqs = self.origin_reqs
            self.greedy()
            
            while time.time() - start_time < time_limit:
                self.local_search()
            
            self.best_routes = [x.route for x in self.trucks]
            
            
    def write(self, file = ""):
        ans = str(self.K) + "\n"
        for route in self.best_routes:
            ans += str(len(route)) + "\n"
            ans += " ".join(map(str, route)) + "\n"

        if file == "":
            print(ans)
        else:
            with open(file, 'w') as f:
                f.write(ans)

def main():
    inp_file = ""
    out_file = ""

    solver = Solver(inp_file)

    solver.solve()

    solver.write(out_file)


if __name__ == "__main__":
    main()
