from functools import reduce
import random, os, numpy as np
import statistics
from operator import itemgetter
from threading import Thread
from tetris import Tetris

def create_individual(size):
    result = []
    for i in range(0, size):
        result.append(random.uniform(-10, 10))
    return result

def create_generation(number, size):
    population = []
    continue_train_path = "weights/continue_train.npy"
    if os.path.exists(continue_train_path):
        population = np.loadtxt(continue_train_path).tolist()
    while len(population) < number:
        tmp = create_individual(size)
        population.append(tmp)
    return population

def individualFromDistribution(size, average, std):
    result = []
    for i in range(0, size):
        result.append(random.normalvariate(average[i], std[i]))
    return result

def generationFromDistribution(number, size, average, std):
    results = []
    for i in range(0, number):
        tmp = individualFromDistribution(size, average, std)
        results.append(tmp)
    return results

def mutate(x):
    for i in range(len(x)):
        if random.uniform(0, 1) > 0.6:
            x[i] = random.uniform(-10, 10)
    return x

def cross_over(x, y): # lai chéo giữa các  cá thể bố mẹ.
    result = []
    for i in range(0, len(x)):
        if random.uniform(0, 1) > 0.5:
            result.append(y[i])
        else:
            result.append(x[i])
    return result

def compute_average(population): # tính trung bình các giá trị heuristic của quần thể
    result = list(reduce(lambda i1, i2: [a+b for a,b in zip(i1, i2)], population))
    result = list(map(lambda x: x/len(population), result))
    return result

def computeStandardDeviation(population):
    average = compute_average(population)
    result = [[] for _ in range(0, len(population[0]))]
    for individual in population:
        for index, weight in enumerate(individual):
            result[index].append(weight)
    result = list(map(lambda weights: statistics.stdev(weights), result))
    return result

def select_survivors(scores, number): # chọn ra number cá thể tốt nhất
    bests = list(reversed(sorted(scores, key=itemgetter(0))))[0:number]
    return list(map(lambda x: x[0], bests)), list(map(lambda x: x[1], bests))

def fill_generation(generation, survivors, best_rate, mutate_chance, number):
    while len(generation) < number:
        individual = cross_over(*random.sample(survivors[:int(best_rate * number)], k=2))
        if random.uniform(0, 1) < mutate_chance:
            individual = mutate(individual)
        generation.append(individual)

def run_with_thread(results, display, seed, individual, pieceLimit):
    res = Tetris(display=display, user=False, seed=seed).run(individual, pieceLimit)
    results.append(res)

def fitness(individual, seeds, pieceLimit): # hàm fitness bằng trung bình cộng các điểm qua các lần chơi của 1 cá thể
    results, threads = [], []
    for seed in seeds:
        thread = Thread(target=run_with_thread, args=(results, False, seed, individual, pieceLimit))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return int(sum(results)/len(results))



