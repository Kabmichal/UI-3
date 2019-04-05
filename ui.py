import random
import numpy as np
import matplotlib.pyplot as plt

def number_of_population():
    return 100


def gems():
    return [11, 16, 27, 29, 39]


def load_map():
    map_size = 7
    start_position = 45
    return start_position, map_size


def incrementation(array, position):
    if array[position] == 256:
        array[position] = 0
    else:
        array[position] += 1
    return array


def decrementation(array, position):
    if array[position] == 0:
        array[position] = 256
    else:
        array[position] -= 1
    return array


def jump(array, position):
    new_position = array[position] & 63
    return new_position, array


def output(array, position, move_array, actual_position, size_of_map):
    next_move = array[position] & 3
    if next_move == 0:
        actual_position += size_of_map
        move_array.append(actual_position)
    elif next_move == 1:
        actual_position -= size_of_map
        move_array.append(actual_position)
    elif next_move == 2:
        actual_position -= 1
        move_array.append(actual_position)
    elif next_move == 3:
        actual_position += 1
        move_array.append(actual_position)
    return actual_position, move_array


def generate():
    """
    generovanie zakladnej populacie
    :return: vratenie pola o velkosti 64 s cislami od 0 do 255
    """
    return np.random.randint(0, 255, 64)


def convert(position, size_of_map):
    return position // size_of_map, position % size_of_map


def check(old_position, new_position, move_array, size_of_map):
    prev_x, prev_y = convert(old_position, size_of_map)
    next_x, next_y = convert(new_position, size_of_map)
    number = move_array[-1]
    if number < 0 or number > size_of_map * size_of_map - 1 or prev_x != next_x and prev_y != next_y:
        return True
    return False


def move(start_position, array, size_of_map):
    """

    :param start_position:
    :return:
    """
    actual_position = start_position
    position = 0
    move_array = []
    f_value = array[position] >> 6
    moves = 0
    gem = gems()
    """
    prvych 500 iteracii po nich sa dany genofond skonci
    """
    while moves != 500:
        """
        ak presiahnem 8 bitov
        """
        if array[position] > 255:
            array[position] %= 255
        """
        kontrolovanie prvych 2 bitov, podla nich viem co sa ma vykonat
        """
        new_position = array[position] & 63

        if f_value == 0:
            array = incrementation(array, new_position)
        elif f_value == 1:
            array = decrementation(array, new_position)
        elif f_value == 3:
            old_position = actual_position
            actual_position, move_array = output(array, new_position, move_array, actual_position, size_of_map)
            if check(old_position, actual_position, move_array, size_of_map):
                move_array.pop()
                break

            count = 0
            for i in gem:
                if i in move_array:
                    count += 1
            if count == gem.__len__():
                break

        if f_value == 2:
            position, array = jump(array, position)
        else:
            position += 1
            if position > 63:
                position = 0
        f_value = array[position] >> 6
        moves += 1
    return move_array


def first_population(number):
    """
    vygenerovanie prvych 20 jednotiek populacie
    :return: vygenerovanych prvych 20 jedincov s genami
    """
    input_array = []
    for i in range(number):
        input_array.append(generate())
    return input_array


def fitness(arrays):
    fitnes = 1
    start_position, map_size = load_map()
    gem = gems()
    array = move(start_position, arrays.copy(), map_size)
    for i in gem:
        if i in array:
            fitnes += 1
    if array.__len__() > map_size * map_size:
        fitnes -= (array.__len__() * map_size * 0.001)
    if fitnes == gem.__len__() + 1:
        print("cesta je: ")
        for i in array:
            print("(", i // map_size, i % map_size, ")")
            if i in gem:
                print("zobral som poklad cislo ", i)

    return fitnes


def generate_position(old_generation, total_sum):
    counter = -1
    new_sum = 0
    list_1 = random.randint(0, int(total_sum))
    for m in old_generation:
        counter += 1
        new_sum += m[0]
        if new_sum >= list_1:
            return counter


def roulete(old_generation, count):
    old_generation = sorted(old_generation.copy(), key=lambda x: x[0], reverse=True)
    total_sum = 0
    new_generation = []
    pom_array = []
    for i in old_generation:
        total_sum += i[0]
    #print("priemerna fitness", total_sum / old_generation.__len__())
    for i in range(count):
        list_1 = generate_position(old_generation, total_sum)
        list_2 = generate_position(old_generation, total_sum)
        for j in range(32):
            pom_array.append(old_generation[list_1][1][j])
        for k in range(32, 64):
            pom_array.append(old_generation[list_2][1][k])
        new_generation.append(pom_array)
        pom_array = []
    return new_generation,total_sum

def top_population_first(new_generation, counter):
    """
    funkcia vrati to counter jedincov
    :param new_generation: pole jedincov
    :param counter: pocet kolko najlepsich jedincov ma byt vybratych
    :return: top counter jedincov
    """
    new_population = []
    help_array = sorted(new_generation.copy(), key=lambda x: x[0], reverse=True)
    for i in range(counter):
        new_population.append(help_array[i].copy())
   # for i in range(15):
       # print("Toto su top jedinci ",help_array[i][0])
    return new_population

def top_population(new_generation, counter):
    """
    funkcia vrati to counter jedincov
    :param new_generation: pole jedincov
    :param counter: pocet kolko najlepsich jedincov ma byt vybratych
    :return: top counter jedincov
    """
    new_population = []
    help_array = sorted(new_generation.copy(), key=lambda x: x[0], reverse=True)
    for i in range(counter):
        new_population.append(help_array[i][1].copy())
       # print("pridavam pole s ohodnotenim",help_array[i][0])
   # print(new_population)
    return new_population

def fill_with_random(new_generation,mutation):
    pom_array = []
    new_population = []
    for i in new_generation:
        probability = random.randint(0,100)
        if probability < mutation:
            random_number = random.randint(0, 256)
            for m in range(64):
                k=random.randint(0,1)
                if k==0:
                    new_number = i[m] + random_number
                    if new_number > 255:
                        new_number %= 256
                else:
                    new_number=i[m]
                pom_array.append(new_number)
            new_population.append(pom_array)
            pom_array = []
        else:
            new_population.append(i)
    return new_population,mutation



def roulete_test():
    population = 1
    graph_sum = []
    graph_population = []
    top_members = []
    mutation = 20
    number = number_of_population()
    input_arrays = first_population(number)
    rated_generation = []

    for i in range(number):
        rated_generation.append([fitness(input_arrays[i]), input_arrays[i]])
    sorted_array = sorted(rated_generation.copy(), key=lambda x: x[0], reverse=True)
    best_fitness = sorted_array[0][0]
    gem = gems().__len__()

    while best_fitness != gem + 1:
        population += 1
        new_generation = []
        help_array, total_sum = roulete(rated_generation, number-5)

        for i in help_array:
            new_generation.append(i)
        help_array,mutation=fill_with_random(new_generation,mutation)
        new_generation=[]
        for i in help_array:
            new_generation.append(i)
        help_array = top_population_first(rated_generation, 5)  # funkcia vrati top x jedincov

        for i in help_array:
            top_members.append(i.copy())
        top_members = sorted(top_members, key=lambda x: x[0], reverse=True)
        help_array = top_population(top_members,5)

        for i in help_array:
            new_generation.append(i)
        rated_generation=[]
        for i in range(number):
            rated_generation.append([fitness(new_generation[i]), new_generation[i]])
        rated_generation = sorted(rated_generation, key=lambda x: x[0], reverse=True)
        best_fitness = rated_generation[0][0]

        print("max fitness ", best_fitness, "priemerna fitness ", total_sum/number, "mutacia ",mutation,"populacia", population)
        if best_fitness == gem + 1:
            break
        graph_sum.append(total_sum / number)
        graph_population.append(population)
        if population>2 and mutation < 55:
            if abs(graph_sum[-2] - graph_sum[-1]) > 0.20 :
                mutation -= 1
            else:
                mutation+=1
        elif population>2 and mutation == 0:
            mutation+=1
    print("ciel dosiahnuty na ", population, "tu generaciu")
    return graph_population, graph_sum

def draw_graph():
    generation,total_sum=roulete_test()
    plt.plot(generation,total_sum)
    plt.show()


draw_graph()