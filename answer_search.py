# -*- coding: utf-8 -*-
# -*- name: Dai Yi -*-
# -*- last time: 2024/5/24 -*-

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):#调用数据库进行查询
        #self.g = Graph("http://localhost:7474", username="neo4j", password="123")#老版本neo4j
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123"))#输入自己修改的用户名，密码
        self.num_limit = 20#最多显示字符数量


    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']#sql_里面的关键字
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()#运行图数据库
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)#调用回复模板函数
            if final_answer:
                final_answers.append(final_answer)
        return final_answers



    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        if question_type == 'help1':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '您可以向{0}寻求帮助'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'cause1':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的原因是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'define1':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{1}指的是：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'form1':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}属于：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'method1':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '建议您{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
