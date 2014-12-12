#!coding:utf-8
'''
Created on Dec 7, 2014

@author: xx
'''
import json
from documents import document


class product(object):
    '''
    单个商品（京东）
    '''
      
    def __init__(self, id='', url='', title='', category='', price='', meta='', detail='',
                 comments=[], doc=document()):
        '''    product原始信息    '''
        self.id = id
        self.url = url
        self.title = title
        self.category = category  #实际仅仅是类名，对应category.name
        self.price = price
        self.meta = meta
        self.detail = detail
        self.comments = comments  # a list of comment

        '''    product预处理后的信息    '''
        self.doc = doc            # document type

        

    
    # easy for json
    def to_dict(self):
        p_dict = dict()
        p_dict['id'] = self.id
        p_dict['category'] = self.category
        p_dict['url'] = self.url
        p_dict['title'] = self.title
        p_dict['price'] = self.price
        p_dict['meta'] = self.meta
        p_dict['detail'] = self.detail
        #self.p_dict['comments'] =
        return p_dict
    
    
    # easy for print
    def to_list(self):
        p_list = []
        p_list.extend(['id:' + self.id + '\n'])
        p_list.extend(['category:' + self.category + '\n'])
        p_list.extend(['url:' + self.url + '\n'])
        p_list.extend(['title:' + self.title + '\n'])
        p_list.extend(['price:' + self.price + '\n'])
        p_list.extend(['meta:' + self.meta + '\n'])
        p_list.extend(['detail:' + self.detail + '\n'])
        return p_list




    def load(self, Str, strFormat='json'):
        pass



    # save original info
    def save_info(self, f):
        p_list = self.to_list()
        f.writelines(p_list + ['\n'])     
        
        
    # save json format
    def save_info_json(self, f):
        p_dict = self.to_dict()
        p_json = json.dumps(p_dict)
        f.write(p_json + '\n')
        
    def save_comments(self, f):
        # write comments
        f.write('product_id:' + self.id + '\n')
        for c in self.comments:
            f.write(c.u_info + ':' + c.u_score + ':' + c.u_sum + '\n')
        f.write('\n')
    

class comment(object):
    '''    
    商品评论
    '''
    def __init__(self, u_info='', u_score='', u_sum=''):
        '''
        Constructor
        '''
        self.u_info = u_info   # 用户
        self.u_score = u_score # 评分
        self.u_sum = u_sum     # 总结/评论
    
    def show(self):
        print 'u_info: ' + self.u_info
        print 'u_score: ' + self.u_info
        print 'u_sum: ' + self.u_info



class category(object):
    '''
    商品类型
    '''
    def __init__(self, name='', url='', sub_url='', sub_category='', products={}):
        '''
        Constructor
        '''
        self.name = name
        self.url = url      # 大类url
        self.sub_url = sub_url  # 大类下还有小类 （这里未存储所有小类url，仅作临时变量用）
        self.sub_category = sub_category 
        self.products = products
        
        
    def save(self, products, fname):
        f = open(fname, 'w')
        f.write('\n'.join([cat for cat in products.keys()]))
        f.close()
    

    