#!coding:utf-8
'''
Created on Dec 8, 2014

@author: xx
'''
import FileUtil

class dictionary(object):
    '''
    词典--所有文档共享
    '''

    def __init__(self, word2id={}, id2word=[], wordCount={}):
        self.word2id = word2id
        self.id2word = id2word
        self.wordCount = wordCount
    
    '''    get methods  '''
    def getWord(self, _id):
        return self.id2word[_id]
    
    def getID(self, word):
        return self.word2id[word]
    
    def size(self):
        assert(len(self.word2id)==len(self.id2word))
        assert(len(self.word2id)==len(self.wordCount))
        return len(self.word2id)
    
    '''    check methods  '''
    def has(self, word):
        return self.word2id.has_key(word)
    
    '''    add methods  '''
    def addWordList(self, wordList):
        for word in wordList:
            self.addWord(word)
    

    def addWord(self, word):
        if(not self.word2id.has_key(word)):
            _id = len(self.word2id)
            self.word2id[word] = _id
            self.wordCount[word] = 1
            self.id2word.append(word)
            return _id
        else:
            self.wordCount[word] = self.wordCount[word] + 1
            return self.getID(word)

    '''    delete methods  '''
    def clear(self):
        self.id2word.clear()
        self.word2id.clear()
        self.wordCount.clear()
        

    def rmWordList(self, rmList):
        '''
        删除一个word list，并重新做词典
        '''
        newList = list(set(self.id2word)-set(rmList))
        
        # 记录原始wordCount，并移除部分word
        wordCount = self.wordCount
        for word in rmList:
            if wordCount.has_key(word):
                wordCount.pop(word)
        
        # 重新做词典，更新word-id映射
        self.clear()
        self.addWordList(newList)
        
        # wordCount不变
        self.wordCount = wordCount
        

    
    def rmLowCount(self, lowerBound=4):
        '''
        删除低频词，很多时候低频词会是一些noise
        减少低频次同时能大幅度减小字典大小
        '''
        # 记录低频词
        rmList = [w for w in self.wordCount.keys() if self.wordCount[w]<lowerBound]
        self.rmWordList(rmList)
        

        
    def rmHighCount(self, higherBound=None):
        '''
        删除高频词，有时高频词会是一些noise，比如漏删的停用词
        '''
        if higherBound is None:
            maxCount = max([value for value in self.wordCount.values()])
            higherBound = maxCount*3/4
        rmList = [w for w in self.wordCount.keys() if self.wordCount[w]>higherBound]
        self.rmWordList(rmList)
        
        
    
        
    '''    I/O methos '''
    def readDict(self, fname):
        f = open(fname)
        words = f.readlines()
        f.close()
        
        for i in range(len(words)):
            word = words[i].strip()
            self.id2word[i] = word
            self.word2id[word] = i
        return True
    
    def saveDict(self, fname):
        f = open(fname, 'w')
        f.write('\n'.join([self.id2word[i] for i in range(len(self.id2word))]))
        f.close()
        return True
    
    def saveCount(self, fname, isSort=True):
        '''    默认存储标准： 按照count从高到低排序  '''
        wordCount = sorted(self.wordCount.iteritems(),
                                key=lambda d:d[1], reverse = True)
        
        f = open(fname, 'w')
        f.write('\n'.join([word[0]+':'+str(word[1]) for word in wordCount]))
        f.close()
    
            

        




class document(object):
    '''
    单个文档
    '''
    def __init__(self, rawStr='', wordList={}):
        '''
        Constructor
        '''
        self.rawStr = rawStr             #原始字段
        self.wordList = wordList         #分词后的word list
        #self.wordCount = wordCount       #存储格式： [(word, count), ...]
        #self.BOW = BOW                   #存储格式： [(id, count), ...]
        # wordList，wordCount，BOW详细但冗余，是否有必要都保留？
        # 优势：方便查看，不用每次查看都临时计算
        # 缺陷，三个的同时更新存在问题。


    
    def getList(self):
        '''    
        wordList依赖rawStr，但获取较慢，且经常用，因此设置为静态属性
        '''
        wordList = FileUtil.cutWords(self.rawStr)  # 去燥并分词
        wordList = FileUtil.rmStopwords(wordList)  # 去停用词
        
        self.wordList = wordList

        return self.wordList
    
    def getCount(self):
        '''    
        wordCount获取较快，且完全依赖wordList，因此未设置为静态属性
        '''
        if len(self.wordList)==0:
            print 'warning: wordList has no element'
            self.getList()
            self.getCount()

        wordCount = {key:self.wordList.count(key) 
                     for key in set(self.wordList)}
        return wordCount
    


    def getBOW(self, word2id):
        '''    
        × BOW获取较快，且完全依赖wordList，因此未设置为静态属性
        × 不宜主动频繁读取，推荐尽量从文件读取BOW
        '''
        wordCount = self.getCount()
        BOW = {word2id[key]:wordCount[key]
                    for key in wordCount.keys() if word2id.has_key(key)}
        return BOW
    
    
    def filterByDict(self, dicList):
        '''    
        过滤wordlist，一般用于词典变化过滤
        '''
        return [w for w in self.wordList if w in dicList] 

    def saveList(self, fname, saveFormat='csv'):
        '''    
        一般不存储为独立文件，因此以追加方式，或者传递File格式参数
        '''    
        wordList = self.getList()
        f = open(fname, 'a')
        f.write(','.join(wordList) + '\n')
        f.close()
        


    def saveBOW(self, fname, word2id, saveFormat='libSVM', isSort=True):
        '''    
        * doc是独立于documents的，因此必须要有dict才能存储BOW
        * 默认存储标准： 按照id从小到大排序
        '''
        f = open(fname, 'a')
        BOW = self.getBOW(word2id)
        BOW = sorted(BOW.iteritems(), key=lambda d:d[0], reverse = False)
        
        if saveFormat=='libSVM':
            f.write(' '.join([str(word[0])+':'+str(word[1])
                              for word in BOW]) + '\n')
        elif saveFormat=='json':
            pass
        elif saveFormat=='arff':
            pass
        else:
            print 'wrong format'
        
        f.close()
        return True
        
    def readDoc(self):
        pass
    
    def saveDoc(self):
        pass
        

        



    

class documents(object):
    '''
    文集
    '''
    dic = dictionary()
    wordCount = {}

    def __init__(self, dic=dictionary(), wordCount={}):
        pass
    
    def addDoc(self, doc=document()):
        ''' add a document   '''
        pass
    
    def addWord(self, word):
        ''' add a word   '''
        if not self.dic.has(word):
            self.dic.addWord(word)
            self.wordCount[word] = 1
    
    
    def saveWordCount(self):
        pass



        