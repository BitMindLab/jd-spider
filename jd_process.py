#!coding:utf-8
'''
Created on Dec 7, 2014

@author: xx
'''
import os
import json
from jd_item import product
from documents import dictionary, document
import jd_config



def object_decoder(obj):
    """
    convert json to object
    """   
    if '__type__' in obj and obj['__type__'] == 'product':
        return product(obj['id'], obj['url'], obj['title'], obj['category'],\
                       obj['price'], obj['meta'], obj['detail'])
    return obj




def merge_BOW():
    f_category = open(os.path.join(jd_config.dataPath, 'category'))
    lines = f_category.readlines()
    id2cat = [line.strip() for line in lines]
    
    f_category.close()
    
    
    f_BOW = open(os.path.join(jd_config.dataPath, 'product.BOW'), 'w') 
    for i in range(len(id2cat)):   # 遍历每个类
        cat = id2cat[i].strip()
        f_info_BOW = open(os.path.join(jd_config.BOWPath, cat + '.product.info.BOW')) 
        lines = f_info_BOW.readlines()
        newlines = [str(id2cat.index(cat))+' '+line.strip() 
                    for line in lines]
        f_info_BOW.close()
        f_BOW.write('\n'.join(newlines))
        
    f_BOW.close()
    





def preprocess(products):
    #stop=[line.strip().decode('gbk','ignore')for line in open(stopFile).readlines()]
    
    # 分词，去停用词，做词典
    dic = dictionary()
    for cat in products.keys():      # 遍历每个类
        prods = products[cat]
        for i in range(len(prods)):
            prod = prods[i]
            print prod.category +':' + str(i) + ':' + prod.id + ':' + prod.title
            prod.doc.getList()        # 分词，去停用词           
            dic.addWordList(prod.doc.wordList)
    
    # 词典浓缩（去除高频词/低频词）
    print 'dic_size before compress: ' + str(dic.size())
    if jd_config.is_rmLowCount:
        dic.rmLowCount(4)
    if jd_config.is_rmHighCount:
        dic.rmHighCount()
    print 'dic_size after compress: ' + str(dic.size())
    
    # 词频存储
    f_word_count = os.path.join(jd_config.dataPath,'word.count') 
    dic.saveCount(f_word_count)        
    
    # 做BOW
    for cat in products.keys():   # 遍历每个类
        #目录+文件检查  
        if (not os.path.exists(jd_config.txtPath) ):
            os.mkdir(jd_config.txtPath)
        f_info_txt = os.path.join(jd_config.txtPath, cat + '.product.info.word')
        if os.path.exists(f_info_txt):
            os.remove(f_info_txt)        
        if (not os.path.exists(jd_config.BOWPath) ):
            os.mkdir(jd_config.BOWPath)  
        f_info_BOW = os.path.join(jd_config.BOWPath, cat + '.product.info.BOW') 
        if os.path.exists(f_info_BOW):
            os.remove(f_info_BOW)
        
        # 获取并存储BOW和wordList    
        prods = products[cat]
        for i in range(len(prods)):
            prod = prods[i]
            prod.doc.filter(dic.id2word)  #对新词典重新过滤doc.wordList
            prod.doc.saveList(f_info_txt)  
            prod.doc.saveBOW(f_info_BOW, dic.word2id)
     
    merge_BOW()
            
    return products
        


def load_json_file(json_file):
    """
    return a list of product [single category]
    """   
    prods = []
    f = open(json_file)
    lines = f.readlines()
    aa=[]
    for line in lines:
        
        line = '{"__type__": "product", ' + line[1:]
        prod = json.loads(line, object_hook=object_decoder)
        Str = prod.title + prod.meta
        if (prod.detail != '暂无'):
            Str = Str + prod.detail
        doc = document()
        doc.rawStr = Str
        prod.doc = doc
        aa.append(Str)
        prods.append(prod)
    f.close()
    aa=prods
    return prods






def load_json_path(json_path):
    """
    return a list of product [all category]
    """   
   
    f_category = open(os.path.join(jd_config.dataPath, 'category'), 'w')

    products = dict()
    json_files = os.listdir(json_path)
    for json_file in json_files:
        if(json_file.endswith('json')):
            cat = json_file.split('.')[0]
            f_category.write(cat + '\n')     
            fullname = os.path.join(json_path, json_file)
            prods = load_json_file(fullname)
            products[cat] = prods
    f_category.close()
    return products

   
if (__name__ == '__main__'):

    
    products = load_json_path(jd_config.jsonPath)    
    products = preprocess(products)

    
    


        

        


