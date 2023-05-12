# qqrobot
## 基于go-cqhttp的qq机器人

## 环境安装

安装 python3.8以上版本

安装依赖

~~~python
pip install -r requirements.txt
~~~



## 部署方法


首先打开data.yaml填写主人QQ号,以及cluai的apikey还有邮箱的一些东西，邮箱不需要可以不用配置,打开qq_login 双击config.yaml 然后按照提示写QQ号和密码，然后双击go-cqhttp.bat 运行用机器人然后滑块验证登录。然后关闭这个窗口

点start.bat
如果出现爆红可以按照翻译，差什么模块就输入
~~~cmd
pip install 模块名
~~~

### 安装ffmpeg

可以去[ffmpeg](https://ffmpeg.org/download.html)下载最新版安装，如果觉得下载速度慢可以用这个[ffmpeg](https://pan.baidu.com/s/1fjNt_ETij787CtEQvXi9PA?pwd=02uw )
sellenium不需要可以不用配置

#### 安装方法

把压缩包减压放到C:\Program Files下，然后推荐加环境变量

点开属性

![1](https://github.com/luoguixin/qqrobot/blob/main/img/1.png)

找到高级系统设置

![2](https://github.com/luoguixin/qqrobot/blob/main/img/2.png)

点开环境变量

![3](https://github.com/luoguixin/qqrobot/blob/main/img/3.png)

点开path

![4](https://github.com/luoguixin/qqrobot/blob/main/img/4.png)

新建添加刚刚ffmpeg的存放地址C:\Program Files\ffmpeg\bin

![5](https://github.com/luoguixin/qqrobot/blob/main/img/5.png)

复制粘贴进去

然后全部确定

最后win + R 输入cmd  在终端里面输入ffmpeg -version

出现

就算安装完成了

接下来用管理员身份打开cmd

输入

~~~python
setx /M PATH "C:\Program Files\ffmpeg\bin;%PATH%"
~~~

回车出现成功就行

至此安装完成

### 本机器人目前功能有


1.聊天机器人，回答编程问题，和唠嗑

### 联系方式

可以加qq群784469488
也可以加本人qq3052405886(有很多隐藏指令,只是因为我不想写那么多菜单，请见谅)


如果配置不成功或者qq登录不上，可以在login_qq目录下打开cmd输入
~~~cmd
.\go–cqhttp.exe update
~~~
然后输入y回车就能更新了,之后吧原来的那个删掉就行了
