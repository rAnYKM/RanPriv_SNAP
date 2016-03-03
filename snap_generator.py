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


import snap_core as sc


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
    cst_feats = [(index, __which_keyword(value[0], keyword)[1]) \
                 for index, value in enumerate(feats) \
                 if value[1] == cate and __which_keyword(value[0], keyword)[0] >= 0]
    return cst_feats

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

