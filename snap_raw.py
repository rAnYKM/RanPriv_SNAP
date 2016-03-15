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
# Create Date   :   Mar. 11, 2016
# Version       :   1.0.0
# Description   :   Raw data processor


from snap_core import *
from collections import Counter
import snap_generator as sg


LABEL_FILE = 'labeled.keyword'


def __feat2label(feat, labels):
    pure_feat = feat.strip(SYMBOLS)
    if pure_feat not in labels:
        return 'null'
    else:
        return labels[pure_feat]


def __set_builder(li):
    S = set()
    for item in li:
        pure_item = item.strip(SYMBOLS)
        S.add(pure_item)
    return S


def feats2labels(feats, labels, category):
    feat_dict = {index: __feat2label(name, labels)
                 for name, cate, index in feats
                 if cate == category and __feat2label(name, labels) != 'null'}
    print feat_dict
    return feat_dict


def nodes_labeler(egos, labels):
    new_nodes = {}
    for ego in egos:
        feats = load_feat_name(ego)
        nodes = load_node_feat(ego)
        feat_dict = feats2labels(feats, labels, 'job_title')
        for uid, feat_index in nodes:
            label = 'null'
            if uid in new_nodes:
                continue
            for index in feat_index:
                if index in feat_dict:
                    tmp_label = feat_dict[index]
                    if tmp_label == 'mns':
                        label = tmp_label
                    elif tmp_label == 'exe' and tmp_label not in ['mns']:
                        label = tmp_label
                    elif tmp_label == 'rnd' and tmp_label not in ['mns', 'exe']:
                        label = tmp_label
            if label != 'null':
                new_nodes[uid] = label
        label_count = [label for uid, label in new_nodes.iteritems()]
        ctr = Counter(label_count)
        print ctr
        print(uid, str(len(new_nodes.keys())))
    print 'end'
    with open(os.path.join(OUT_DATA_DIR, 'ranykm.nodes'), 'wb') as fp:
        for uid, feat in new_nodes.iteritems():
            fp.write(uid + ',' + feat + '\r\n')
    print 'finished'
    sg.small_edge_generator(new_nodes.keys(), EGO_EDGE, 'ranykm.edges')


def frequency_analysis(feats, nodes, category, former_set, threshold=5):
    ctr_feat = {index: 0 for name, cate, index in feats if cate == category and 'ascii' not in name and len(name) > 1}
    for uid, feat_index in nodes:
        for index in feat_index:
            if index in ctr_feat:
                ctr_feat[index] += 1
    freq_feat = {feats[index][0]: value for index, value in ctr_feat.iteritems() if value >= threshold}
    feat_set = __set_builder(freq_feat.keys())
    return feat_set | former_set


def load_labeled_keyword(filename=LABEL_FILE):
    with open(os.path.join(RAW_DATA_DIR, filename), 'r') as fp:
        lines = [line.strip('\r\n').split(' ') for line in fp.readlines()]
        labels = {l[0]: l[1] for l in lines}
    return labels


def test_Mar11():
    egos = load_egos()
    feat_set = set()
    for ego in egos:
        feats = load_feat_name(ego)
        nodes = load_node_feat(ego)
        feat_set = frequency_analysis(feats, nodes, 'job_title', feat_set, 10)
    with open(os.path.join(RAW_DATA_DIR, 'labeled.keyword'), 'w+') as fp:
        for feat in feat_set:
            fp.write(feat + '\n')


def test_Mar12():
    egos = load_egos()
    labels =load_labeled_keyword()
    nodes_labeler(egos, labels)
    print ('Fin. by rAn')


if __name__ == '__main__':
    test_Mar12()
