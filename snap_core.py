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


DATA_SET_NAME = 'RanPriv'
SNAP_DIR = 'E:\\RanPriv\\gplus\\gplus'
RAW_DATA_DIR = 'data'
OUT_DATA_DIR = 'out'
EGO_FILE = 'ego.nodes'
EGO_EDGE = 'gplus_combined.txt'
SYMBOLS = ',.?;:[]\!@#$%^&*()-'


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


def load_data_set(filename=DATA_SET_NAME):
    with open(os.path.join(OUT_DATA_DIR, filename + '.node'), 'rb') as fp:
        lines = [line.strip('\r\n').split(' ') for line in fp.readlines()]
        nodes = {item[0]:(item[1].split(','), item[2].split(','))
                 for item in lines}
    with open(os.path.join(OUT_DATA_DIR, filename + '.edge'), 'rb') as fp:
        edges = [line.strip('\r\n').split(' ') for line in fp.readlines()]
    with open(os.path.join(OUT_DATA_DIR, filename + '.feat'), 'rb') as fp:
        lines = [line.strip('\r\n').split(' ') for line in fp.readlines()]
        feats = {item[1]:item[2] for item in lines}
    return nodes, edges, feats


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
