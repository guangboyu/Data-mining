import sys


def transform(filename):
    output = []
    for i in filename.readlines():
        entry = i.split(',')
        buying, maint, doors, persons, lug_boot, safety, label = entry
        label = label.split('\r')[0]
        if buying == 'vhigh':
            buying = 4
        elif buying == 'high':
            buying = 3
        elif buying == 'med':
            buying = 2
        elif buying == 'low':
            buying = 1
        else:
            buying = 0.0

        if maint == 'vhigh':
            maint = 4
        elif maint == 'high':
            maint = 3
        elif maint == 'med':
            maint = 2
        elif maint == 'low':
            maint = 1
        else:
            maint = 0.0

        if doors == '5more':
            doors = 6
        elif doors == '2':
            doors = 2
        elif doors == '3':
            doors = 3
        elif doors == '4':
            doors = 4
        else:
            doors = float(doors)

        if persons == 'more':
            persons = 5
        elif persons == '2':
            persons = 20
        elif persons == '4':
            persons = 4
        else:
            persons = float(persons)

        if lug_boot == 'small':
            lug_boot = 1
        elif lug_boot == 'med':
            lug_boot = 2
        elif lug_boot == 'big':
            lug_boot = 3

        if safety == 'low':
            safety = 10
        elif safety == 'med':
            safety = 2
        elif safety == 'high':
            safety = 3

        output.append([buying, maint, doors, persons, lug_boot, safety, label])

    return output


def calculateDistance(vector1, vector2):
    """
    \n vector1 & vector2 are in the form (x0,y0,z0,...)
    """
    calc_sum = 0.0
    pairs = zip(vector1, vector2)
    for pair in pairs:
        calc_sum = calc_sum + (pair[0] - pair[1]) ** 2
    return calc_sum ** 0.5


def kmeans(list_features, centroids, k, iter_num):
    """
    \n centroids - list of tuples of coordinates with their label
    \n eg. [((x0,y0,z0),label0),((x1,y1,z1),label1),...]
    """
    # the last column is label
    num_dimension = len(list_features) - 1
    # store the true labels
    labels = list_features[-1]
    # store the predicted labels(cluster)
    predicted_labels = ["None"] * len(labels)

    # pre-calculate vectors for all points
    # each element of vector_data is a tuple of coordinates
    # eg. [(1,2,3),(4,5,6),...]
    vector_data = zip(*list_features[0:len(list_features) - 1])

    iteration_count = 0
    while (iteration_count < iter_num):
        iteration_count += 1

        # assign a new centroid for each point
        for i in range(len(vector_data)):
            data_point = vector_data[i]
            # eg. data_point -> (x0,y0,z0)
            min_distance = -1
            for centroid in centroids:
                # eg. centroid_vector -> (xA,yA,zA)
                centroid_vector = centroid[0]
                # eg. centroid_label -> "0"
                centroid_label = centroid[1]
                distance = calculateDistance(data_point, centroid_vector)

                if (min_distance == -1 or distance < min_distance):
                    predicted_labels[i] = centroid_label
                    min_distance = distance

        # calculate new centroids
        new_centroids = []
        num_dup_centroid = 0
        for old_centroid in centroids:
            old_centroid_vector, l = old_centroid
            centroid_vector = [-1] * num_dimension
            for i in range(num_dimension):
                features = list_features[i]
                filter_features = [features[j] for j in range(len(features)) if predicted_labels[j] == l]
                centroid_vector[i] = sum(filter_features) / len(filter_features)

            centroid_vector = tuple(centroid_vector)
            if (centroid_vector == old_centroid_vector):
                num_dup_centroid += 1
            new_centroids.append((centroid_vector, l))

        # stop if we repeat all previous centroids
        if (num_dup_centroid == k):
            break

        centroids = new_centroids

    # re-assign the labels of predicted cluster
    pairs = zip(labels, predicted_labels)
    for label in set(predicted_labels):
        true_labels = [pairs[i][0] for i in range(0, len(pairs)) if pairs[i][1] == label]
        # get the most occurence label
        common_label = max(set(true_labels), key=true_labels.count)
        predicted_labels = [common_label if predicted_labels[i] == label else predicted_labels[i] for i in
                            range(len(predicted_labels))]

    return predicted_labels


def readInitCentroids(file_name):
    list_centroids = []
    index = 0
    for line in open(file_name):
        l = line.replace("\n", "")
        if (len(l) == 0):
            break
        fields = l.split(",")
        coords = (fields[0:len(fields) - 1])
        coords = [float(x) for x in coords]
        centroid_tuple = (tuple(coords)), str(index)
        list_centroids.append(centroid_tuple)
        index += 1

    return list_centroids


def readCSV(file_name):
    """
    \n read .csv file, assume that the last column is label
    \n return - a list of columns of data points, the last column is label
    \n e.g. [[1,2,3],[4,5,6],['label1','label2','label1']]
    """
    list_features = []
    for line in open(data_file):
        l = line.replace("\n", "")
        if (len(l) == 0):
            break
        fields = l.split(",")
        num_cols = len(fields)
        if (len(list_features) == 0):
            list_features = [[] for i in range(num_cols)]

        [list_features[i].append(fields[i]) if i == num_cols - 1 else list_features[i].append(float(fields[i])) for i in
         range(len(fields))]
    return list_features


if __name__ == '__main__':
    data_file = sys.argv[1]
    k = int(sys.argv[3])
    iter_num = int(sys.argv[4])
    init_points_file = sys.argv[2]

    list_features = readCSV(data_file)
    centroids = readInitCentroids(init_points_file)

    predicted_labels = kmeans(list_features, centroids=centroids, k=k, iter_num=iter_num)

    # print out the result
    vector_data = zip(*list_features)

    dist_labels = sorted(set(predicted_labels))
    for dist_label in dist_labels:
        print("Cluster {0}".format(dist_label))
        for i in range(len(predicted_labels)):
            if predicted_labels[i] == dist_label:
                print(list(vector_data[i]))
        print("")

        # check the number of wrong labels
    check_pairs = zip(predicted_labels, list_features[-1])
    num_wrong = 0
    for pair in check_pairs:
        if (pair[0] != pair[1]):
            num_wrong += 1
    print("Number of points assigned to wrong cluster:")
    print(num_wrong)
