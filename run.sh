#!/bin/sh
# 具体参数设置见jd_config.py
# 如果快速测试，请跳过1（利用已经爬取的数据，节省数据爬取的时间消耗）

#1. 京东数据抓取
python jd_wap.py

#2. 数据预处理
python jd_process.py

# 3.分类
python jd_classify.py








