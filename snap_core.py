# Project Name  :   RanPriv
# Author        :   rAnYKM (Jiayi Chen)
# ______              ______       _
# | ___ \             | ___ \     (_)
# | |_/ / __ _  _ __  | |_/ /_ __  _ __   __
# |    / / _` || '_ \ |  __/| '__|| |\ \ / /
# | |\ \| (_| || | | || |   | |   | | \ V /
# \_| \_|\__,_||_| |_|\_|   |_|   |_|  \_/
#
# Script Name   :   snap_core.py
# Create Date   :   Mar. 2, 2016
# Version       :   1.0.0
# Description   :   This is the core file to deal with SNAP data set.


import os


SNAP_DIR = 'E:\\RanPriv\\gplus\\gplus'
RAW_DATA_DIR = 'data'
OUT_DATA_DIR = 'out'
EGO_FILE = 'ego.nodes'


def __feat_process(feat):
    """
    :type feat: string
    """
    pairs = feat.strip('\r\n').split(':')
    name = pairs[1]
    no_cate = pairs[0].split(' ')
    return name, no_cate[1], eval(no_cate[0])


def __node_process(feat):
    li = feat.strip('\r\n').split(' ')
    uid = li[0]
    fea = li[1:]
    index = [num for num, value in enumerate(fea) if value == '1']
    return uid, index


def load_egos(filename=EGO_FILE):
    """
    Load root nodes of all the ego networks
    Return a list of root node ids
    :type filename: string
    """
    with open(os.path.join(RAW_DATA_DIR, filename), 'rb') as fp:
        egos = [line.strip('\r\n') for line in fp.readlines()]
        return egos


def load_feat_name(uid):
    """
    Load all feature names of an ego network rooted by uid
    :type uid: string
    """
    with open(os.path.join(SNAP_DIR, uid + '.featnames'), 'rb') as fp:
        feats = [__feat_process(feat) for feat in fp.readlines()]
        return feats


def load_node_feat(uid):
    """
    Load all feature names of an ego network rooted by uid
    :type uid: string
    """
    with open(os.path.join(SNAP_DIR, uid + '.feat'), 'rb') as fp:
        nodes = [__node_process(feat) for feat in fp.readlines()]
        return nodes
