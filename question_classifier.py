# -*- coding: utf-8 -*-
# -*- name: Dai Yi -*-
# -*- last time: 2024/5/24 -*-

import os
import ahocorasick #调用这个（ac算法包）库函数

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        #　特征词路径
        self.name_path = os.path.join(cur_dir, 'dict/name.txt')
        self.define_path = os.path.join(cur_dir, 'dict/define.txt')
        self.form_path = os.path.join(cur_dir, 'dict/form.txt')
        self.cause_path = os.path.join(cur_dir, 'dict/cause.txt')
        self.method_path = os.path.join(cur_dir, 'dict/method.txt')
        self.help_path = os.path.join(cur_dir, 'dict/help.txt')


        # 加载特征词
        self.name_wds= [i.strip() for i in open(self.name_path,encoding="utf-8") if i.strip()]#encoding="utf-8"
        self.define_wds= [i.strip() for i in open(self.define_path,encoding="utf-8") if i.strip()]
        self.form_wds= [i.strip() for i in open(self.form_path,encoding="utf-8") if i.strip()]
        self.cause_wds= [i.strip() for i in open(self.cause_path,encoding="utf-8") if i.strip()]
        self.method_wds= [i.strip() for i in open(self.method_path,encoding="utf-8") if i.strip()]
        self.help_wds= [i.strip() for i in open(self.help_path,encoding="utf-8") if i.strip()]
        self.region_words = set(self.name_wds + self.define_wds + self.form_wds + self.cause_wds + self.method_wds + self.help_wds)
        # self.deny_words = [i.strip() for i in open(self.deny_path,encoding="utf-8") if i.strip()]


        # 构造领域actree，基于树匹配比关键词分割匹配更高效，ahocorasick是个现成的快速匹配函数
        self.region_tree = self.build_actree(list(self.region_words))#调用下面的build_actre函数


        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()#调用下面定义的build_wdtype_dict函数，构造词类型


        # 问句疑问词
        self.define_qwds = ['定义', '是什么', '是', '含义', '指的是', '内涵', '其实是', '通常是', '通常指',
                            '介绍', '简介', '解释', '释义', '想了解', '弄明白', '科普', '普及', '指']
        self.form_qwds = ['属于', '属于什么', '类型', '事件类型', '类', '种类', '哪一种', '哪种', '分为',
                            '分类']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会',
                           '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.method_qwds = ['解决', '怎么办', '如何', '方法', '措施', '方式', '针对', '有效应对',
                            '对策', '采取', '怎么', '怎样', '如何可以', '怎样才能', '怎么才能',
                            '咋样才能', '咋才能', '如何才能', '怎样才', '怎么才', '咋样才', '咋才',
                            '如何才', '应急', '怎样才可以', '怎么才可以', '咋样才可以', '咋才可以',
                            '怎样才可', '怎么才可', '咋样才可', '咋才可', '如何可', '咋']
        self.help_qwds = ['人员', '什么人', '工作人员', '向谁', '找谁', '谁', '联系谁', '帮助',
                          '向谁求助', '人或机构', '寻求支援', '帮助解决', '提供帮助', '帮忙', '助力',
                          '救助', '救急', '救星', '帮我', '挽救', '拯救', '求救']

        print('model init finished ......')


        return


    '''分类主函数'''
    def classify(self, question):
        data = {}
        emerhency_dict = self.check(question)#调用下面定义的check问句过滤函数
        if not emerhency_dict:
            return {}
        data['args'] = emerhency_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in emerhency_dict.values():
            types += type_
        question_type = 'others'#这句话无意义

        question_types = []

        #
        if self.check_words(self.define_qwds, question) and ('name' in types):#self.symptom_qwds来自于init，查找self.symptom_qwds是否在question内
            question_type = 'define1'
            question_types.append(question_type)

        if self.check_words(self.form_qwds, question) and ('name' in types):#check_words是下面定义的特征词分类函数
            question_type = 'form1'
            question_types.append(question_type)

        #
        if self.check_words(self.cause_qwds, question) and ('name' in types):
            question_type = 'cause1'
            question_types.append(question_type)
        #
        if self.check_words(self.method_qwds, question) and ('name' in types):
            question_type = 'method1'
            question_types.append(question_type)

        #
        if self.check_words(self.help_qwds, question) and 'name' in types:
            question_type = 'help1'
            question_types.append(question_type)


        # 若没有查到相关的外部查询信息，那么则将描述信息返回
        if question_types == [] and 'name' in types:
            question_types = ['name']


        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data


    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:#找到用户输入的词是什么范围的，比如用户输入火灾，这个单词属于？
            wd_dict[wd] = []
            if wd in self.name_wds:
                wd_dict[wd].append('name')
            if wd in self.define_wds:
                wd_dict[wd].append('define')
            if wd in self.form_wds:
                wd_dict[wd].append('form')
            if wd in self.cause_wds:
                wd_dict[wd].append('cause')
            if wd in self.method_wds:
                wd_dict[wd].append('method')
            if wd in self.help_wds:
                wd_dict[wd].append('help')
        return wd_dict


    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton() # 初始化trie树，ahocorasick 库 ac自动化 自动过滤违禁数据
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))   # 向trie树中添加单词
        actree.make_automaton()   # 将trie树转化为Aho-Corasick自动机
        return actree


    '''问句过滤'''
    def check(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):   # ahocorasick库 匹配问题  iter返回一个元组，i的形式如(3, (23192, '火灾'))
            wd = i[1][1]  # 匹配到的词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)   # stop_wds取重复的短的词
        final_wds = [i for i in region_wds if i not in stop_wds]     # final_wds取长词
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}#来自于构造词典，# 获取词和词所对应的实体类型

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
