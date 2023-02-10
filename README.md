# 需求背景
在walmart平台进行关键词搜索，或访问关键词搜索的链接，爬取所有搜索结果的产品详情页数据。
# 项目初始化及运行
1、启动redis服务。

2、运行`walmart_cookie_generate.py`，创建cookie池。cookie池数量视总爬取量而定。由于walmart反爬比较严格，建议每解析一个链接，消费一个cookie。

3、修改`walmart_keyword_crawl.py`中的`run(url_front, ky)`，直接运行即可。
# 爬取信息
1、搜索结果数：获取方式见图1.8

2、是否做广告：获取方式见图1.8

3、品牌：获取方式见图1.9

4、类目路径：获取方式见图1.9

5、标题：获取方式见图1.9

6、价格：（如果是变体，价格都抓下来）获取方式见图1.9

7、是否带有Pro Seller标签：获取方式见图1.9

8、变体：（颜色/尺寸变体都抓下来）获取方式见图1.10

9、卖家形式：（分为Walmart和第三方卖家，即Sold by Walmart或者Sold by Seller）获取方式见图1.11-图1.13
    
10、发货方式：
    若卖家形式为Sold by Walmart填WFS；
    卖家形式为Sold by Seller时，需判断是否为Fulfilled By Walmart，若是，则填WFS，
    若否，则填FBM即可；获取方式见图1.11-图1.13

11、描述：获取方式见图1.14

12、评论数：获取方式见图1.15

13、星级：获取方式见图1.15

14、一星/二星/三星review（内容抓下来，如果有变体，变体也要抓下来）获取方式见图1.15

15、上架时间（就是抓取评论最早的日期），点击查看所有评论，选择“All Review”后选择“Oldest to Newest”，见图1.16
    
16、产品信息都抓下来：获取方式见图2.0

17、排名：排名就是在三级类目页，例如,排名P13 第一页第三个位置

![img_1.png](img/img_1.png) 图1.8
![img_2.png](img/img_2.png) 图1.9
![img_3.png](img/img_3.png) 图1.10
![img_4.png](img/img_4.png) 图1.11
![img_5.png](img/img_5.png) 图1.12
![img_6.png](img/img_6.png) 图1.13
![img_7.png](img/img_7.png) 图1.14
![img_8.png](img/img_8.png) 图1.15
![img_9.png](img/img_9.png) 图1.16
![img_10.png](img/img_10.png) 图2.0

