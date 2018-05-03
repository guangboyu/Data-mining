import sys
import itertools
import random

def sampling(bskt, frac):
    return random.sample(bskt, int(len(bskt)*frac))

def generate_freq(lines, size, s):
    item_count = dict()
    freq_item = []
    for line in lines:  #read bkt like''a,b,c,d,e\n''
        line = line.strip().split(',')  #like ['a', 'b', 'c']
        for item in itertools.combinations(line, size):
            item = list(item)
            item.sort()
            item = tuple(item)
            #count
            item_count.setdefault(item, 0)
            item_count[item] += 1

    for k,v in item_count.items():
        if v >= s:
            freq_item.append(list(k))
    freq_item.sort()
    return freq_item

def aprior(lines, threshold):
    size = 1
    freq_itemset = []
    freq_item = generate_freq(lines, size, threshold)
    while freq_item:
        size += 1
        for item in freq_item:
            freq_itemset.append(item)
        freq_item = generate_freq(lines, size, threshold)
    return freq_itemset

#freq: [['a'],['b'],['c']]
def neg_border(sample, freq_itemsets):
    size = 1
    neg_borders = []
    neg_border = []

    max_size = []
    for line in sample:
        line = line.strip().split(',')
        for item in itertools.combinations(line, size):  # generate pairs
            item = list(item)
            if item in freq_itemsets:
                continue
            if (item not in freq_itemsets) and (item not in neg_border):
                    neg_border.append(item)

    for item in freq_itemsets:
        max_size.append(len(item))

    max_size = max(max_size)

    for x in range(max_size + 1):
        size += 1
        for item in neg_border:
            neg_borders.append(list(item))
        neg_border = []
        for line in sample:
            line = line.strip().split(',')
            for item in itertools.combinations(line, size):  #generate pairs
                item = list(item)
                item.sort()
                flag = True
                if item in freq_itemsets:
                    flag = False
                    continue
                if item not in freq_itemsets:   #decide if nb
                    for i in itertools.combinations(item, len(item) - 1):
                        i = list(i)
                        if i not in freq_itemsets:
                            flag = False
                if flag:
                    if item not in neg_border:
                        neg_border.append(item)

    neg_border.sort()
    return neg_borders

def pass1(lines, threshold):
    freq = aprior(lines, threshold)
    nb = neg_border(lines, freq)
    return freq, nb

def check_nb(nb, lines, threshold):
    for items in nb:    #each nb_pairs items=['abc']
        count = 0
        for line in lines:  #each bskt  line=['abcd']
            flag = True
            line = line.strip().split(',')  #bskt's list    line=['a','b','c','d']
            x = set(items)
            y = set(line)
            if x.issubset(y):
                count += 1
        if count >= threshold:
            return False
    return True

#
def extract_freq(cp, lines, threshold):
    fp = []
    for items in cp:
        count = 0
        for line in lines:
            flag = True
            line = line.strip().split(',')
            x = set(items)
            y = set(line)
            if x.issubset(y):
                count += 1
        if count >= threshold:
            fp.append(items)
    return fp

def pass2(lines, cp, nb, threshold):
    fq = extract_freq(cp, lines, threshold)
    nb = check_nb(nb,lines,threshold)
    return nb, fq

def main():
    frac = 0.5
    f = sys.argv[1]
    threshold = int(sys.argv[2])
    flag = False
    fp = []
    s_threshold = frac * threshold * 0.9
    iter = 0

    while not flag:
        lines = file(f).readlines()
        sample = sampling(lines, frac)
        cp, nb = pass1(sample, s_threshold)
        flag, fp = pass2(lines, cp, nb, threshold)
        iter += 1

    print(iter)
    print(frac)
    print(fp)

    #itertools.combinations(pairs, len(pairs) - 1)

if __name__ == '__main__':
    main()