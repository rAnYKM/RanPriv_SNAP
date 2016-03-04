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
    nodes, edges, feats = sc.load_data_set()
    print len(nodes), len(edges), len(feats)

if __name__ == '__main__':
    main()
