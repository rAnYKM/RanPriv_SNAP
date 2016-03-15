# Project Name  :   RanPriv
# Author        :   rAnYKM (Jiayi Chen)
# ______              ______       _
# | ___ \             | ___ \     (_)
# | |_/ / __ _  _ __  | |_/ /_ __  _ __   __
# |    / / _` || '_ \ |  __/| '__|| |\ \ / /
# | |\ \| (_| || | | || |   | |   | | \ V /
# \_| \_|\__,_||_| |_|\_|   |_|   |_|  \_/
#
# Script Name   :   ranpriv.py
# Create Date   :   Mar. 2, 2016
# Version       :   1.0.0
# Description   :   This is the main file of the whole project

import snap_core as sc
import snap_generator as sg
import snap_analysis as sa
import networkx as nx
import os
from collections import Counter

IT_COMPANY = [
    'Apple', 'Amazon', 'Dell',
    'Facebook', 'Google', 'IBM',
    'Microsoft', 'Yahoo', 'Youtube',
    'Intel', 'Mozilla', 'Cisco',
    'HP', 'Hewlett Packard', 'Hewlett-Packard'
    ]


def new_data_set():
    nodes, edges = sc.load_sample_data_set('ranykm')
    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    un_graph = sc.fetch_undirected_graph(graph)
    with open(os.path.join(sc.RAW_DATA_DIR, 'ranykm.compress.edges'), 'w') as fp:
        for edge in un_graph.edges():
            fp.write(edge[0] +',' + edge[1] + '\n')
    with open(os.path.join(sc.RAW_DATA_DIR, 'ranykm.compress.nodes'), 'w') as fp:
        for node in un_graph.nodes():
            fp.write(node + ',' + nodes[node] + '\n')


def big_data_set(threshold=5):
    nodes, edges = sc.load_sample_data_set('ranykm.compress')
    graph = nx.Graph()
    graph.add_edges_from(edges)
    print ("network information %d nodes %d edges" % (graph.number_of_nodes(), graph.number_of_edges()))
    sel_nodes = [node for node in graph.nodes() if len(graph.neighbors(node)) >= threshold]
    tag = [nodes[node] for node in sel_nodes]
    ctr = Counter(tag)
    print ctr['rnd'], ctr['mns'], ctr['exe']
    print ("Important nodes number: %d" % len(sel_nodes))
    # node_tri = sa.fetch_triangles(graph, nodes, sel_nodes)
    # sa.save_triangles('ranykm_big_data.tri', node_tri)
    node_tri = sa.load_triangles('ranykm_big_data.tri')
    # sc.capture_ego(graph, nodes, '113006028898915385825', node_tri, 'sample.ego')

    # sa.fetch_homophily(graph, nodes, sel_nodes, ['unl'])
    # sa.fetch_AND(graph, nodes, sel_nodes, ['unl'])
    # print sa.fetch_label_homophily(graph, nodes, 'rnd', [])
    # print sa.fetch_label_homophily(graph, nodes, 'mns', [])
    # print sa.fetch_label_homophily(graph, nodes, 'exe', [])

    # weight = {'rnd':0.5, 'mns':2.5, 'exe':1, 'unl':0.1}
    # sa.analyze_triangle(node_tri, nodes, weight)
    # sa.analyze_nodes(graph, nodes, node_tri, sel_nodes)
    sa.machine_learning(graph, nodes, sel_nodes, node_tri)
    # node_analysis, node_label = sa.load_analysis('stat.csv')
    # sa.analysis_learning(graph, nodes, node_analysis, node_label)


def small_data_set(threshold=5):
    nodes, edges, feats = sc.load_data_set()
    social_net = sc.build_directed_graph(nodes, edges)
    graph = sc.fetch_undirected_graph(social_net)
    labeled_nodes = sc.fetch_node_label(nodes, feats, graph.nodes())
    print ("network information %d nodes %d edges" % (graph.number_of_nodes(), graph.number_of_edges()))
    sel_nodes = [node for node in graph.nodes() if len(graph.neighbors(node)) >= threshold]
    tag = [labeled_nodes[node] for node in sel_nodes]
    ctr = Counter(tag)
    print ctr['rnd'], ctr['mns'], ctr['exe']
    print ("Important nodes number: %d" % len(sel_nodes))
    # sa.fetch_homophily(graph, labeled_nodes, sel_nodes, ['unl'])


def main():
    """
    :rtype: int
    """
    # egos = sc.load_egos()
    # print len(egos)
    # ignores = sg.load_ignore_feat()
    # sg.data_generator(egos, 'job_title', ignores, 'institution', IT_COMPANY)
    '''
    nodes, edges, feats = sc.load_data_set()
    print len(nodes), len(edges), len(feats)
    social_net = sc.build_directed_graph(nodes, edges)
    print social_net.number_of_nodes(), social_net.number_of_edges()
    un_net = sc.fetch_undirected_graph(social_net)
    # print un_net.number_of_edges(), un_net.number_of_nodes()
    labeled_nodes = sc.fetch_node_label(nodes, feats, un_net.nodes())
    num_edges = [len(un_net.neighbors(node)) for node in un_net.nodes()]
    a = Counter(num_edges)
    print a[0], a[1], a[2], a[3], a[4], a[5]
    tongji = [val for _, val in labeled_nodes.iteritems()]
    ctr = Counter(tongji)
    for i in ['rnd', 'mns', 'exe', 'other', 'unl']:
        print i,ctr[i]
    sa.fetch_homophily(un_net, labeled_nodes, ['unl'])
    '''
    # print sa.fetch_label_homophily(un_net, labeled_nodes, 'rnd', [])
    # nodes, edges = sc.load_sample_data_set()
    big_data_set()



if __name__ == '__main__':
    main()
