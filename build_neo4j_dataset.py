# -*- coding: utf-8 -*-
from build_node_relation import DataToNeo4j
import pandas as pd

test_data = pd.read_excel('test_data_Demo.xls', header=0, keep_default_na=False)

# 可以先阅读下文档介绍API应用：https://py2neo.org/v4/index.html

def data_extraction():
    """节点数据抽取"""

    # 取出事件名称到list
    node_name_key = []
    for i in range(0, len(test_data)):
        node_name_key.append(test_data['事件名称'][i])

    # 取出事件定义到list
    node_define_key = []
    for i in range(0, len(test_data)):
        node_define_key.append(test_data['事件定义'][i])

    # 取出事件种类到list
    node_form_key = []
    for i in range(0, len(test_data)):
        node_form_key.append(test_data['事件种类'][i])

    # 取出事件原因到list
    node_cause_key = []
    for i in range(0, len(test_data)):
        node_cause_key.append(test_data['事件原因'][i])

    # 取出解决流程到list
    node_method_key = []
    for i in range(0, len(test_data)):
        node_method_key.append(test_data['解决流程'][i])

    # 取出向谁求助到list
    node_help_key = []
    for i in range(0, len(test_data)):
        node_help_key.append(test_data['向谁求助'][i])

    # 去除重复名称
    node_name_key = list(set(node_name_key))
    node_define_key = list(set(node_define_key))
    node_form_key = list(set(node_form_key))
    node_cause_key = list(set(node_cause_key))
    node_method_key = list(set(node_method_key))
    node_help_key = list(set(node_help_key))

    # value抽出作node
    node_list_value = []
    for i in range(0, len(test_data)):
        for n in range(1, len(test_data.columns)):
            node_list_value.append(test_data[test_data.columns[n]][i])

    # 去重
    node_list_value = list(set(node_list_value))
    # 将list中浮点及整数类型全部转成string类型
    node_list_value = [str(i) for i in node_list_value]

    return node_name_key, node_define_key, node_form_key, node_cause_key, node_method_key, node_help_key, node_list_value


def relation_extraction():

    links_dict = {}
    help_list = []
    method_list = []
    cause_list = []
    form_list = []
    define_list = []
    name_list = []

    for i in range(0, len(test_data)):  # 遍历数据，采集数据
        help_list.append(test_data[test_data.columns[5]][i])  # 向谁求助
        method_list.append(test_data[test_data.columns[4]][i])  # 方法
        cause_list.append(test_data[test_data.columns[3]][i])
        form_list.append(test_data[test_data.columns[2]][i])
        define_list.append(test_data[test_data.columns[1]][i])
        name_list.append(test_data[test_data.columns[0]][i])


    # 将数据中int类型全部转成string，全部数据转换为字符串
    help_list = [str(i) for i in help_list]
    method_list = [str(i) for i in method_list]
    cause_list = [str(i) for i in cause_list]
    form_list = [str(i) for i in form_list]
    define_list = [str(i) for i in define_list]
    name_list = [str(i) for i in name_list]

    # 整合数据，将list整合成一个dict
    links_dict['help'] = help_list
    links_dict['method'] = method_list
    links_dict['cause'] = cause_list
    links_dict['form'] = form_list
    links_dict['define'] = define_list
    links_dict['name'] = name_list

    links_dict['help1'] = 'turn_to'
    links_dict['method1'] = 'method'
    links_dict['cause1'] = 'cause'
    links_dict['form1'] = 'form'
    links_dict['define1'] = 'meaning'


    # 将数据转成DataFrame
    df_data = pd.DataFrame(links_dict)
    print(df_data)  # 练习题中34个元素
    return df_data


create_data = DataToNeo4j()  # 调用外部py的子函数，建立连接，把图数据库先建好
create_data.create_node(data_extraction()[0], data_extraction()[1], data_extraction()[2], data_extraction()[3], data_extraction()[4], data_extraction()[5])  # 建立结点。利用函数的第0个，第1个返回值
create_data.create_relation(relation_extraction())  # 建立关系，利用relation_extraction返回的dataframe
