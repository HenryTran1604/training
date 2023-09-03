from environment.genetics import *
# generation = []
# number = 10
# survivors = create_generation(5, 4)
# print('-----------------------------')
# bests_rate = 0.5
# while len(generation) < number:
#     par = random.sample(survivors[:int(bests_rate * number)], k=2)
#     print(*par, sep='\n')
#     individual = cross_over(*par)
#     print('cross:', individual)
#     if random.uniform(0, 1) < 0.05:
#         individual = mutate(individual)
#         print('mutate: ', individual)
#     # print(individual)
#     generation.append(individual)

print(cross_over([0.01, 0.01, 0.1, 0.05], [0.09, -0.08, 0.07, 0.06]))
