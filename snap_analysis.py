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
from sklearn.cross_validation import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from snap_core import *
from ran_priv_core import *

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
    '''
    tre = DecisionTreeClassifier(random_state=0)
    clf = SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
              decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
              max_iter=-1, probability=False, random_state=None, shrinking=True,
              tol=0.001, verbose=False)
    gnb = GaussianNB()
    features = []
    small_ctr = 0
    node_dc = nx.degree_centrality(graph)
    node_and = nx.average_neighbor_degree(graph)
    for node in sel_nodes:
        small_ctr += 1
        if small_ctr % 100 == 0:
            print small_ctr # , feature
        neighbors = graph.neighbors(node)
        nei_feature = [nodes[nd] for nd in neighbors]
        ctr = Counter(nei_feature)
        tot = float(len(neighbors))
        feature = [ctr['rnd'] / tot, ctr['mns'] / tot, ctr['exe'] / tot]
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
                feature += [p_ctr['rnd,rnd'] / f_num, p_ctr['exe,rnd'] / f_num, p_ctr['mns,rnd'] / f_num,
                            p_ctr['exe,exe'] / f_num, p_ctr['exe,mns'] / f_num, p_ctr['mns,mns'] / f_num]
        feature += [node_dc[node], node_and[node]]
        features.append(feature)
    feature_x = np.array(features)
    '''
    print ('start to learn features')
    for train_index, test_index in sss:
        # X_train = feature_x[train_index]
        Y_train = label_y[train_index]
        # X_test = feature_x[test_index]
        Y_test = label_y[test_index]
        # y_pred = gnb.fit(X_train, Y_train).predict(X_test)
        #y_pred = ran_prob_model(\
        #    graph, nodes, np.array(sel_nodes)[test_index], np.array(sel_nodes)[train_index], ['rnd', 'mns', 'exe'])
        y_pred = ran_tri_prob_model(\
            graph, nodes, tri_nodes, np.array(sel_nodes)[test_index], np.array(sel_nodes)[train_index], ['rnd', 'mns', 'exe'])
        ta = 0.0 # true
        ga = 0.0 # guess true but wrong
        za = 0.0 # how many a ta/za = recall ta/(ta+ga) = precision
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
            print 'RND: ', ta, ga, za, ta / (ga + ta), ta / za
        else:
            print 'RND: ', 0, ta / za
        if int(gb) != 0:
            print 'MNS: ', tb, gb, zb, tb / (gb + tb), tb / zb
        else:
            print 'MNS: ', 0, tb / zb
        if int(gc) != 0:
            print 'EXE: ', tc, gc, zc, tc / (gc + tc), tc / zc
        else:
            print 'EXE: ', 0, tc / zc
