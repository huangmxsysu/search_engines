#-*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render
# import sys
# sys.reload()
# sys.setdefaultencoding('utf-8')

def shouye(request):
    return render(request,'base.html')

# #!/usr/lib/python3
# #!----coding: utf-8 -----------
import operator
# import mysqldb
import jieba
import json
import io
import math
import os
'''
#合并多个文件
def convert_to_alldata():
    with open('data_/gzdata.json', 'r', encoding='utf-8') as f1:
        js1 = json.load(f1)
        f2 = open('data_/hzdata.json', 'r', encoding='utf-8')
        f3 = open('data_/szdata.json', 'r', encoding='utf-8')
        js2 = json.load(f2)
        js3 = json.load(f3)
        js1 = js1 + js2 + js3
        f2.close()
        f3.close()

    js1 = json.dumps(js1, ensure_ascii=False)
    with open('alldata.json', 'w', encoding='utf-8') as outputfile:
        outputfile.write(js1)
'''

class IndexModule:
    stop_words = {}
    docs = []
    postings_lists = {}
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data_/stop_words.txt')
    def __init__(self):
        words = open(self.file_path, 'r', encoding='utf-8').read()
        self.stop_words = set(words.split('\n'))

    def is_number(self, n):
        try:
            n = float(n)
            return True
        except:
            return False

    def cal_df(self, items):
        dict_df = {}
        #统计词频
        n = 0
        for item in items:
            item = item.strip().lower()
            if item != '' and not self.is_number(item) and item not in self.stop_words:
                n = n + 1
                if item in dict_df.keys():
                    dict_df[item] += 1
                else:
                    dict_df[item] = 1
        return n, dict_df

    def construct_postings_lists(self):
        f = open('alldata.json', 'r', encoding='utf-8')
        self.docs = json.load(f)
        index_lists = {}
        doc_id = -1
        # docs [ 0, 1, 2,...]
        for doc in self.docs:
            doc_id += 1
            toparse = doc['description'] + '。' + doc['title']
            items = jieba.lcut(toparse, cut_all=False)
            n, dict_df = self.cal_df(items)
            for key, value in dict_df.items():
                d = (doc_id, value, n)   #doc, frequency
                if key in self.postings_lists.keys():
                    self.postings_lists[key][0] += 1
                    self.postings_lists[key][1].append(d)
                else:
                    self.postings_lists[key] = [1, [d]]
        f.close()
    
    def save_postings_lists(self):
        global pl_fname
        pls = json.dumps(self.postings_lists, ensure_ascii=False)
        with open(pl_fname, 'w', encoding='utf-8') as outputfile:
            outputfile.write(pls)

    def read_postings_lists(self):
        pl_fname = 'se/save.db'
        filename = os.path.join(self.module_dir, 'se/alldata.json')
        f = open(filename, 'r', encoding='utf-8')
        self.docs = json.load(f)
        filename = os.path.join(self.module_dir, pl_fname)
        with open(filename, 'r', encoding='utf-8') as f:
            self.postings_lists = json.load(f)

class Search_Engine:
    K1 = 0
    B = 0
    N = 0
    AVG_L = 0 #平均文档长度
    idx = 0
    def __init__(self, idx):
        self.idx = idx
        totalL = 0
        self.B = 0.75
        self.K1 = 1.5
        self.N  = len(self.idx.docs)
        for key, value in self.idx.postings_lists.items():
            items = value[1]
            for item in items:
                totalL += item[2]
        self.AVG_L = totalL / float(len(self.idx.docs))

    def cal_df(self, items):
        dict_df = {}
        #统计词频
        n = 0
        for item in items:
            item = item.strip().lower()
            if item != '' and not self.idx.is_number(item) and item not in self.idx.stop_words:
                n = n + 1
                if item in dict_df.keys():
                    dict_df[item] += 1
                else:
                    dict_df[item] = 1
        return n, dict_df

    def search_by_BM25(self, sentence):
        seg_list = jieba.lcut(sentence, cut_all=False)
        n, cleaned_dict = self.cal_df(seg_list)
        BM25_scores = {}
        for term in cleaned_dict.keys():
            r = self.fetch_from_db(term)
            if r is None:
                continue
            #[key] = [df, (docs,df),...]
            df = r[0]
            w = math.log2((self.N - df + 0.5) / (df + 0.5))
            docs_info = r[1]
            for doc in docs_info:
                docid, tf, ld = doc
                docid = int(docid)
                tf = int(tf)
                ld = int(ld)
                s = (self.K1 * tf * w) / (tf + self.K1 * (1 - self.B + self.B * ld / self.AVG_L))
                if docid in BM25_scores:
                    BM25_scores[docid] = BM25_scores[docid] + s
                else:
                    BM25_scores[docid] = s

        BM25_scores = sorted(BM25_scores.items(), key = operator.itemgetter(1))
        BM25_scores.reverse()
        if len(BM25_scores) == 0:
            return 0, []
        else:
            return 1, BM25_scores


    # 文件读写当db
    def fetch_from_db(self, term):
        '''CREATE TABLE postings (term TEXT PRIMARY KEY, df INTEGER, docs TEXT)'''
        if term in self.idx.postings_lists.keys():
            return self.idx.postings_lists[term]
        else:
            return None

# if __name__ == '__main__':
#     idx = IndexModule()
#     # 待填充配置
#     config = {}
#     pl_fname = 'save.db'
#     # idx.construct_postings_lists()
#     # idx.save_postings_lists()
#     idx.read_postings_lists()
#     se = Search_Engine()
#     while 1:
#         a = input('Please input keywords:')
#         a, res = se.search_by_BM25(a)
#         for doc_id, name in res[:10]:
#             print(idx.docs[doc_id])


def search(request):
    idx = IndexModule()
    # 待填充配置
    config = {}
    pl_fname = 'save.db'
    idx.read_postings_lists()
    se = Search_Engine(idx)

    # if 'searchword' in request.GET:
    #     message = 'You searched for: %r' % request.GET['searchword']
    # else:
    #     message = 'You submitted an empty form.'
    print(request.GET['searchword'])
    print(type(request.GET['searchword']))
    searchword = request.GET['searchword']

    a, sousuolist = se.search_by_BM25(searchword)
    newlist = []
    for doc_id, name in sousuolist[:40]:
        print(idx.docs[doc_id])
        newlist.append(idx.docs[doc_id])


    # sousuolist = [ { 'link': 'http://zu.sz.fang.com//chuzu/1_51929532_-1.htm',
    #                 'title': '龙岗布吉怡康家园56平米',
    #                 'price': 2200,
    #                 'description': '住宅 1室1厅1卫 56 中层共30层 南北 豪华装修',
    #                 'addr': '大芬村深惠公路西侧沃尔玛斜',
    #                 'imageurl': 'http://img11.soufunimg.com/viewimage/rent/2017_06/10/M14/06/B0/ChCE4Vk7VcuIfet5AADeNEAX82MAAgEAQKhLW0AAN5M943/722x542.jpg' } ,
                    

    #                 { 'link': 'http://zu.sz.fang.com//chuzu/1_51929532_-1.htm',
    #                 'title': '龙岗布吉怡康家园56平米',
    #                 'price': 2200,
    #                 'description': '住宅 1室1厅1卫 56 中层共30层 南北 豪华装修',
    #                 'addr': '大芬村深惠公路西侧沃尔玛斜',
    #                 'imageurl': 'http://img11.soufunimg.com/viewimage/rent/2017_06/10/M14/06/B0/ChCE4Vk7VcuIfet5AADeNEAX82MAAgEAQKhLW0AAN5M943/722x542.jpg' } ,


    #                 { 'link': 'http://zu.sz.fang.com//chuzu/1_51929532_-1.htm',
    #                 'title': '龙岗布吉怡康家园56平米',
    #                 'price': 2200,
    #                 'description': '住宅 1室1厅1卫 56 中层共30层 南北 豪华装修',
    #                 'addr': '大芬村深惠公路西侧沃尔玛斜',
    #                 'imageurl': 'http://img11.soufunimg.com/viewimage/rent/2017_06/10/M14/06/B0/ChCE4Vk7VcuIfet5AADeNEAX82MAAgEAQKhLW0AAN5M943/722x542.jpg' } 
    #                 ]

    print(type(newlist))

    return render(request, 'show_result.html', {'searchword':searchword,'sousuolist': newlist})



