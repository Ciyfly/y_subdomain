# Y-SubDomain

子域名获取工具

## 分析如下:
分析结合几个现有的工具发现都是如下几点实现:
1. 多种第三方接口 获取子域名
2. 字典加异步dns暴力穷举
3. 利用ca证书获取

### 泛解析的解决办法
都是采用 先测试一个不存在的域名然后是否成功解析


### 为什么要做
1. 重复造轮子 深入理解轮子 做出更好用的轮子
2. 是大扫描器的信息收集的一部分功能的实现


## 具体功能设计
1. 命令行形式执行 基于python3
2. 这次增加进度条功能(之前我写的东西进度条都不好看)
3. 结合多个现有的工具 结合多个接口 高扩展性
4. 增加网页爬取获取子域名信息
5. ...


## 实现  
这里参考 poc的形式 动态的从script文件夹下的脚本中执行 也就是说把每个采集子域名的作成一个Scan类 然后只要增加新的就可以了  
多个web接口的形式获取子域名 然后对这些子域名加上字典进行爆破

**接口引擎脚本完成：**
1. 百度云检测  
2. hackertarget
3. threatcrowd (默认关闭)
4. virustotal
5. 微步(没有私有api)
6. 爬虫形式解析获取子域名(默认关闭)
7. 通过证书获取  
8. dns暴力穷举(目前采用线程池实现)


## 使用  
不使用暴力穷举  
![20190625174441.png](https://i.loli.net/2019/06/25/5d11ed1cdbd7b80753.png)


默认生成的txt在 output目录下  
生成的html

![20190625174349.png](https://i.loli.net/2019/06/25/5d11ece9489dc60057.png)

##版本
**V0.1**  
采用线程池的形式进行dns解析  
采用多接口的形式获取域名 (爬虫有个问题 开启爬虫后再进行dns解析会很慢很慢 于是默认关闭了爬虫)  
每个接口都可以在代码中增加 `self.enable=False` 来进行默认开关  
暴力穷举效果确实不错  

**V0.2**
TODO  
增加更多的接口  
使用异步dns来解析 dns  
让使用和输出更简洁流畅  
参考更多的子域名工具  
待定....
## 参考
[aiodnsbrute](https://github.com/blark/aiodnsbrute/tree/master/aiodnsbrute)  
后面再参考这个的日志做新的版本  

[ESD](https://github.com/FeeiCN/ESD)  

[wydomain](https://github.com/ring04h/wydomain)  

git log --oneline --color | emojify | less -r
