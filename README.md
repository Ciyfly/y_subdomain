# Y-SubDomain

子域名获取工具

### 泛解析的解决办法
先测试一个不存在的域名然后是否成功解析


### 为什么要做
1. 重复造轮子 深入理解轮子 做出更好用的轮子
2. 是大扫描器的信息收集的一部分功能的实现


## 实现  
### 接口的实现
这里参考 poc的形式 动态的从script文件夹下的脚本
动态载入实例化并执  
继承Base类默认有个 `self.enable=True` 可以控制是否开启脚本  
如果使用 -e 指定接口 enable是False也会强制执行  
对于接口返回的域名会使用线程池再去dns解析验证 (默认线程池大小 50)

**接口引擎脚本完成：**
1. 百度云检测  
2. hackertarget
3. virustotal (需要在config/config.py 中添加api key才能使用不然默认不会执行)
4. 通过证书获取

### 暴力穷举的实现  
一口气加载字典到内存中 占内存不大  
使用共享队列+多线程的形式进行解析dns 默认线程开启100个  
这个地方有进度条功能 可以在实例化穷举类的时候进行选择是否开启  

## 使用  
不使用暴力穷举  

![20190628114320.png](https://i.loli.net/2019/06/28/5d158cf51a27539916.png)  


使用暴力穷举  

![20190628114417.png](https://i.loli.net/2019/06/28/5d158d2b4118d84421.png)  


关闭进度条输出 使用HUP信号获取字典队列大小  
![20190628114457.png](https://i.loli.net/2019/06/28/5d158d53f159d86830.png)  


默认生成的txt在 output目录下  
可以选择是否生成json  
选择生成的html如下  

![20190625174349.png](https://i.loli.net/2019/06/25/5d11ece9489dc60057.png)  

## 版本
**V0.1**  
采用多接口的形式获取域名 动态插件形式添加接口脚本  
接口验证和穷举都采用线程池的形式进行dns解析  

**V0.2**  
修改 穷举采用共享队列+多线程的形式  
去除多余代码  
修改了代码结构 便于作为api使用  
穷举增加了进度条  
扩大了字典 目前字典 2350706 (235w) (跑一次大概 40分钟左右)  
增加了HUP小调试 发起HUP信号会输出 此时队列大小 (在 api形式使用不输出进度条的时候 如果长时间未结束可调试使用)  
`kill -HUP 进程id`  

# api形式使用  
使用接口解析
```python
from lib.core import EngineScan

engine_scan = EngineScan(scan_domain, engine)
# scan_domain 为扫描的域名 engine 是指定的接口 空的话就全部都跑 默认也是全部都跑  
engine_domain_ips_dict = engine_scan.run()
# 调用 run方法会返回 解析的结果 是 字典形式 子域名对应ip列表  
```
使用穷举解析
```python
from lib.core import ExhaustionScan

exhaustion_scan =  ExhaustionScan(scan_domain, thread_count=100, is_output=True)
# is_output 是否输出进度条 默认是False的
exh_domain_ips_dict = exhaustion_scan.run()
```  

## update

2019 0709
经测试 修改对于泛解析的解决  
如果随机字符串跑出来泛解析还继续进行穷举但是过滤掉这个泛解析的ip  
对于接口里的也进行泛解析剔除  
对于暴力穷举的会默认使用配置文件中的 50 阈值 作为判断泛解析的条件 当超过50个域名指向一个ip进行剔除  



## 参考

[ESD](https://github.com/FeeiCN/ESD)  

[wydomain](https://github.com/ring04h/wydomain)  
