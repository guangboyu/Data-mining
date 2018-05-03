import sys
import math


def transform(filename):
    output = []
    for i in filename.readlines():
        entry = i.split(',')
        buying, maint, doors, persons, lug_boot, safety, label = entry
        label = label.split('\r')[0]
        if buying == 'vhigh':
            buying = 4.0
        elif buying == 'high':
            buying = 3.0
        elif buying == 'med':
            buying = 2.0
        elif buying == 'low':
            buying = 1.0
        else:
            buying = 0.0

        if maint == 'vhigh':
            maint = 4.0
        elif maint == 'high':
            maint = 3.0
        elif maint == 'med':
            maint = 2.0
        elif maint == 'low':
            maint = 1.0
        else:
            maint = 0.0

        if doors == '5more':
            doors = 5
        else:
            doors = float(doors)

        if persons == 'more':
            persons = 5
        else:
            persons = float(persons)

        if lug_boot == 'small':
            lug_boot = 1
        elif lug_boot == 'med':
            lug_boot = 2
        elif lug_boot == 'big':
            lug_boot = 3

        if safety == 'low':
            safety = 1
        elif safety == 'med':
            safety = 2
        elif safety == 'high':
            safety = 3

        output.append([buying, maint, doors, persons, lug_boot, safety, label])

    return output


def compute_distance(x, y):
    sum = 0.0
    z = zip(x, y)
    for i in z:
        sum += (i[0] - i[1]) ** 2
    sum = math.sqrt(sum)
    return sum


def k_means(input, initial, k, iter):
    centroids = initial
    #iter
    for i in range(1):
        #assign centroid
        for entry in input:
            distance_group = []
            for centroid in centroids:
                distance = compute_distance(entry[0: -1], centroid[0: -1])
                cent_label = [distance, centroid[-1]]
                distance_group.append(cent_label)
            distance_min = min(distance_group, key= lambda x: x[0])

        #update centroid

def main():
    input_file = file(sys.argv[1])
    initial_file = file(sys.argv[2])
    k = int(sys.argv[3])
    iter = int(sys.argv[4])
    input = transform(input_file)
    initial = transform(initial_file)
    k_means(input, initial, k, iter)





if __name__ == '__main__':
    main()


