import sys
import math
import numpy as np
import operator


def transform(filename):
    output = []
    labelset = []
    rawoutput = []
    for i in filename.readlines():
        entry = i.split(',')
        buying, maint, doors, persons, lug_boot, safety, label = entry
        label = label.split('\r')[0]
        rawoutput.append([buying, maint, doors, persons, lug_boot, safety, label])

        if buying == 'vhigh':
            buying = 1.0/4.0
        elif buying == 'high':
            buying = 2.0/4.0
        elif buying == 'med':
            buying = 3.0/4.0
        elif buying == 'low':
            buying = 4.0/4.0


        if maint == 'vhigh':
            maint = 1.0/4.0
        elif maint == 'high':
            maint = 2.0/4.0
        elif maint == 'med':
            maint = 3.0/4.0
        elif maint == 'low':
            maint = 4.0/4.0


        if doors == '5more':
            doors = 5.0/5.0
        elif doors == '2':
            doors = 2.0/5.0
        elif doors == '3':
            doors = 3.0/5.0
        elif doors == '4':
            doors = 4.0/5.0

        if persons == 'more':
            persons = 3.0/3.0
        elif persons == '2':
            persons = 1.0/3.0
        elif persons == '4':
            persons = 2.0/3.0


        if lug_boot == 'small':
            lug_boot = 1.0/3.0
        elif lug_boot == 'med':
            lug_boot = 2.0/3.0
        elif lug_boot == 'big':
            lug_boot = 3.0/3.0

        if safety == 'low':
            safety = 1.0/3.0
        elif safety == 'med':
            safety = 2.0/3.0
        elif safety == 'high':
            safety = 3.0/3.0

        output.append([float(buying), float(maint), float(doors), float(persons), float(lug_boot), float(safety)])
        labelset.append(label)
    output = np.array(output)
    return output, labelset, rawoutput


def compute_distance(v1, v2):
    distance = np.sqrt(np.sum(np.power(v1 - v2, 2)))
    return distance


def kmeans(dataSet, initial, k, iters):
    num = dataSet.shape[0]
    dim = dataSet.shape[1]
    centroids = initial
    clusters = np.zeros(num)
    for time in range(iters):
        # compute distance and closet centroid
        for i in range(num):
            min_distance = 1e10
            min_centroids = 0
            # compute each centroid and closet one
            for j in range(k):
                distance = compute_distance(centroids[j, :], dataSet[i, :])
                if distance < min_distance:
                    min_distance = distance
                    min_centroids = j

            # reassign
            if clusters[i] != min_centroids:
                converged = False
                clusters[i] = min_centroids

        # change centroids
        centroids = np.zeros((k, dim))
        # loop cluser
        for i in range(k):
            # loop row
            for d in range(dim):
                sum_coordinate = 0
                cluster_num = 0
                # loop dimension
                for r in range(num):
                    if clusters[r] == i:
                        sum_coordinate += dataSet[r, d]
                        cluster_num += 1
                centroids[i, d] = sum_coordinate / cluster_num

    return centroids, clusters


def main():
    input_file = file(sys.argv[1])
    initial_file = file(sys.argv[2])
    k = int(sys.argv[3])
    iters = int(sys.argv[4])
    input, label1, output = transform(input_file)
    initial, label2, _ = transform(initial_file)
    centroids, clusters = kmeans(input, initial, k, iters)


    clusters_name = []
    for i in range(k):
        count = dict()
        for j in range(input.shape[0]):
            if clusters[j] == i:
                if output[j][-1] == 'unacc':
                    count.setdefault('unacc', 0)
                    count['unacc'] += 1
                elif output[j][-1] == 'acc':
                    count.setdefault('acc', 0)
                    count['acc'] += 1
                elif output[j][-1] == 'good':
                    count.setdefault('good', 0)
                    count['good'] += 1
                else:
                    count.setdefault('vgood', 0)
                    count['vgood'] += 1
        total = max(count.iteritems(), key = operator.itemgetter(1))[0]
        clusters_name.append(total)

    f = open('yu_guangbo_clustering.txt', 'w+')
    error = 0
    for i in range(k):
        f.write('cluster: ')
        f.write(str(clusters_name[i]))
        f.write('\n')
        for j in range(input.shape[0]):
            if clusters[j] == i:
                f.write(str(output[j]))
                f.write('\n')
                if output[j][-1] != clusters_name[i]:
                    error += 1
        f.write('\n')
        f.write('\n')

    f.write('Number of points wrongly assigned:')
    f.write('\n')
    f.write(str(error))


if __name__ == '__main__':
    main()


