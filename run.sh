#!/bin/sh
# ./crawl.sh data/brands.json proxy.txt
# 具体参数设置见jd_config.py
#1. 京东数据抓取
python jd_wap.py


#2. 数据预处理
python jd_process.py

# 3.分类
python jd_classify.py


