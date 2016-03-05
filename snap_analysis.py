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
from snap_core import *


def fetch_homophily(graph, labeled_nodes, not_included):
    labels = {'rnd': [], 'mns': [], 'exe': [], 'law': [], 'hr': []}
    for node, label in labeled_nodes.iteritems():
        if label in not_included:
            continue
        node_neighbor = graph.neighbors(node)
        ctr = Counter([labeled_nodes[item] for item in node_neighbor])
        percentage = 0
        if len(node_neighbor) - ctr['unlabeled'] == 0:
            percentage = 0
            continue
        else:
            percentage = ctr[label]/float(len(node_neighbor) - ctr['unlabeled'])

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
    return n/m

def show_distribution(distribution, start, end, step):
    for lab, li in distribution.iteritems():
        true_li = []
        for i in li:
            for j in np.arange(start, end, step):
                if j >= end - step and i >= j:
                    true_li.append(j)
                    break
                if i >= j and i < j + step:
                    true_li.append(j)
                    break
        ctr = Counter(true_li)
        print lab
        for x, y in ctr.iteritems():
            print x, y/float(len(li))



