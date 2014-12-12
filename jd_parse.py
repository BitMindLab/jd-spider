#!coding:utf-8
'''
Created on Dec 7, 2014

@author: xx
'''

import urllib2
from bs4 import BeautifulSoup
import re
import os
import string
import jd_config
from jd_item import category, product, comment


def parse_root(root_url, start_cat = None):
    """
    1. 所有类别主页（所有大类）
    start_cat: 设置起始点，常用于中断后断点继续
    return：categorys
    """    
    categorys = []
    print 'loading root categorys'
    page = urllib2.urlopen(root_url).read()#.decode('utf-8')
    soup = BeautifulSoup(page)
    links = soup.select('div[class="content1"] > div[class="mc"] > span > a')
    
    
    # 遍历每个大类
    for link in links:
        cat = category()
        cat.url = 'http://wap.jd.com' + link.get('href')
        cat.name = link.string
        if ((not start_cat is None) and (not start_cat == cat.name)):
            continue
        start_cat = None
        
        global f_info, f_info_json, f_comments
        if (not os.path.exists(jd_config.infoPath) ):
            os.mkdir(jd_config.infoPath)
        f_info = open(os.path.join(jd_config.infoPath, cat.name + '.product.info'), 'w')
        if (not os.path.exists(jd_config.jsonPath) ):
            os.mkdir(jd_config.jsonPath)
        f_info_json = open(os.path.join(jd_config.jsonPath, cat.name + '.product.info.json'), 'w')
        if (not os.path.exists(jd_config.commentPath) ):
            os.mkdir(jd_config.commentPath)
        f_comments = open(os.path.join(jd_config.commentPath, cat.name + '.product.comment'), 'w')
        cat.products = parse_category(cat.url)
        f_info.close()
        f_info_json.close
        f_comments.close()
        
        categorys.append(cat)
    return categorys


def parse_category(cat_url, num = jd_config.num_subcategory):
    """
    2. 单个类别主页（一个大类下的所有小类）
    return： 类别下所有products
    """   
    products = []
    if (not cat_url.startswith('http://wap.jd.com/category/')):
        print 'warning: category_url is wrong\n'
        return products
     
    page = urllib2.urlopen(cat_url).read()#.decode('utf-8')
    soup = BeautifulSoup(page)
    links = soup.select('div[class="m2"] > div > a') # 得到子类别url
        
    # 遍历每个小类
    i = 0
    for link in links:
        if (i < num):
            i = i + 1
        else:
            break
        sub_url = 'http://wap.jd.com' + link.get('href')
        products.extend(parse_products(sub_url))
    return products


# 
def parse_products(url, num = jd_config.num_product):
    """
    3. 商品列表页
    return： 单个页面所有products
    """   
    products = []
    if (not url.startswith('http://wap.jd.com/products/')):
        print 'warning: products_url is wrong\n' + url + '\n'
        return products
    
    page = urllib2.urlopen(url).read()#.decode('utf-8')
    soup = BeautifulSoup(page)
    
    # 下一页
#    next_page = soup.find("div", class_ = "page").find("a").get('href')
#    if next_page:
#        url = "http://wap.jd.com" + next_page
#        req.append(parse_products(next_page))
    
    
    # 商品url
    links = soup.select('div[class="pmc"] > div[class="title"] > a')
    
    # 遍历每一个商品
    i = 0
    for link in links:
        if (i < num):
            i = i + 1
        else:
            break
        product_url = 'http://wap.jd.com' + link.get('href')
        prod = parse_product(product_url)
        if (len(prod.id) > 0):  # 成功解析
            prod.save_info(f_info)
            prod.save_info_json(f_info_json)
            prod.save_comments(f_comments)
            products.append(prod)

    return products
    


def parse_product(url, num = 100):
    """
    4. 商品页
    return： 单个页面所有products
    """
    prod = product()
    if (not url.startswith('http://wap.jd.com/product/')):
        print 'warning: product_url is wrong\n' + url + '\n'
        return prod    
    
    page = urllib2.urlopen(url).read()#.decode('utf-8')
    soup = BeautifulSoup(page)
    
    prod.url = url
    prod.id = re.match(r'(.*)product/(\d*).html(.*)', url).group(2)
    prod.title = soup.title.string[:-8]
    print 'loading product ' + prod.id
    print 'url: ' + prod.url + '\ntitle: ' + prod.title
    
    if(len(soup.select('div[class="pro"] > a')) > 1):
        prod.category = soup.select('div[class="pro"] > a')[1].string
    else:
        print 'warning: wrong format in product page' + url
        return product()
    if(len(soup.select('div[class="p-price"] > font[color="red"]'))):
        prod.price = soup.select('div[class="p-price"] > font[color="red"]')[0].get_text()
    else:
        print 'warning: wrong format in product page' + url
        return product()
    prod.comments = parse_comments(re.sub('product','comments',url))
    prod.detail = parse_detail(re.sub('product','detail',url))
    
    # prod.meta
    keyword = soup.head.select('meta[name="Keywords"]')
    description = soup.head.select('meta[name="description"]')
    if (len(keyword)):
        prod.meta = (keyword[0]['content'])
    if (len(description)):
        prod.meta = prod.meta + ' ' + description[0]['content']
    prod.meta = re.sub(re.compile('\s+'), '', prod.meta) 
    
    print '\n'
    return prod



def parse_detail(url):
    """
    5. 商品详情页
    return： 一个product的详细介绍
    """   
    print 'parsing detail'
    detail = ''
    if (not url.startswith('http://wap.jd.com/detail/')):
        print 'warning: detail_url is wrong\n' + url + '\n'
        return detail
    #url = 'http://wap.jd.com/detail/352934.html'
    page = urllib2.urlopen(url).read()#.decode('utf-8')
    soup = BeautifulSoup(page)
    soup.find("div", class_ = "content")#.get_text()
    contents = soup.select('div[class="content"] > div[class="m3"]')
    for content in contents[:-1]:
        if (content.find('a')):
            content.a.extract()
        mt = content.find("div", class_="mt").string
        mc = content.find("div", class_="mc").get_text().strip()
        if (string.find(mc,'暂无') == -1 and string.find(mt,'售后') == -1 and len(mc) > 0): # 未找到
            detail = detail + mt + ':' + mc + ';'  
            
    detail = re.sub(re.compile('\s+'), '', detail) 
    if (len(detail) == 0):
        detail = '暂无'
    
    return detail



def parse_comments(url):
    """
    6. 商品评价页
    return： 一个product的所有comments
    """   
    print 'parsing comments'
    comments = []
    page = urllib2.urlopen(url).read()#.decode('utf-8')
    soup = BeautifulSoup(page)
    
    sub_urls = soup.select('div[class="content"] > div[style="padding-left:36px;"] > a')
    
    for sub_url in sub_urls:
        sub_url = 'http://wap.jd.com' + sub_url.get('href')
        page = urllib2.urlopen(sub_url).read()#.decode('utf-8')
        soup = BeautifulSoup(page)
        contents = soup.select('div[class="eval"]')
        for content in contents:
            c = comment()
            # dict和list都不爽
            if (not len(content.select('div[class="u-info"]'))):
                continue
            c.u_info = content.select('div[class="u-info"]')[0].string[:-2]
            if (not len(content.select('div[class="u-score"] > span'))):
                continue
            c.u_score = content.select('div[class="u-score"] > span')[0].string[:-1]
            if (not len(content.select('div[class="u-summ"]'))): #空评论 或者bug
                continue
            c.u_sum = content.select('div[class="u-summ"]')[0].string[3:].strip()
            comments.append(c)

    return comments

def test():
    """
    测试模块
    """   
    #product = parse_product('http://wap.jd.com/product/19309872.html')
    #product = parse_product('http://wap.jd.com/product/1252847578.html')
    #parse_product('http://wap.jd.com/product/19309872.html')
    
    # 1. 测试主页面
    #parse_root('http://wap.jd.com/category/all.html' , '图书')
    # 2. 测试商品页面
    print parse_product('http://wap.jd.com/product/232875.html').to_list()
    # 3. 测试评论页面    
    parse_comments('http://wap.jd.com/comments/1052783125.html') 
    
    
def check(list_a, num, message):
    pass