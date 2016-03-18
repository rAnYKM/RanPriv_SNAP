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


def net_extractor(ego, conditions, categories, new_feats):
    """
    Get a list of nodes with features in specific categories.
    Condition Format Example:
    {'institution':['Google', 'Apple']}
    :param ego: String
    :param conditions: Dict
    :param categories: List
    :return:
    """
    feats = load_feat_name(ego)
    nodes = load_node_feat(ego)
    cons = __conditions_transform(conditions, feats)
    nodes.append((ego, ego_loader(ego)))
    sel_nodes = dict()
    for uid, indices in nodes:
        flag = False
        for index in indices:
            if index in cons:
                flag =True
                break
        if flag:
            sel_nodes[uid] = indices
    new_nodes, new_feats = __fetch_new_features(sel_nodes, feats, new_feats, categories)
    return new_nodes, new_feats


def main():
    egos = load_egos()
    print 'Start!'
    nodes, feats = net_extractor(egos[0], {'institution': 'Google'}, ['job_title'], [])
    # print feats
    for n, indices in nodes.iteritems():
        print n,
        for index in indices:
            print feats[index][0],
        print '\n'

if __name__ == '__main__':
    main()




