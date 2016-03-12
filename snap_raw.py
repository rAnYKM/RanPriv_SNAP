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


def __set_builder(li):
    S = set()
    for item in li:
        pure_item = item.strip(SYMBOLS)
        S.add(pure_item)
    return S


def frequency_analysis(feats, nodes, category, former_set, threshold=5):
    ctr_feat = {index: 0 for name, cate, index in feats if cate == category and 'ascii' not in name and len(name) > 1}
    for uid, feat_index in nodes:
        for index in feat_index:
            if index in ctr_feat:
                ctr_feat[index] += 1
    freq_feat = {feats[index][0]: value for index, value in ctr_feat.iteritems() if value >= threshold}
    feat_set = __set_builder(freq_feat.keys())
    return feat_set | former_set


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


if __name__ == '__main__':
    test_Mar11()
