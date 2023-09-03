from sys import stdout
import time
from environment.genetics import *
import random
from datetime import date
survivors_rate = 0.7 # số lượng sống sót
bests_rate = 0.1
mutate_chance = 0.2
pieceLimit = 1000 # số lượng tetromino chơi tối đa
number = 100 # số lượng cá thể trong 1 quần thể
batch = 20 # số lần lặp
size = 8 # số lượng thuộc tính trong hàm heuristic

survivors = create_generation(number, size)
generation = survivors

average = compute_average(survivors)
extra_var_multiplier = max((1.0-10/float(batch/2)),0)
std = list(map(lambda std: std + 0.001 * extra_var_multiplier, computeStandardDeviation(survivors)))

# for individual in generationFromDistribution(number-len(generation), size, average, std):
#     generation.append(individual)


optimal_weight = [0, [0] * size]
total_duration = 0


with open('weights/v1.txt', 'a') as file:
    file.write(f'\n--- Training start on {date.today()} -----')
    for iteration in range(0, batch):
        start_time = time.time()
        seeds = []
        for _ in range(0, 1):
            seeds.append(random.randint(0, 100000000))

        file.write("\n")
        file.write("--- Batch " + str(iteration+1) + " ---")
        file.write("\n")
        scores = []
        print(f'\nBatch {iteration+1}/{batch}')
        threads = []
        for index, indiv in enumerate(generation):
            message = "\rindiv. " + str(index+1) + "/" + str(len(generation))
            stdout.write(message)
            stdout.flush()
            scores.append([fitness(indiv, seeds, pieceLimit), indiv])
        file.write('\n')
        for value in (list(reversed(sorted(scores, key=itemgetter(0))))):
            file.write(str(value) + '\n')
    
        survivors_score, survivors = select_survivors(scores, int(len(scores)*survivors_rate))
        if survivors_score[0] > optimal_weight[0]:
            optimal_weight = [survivors_score[0], survivors[0]]
        # file.write(len(bests))
        generation = survivors
        file.write("average: " + str(compute_average(generation)))
        duration = time.time() - start_time
        file.write(f'\ntrain for generation {iteration+1} take {duration} seconds')
        total_duration += duration
        fill_generation(generation, survivors, bests_rate, mutate_chance, number)
        np.save('weights/continue_train.npy', generation)
    file.write(f'\ntotal time for training: {total_duration} seconds')
np.save('weights/optimal.npy', optimal_weight)
