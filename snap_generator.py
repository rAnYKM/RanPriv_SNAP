# Project Name  :   RanPriv
# Author        :   rAnYKM (Jiayi Chen)
# ______              ______       _
# | ___ \             | ___ \     (_)
# | |_/ / __ _  _ __  | |_/ /_ __  _ __   __
# |    / / _` || '_ \ |  __/| '__|| |\ \ / /
# | |\ \| (_| || | | || |   | |   | | \ V /
# \_| \_|\__,_||_| |_|\_|   |_|   |_|  \_/
#
# Script Name   :   snap_generator.py
# Create Date   :   Mar. 2, 2016
# Version       :   1.0.0
# Description   :   Generate a small data set with constraints


from snap_core import *

IGNORE_FILE = 'ignore.keyword'
FEAT_FILE = 'RanPriv.feat'
NODE_FILE = 'RanPriv.node'
EDGE_FILE = 'RanPriv.edge'


def __which_keyword(item, keyword):
    for index, value in enumerate(keyword):
        if value.lower() in item.lower():
            return index, value
    return -1, 'null'


def __constraints(feats, cate, keyword):
    """
    Extract keyword related features
    :param feats: list of tuples
    :param cate: string
    :param keyword: string
    """
    cst_feats = [(index, __which_keyword(value[0], keyword)[1])
                 for index, value in enumerate(feats)
                 if value[1] == cate and __which_keyword(value[0], keyword)[0] >= 0]
    return cst_feats


def __list2dict(nodes):
    node_set = {}
    for uid, index in nodes:
        node_set[uid] = index
    return node_set


def fetch_nodes(nodes, feats, cate, keyword):
    cst_feats = __constraints(feats, cate, keyword)
    sel_nodes = []
    for uid, feat in nodes:
        sel_feat = []
        selected = False
        for index, value in cst_feats:
            if index in feat and value not in sel_feat:
                sel_feat.append(value)
                selected = True
        if selected:
            sel_nodes.append((uid, sel_feat))
    return sel_nodes


def data_generator(egos, cate, ignores, key_cate, keyword):
    print ('Welcome to use RanPriv Data Generator')
    new_feats = []
    new_nodes = {}
    for ego in egos:
        print ('Ego network: %s' % ego)
        feats = load_feat_name(ego)
        nodes = load_node_feat(ego)
        sel_nodes = fetch_nodes(nodes, feats, key_cate, keyword)
        node_set = __list2dict(nodes)
        print ('Features and Nodes Loaded')
        for uid, attr in sel_nodes:
            if uid in new_nodes:
                continue
            feat = node_set[uid]
            sel_feat = [feats[index][0].strip(SYMBOLS)
                        for index in feat
                        if feats[index][1] == cate and
                        feats[index][0] not in ignores and 'ascii' not in feats[index][0]]
            new_index = []
            for fea in sel_feat:
                if fea not in new_feats:
                    new_index.append(len(new_feats))
                    new_feats.append(fea)
                else:
                    new_index.append(new_feats.index(fea))
            if not new_index:
                new_index = [-1]
            new_node = (sorted(new_index), attr)
            new_nodes[uid] = new_node
        print ('Nodes added')
    print ('Begin to write files')
    write_nodes(new_nodes, new_feats)
    print ('Begin to write edges')
    edge_generator(new_nodes.keys())
    print ('Fin. By Ran')


def edge_generator(nodes, filename=EGO_EDGE, out_filename=EDGE_FILE):
    small_network = set()
    large_network = set()
    with open(os.path.join(SNAP_DIR, filename), 'rb') as fp:
        line = fp.readline().strip('\r\n')
        ctr = 0
        while line:
            pairs = line.split(' ')
            if pairs[0] in nodes:
                if pairs[1] in nodes:
                    small_network.add(line)
                else:
                    large_network.add(line)
            elif pairs[1] in nodes:
                large_network.add(line)
            line = fp.readline().strip('\r\n')
            ctr += 1
            if ctr % 50000 == 0:
                print ctr
        print ctr
    with open(os.path.join(OUT_DATA_DIR, out_filename), 'wb') as fp:
        for elem in small_network:
            fp.write(elem + '\r\n')
    print ('small network written')
    with open(os.path.join(OUT_DATA_DIR, 'large_' + out_filename), 'wb') as fp:
        for elem in large_network:
            fp.write(elem + '\r\n')
    print ('large network written')


def load_ignore_feat(filename=IGNORE_FILE):
    with open(os.path.join(RAW_DATA_DIR, filename), 'rb') as fp:
        igns = [line.strip('\r\n') for line in fp.readlines()]
        return igns


def write_nodes(nodes, feats, feat_file=FEAT_FILE, node_file=NODE_FILE):
    # write feature files
    with open(os.path.join(OUT_DATA_DIR, feat_file), 'wb') as fp:
        for index, value in enumerate(feats):
            fp.write(str(index) + ' ' + value + '\r\n')
    with open(os.path.join(OUT_DATA_DIR, node_file), 'wb') as fp:
        for uid, feat in nodes.iteritems():
            fp.write(uid + ' ' + ','.join(feat[1]) + ' ')
            str_index = [str(index) for index in feat[0]]
            fp.write(','.join(str_index) + '\r\n')
