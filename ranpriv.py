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
from collections import Counter

IT_COMPANY = [
    'Apple', 'Amazon', 'Dell',
    'Facebook', 'Google', 'IBM',
    'Microsoft', 'Yahoo', 'Youtube',
    'Intel', 'Mozilla', 'Cisco',
    'HP', 'Hewlett Packard', 'Hewlett-Packard'
    ]


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
    print un_net.number_of_edges(), un_net.number_of_nodes()
    labeled_nodes = sc.fetch_node_label(nodes, feats, un_net.nodes())
    tongji = [val for _, val in labeled_nodes.iteritems()]
    ctr = Counter(tongji)
    for i in ['rnd', 'mns', 'exe', 'other', 'unl']:
        print i,ctr[i]
    sa.fetch_homophily(un_net, labeled_nodes, ['unl'])
    '''
    #print sa.fetch_label_homophily(un_net, labeled_nodes, 'rnd', [])
    nodes, edges = sc.load_sample_data_set()
    un_net = sc.build_undirected_graph(nodes.keys(), edges)
    tongji = [val for _, val in nodes.iteritems()]
    ctr = Counter(tongji)
    for i in ['rnd', 'mns', 'exe', 'unlabeled']:
        print i,ctr[i]
    sa.fetch_homophily(un_net, nodes, ['unlabeled'])
    print sa.fetch_label_homophily(un_net, nodes, 'rnd', [])


if __name__ == '__main__':
    main()
