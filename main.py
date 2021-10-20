import math
from tkinter import *
import random
from itertools import permutations
from scipy.spatial import distance

root = Tk()
root.title("Найду Вам оптимальный путь")

N = 9
root.geometry(str(N*100) + "x" + str(N*100))

my_canvas = Canvas(root, width=N*100, height=N*100, bg="black")
my_canvas.pack(pady=1)


recordDistance = 0
# matrix = [[randrange(N * 100) for i in range(2)] for j in range(N)]
matrix = [[658, 791], [258, 286], [31, 701], [883, 522], [142, 578], [585, 740], [741, 21], [279, 97], [196, 636]]
firstOrder = list(range(0, N))
perm = []
bestPerm = []
print(matrix)


def lexicographical_permutation(arr):
    global perm
    str_arr = [str(x) for x in arr]
    arr_str_perm = sorted(list(integer) for integer in permutations(str_arr))

    for y in arr_str_perm:
        perm += [list(map(int, y))]


def find_optimal_path():
    global recordDistance, bestPerm
    first_time = True
    for p in perm:
        dist = 0
        for idx in p:
            if idx + 1 < len(matrix):
                a = (matrix[p[idx]][0], matrix[p[idx]][1], 0)
                b = (matrix[p[idx + 1]][0], matrix[p[idx + 1]][1], 0)
                dist += distance.euclidean(a, b)
        if first_time:
            recordDistance = dist
            bestPerm = p
            first_time = False
        elif dist < recordDistance:
            recordDistance = dist
            bestPerm = p
        # print(p)
        # print(dist)


def create_dot(x, y, idx, offset):
    my_canvas.create_oval(x - 2 - offset, y - 2 - offset, x + 2 - offset, y + 2 - offset, fill="red")
    my_canvas.create_text(x - 10, y + 10, anchor=W, font="Purisa",
                          text=idx, fill="yellow")


def draw_path(color, path, offset):
    for i, coords in enumerate(matrix):
        create_dot(coords[0], coords[1], i, offset)
    for idx in range(len(path)):
        if idx + 1 < len(path):
            my_canvas.create_line(matrix[path[idx]][0] - offset, matrix[path[idx]][1] - offset,
                                  matrix[path[idx + 1]][0] - offset, matrix[path[idx + 1]][1] - offset,
                                  fill=color)


# lexicographical_permutation(firstOrder)
# find_optimal_path()

# bestPerm = [0, 2, 3, 1, 4]
# recordDistance = 678.3042142670913

bestPerm = [3, 0, 5, 8, 2, 4, 1, 7, 6]
recordDistance = 2157.9982622423195

print(bestPerm)
print(recordDistance)
draw_path('white', bestPerm, 0)

GenOrder = list(range(0, N))
popSize = 200
# тут вариации GenOrder
population = []
bestPopulation = []
recordGenDistance = math.inf

fitness = []


def generate_population():
    global population
    for pop in range(popSize):
        random.shuffle(GenOrder)
        population += [GenOrder.copy()]


def calculate_fitness():
    global fitness, recordGenDistance, bestPopulation
    for pop in population:
        dist = 0
        for val, idx in enumerate(pop):
            if idx + 1 < len(matrix):
                a = (matrix[pop[idx]][0],     matrix[pop[idx]][1],     0)
                b = (matrix[pop[idx + 1]][0], matrix[pop[idx + 1]][1], 0)
                dist += distance.euclidean(a, b)
        fitness += [1/dist]
        if dist < recordGenDistance:
            bestPopulation = pop
            recordGenDistance = dist


def normalize_fitness():
    fit_sum = sum(fitness.copy())
    for idx in range(len(fitness)):
        fitness[idx] = fitness[idx]/fit_sum


def select_population(arr, prop):
    index = 0
    r = random.randrange(1)
    while r > 0:
        r = r - prop[index]
        index += 1
    index -= 1
    return arr[index].copy()


def mutate(arr):
    for _ in range(N):
        if random.random() < 0.2:
            idx_a = random.randrange(len(arr))
            idx_b = (idx_a + 1) % N
            temp = arr[idx_a]
            arr[idx_a] = arr[idx_b]
            arr[idx_b] = temp
    return arr


def cross_over(arr_a, arr_b):
    start = random.randrange(len(arr_b))
    if start + 1 == len(arr_a):
        return arr_a
    end = random.randrange(start + 1, len(arr_a))
    new_order = arr_a[start:end + 1].copy()
    for idx in range(len(arr_b)):
        if arr_b[idx] not in new_order:
            new_order += [arr_b[idx]]
    return new_order


def next_generation():
    global population
    new_pop = []
    for _ in range(popSize):
        pop_a = select_population(population, fitness)
        pop_b = select_population(population, fitness)
        cross_pop = cross_over(pop_a, pop_b)
        mutate(cross_pop)
        new_pop += [cross_pop]
    population = new_pop


generate_population()
calculate_fitness()
normalize_fitness()

why = 0
for why in range(500):
    next_generation()
    calculate_fitness()
    normalize_fitness()
    print(recordGenDistance)

print(bestPopulation)
print(recordGenDistance)
draw_path('green', bestPopulation, 10)
root.mainloop()
