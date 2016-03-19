# Project Name  :   RanPriv
# Author        :   rAnYKM (Jiayi Chen)
# ______              ______       _
# | ___ \             | ___ \     (_)
# | |_/ / __ _  _ __  | |_/ /_ __  _ __   __
# |    / / _` || '_ \ |  __/| '__|| |\ \ / /
# | |\ \| (_| || | | || |   | |   | | \ V /
# \_| \_|\__,_||_| |_|\_|   |_|   |_|  \_/
#
# Script Name   :   snap_specific.py
# Create Date   :   Mar. 17, 2016
# Version       :   1.0.0
# Description   :   Get specific information from data sets.


from snap_generator import *


def __in_list(item, li):
    if item not in li:
        return -1
    else:
        return li.index(item)


def __conditions_transform(conditions, feats):
    index = []
    for cate, names in conditions.iteritems():
        for n in names:
            tmp_index = [no - 1 for name, cat, no in feats if n in name and cat == cate]
            index += tmp_index
    print index
    return index


def __fetch_new_features(sel_nodes, feats, new_feats, categories):
    new_nodes = {}
    for uid, indices in sel_nodes.iteritems():
        new_indices = []
        for index in indices:
            feat, cate, no = feats[index]
            if cate not in categories:
                continue
            feat = feat.strip(SYMBOLS)
            if 'ascii' in feat or len(feat) <= 1:
                continue
            val = __in_list((feat, cate), new_feats)
            if val == -1:
                new_feats.append((feat, cate))
                new_indices.append(len(new_feats) - 1)
            else:
                new_indices.append(val)
        new_nodes[uid] = new_indices
    return new_nodes, new_feats


def __process_nodes(line):
    l = line.strip('\n').split(':')
    if l[1] != '':
        indices = [eval(item) for item in l[1].split(' ')]
    else:
        indices = [-1]
    return l[0], indices


def ego_loader(ego):
    """
    Fetch selected ego's feature pattern
    :param ego: String
    :return: List
    """
    with open(os.path.join(SNAP_DIR, ego + '.egofeat'), 'rb') as fp:
        l = fp.readline().strip('\r\n')
        bin_feats = l.split(' ')
        index = [num for num, value in enumerate(bin_feats) if value == '1']
    return index


def load_sp_node_feat(filename):
    nodes = {}
    with open(os.path.join(OUT_DATA_DIR, filename + '[sp].nodes')) as fpa:
        lines = fpa.readlines()
        for l in lines:
            uid, indices = __process_nodes(l)
            nodes[uid] = indices
    with open(os.path.join(OUT_DATA_DIR, filename + '[sp].feats')) as fpb:
        lines = fpb.readlines()
        feats = [line.strip('\r\n').split(',') for line in lines]
    return nodes, feats


def net_extractor(ego, conditions, categories, new_nodes, new_feats):
    """
    Get a list of nodes with features in specific categories.
    Condition Format Example:
    {'institution':['Google', 'Apple']}
    :param ego: String
    :param conditions: Dict
    :param categories: List
    :param new_nodes: Dict
    :param new_feats: List
    :return: Dict, List
    """
    feats = load_feat_name(ego)
    nodes = load_node_feat(ego)
    cons = __conditions_transform(conditions, feats)
    nodes.append((ego, ego_loader(ego)))
    sel_nodes = dict()
    for uid, indices in nodes:
        if uid in new_nodes:
            continue
        flag = False
        for index in indices:
            if index in cons:
                flag = True
                break
        if flag:
            sel_nodes[uid] = indices
    tmp_nodes, new_feats = __fetch_new_features(sel_nodes, feats, new_feats, categories)
    new_nodes.update(tmp_nodes)
    return new_nodes, new_feats


def write_sp_node_files(filename, nodes, feats):
    """
    write nodes and feats into files, and generate a preview file for classification
    :param filename: String
    :param nodes: Dict
    :param feats: List
    :return: None
    """
    with open(os.path.join(OUT_DATA_DIR, filename + '[sp].nodes'), 'wb') as fpa,\
            open(os.path.join(OUT_DATA_DIR, filename + '[sp].labels'), 'wb') as fpb:
        for uid, indices in nodes.iteritems():
            str_indices = [str(i) for i in indices]
            name_indices = [feats[i][0] for i in indices]
            fpa.write(uid + ':' + ' '.join(str_indices) + '\n')
            fpb.write(uid + ':' + ' '.join(name_indices) + ':\n')
    with open(os.path.join(OUT_DATA_DIR, filename + '[sp].feats'), 'wb') as fp:
        for name, cate in feats:
            fp.write(name + ',' + cate + '\n')


def main():
    egos = load_egos()
    nodes = {}
    feats = []
    print 'Start!'
    for ego in egos:
        print ego + ' -> extracting start!'
        nodes, feats = net_extractor(ego, {'institution': ['Google']}, ['job_title'], nodes, feats)
        print 'Current Node Number: %d, Feat Number: %d' % (len(nodes), len(feats))
    # print feats
    '''
    for n, indices in nodes.iteritems():
        print n,
        for index in indices:
            print feats[index][0],
        print '\n'
    '''
    write_sp_node_files('RanGoogle', nodes, feats)
    print ('Fin. by rAnYKM')


def __ran_test():
    nodes, feats = load_sp_node_feat('RanGoogle')
    print 'Start Edge Generator'
    edge_generator(nodes.keys(), EGO_EDGE, 'RanGoogle[sp]')
    print 'Fin. by rAnYKM'


if __name__ == '__main__':
    __ran_test()
