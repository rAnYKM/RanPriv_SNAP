# Project Name  :   RanPriv
# Author        :   rAnYKM (Jiayi Chen)
# ______              ______       _
# | ___ \             | ___ \     (_)
# | |_/ / __ _  _ __  | |_/ /_ __  _ __   __
# |    / / _` || '_ \ |  __/| '__|| |\ \ / /
# | |\ \| (_| || | | || |   | |   | | \ V /
# \_| \_|\__,_||_| |_|\_|   |_|   |_|  \_/
#
# Script Name   :   snap_analysis.py
# Create Date   :   Mar. 4, 2016
# Version       :   1.0.0
# Description   :   Obtain various analysis methods for SNAP data set (Google+)

import numpy as np
from collections import Counter
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OutputCodeClassifier
from snap_core import *
from ran_priv_core import *
import csv


def analyze_triangle(node_tri, labeled_nodes, weight):
    top_dict = {}
    for node, tri in node_tri.iteritems():
        lab = labeled_nodes[node]
        pat = []
        if [''] in tri:
            continue
        for t in tri:
            lab1 = labeled_nodes[t[0]]
            lab2 = labeled_nodes[t[1]]
            if lab1 > lab2:
                pattern = lab2 + ',' + lab1
            else:
                pattern = lab1 + ',' + lab2
            pat.append(pattern)
        ctr = Counter(pat)
        maximum = -1
        for pattern, val in ctr.iteritems():
            patt = pattern.split(',')
            wei = (weight[patt[0]] + weight[patt[1]]) * val
            if wei > maximum:
                top_pattern = pattern
                maximum = wei
        if lab in top_dict:
            li = top_dict[lab]
            li.append(top_pattern)
            top_dict[lab] = li
        else:
            top_dict[lab] = [top_pattern]
    ctr_top = Counter(top_dict['rnd'])
    print ctr_top
    ctr_top = Counter(top_dict['mns'])
    print ctr_top
    ctr_top = Counter(top_dict['exe'])
    print ctr_top


def analyze_nodes(graph, nodes, triples, sel_nodes):
    labels, node_pair = pair_distribution(graph, nodes, sel_nodes, ['rnd', 'mns', 'exe'])
    label_pattern, node_tri = triple_distribution(graph, nodes, triples, sel_nodes, ['rnd', 'mns', 'exe'])
    with open(os.path.join(OUT_DATA_DIR, 'stat.csv'), 'w') as fp:
        fp.write('id,label,' + ','.join(labels) + ',' + ','.join(label_pattern) + '\n')
        for node in sel_nodes:
            fp.write(node + ',' + nodes[node] + ',' + \
                     ','.join([str(n) for n in node_pair[node] + node_tri[node]]) + '\n')


def fetch_homophily(graph, labeled_nodes, sel_nodes, not_included):
    labels = {'rnd': [], 'mns': [], 'exe': []}
    for node in sel_nodes:
        label = labeled_nodes[node]
        if label in not_included:
            continue
        node_neighbor = graph.neighbors(node)
        ctr = Counter([labeled_nodes[item] for item in node_neighbor])
        if len(node_neighbor) == 0:
            percentage = 0
        else:
            percentage = ctr[label] / float(len(node_neighbor))

        li = labels[label]
        li.append(percentage)
        labels[label] = li
    show_distribution(labels, 0, 1, 0.1)


def fetch_label_homophily(graph, labeled_nodes, label, not_included):
    n = 0.0
    m = 0.0
    for edge in graph.edges():
        a = labeled_nodes[edge[0]]
        b = labeled_nodes[edge[1]]
        if a in not_included or b in not_included:
            continue
        if a == label:
            m += 1
            if b == label:
                n += 1
        elif b == label:
            m += 1
    return n / m


def fetch_degree_closeness(graph, nodes, sel_nodes, not_included):
    labels = {'rnd': [], 'mns': [], 'exe': []}
    node_dc = nx.degree_centrality(graph)
    for node in sel_nodes:
        label = nodes[node]
        if label in not_included:
            continue
        li = labels[label]
        li.append(node_dc[node])
        labels[label] = li
    # print labels
    show_distribution(labels, 0, 0.01, 0.0002)


def fetch_AND(graph, nodes, sel_nodes, not_included):
    labels = {'rnd': [], 'mns': [], 'exe': []}
    node_dc = nx.average_neighbor_degree(graph)
    for node in sel_nodes:
        label = nodes[node]
        if label in not_included:
            continue
        li = labels[label]
        li.append(node_dc[node])
        labels[label] = li
    print labels
    show_distribution(labels, 0, 300, 10)


def fetch_triangles(graph, labeled_nodes, sel_nodes):
    nodes_tri = {}
    crt = 0
    for node in sel_nodes:
        neighbors = graph.neighbors(node)
        tri = []
        for i in range(len(neighbors) - 1):
            for j in range(i + 1, len(neighbors)):
                if graph.has_edge(neighbors[i], neighbors[j]):
                    tri.append([neighbors[i], neighbors[j]])
        nodes_tri[node] = tri
        crt += 1
        if crt % 200 == 0:
            print crt
    return nodes_tri


def load_triangles(filename):
    nodes_tri = {}
    with open(os.path.join(OUT_DATA_DIR, filename), 'rb') as fp:
        lines = [line.strip(' \r\n') for line in fp.readlines()]
        for l in lines:
            pairs = l.split(':')
            node = pairs[0]
            tri = []
            for i in pairs[1].split(' '):
                item = i.split(',')
                tri.append(item)
            nodes_tri[node] = tri
    return nodes_tri


def save_triangles(filename, node_tri):
    with open(os.path.join(OUT_DATA_DIR, filename), 'wb') as fp:
        for node, tri in node_tri.iteritems():
            fp.write(node + ':')
            for t in tri:
                fp.write(t[0] + ',' + t[1] + ' ')
            fp.write('\r\n')


def show_distribution(distribution, start, end, step):
    for lab, li in distribution.iteritems():
        true_li = []
        for i in li:
            for j in np.arange(start, end, step):
                if j >= end - step - 0.000001:
                    true_li.append(j)
                    break
                if i >= j - 0.000001 and i < j + step:
                    true_li.append(j)
                    break
        ctr = Counter(true_li)
        print lab
        for i in np.arange(start, end, step):
            print ctr[i] / float(len(li)),
        print '\n'


def machine_learning(graph, nodes, sel_nodes, tri_nodes):
    num_label = {'rnd': 0, 'mns': 1, 'exe': 2}
    labels = [num_label[nodes[node]] for node in sel_nodes]
    label_y = np.array(labels)
    sss = StratifiedShuffleSplit(label_y, 10, test_size=0.1, random_state=0)

    tre = DecisionTreeClassifier(random_state=0)
    clf = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
              decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
              max_iter=-1, probability=False, random_state=None, shrinking=True,
              tol=0.001, verbose=False)
    mnb = MultinomialNB()
    gnb = GaussianNB()
    features = []
    small_ctr = 0
    node_dc = nx.degree_centrality(graph)
    node_and = nx.average_neighbor_degree(graph)
    for node in sel_nodes:
        small_ctr += 1
        # if small_ctr % 100 == 0:
        #     print small_ctr # , feature
        neighbors = graph.neighbors(node)
        nei_feature = [nodes[nd] for nd in neighbors]
        ctr = Counter(nei_feature)
        tot = float(len(neighbors))
        feature = [ctr['rnd'], ctr['mns'], ctr['exe']]

        tri = tri_nodes[node]
        num_tri = len(tri)
        # feature = []
        if num_tri == 0:
            feature += [0, 0, 0, 0, 0, 0]
        else:
            pat = []
            f_num = float(num_tri)
            if [''] in tri:
                feature += [0, 0, 0, 0, 0, 0]
            else:
                for t in tri:
                    lab1 = nodes[t[0]]
                    lab2 = nodes[t[1]]
                    if lab1 > lab2:
                        pattern = lab2 + ',' + lab1
                    else:
                        pattern = lab1 + ',' + lab2
                    pat.append(pattern)
                p_ctr = Counter(pat)
                feature += [p_ctr['rnd,rnd'], p_ctr['exe,rnd'], p_ctr['mns,rnd'],
                            p_ctr['exe,exe'], p_ctr['exe,mns'], p_ctr['mns,mns']]
        feature += [node_dc[node], node_and[node]]

        features.append(feature)
    feature_x = np.array(features)

    print ('start to learn features')
    for train_index, test_index in sss:
        X_train = feature_x[train_index]
        Y_train = label_y[train_index]
        X_test = feature_x[test_index]
        Y_test = label_y[test_index]
        # y_pred = mnb.fit(X_train, Y_train).predict(X_test)
        # y_pred = ran_log_model(\
        #    graph, nodes, np.array(sel_nodes)[test_index], np.array(sel_nodes)[train_index], ['rnd', 'mns', 'exe'])
        y_pred = ran_tri_prob_model(\
            graph, nodes, tri_nodes, np.array(sel_nodes)[test_index], np.array(sel_nodes)[train_index], ['rnd', 'mns', 'exe'])
        # y_pred = ran_mixture_model(\
        #    graph, nodes, tri_nodes, np.array(sel_nodes)[test_index], np.array(sel_nodes)[train_index], ['rnd', 'mns', 'exe'])
        #y_pred = ran_node_model(\
        #    graph, nodes, np.array(sel_nodes)[test_index], np.array(sel_nodes)[train_index], ['rnd', 'mns', 'exe'])
        ta = 0.0  # true
        ga = 0.0  # guess true but wrong
        za = 0.0  # how many a ta/za = recall ta/(ta+ga) = precision
        tb = 0.0
        gb = 0.0
        zb = 0.0
        tc = 0.0
        gc = 0.0
        zc = 0.0
        for i in range(len(Y_test)):
            a = Y_test[i]
            b = y_pred[i]
            if a == 0:
                za += 1
                if b == 0:
                    ta += 1
                elif b == 1:
                    gb += 1
                else:
                    gc += 1
            elif a == 1:
                zb += 1
                if b == 0:
                    ga += 1
                elif b == 1:
                    tb += 1
                else:
                    gc += 1
            else:
                zc += 1
                if b == 0:
                    ga += 1
                elif b == 1:
                    gb += 1
                else:
                    tc += 1
        if int(ga) != 0:
            print 'RND: ', ta, ga, za, ta/(ga + ta), ta/za,
        else:
            print 'RND: ', 0, ta/za,
        if int(gb) != 0:
            print 'MNS: ', tb, gb, zb, tb/(gb + tb), tb/zb,
        else:
            print 'MNS: ', 0, tb/zb,
        if int(gc) != 0:
            print 'EXE: ', tc, gc, zc, tc/(gc + tc), tc/zc,
        else:
            print 'EXE: ', 0, tc/zc,
        print '\n'


def clique_analysis(graph, nodes, sel_nodes):
    node_cliques = {}
    counter = 0
    for node in sel_nodes:
        feature = []
        neighbors = graph.neighbors(node)
        rnd_set = [node for node in sel_nodes if nodes[node] == 'rnd']
        mns_set = [node for node in sel_nodes if nodes[node] == 'mns']
        exe_set = [node for node in sel_nodes if nodes[node] == 'exe']
        rnd_graph = graph.subgraph(rnd_set + [node])
        mns_graph = graph.subgraph(mns_set + [node])
        exe_graph = graph.subgraph(exe_set + [node])
        rnd_cliques = nx.graph_clique_number(rnd_graph)
        mns_cliques = nx.graph_clique_number(mns_graph)
        exe_cliques = nx.graph_clique_number(exe_graph)
        if len(rnd_set) == 0:
            feature.append(0)
        else:
            feature.append(rnd_cliques/float(len(rnd_set)))
        if len(mns_set) == 0:
            feature.append(0)
        else:
            feature.append(mns_cliques/float(len(mns_set)))
        if len(exe_set) == 0:
            feature.append(0)
        else:
            feature.append(exe_cliques/float(len(exe_set)))
        node_cliques[node] = feature
        counter += 1
        if counter % 5 == 0:
            print counter
    return node_cliques


def analysis_learning(graph, nodes, node_analysis, node_label):
    num_label = {'rnd': 0, 'mns': 1, 'exe': 2}
    set_pairs = [(n, num_label[l], node_analysis[n]) for n, l in node_label.iteritems()]
    uid = [item[0] for item in set_pairs]
    y = [item[1] for item in set_pairs]
    raw_x = [item[2] for item in set_pairs]
    sss = StratifiedShuffleSplit(y, 10, test_size=0.1, random_state=0)
    x = []
    node_dc = nx.degree_centrality(graph)
    node_and = nx.average_neighbor_degree(graph)
    # node_cliques = clique_analysis(graph, nodes, uid)
    for index, item in enumerate(raw_x):
        feature = []
        s = item['rnd'] + item['mns'] + item['exe']
        if s == 0:
            homo_rnd = 0
            homo_mns = 0
            homo_exe = 0
        else:
            homo_rnd = item['rnd']/float(s)
            homo_mns = item['mns']/float(s)
            homo_exe = item['exe']/float(s)
        feature += [homo_rnd, homo_mns, homo_exe]
        s2 = item['rnd-rnd'] + item['mns-mns'] + item['exe-exe'] + \
             item['mns-rnd'] + item['exe-mns'] + item['exe-rnd']
        if s2 == 0:
            triple_rnd_rnd = 0
            triple_mns_mns = 0
            triple_exe_exe = 0
            triple_mns_rnd = 0
            triple_exe_mns = 0
            triple_exe_rnd = 0
        else:
            triple_rnd_rnd = item['rnd-rnd']/float(s2)
            triple_mns_mns = item['mns-mns']/float(s2)
            triple_exe_exe = item['exe-exe']/float(s2)
            triple_mns_rnd = item['mns-rnd']/float(s2)
            triple_exe_mns = item['exe-mns']/float(s2)
            triple_exe_rnd = item['exe-rnd']/float(s2)
        feature += [triple_rnd_rnd, triple_mns_mns, triple_exe_exe, triple_mns_rnd, triple_exe_mns, triple_exe_rnd]
        # feature += [node_dc[uid[index]], node_and[uid[index]]]
        feature += node_cliques[uid[index]]
        x.append(feature)
    npx = np.array(x)
    npy = np.array(y)
    gnb = GaussianNB()
    tre = DecisionTreeClassifier(random_state=0)
    clf = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,\
    decision_function_shape='ovo', degree=3, gamma='auto', kernel='rbf',\
    max_iter=-1, probability=False, random_state=None, shrinking=True,\
    tol=0.001, verbose=False)
    print ('start to learn features')
    for train_index, test_index in sss:
        x_train = npx[train_index]
        y_train = npy[train_index]
        x_test = npx[test_index]
        y_test = npy[test_index]
        y_pred = tre.fit(x_train, y_train).predict(x_test)
        #y_pred = OutputCodeClassifier(LinearSVC(random_state=0), code_size=2, random_state=0).fit(x_train, y_train).predict(x_test)
        ta = 0.0  # true
        ga = 0.0  # guess true but wrong
        za = 0.0  # how many a ta/za = recall ta/(ta+ga) = precision
        tb = 0.0
        gb = 0.0
        zb = 0.0
        tc = 0.0
        gc = 0.0
        zc = 0.0
        for i in range(len(y_test)):
            a = y_test[i]
            b = y_pred[i]
            if a == 0:
                za += 1
                if b == 0:
                    ta += 1
                elif b == 1:
                    gb += 1
                else:
                    gc += 1
            elif a == 1:
                zb += 1
                if b == 0:
                    ga += 1
                elif b == 1:
                    tb += 1
                else:
                    gc += 1
            else:
                zc += 1
                if b == 0:
                    ga += 1
                elif b == 1:
                    gb += 1
                else:
                    tc += 1
        if int(ga) != 0:
            print 'RND: ', ta, ga, za, ta/(ga + ta), ta/za,
        else:
            print 'RND: ', 0, ta/za,
        if int(gb) != 0:
            print 'MNS: ', tb, gb, zb, tb/(gb + tb), tb/zb,
        else:
            print 'MNS: ', 0, tb/zb,
        if int(gc) != 0:
            print 'EXE: ', tc, gc, zc, tc/(gc + tc), tc/zc,
        else:
            print 'EXE: ', 0, tc/zc,
        print '\n'


def load_analysis(filename):
    node_analysis = {}
    node_label = {}
    with open(os.path.join(OUT_DATA_DIR, filename), 'rb') as fp:
        reader= csv.DictReader(fp)
        for row in reader:
            node_analysis[row['id']] = {name: eval(val) for name, val in row.iteritems() if name not in ['id', 'label']}
            node_label[row['id']] = row['label']
    return node_analysis, node_label
