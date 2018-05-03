import networkx as nx
import sys
import community
import matplotlib.pyplot as plt
import operator
import copy
import centrality


def loadData(filename):
    G = nx.Graph()
    lines = file(filename).readlines()
    for line in lines:
        line = line.strip('\r\n').split(' ')
        e = (int(line[0]), int(line[1]))
        G.add_edge(*e)
    return G




def girvanNewman(origin_G):
    G = copy.deepcopy(origin_G)
    best_modu = 0.0
    best_partition = dict()
    while G.number_of_edges() >= 2:
        partition = dict()

        betweeness = nx.edge_betweenness_centrality(G, normalized=False)
        eliminate = max(betweeness.iteritems(), key=operator.itemgetter(1))[0]
        G.remove_edge(*eliminate)

        component = sorted(nx.connected_components(G), key=len, reverse=True)
        for i in range(len(component)):
            temp = list(component[i])
            for j in temp:
                partition[j] = i
        modu = community.modularity(partition, origin_G)
        if modu >= best_modu:
            best_modu = modu
            best_partition = partition
    return best_partition, best_modu


def main():
    filename = sys.argv[1]
    imagename = sys.argv[2]

    G = loadData(filename)
    temp_G = copy.deepcopy(G)

    best_partition, best_modu = girvanNewman(temp_G)

    size = float(len(set(best_partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(best_partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in best_partition.keys()
                      if best_partition[nodes] == com]
        print(list_nodes)
        nx.draw_networkx_nodes(G, pos, nodelist = list_nodes, node_size=500, node_color=str(count / size))
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.axis('off')
    plt.savefig(imagename)

    print('')






if __name__ == '__main__':
    main()