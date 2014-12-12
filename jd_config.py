#!coding:utf-8
'''
Created on Dec 8, 2014

@author: xx
'''


'''   
default path
'''
dataPath = 'data/'       #主路径
infoPath = dataPath + 'info/'
commentPath = dataPath + 'comments/'
jsonPath = dataPath + 'info.json/'
txtPath = dataPath + 'info.word/'
BOWPath = dataPath + 'info.BOW/'
wordPath = dataPath + 'info.word/'



'''   
default files
'''
# 停用词表
stopFile = [dataPath + 'stopwords/stop_ch.txt', 
            dataPath + 'stopwords/stop_chr.txt', 
            dataPath + 'stopwords/stop_en.txt']



'''   
default parameters
'''
# 爬虫参数
root_url = 'http://wap.jd.com/category/all.html' #爬虫根页面
is_test = False         # 是否测试爬虫
num_subcategory = 30    # 默认每个类下爬取30个小类 
num_product = 10        # 默认每个小类爬取10个商品
start_cat = None

# 预处理参数
is_rmLowCount = True    # 是否删除低频词
is_rmHighCount = False  # 是否删除高频词
is_rmLong = True        # 是否删除过长的word（默认15）
is_rmShort = True       # 是否删除过短的word（默认1）
verbose = False         # 冗余模式显示







