# 京东商品分类 #
推荐通过git下载，请使用以下命令

    git clone https://song_xu@bitbucket.org/song_xu/jd-spider.git

或者请点 [这里](https://bitbucket.org/song_xu/jd/downloads) 下载压缩包(不推荐)

-------
# 一、流程简介 #

## 1. 数据爬取 ##
#### 预分析 ####

* 电脑版 www.jd.com
* 移动版 [wap.jd.com](http://wap.jd.com/)
* 触屏版 [m.jd.com](http://m.jd.com)

移动版比较简单，所以选择移动版抓取
#### 抓取字段及存储 ####

* [info](http://wap.jd.com/product/1227234.html) :  即product的基本信息，存储字段 [id, url, title, category, price, meta, [detail](http://wap.jd.com/detail/1227234.html)]
* [comment](http://wap.jd.com/comments/1227234.html)   :   product的评论，存储格式  u_info:u_score:u_sum



##2. 数据处理流程 ##

#### 输入 ####
* json文件，见info.json 目录
* 未考虑评论信息, 只考虑了三个字段	rawStr = title + meta + detail

#### 数据预处理 ####
* 对rawStr处理流程：去噪，分词，去停用词，做词典，词频统计分析，做BOW
* 输出BOW特征，存储为libSVM格式

## 3. 分类 ##
* 输入： BOW特征 + 类别信息， 见info.BOW目录
* 输出： 

分类准确率：

        logistic regression:
        accuracy:0.95652173913
        SVM for classification:
        accuracy:0.95652173913

-------

# 二、代码简介 #

代码入口：

* jd_wap：    爬虫入口
* jd_process：数据预处理入口
* classify:   分类器入口


代码模块：

* jd_parse模块： 主要负责京东相关页面解析
* jd_item 模块： 定义了商品、类别、评论的基本属性及方法
* documnts模块： 定义了文档、字典的基本属性及方法
* FileUtil模块： 负责基本的NLP任务，如去停用词、分词等任务

-------


# 三、数据简介 ###
data目录：

* comments目录： 商品评论
* info目录：     商品基本信息（易读格式，供浏览）
* info.json目录:     info目录文件的json格式（用于数据处理）
* info.word目录：      商品基本信息提取的特征（即每个单词，供浏览）
* info.BOW目录：       info.word对应的BOW转码（libSVM格式，用于分类）
* stopwords目录： 停用词表（用于数据处理）

文件：

* category：      类别表（即label，共八类，行号对应id 0-7）
* product.BOW：     所有类别的BOW汇总（即info.BOW目录中的汇总）
* word.count：      所有文档的词频（用于视觉分析，或浏览）

-------

# 四、Tips #

* 如果快速测试，请跳过1（利用已经爬取的数据，节省数据爬取的时间消耗）
* 运行依赖 scikit-learn 和 beautifullsoup， 如需安装请参考官网


-------

仓促完成，多有不足，期待您的反馈，song.xu@nlpr.ia.ac.cn

更新中 ...