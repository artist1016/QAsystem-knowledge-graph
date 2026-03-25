# -*- coding: utf-8 -*-
from py2neo import Node, Graph, Relationship, NodeMatcher


# 过程：1、创建图 2、创建节点 3、建立关系 4、查找

class DataToNeo4j(object):
    """将excel中数据存入neo4j"""

    def __init__(self):
        """建立连接"""
        # link = Graph("http://localhost:7474", username="neo4j", password="wangmeng")#老版本neo4j用这个调用
        link = Graph("http://localhost:7474", auth=("neo4j", "123"))  # 在高版本Graph不支持username参数，也创建了图
        self.graph = link
        # self.graph = NodeMatcher(link)
        # 定义label
        self.name = 'name'
        self.define = 'define'
        self.form = 'form'
        self.cause = 'cause'
        self.method = 'method'
        self.help = 'help'


        self.graph.delete_all()  # 之前做的所有内容先删掉
        self.matcher = NodeMatcher(link)


    def create_node(self, node_name_key, node_define_key, node_form_key, node_cause_key, node_method_key, node_help_key):
        """建立节点"""
        for name in node_name_key:
            name_node = Node(self.name, name=name)  # name是这个节点的属性
            self.graph.create(name_node)
        for name in node_define_key:
            define_node = Node(self.define, name=name)
            self.graph.create(define_node)
        for name in node_form_key:
            form_node = Node(self.form, name=name)
            self.graph.create(form_node)
        for name in node_cause_key:
            cause_node = Node(self.cause, name=name)
            self.graph.create(cause_node)
        for name in node_method_key:
            method_node = Node(self.method, name=name)
            self.graph.create(method_node)
        for name in node_help_key:
            help_node = Node(self.help, name=name)
            self.graph.create(help_node)


    def create_relation(self, df_data):
        """建立关系"""
        m = 0
        for m in range(0, len(df_data)):
            try:
                print(list(self.matcher.match(self.name).where(
                    "_.name=" + "'" + df_data['name'][m] + "'")))  # 打印关系里面的buy和sell节点，.where是匹配条件
                print(list(self.matcher.match(self.define).where(
                    "_.name=" + "'" + df_data['define'][m] + "'")))  # 这样写是为了匹配dataframe里面的字符串
                print(list(self.matcher.match(self.form).where(
                    "_.name=" + "'" + df_data['form'][m] + "'")))  # 这样写是为了匹配dataframe里面的字符串
                print(list(self.matcher.match(self.cause).where(
                    "_.name=" + "'" + df_data['cause'][m] + "'")))  # 这样写是为了匹配dataframe里面的字符串
                print(list(self.matcher.match(self.method).where(
                    "_.name=" + "'" + df_data['method'][m] + "'")))  # 打印关系里面的buy和sell节点，.where是匹配条件
                print(list(self.matcher.match(self.help).where(
                    "_.name=" + "'" + df_data['help'][m] + "'")))  # 这样写是为了匹配dataframe里面的字符串


                rel1 = Relationship(
                    self.matcher.match(self.name).where("_.name=" + "'" + df_data['name'][m] + "'").first(),
                    df_data['define1'][m],
                    self.matcher.match(self.define).where("_.name=" + "'" + df_data['define'][m] + "'").first())

                rel2 = Relationship(
                    self.matcher.match(self.name).where("_.name=" + "'" + df_data['name'][m] + "'").first(),
                    df_data['form1'][m],
                    self.matcher.match(self.form).where("_.name=" + "'" + df_data['form'][m] + "'").first())

                rel3 = Relationship(
                    self.matcher.match(self.name).where("_.name=" + "'" + df_data['name'][m] + "'").first(),
                    df_data['cause1'][m],
                    self.matcher.match(self.cause).where("_.name=" + "'" + df_data['cause'][m] + "'").first())

                rel4 = Relationship(
                    self.matcher.match(self.name).where("_.name=" + "'" + df_data['name'][m] + "'").first(),
                    df_data['method1'][m],
                    self.matcher.match(self.method).where("_.name=" + "'" + df_data['method'][m] + "'").first())

                rel5 = Relationship(
                    self.matcher.match(self.name).where("_.name=" + "'" + df_data['name'][m] + "'").first(),
                    df_data['help1'][m],
                    self.matcher.match(self.help).where("_.name=" + "'" + df_data['help'][m] + "'").first())


                self.graph.create(rel1)
                self.graph.create(rel2)
                self.graph.create(rel3)
                self.graph.create(rel4)
                self.graph.create(rel5)


            except AttributeError as e:
                print(e, m)
