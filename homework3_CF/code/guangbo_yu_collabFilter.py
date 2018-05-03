import numpy as np
import math
import sys


def pearson_correlation(user1, user2):
    common_movie = set(user1.keys()).intersection(user2.keys())
    user1_sum = 0
    user2_sum = 0
    n = 0
    sum = 0
    squa_sum_1 = 0
    squa_sum_2 = 0
    for movie in common_movie:
        user1_sum += user1[movie]
        user2_sum += user2[movie]
        n += 1
    user1_avg = user1_sum/n
    user2_avg = user2_sum/n

    for movie in common_movie:
        rate1 = (user1[movie] - user1_avg)
        rate2 = (user2[movie] - user2_avg)
        sum += (rate1 * rate2)
        squa_sum_1 += ((user1[movie] - user1_avg) ** 2)
        squa_sum_2 += ((user2[movie] - user2_avg) ** 2)
    l2_sum1 = math.sqrt(squa_sum_1)
    l2_sum2 = math.sqrt(squa_sum_2)
    if l2_sum1*l2_sum2 == 0:
        pearson = -2
    else:
        pearson = sum / (l2_sum1 * l2_sum2)
    return pearson


def K_nearest_neighbors(user1, k, user, item):
    user_name = []
    for name in user.keys():
        if user1 == name:
            continue
        movie = user[name].get(item)
        if movie:
            user_name.append(name)

    neighbors = []
    for name in user_name:
        pearson = pearson_correlation(user[user1], user[name])
        pair = [name, pearson]
        neighbors.append(pair)

    neighbors = sorted(neighbors, key=lambda rate: rate[1], reverse = True)

    return neighbors[0:k]


def Predict(user1, item, k_nearest_neighbors, user):
    avg1 = np.mean(user1.values())
    sum_up = 0
    sum_down = 0
    for i in k_nearest_neighbors:
        user_name = i[0]
        w = i[1]

        sum = 0
        n = 0
        common_movie = set(user1.keys()).intersection(user[user_name].keys())
        for j in common_movie:
            sum += user[user_name][j]
            n += 1
        avg = sum/n

        rate = user[user_name].get(item)
        if rate:
            sum_up += (rate - avg) * w
            sum_down += np.abs(w)

    predict = avg1 + (sum_up / sum_down)
    return predict


def main():
    filename = sys.argv[1]
    user_name = sys.argv[2]
    target_movie = sys.argv[3]
    k = int(sys.argv[4])
    lines = file(filename).readlines()
    users = dict()
    for line in lines:
        attr = line.split("\t")
        user_id, trating, tmovie_title = attr
        tmovie_title = tmovie_title.split('\n')[0]
        rating = {tmovie_title : float(trating)}
        users.setdefault(user_id, [])
        users[user_id].append(rating)

    users_new = dict()
    for i in users.keys():
        d = dict()
        item = users[i]
        for j in item:
            d = dict(d, **j)
        users_new.setdefault(i, dict)
        users_new[i] = d
    neighbors = K_nearest_neighbors(user_name, k, users_new, target_movie)
    for i in neighbors:
        print i[0],i[1]

    result = Predict(users_new[user_name], target_movie, neighbors, users_new)
    print(result)


if __name__ == '__main__':
    main()

