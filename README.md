# 将微博热搜爬到本地
- beautifulsoup解析html
- 可以写入execl。
- 也可以写入mysql数据库。

------------------

- 添加邮件功能

# 每日Secwiki
- 很久之前写的一个小爬虫，方便查看每日secwiki的文章
- 基于之前的微博爬虫
- 需要添加定时任务

    ```shell
    0 7 * * * /root/anaconda3/bin/python /root/Documents/SecWiki_spider.py
    1 8 * * * /root/anaconda3/bin/python /root/Documents/test_mail.py
    ```

