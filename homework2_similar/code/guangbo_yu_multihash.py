import sys
import itertools


def hashcode1(itemsets, bkt_num):
    total = 53
    for item in itemsets:
        total += ord(item)
    return total % bkt_num


def hashcode2(itemsets, bkt_num):
    total = 107
    for item in itemsets:
        total += ord(item)
    return total % bkt_num


def frequent_item(fq, s):
    data = []
    for k, v in fq.items():
        if v >= s:
            data.append(k)
    data.sort()
    return data


def bitmap(hm, s):
    bm = dict()
    for k, v in hm.items():
        bm.setdefault(k, 0)
        if v >= s:
            bm[k] = 1
    return bm


def main():
    threshold = int(sys.argv[2])
    bkt_num = int(sys.argv[3])

    freq_item = dict()
    # pass 1
    hash_1 = dict()
    hash_2 = dict()
    fi_list = []
    size = 2

    # generate hash
    for line in file(sys.argv[1]).readlines():
        line = line.strip().split(',')
        for item in line:
            freq_item.setdefault(item, 0)
            freq_item[item] += 1
        for itemsets in itertools.combinations(line, size):
            itemsets = list(itemsets)
            itemsets.sort()
            itemsets = tuple(itemsets)
            hv_1 = hashcode1(itemsets, bkt_num)
            hv_2 = hashcode2(itemsets, bkt_num)
            hash_1.setdefault(hv_1, 0)
            hash_2.setdefault(hv_2, 0)
            hash_1[hv_1] += 1
            hash_2[hv_2] += 1
    bm_1 = bitmap(hash_1, threshold)
    bm_2 = bitmap(hash_2, threshold)
    fi_list = frequent_item(freq_item, threshold)
    print(fi_list)
    print('\n')
    print(hash_1)
    print(hash_2)

    # count freq_pairs
    pair_count = dict()
    for line in file(sys.argv[1]).readlines():
        line = line.strip().split(',')
        for itemsets in itertools.combinations(line, size):
            itemsets = list(itemsets)
            itemsets.sort()
            itemsets = tuple(itemsets)
            hv_1 = hashcode1(itemsets, bkt_num)
            hv_2 = hashcode2(itemsets, bkt_num)
            flag = True
            for i in range(len(itemsets)):
                if itemsets[i] not in fi_list:
                    flag = False
            if (bm_1[hv_1] == 1) and (bm_2[hv_2] == 1) and (flag == True):
                pair_count.setdefault(itemsets, 0)
                pair_count[itemsets] += 1

    fp_list = frequent_item(pair_count, threshold)

    print(fp_list)
    print('\n')

    # >2
    prev_fp_list = fp_list
    while prev_fp_list:
        fp_list = []
        hash_1 = dict()
        hash_2 = dict()
        bm_1 = dict()
        bm_2 = dict()
        pair_count = dict()
        size += 1
        # generate hash
        for line in file(sys.argv[1]).readlines():
            line = line.strip().split(',')
            for itemsets in itertools.combinations(line, size):
                itemsets = list(itemsets)
                itemsets.sort()
                itemsets = tuple(itemsets)
                hv_1 = hashcode1(itemsets, bkt_num)
                hv_2 = hashcode2(itemsets, bkt_num)
                hash_1.setdefault(hv_1, 0)
                hash_2.setdefault(hv_2, 0)
                hash_1[hv_1] += 1
                hash_2[hv_2] += 1
        bm_1 = bitmap(hash_1, threshold)
        bm_2 = bitmap(hash_2, threshold)

        # count pair
        for line in file(sys.argv[1]).readlines():
            line = line.strip().split(',')
            for itemsets in itertools.combinations(line, size):
                itemsets = list(itemsets)
                itemsets.sort()
                itemsets = tuple(itemsets)
                hv_1 = hashcode1(itemsets, bkt_num)
                hv_2 = hashcode2(itemsets, bkt_num)
                flag = True
                #                for i in range(len(itemsets)):
                #                    if itemsets[i] not in prev_fp_list:
                #                        flag = False
                if (bm_1[hv_1] == 1) and (bm_2[hv_2] == 1) and (flag == True):
                    pair_count.setdefault(itemsets, 0)
                    pair_count[itemsets] += 1

        fp_list = frequent_item(pair_count, threshold)
        if len(fp_list) != 0:
            print(hash_1)
            print(hash_2)
            print(fp_list)
            print('\n')
        prev_fp_list = fp_list


if __name__ == '__main__':
    main()




