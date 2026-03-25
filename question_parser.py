# -*- coding: utf-8 -*-
# -*- name: Dai Yi -*-
# -*- last time: 2024/5/24 -*-


class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict


    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)#调用上面的构造实体节点函数
        question_types = res_classify['question_types']#需要question_classifier.py完成问题类型的识别
        sqls = []
        for question_type in question_types:
            sql_ = {}#注意与下面sql的区别
            sql_['question_type'] = question_type
            sql = []

            if question_type == 'help1':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))#sql_transfer是下面定义的分开处理问题子函数

            elif question_type == 'define1':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'form1':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'cause1':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'method1':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))


            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls#返回sql查询语句，可以是多条，给图谱



    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询原因，在debug的时候，运行到对应的elif（说明已经找到合适的关系）会自动停止该函数的执行


        # 查询求助对象
        if question_type == 'help1':
            #sql = ["MATCH (m:name) where m.name = '{0}' return m.name".format(i) for i in entities]#调用match语句
            sql = ["MATCH (m:name)-[r:turn_to]->(n:help) where m.name = '{0}' return n.name".format(i) for i in entities]#调用match语句


        # 查询原因
        elif question_type == 'cause1':
            # sql = ["MATCH (m:name) where m.name = '{0}' return m.name".format(i) for i in entities]#调用match语句
            sql = ["MATCH (m:name)-[r:cause]->(n:cause) where m.name = '{0}' return m.name, n.name".format(i)
                   for i in entities]  # 调用match语句


        # 查询定义
        elif question_type == 'define1':
            sql = ["MATCH (m:name)-[r:meaning]->(n:define) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]


        # 查询种类
        elif question_type == 'form1':
            sql = ["MATCH (m:name)-[r:form]->(n:form) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]


        # 查询措施
        elif question_type == 'method1':
            sql = ["MATCH (m:name)-[r:method]->(n:method) where m.name = '{0}' return n.name".format(i) for i in entities]


        return sql



if __name__ == '__main__':
    handler = QuestionPaser()
