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
from collections import Counter

IT_COMPANY = [
    'Apple', 'Amazon', 'Dell',
    'Facebook', 'Google', 'IBM',
    'Microsoft', 'Yahoo', 'Youtube',
    'Intel', 'Mozilla', 'Cisco',
    'HP', 'Hewlett Packard', 'Hewlett-Packard'
    ]


def big_data_set(threshold=5):
    nodes, edges = sc.load_sample_data_set('h_big_data')
    graph = nx.Graph()
    graph.add_edges_from(edges)
    print ("network information %d nodes %d edges" % (graph.number_of_nodes(), graph.number_of_edges()))
    sel_nodes = [node for node in graph.nodes() if len(graph.neighbors(node)) >= threshold]
    tag = [nodes[node] for node in sel_nodes]
    ctr = Counter(tag)
    print ctr['rnd'], ctr['mns'], ctr['exe']
    print ("Important nodes number: %d" % len(sel_nodes))
    sa.fetch_homophily(graph, nodes, sel_nodes, ['unl'])
    sa.fetch_label_homophily(graph, nodes, 'rnd', [])
    # node_tri = sa.fetch_triangles(graph, nodes, sel_nodes)
    # sa.save_triangles('big_data.tri', node_tri)
    node_tri = sa.load_triangles('big_data.tri')
    weight = {'rnd':0.5, 'mns':2.5, 'exe':1, 'unl':0.1}
    #sa.analyze_triangle(node_tri, nodes, weight)
    sa.machine_learning(graph, nodes, sel_nodes, node_tri)


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
