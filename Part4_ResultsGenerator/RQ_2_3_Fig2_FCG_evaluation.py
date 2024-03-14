# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/10
# System: linux


# coding: utf-8
# Author: kaifa.zhao@connect.polyu.hk
# Copyright 2021@Kaifa Zhao (Zachary)
# Date: 2023/5/8
# System: linux
import os
import matplotlib.pyplot as plt


def get_fcg_node_number(fcg_file):
    nodes = []
    f = open(fcg_file, 'r')
    for i in f.readlines():
        caller = '<' + i.split('> ==> <')[0].split(' in <')[1] + '>'
        callee = '<' + i.split('> ==> <')[1].replace('\n', '')
        if caller not in nodes:
            nodes.append(caller)
        if callee not in nodes:
            nodes.append(callee)
    f.close()
    return len(nodes)


def analyze_fcg_file(fcg_folder):
    data = {}
    raw_folder = os.path.join(fcg_folder, 'raw')
    enhanced_folder = os.path.join(fcg_folder, 'enhanced')
    for t in os.listdir(raw_folder):
        print(t)
        if 'DS_Store' in t:
            continue
        tpl_name = t.replace('.txt', '')
        raw_file = os.path.join(raw_folder, t)
        raw_fcg_nodes_number = get_fcg_node_number(raw_file)
        enhanced_file = os.path.join(enhanced_folder, t)
        enhanced_fcg_nodes_number = get_fcg_node_number(enhanced_file)
        data[tpl_name] = [raw_fcg_nodes_number, enhanced_fcg_nodes_number]
    return data


def get_statistic_data(statistics_file):
    print(statistics_file)
    data = {}
    f = open(statistics_file, 'r')
    line = f.readline()
    line = f.readline()
    while (line):
        tmp = line.replace('\n', '').split(',')
        if tmp[0] not in data:
            data[tmp[0]] = [int(k) for k in tmp[1:]]
        line = f.readline()
    return data


if __name__ == '__main__':
    fcg_folder = '../Part3_BinaryFilesAnalysis/ATPChecker/FCG_Compare'
    statistics = '../Part3_BinaryFilesAnalysis/ATPChecker/fcg_statistic.csv'
    data_sta = get_statistic_data(statistics)
    data_fcg = analyze_fcg_file(fcg_folder)

    data_for_fig = []
    enhanced_edge_num_graph = []
    raw_edge_num_graph = []
    raw_FCG_cov_graph = []
    enhanced_FCG_Cov = []
    for i in data_fcg:
        num_enhanced_edge = data_sta[i][5]
        num_raw_edge = data_sta[i][2]
        num_enhanced_method = data_sta[i][3]
        num_raw_method = data_sta[i][0]
        num_enhanced_node = data_fcg[i][1]
        num_raw_node = data_fcg[i][0]
        #
        enhanced_edge_num_graph.append(num_enhanced_edge)
        enhanced_FCG_Cov.append(num_enhanced_node / num_enhanced_method)
        raw_edge_num_graph.append(num_raw_edge)
        raw_FCG_cov_graph.append(num_raw_node / num_raw_method)

    enhanced_edge_num_graph = [i / 1e5 for i in enhanced_edge_num_graph]
    raw_edge_num_graph = [i / 500 for i in raw_edge_num_graph]
    raw_FCG_cov_graph = [i * 100 for i in raw_FCG_cov_graph]
    enhanced_FCG_Cov = [i for i in enhanced_FCG_Cov]
    data = [raw_FCG_cov_graph, enhanced_FCG_Cov, raw_edge_num_graph, enhanced_edge_num_graph]

    fig7, ax7 = plt.subplots()
    ax7.boxplot(data)
    plt.ylim([0, 1])
    annotate_params = dict(fontsize=12, fontname='Courier', fontweight='bold')
    # plt.annotate('*100%', (0.121938779055203,0.0687074845224127),
    #              **annotate_params)
    plt.text(1, 0.420768705953779, '*100%', **annotate_params)
    plt.text(2, 0.624170066498, '*1%', **annotate_params)
    plt.text(3, 0.181312923640856, '500', **annotate_params)
    plt.text(4, 0.156823127351771, '*10^5', **annotate_params)
    #
    x_tick = ['raw_{cov}', 'ATPChecker_{cov}', 'raw_{#edge}', 'ATPChecker_{#edge}']
    ticks_kwargs = dict(fontsize=12, fontname='Courier', fontweight='bold')
    plt.xticks([i for i in range(1, 5, 1)], x_tick, rotation=15, **ticks_kwargs)

    #
    plt.grid(axis='both', linestyle='--')
    plt.show()