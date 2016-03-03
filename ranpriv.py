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

IT_COMPANY = [ \
    'Apple', 'Amazon', 'Dell', \
    'Facebook', 'Google', 'IBM', \
    'Microsoft', 'Yahoo', 'Youtube', \
    'Intel', 'Mozilla', 'Cisco' \
    ]


def main():
    """
    :rtype: int
    """
    egos = sc.load_egos()
    print len(egos)
    feats = sc.load_feat_name(egos[0])
    nodes = sc.load_node_feat(egos[0])
    # node_feat = [feats[n][0] for n in nodes[5][1]]
    sel_nodes = sg.fetch_nodes(nodes, feats, 'institution', IT_COMPANY)
    print sel_nodes


if __name__ == '__main__':
    main()
