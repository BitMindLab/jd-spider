京东商品分类



1.  数据爬取
1.1 网页分析
	电脑版 www.jd.com
	移动版 wap.jd.com
	触屏版 m.jd.com
	移动版比较简单，所以选择移动版抓取

1.2 抓取字段及存储
	.info      :   product的基本信息，存储字段 [id, url, title, category, price, meta, detail]
	.info.json :   .info对应的json格式文件
	.comment   :   product的评论，存储格式  u_info:u_score:u_sum



2.  数据处理流程： 
	输入：.json 文件     
	输出：info.BOW目录
2.1 load原始数据： .info.json 目录下所有文件 
	(未考虑评论信息, 只考虑了三个字段	rawStr = title + meta + detail）

2.2 数据处理　preprocess
	对rawStr处理流程：去噪，分词，去停用词，做词典，词频统计分析，做bow
	存储为libSV格式，


3.  分类
	输入： prodct.BOW文件　　
	输出：
	logistic regression:
	accuracy:0.95652173913
	SVM for classification:
	accuracy:0.95652173913
	
4.  代码简介
	代码入口：
	jd_wap：    爬虫入口
	jd_process：数据预处理入口
	classify:   分类器入口

	代码模块：
	jd_parse模块主要负责京东相关页面解析
	jd_item 模块定义了商品、类别、评论的基本属性及方法
	documnts模块定义了文档、字典的基本属性及方法
	FileUtil模块负责基本的NLP任务，如去停用词、分词等任务

