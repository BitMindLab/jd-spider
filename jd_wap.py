#!coding:utf-8
# 京东移动版
'''
Created on Dec 7, 2014

@author: xx
'''
import os
import sys
import jd_parse# import parse_root, test
import jd_config


print 'old encoding value:', sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8' )
print 'new encoding value:', sys.getdefaultencoding()

if (__name__ == '__main__'):

    if (not os.path.exists(jd_config.dataPath) ):
        os.mkdir(jd_config.dataPath)

    if(jd_config.is_test):
        jd_parse.test()   # 0. test
    else:
        jd_parse.parse_root(jd_config.root_url, jd_config.start_cat) # 1. crawl products
    



    

    

