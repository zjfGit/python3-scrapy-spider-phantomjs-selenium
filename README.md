# 爬虫Windows环境搭建
## 安装需要的程序包
- Python3.4.3 > https://pan.baidu.com/s/1pK8KDcv
- pip9.0.1  > https://pan.baidu.com/s/1mhNdRN6
- 编辑器pycharm > https://pan.baidu.com/s/1i4Nkdk5
- pywin32 > http://pan.baidu.com/s/1pKZiZWZ
- pyOpenSSL > http://pan.baidu.com/s/1hsgOQJq
- windows_sdk > http://pan.baidu.com/s/1hrM6iRa
- phantomjs > http://pan.baidu.com/s/1nvHm5AD

## 安装过程

### 安装基础环境
1. 安装Python安装包，一路Next
2. 将Python的安装目录添加到环境变量Path中
3. win + r 输入Cmd打开命令行窗口，输入Python 测试是否安装成功

### 安装pip
> pip的作用相当于linux的yum，安装之后可以采用命令行的方式在线安装一些依赖包
1. 解压pip压缩包到某一目录（推荐与Python基础环境目录同级）
2. cmd窗口进入pip解压目录
3. 输入 python setup.py install 进行安装，安装过程中将会在Python目录的scripts目录下进行
4. 将pip的安装目录 C:\Python34\Scripts; 配置到环境变量path中
5. cmd命令行输入pip list 或者 pip --version 进行检验

### 安装Scrapy
> Scrapy是一个比较成熟的爬虫框架，使用它可以进行网页内容的抓取，但是对于windows并不友好，我们需要一些类库去支持它
1. 安装pywin32: 一路next即可
2. 安装wheel：安装scrapy时需要一些whl文件的安装，whl文件的安装需要预先配置wheel文件。在cmd下使用pip安装 ： pip install wheel
3. 安装PyOpenSSL：下载完成PyOpenSSL后，进入下载所在目录，执行安装：pip install pyOpenSSl (**注意，执行安装的wheel文件名一定要tab键自动弹出，不要手动敲入**)
4. 安装lxml: 直接使用pip在线安装 pip install lxml
> ***在Windows的安装过程中，一定会出现 “error: Microsoft Visual C++ 10.0 is required (Unable to find vcvarsall.bat).”的问题，也就是无法找到相对应的编译包。一般的做法是下载VisualStudio来获得Complier，但是我们不这样做。***

> 下载windows-sdk后，执行安装操作，如果安装成功，那么这个问题就解决了。如果失败，那么需要先把安装失败过程中的2个编译包卸载。他们分别为：Microsoft Visual C++ 2010  x86 Redistributable、Microsoft Visual C++ 2010  x64 Redistributable（可以使用360或者腾讯管家来卸载）

> 卸载完成之后，在安装确认过程中，不要勾选Visual C++ compiler，这样他第一次就能安装成功。安装成功之后，再次点击sdk进行安装，这时候又需要把Visual C++ compiler勾选上，再次执行安装。完成以上操作后，就不会出现Microsoft Visual C++ 10.0 is required的问题了。

> 如果在安装过程中出现“failed building wheel for xxx”的问题，那么需要手动下载wheel包进行安装，所有的安装文件都可以在[http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)里找到，找到需要的包并下载完成后执行pip install xxxx即可。

5. 安装Scrapy：pip install Scrapy, 安装完成后可以再命令行窗口输入Scrapy进行验证。





# 豆果爬虫架构设计
为了更好的扩展性和爬虫工作的易于监控，爬虫项目分成3个子项目，分别是url提取、内容爬取、内容更新（包括更新线上内容和定时审核）

	主要是采用 Python 编写的scrapy框架，scrapy是目前非常热门的一种爬虫框架，它把整个爬虫过程分为了多个独立的模块，并提供了多个基类可以供我们去自由扩展，让爬虫编写变得简单而有逻辑性。并且scrapy自带的多线程、异常处理、以及强大的自定义Settings也让整个数据抓取过程变得高效而稳定。
	scrapy-redis：一个三方的基于redis的分布式爬虫框架，配合scrapy使用，让爬虫具有了分布式爬取的功能。github地址： https://github.com/darkrho/scrapy-redis 
	mongodb 、mysql 或其他数据库：针对不同类型数据可以根据具体需求来选择不同的数据库存储。结构化数据可以使用mysql节省空间，非结构化、文本等数据可以采用mongodb等非关系型数据提高访问速度。具体选择可以自行百度谷歌，有很多关于sql和nosql的对比文章。

	其实对于已有的scrapy程序，对其扩展成分布式程序还是比较容易的。总的来说就是以下几步：

* 找一台高性能服务器，用于redis队列的维护以及数据的存储。
* 扩展scrapy程序，让其通过服务器的redis来获取start_urls，并改写pipeline里数据	存储部分，把存储地址改为服务器地址。
* 在服务器上写一些生成url的脚本，并定期执行。

# 1 url提取
## 1.1 分布式抓取的原理
	采用scrapy-redis实现分布式，其实从原理上来说很简单，这里为描述方便，我们把自己的核心服务器称为master，而把用于跑爬虫程序的机器称为slave。

	我们知道，采用scrapy框架抓取网页，我们需要首先给定它一些start_urls，爬虫首先访问start_urls里面的url，再根据我们的具体逻辑，对里面的元素、或者是其他的二级、三级页面进行抓取。而要实现分布式，我们只需要在这个starts_urls里面做文章就行了。

	我们在master上搭建一个redis数据库（注意这个数据库只用作url的存储，不关心爬取的具体数据，不要和后面的mongodb或者mysql混淆），并对每一个需要爬取的网站类型，都开辟一个单独的列表字段。通过设置slave上scrapy-redis获取url的地址为master地址。这样的结果就是，尽管有多个slave，然而大家获取url的地方只有一个，那就是服务器master上的redis数据库。

	并且，由于scrapy-redis自身的队列机制，slave获取的链接不会相互冲突。这样各个slave在完成抓取任务之后，再把获取的结果汇总到服务器上（这时的数据存储不再在是redis，而是mongodb或者 mysql等存放具体内容的数据库了）

	这种方法的还有好处就是程序移植性强，只要处理好路径问题，把slave上的程序移植到另一台机器上运行，基本上就是复制粘贴的事情。
	
## 1.2 url的提取
	首先明确一点，url是在master而不是slave上生成的。
	
	对于每一个门类的urls（每一个门类对应redis下的一个字段，表示一个url的列表），我们可以单独写一个生成url的脚本。这个脚本要做的事很简单，就是按照我们需要的格式，构造除url并添加到redis里面。

	对于slave，我们知道，scrapy可以通过Settings来让爬取结束之后不自动关闭，而是不断的去询问队列里有没有新的url，如果有新的url，那么继续获取url并进行爬取。利用这一特性，我们就可以采用控制url的生成的方法，来控制slave爬虫程序的爬取。
	
## 1.3 url的处理
	1、判断URL指向网站的域名，如果指向外部网站，直接丢弃
	2、URL去重，然后URL地址存入redis和数据库；

# 2 内容爬取
## 2.1 定时爬取
	有了上面的介绍，定时抓取的实现就变得简单了，我们只需要定时的去执行url生成的脚本即可。这里推荐linux下的crontab指令，能够非常方便的制定定时任务，具体的介绍大家可以自行查看文档。

## 2.2 
# 3 内容更新
## 3.1 表设计
    帖子爬取表：
    id          :自增主键
    md5_url     :md5加密URL
    url         :爬取目标URL
    title       :爬取文章标题
    content     :爬取文章内容（已处理）
    user_id     :随机发帖的用户ID
    spider_name :爬虫名
    site        :爬取域名
    gid         :灌入帖子的ID
    module      :
    status      :状态 （1：已爬取；0：未爬取）
    use_time    :爬取时间
    create_time :创建时间
    CREATE TABLE `NewTable` (
        `id`  bigint(20) NOT NULL AUTO_INCREMENT ,
        `md5_url`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `url`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `title`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `content`  mediumtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `user_id`  varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `spider_name`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `site`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `gid`  varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `module`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
        `status`  tinyint(4) NOT NULL DEFAULT 0 ,
        `use_time`  datetime NOT NULL ,
        `create_time`  datetime NOT NULL ,
    PRIMARY KEY (`id`)
    )
    ENGINE=InnoDB
    DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci
    AUTO_INCREMENT=4120
    ROW_FORMAT=COMPACT;



# 4 系统优化
## 4.1 防抓取方法
* 设置download_delay，这个方法基本上属于万能的，理论上只要你的delay足够长，网站服务器都没办法判断你是正常浏览还是爬虫。但它带来的副作用也是显然的：大量降低爬取效率。因此这个我们可能需要进行多次测试来得到一个合适的值。有时候download_delay可以设为一个范围随机值。
* 随机生成User-agent：更改User-agent能够防止一些403或者400的错误，基本上属于每个爬虫都会写的。这里我们可以重写scrapy 里的middleware，让程序每次请求都随机获取一个User-agent，增大隐蔽性。具体实现可以参考 http://www.sharejs.com/codes/python/8310
* 设置代理IP池：网上有很多免费或收费的代理池，可以借由他们作为中介来爬。一个问题是速度不能保证，第二个问题是，这些代理很多可能本来就没办法用。因此如果要用这个方法，比较靠谱的做法是先用程序筛选一些好用的代理，再在这些代理里面去随机、或者顺序访问。
* 设置好header里面的domian和host，有些网站，比如雪球网会根据这两项来判断请求来源，因此也是要注意的地方。

## 4.2 程序化管理、web管理
上述方法虽然能够实现一套完整的流程，但在具体操作过程中还是比较麻烦，可能的话还可以架构web服务器，通过web端来实现url的添加、爬虫状态的监控等，能够减轻非常大的工作量。这些内容如果要展开实在太多，这里就只提一下。



# 5 scrapy部署
## 5.1 安装python3.6

```
```
	1、下载源代码
		wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
			  
	2、解压文件
		cp Python-3.6.1.tgz /usr/local/goldmine/
		tar -xvf Python-3.6.1.tgz
		
	3、编译
		./configure --prefix=/usr/local
		
	4、安装
		make && make altinstall
		
		注意：这里使用的是make altinstall ，如果使用make install，会在系统中有两个版本的Python在/usr/bin/目录中，可能会导致问题。
	4.1 报错---zipimport.ZipImportError: can't decompress data; zlib not available
		# http://www.zlib.net/zlib-1.2.11.tar
		=============================================
		使用root用户：
		
		wget http://www.zlib.net/zlib-1.2.11.tar
		tar -xvf zlib-1.2.11.tar.gz
		cd zlib-1.2.11
		./configure
		make
		sudo make install
		=============================================
		安装完zlib，重新执行 Python-3.6.1中的 make && make altinstall 即可安装成功；	
		
	
	
	
	


# 5.2 服务安装虚拟环境【root安装】
	安装virtualenv可以搭建虚拟且独立的python环境，使每个项目环境和其他的项目独立开来，保持环境的干净，解决包冲突。

### 5.2.1 安装virtualenv	
	/usr/local/bin/pip3.6 install virtualenv
	
	结果报错了，
	===============
	pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
	Collecting virtualenv
	Could not fetch URL https://pypi.python.org/simple/virtualenv/: There was a problem confirming the ssl certificate: Can't connect to HTTPS URL because the SSL module is not available. - skipping
	===============
	rpm -aq  | grep openssl ,发现缺少 openssl-devel ；
	【route add default gw 192.168.1.219】
	yum install openssl-devel -y
	然后，重新编译python，见 5.1 ；
### 5.2.2 创建新的虚拟环境
	virtualenv -p /usr/local/bin/python3.6 python3.6-env
	
### 5.2.3 激活虚拟环境
	source python3.6-env/bin/active
	
	5.2.3.1 虚拟环境中安装 python
	
### 	5.2.4 退出虚拟环境
	deactive 

# 5.2 安装scrapy

# 5.3 安装配置redis
	yum install redis
# 5.4 

# 6 redis安装&配置
## 6.1 安装
	mac ： sudo brew install redis 
	/usr/local/bin/redis-server /usr/local/etc/redis.conf 

# 参考
* 1.[基于Python，scrapy，redis的分布式爬虫实现框架](http://ju.outofmemory.cn/entry/206756)
* 2.[小白进阶之Scrapy第三篇（基于Scrapy-Redis的分布式以及cookies池）](http://ju.outofmemory.cn/entry/299500)
* 3.[CentOS中使用virtualenv搭建python3环境](http://www.jb51.net/article/67393.htm)
* 4.[CentOS使用virtualenv搭建独立的Python环境](http://www.51ou.com/browse/linuxwt/60216.html)
* 5.[python虚拟环境安装和配置](http://blog.csdn.net/pipisorry/article/details/39998317)