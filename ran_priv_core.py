# Project Name  :   RanPriv
# Author        :   rAnYKM (Jiayi Chen)
# ______              ______       _
# | ___ \             | ___ \     (_)
# | |_/ / __ _  _ __  | |_/ /_ __  _ __   __
# |    / / _` || '_ \ |  __/| '__|| |\ \ / /
# | |\ \| (_| || | | || |   | |   | | \ V /
# \_| \_|\__,_||_| |_|\_|   |_|   |_|  \_/
#
# Script Name   :   ran_priv_core.py
# Create Date   :   Mar. 2, 2016
# Version       :   1.0.0
# Description   :   core function for RAN model


import networkx as nx
import numpy as np


def __label_pair(label1, label2, div):
    if label1 > label2:
        return div.join([label2, label1])
    else:
        return div.join([label1, label2])


def __label_triple(label1, label2, label3, div):
    li = sorted([label1, label2, label3])
    return div.join(li)


def ran_prob_model(graph, nodes, sel_nodes, not_sel_nodes, labels):
    """
    return probability of being a certain label
    :type graph: NetworkX undirected graph
    :type nodes: dict
    :type sel_nodes: list
    :type not_sel_nodes: list
    :type labels: list
    Note that sel_nodes are labeled and known and not_sel_nodes are unlabeled nodes
    """
    crt_class_label = {}
    label_dict = {'rnd': 0, 'mns': 1, 'exe': 2}
    # calculate all P(C_k|L_i)
    for i, l1 in enumerate(labels):
        for j, l2 in enumerate(labels[i:]):
            crt_class_label[__label_pair(l1, l2, ',')] = 0
    for edge in graph.edges():
        #if edge[0] not in not_sel_nodes or edge[1] not in not_sel_nodes:
        #    continue
        lab1 = nodes[edge[0]]
        lab2 = nodes[edge[1]]
        crt_class_label[__label_pair(lab1, lab2, ',')] += 1
    prob_class_label = {}
    total = {l1: sum([crt_class_label[p] for p in crt_class_label if l1 in p.split(',')]) for l1 in labels}
    for l1 in labels:
        for l2 in labels:
            prob_class_label['|'.join([l2, l1])] = crt_class_label[__label_pair(l1, l2, ',')]/float(total[l1])
    pred_labs = []
    print prob_class_label
    for node in sel_nodes:
        neighbors = graph.neighbors(node)
        class_prob = {l: total[l]/float(len(nodes.keys())) for l in labels}
        for nei in neighbors:
            lab = nodes[nei]
            for l in labels:
                class_prob[l] *= prob_class_label['|'.join([lab, l])]
        max_index = max(class_prob, key=class_prob.get)
        # print max_index
        pred_labs.append(label_dict[max_index])
    return pred_labs


def ran_tri_prob_model(graph, nodes, tridict, sel_nodes, not_sel_nodes, labels):
    crt_class_label = {}
    label_dict = {'rnd': 0, 'mns': 1, 'exe': 2}
    # calculate all P(C_k|e_i,j)
    pair_pattern = []
    triples = triple_maker(tridict)
    print ('triple obtained')
    for i, l1 in enumerate(labels):
        for j, l2 in enumerate(labels[i:]):
           pair_pattern.append( __label_pair(l1, l2, ','))
    for i, l1 in enumerate(labels):
        for j, l2 in enumerate(labels[i:]):
            for k, l3 in enumerate(labels[j:]):
                crt_class_label[__label_triple(l1, l2, l3, ',')] = 0
    for tri in triples:
        lab1 = nodes[tri[0]]
        lab2 = nodes[tri[1]]
        lab3 = nodes[tri[2]]
        crt_class_label[__label_triple(lab1, lab2, lab3, ',')] += 1
    prob_class_label = {}
    total = {l1: sum([crt_class_label[p] for p in crt_class_label if l1 in p.split(',')]) for l1 in labels}
    for l1 in labels:
        for l2 in pair_pattern:
            pairs = l2.split(',')
            prob_class_label['|'.join([l2, l1])] =\
                crt_class_label[__label_triple(l1, pairs[0], pairs[1], ',')]/float(total[l1])
    pred_labs = []
    print prob_class_label
    for node in sel_nodes:
        class_prob = {l: total[l]/float(len(nodes.keys())) for l in labels}
        if [''] not in tridict[node]:
            for nei in tridict[node]:
                lab1 = nodes[nei[0]]
                lab2 = nodes[nei[1]]
                pair = __label_pair(lab1, lab2, ',')
                for l in labels:
                    class_prob[l] *= prob_class_label['|'.join([pair, l])]
        max_index = max(class_prob, key=class_prob.get)
        # print max_index
        pred_labs.append(label_dict[max_index])
    return pred_labs


def triple_maker(tridict):
    tris = set()
    for uid, couples in tridict.iteritems():
        if [''] in couples:
            continue
        for couple in couples:
            # print couple
            tri_word = __label_triple(uid, couple[0], couple[1], ',')
            tris.add(tri_word)
    triples = [(word.split(',')[0], word.split(',')[1], word.split(',')[2]) for word in tris]
    return triples

