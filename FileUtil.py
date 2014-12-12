#!coding:utf-8
'''
Created on Dec 9, 2014

@author: xx
'''
import jd_config
import jieba
import string


# 所有编码转化为unicode
def all2unicode(s):
    for c in ('utf-8', 'gbk', 'gb2312'):     
        try:  
            return s.decode(c)
        except:  
            pass  
        return 'unknown'  

def getStopWords():
    stopwords = []
    for fname in jd_config.stopFile:
        stopwords.extend([all2unicode(line.strip()) for line in open(fname).readlines()])
    stopwords.extend([u' ', u'\u3000', u'\xa0']) # 一些空格
    stopwords = set(stopwords)
    return stopwords

# unnecessary symbols, punctuation, numbers
def cleanStr(s, coding='unicode'):
    '''  
    分词前 去除某些符号   
    分词阶段去除的话，有可能会出现多符号word，如===作为一个单词，或者其他无意义字符，难以穷举符号组合
    当然还有一些有意义符号，比如O(∩_∩)O，肿么办
    '''
    if coding=='unicode':
        s = s.lower()
        halfStr = u'，。、！？{}￥……（）《》【】' #中文符号删除，或者在停用词库中删除
        #blank =  u' ' + u'\u3000'        # 空格需要在去停用词阶段删除更好
        delEStr = string.digits  + string.punctuation  + halfStr # + blank
        remove_punctuation_map = dict((ord(char), None) for char in delEStr)
        new_str = s.translate(remove_punctuation_map)
    else:
        table = string.maketrans('', '')
        delEStr = string.punctuation + string.digits  #ASCII 标点符号，数字，半角符号    
        new_str = s.translate(table, delEStr)    #去掉ASCII 标点符号和空格  
        
    return new_str

def cutWords(s):
    '''  去除某些符号，并分词   '''
    if jd_config.verbose:    print 'raw string:' + s
    else: print 'raw string:' + s[0:min(max(s),40)]+'...'
    wordList = list(jieba.cut(cleanStr(s)))
    if jd_config.verbose: print 'after wordcuts:' + ', '.join(wordList)
    else: print 'after wordcuts:' + ', '.join(wordList[0:min(max(wordList), 10)]) + '......'
    return wordList


def rmStopwords(wordList):
    '''  去除停用词   '''
    stopwords = getStopWords()
    wordList = [w for w in wordList if w not in stopwords] 
    if jd_config.is_rmLong:
        wordList = [w for w in wordList if len(w)<15]  #去除特别长的字符串
    if jd_config.is_rmShort:
        wordList = [w for w in wordList if len(w)>1]  #去除特别短的字符串
    print 'after stopwords：' + ', '.join(wordList[0:min(max(wordList), 10)]) + '......\n'
    return wordList



