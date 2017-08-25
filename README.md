# 代理爬虫 beta      
每几分钟从免费的代理发布站爬取免费的代理IP，然后在本地每几分钟循环验证它们，同时开启一个简易的web，可以方便调用这些代理。   

#### 模块说明   
###### config.py - 配置文件   
###### fetcher.py - 爬虫主文件   
###### initDB.py - 安装数据库   
###### monitor.py - 代理可用性监控脚本   
###### proxyServer.py - 运行主文件   
###### server.py - WEB服务   
###### database.py - 数据库操作类   
   


#### web   
http://localhost:8888/?limit=获取数量&type=1|0(1表示高匿代理)&protocol=HTTP

#### 依赖   
自己看着缺啥就装啥吧   