# qqrobot
## 基于go-cqhttp的qq机器人

## 环境安装

安装 python3.8以上版本

安装依赖

~~~python
pip install flask
pip install requests
pip install openai
pip install pyyaml
~~~



## 部署方法


首先打开info.ini填写主人QQ号,以及openai的apikey,打开qq_login 双击config.yml 然后按照提示写QQ号，然后双击go-cqhttp.bat 运行用机器人qq扫码登录。

然后到项目根目录打开cmd 输入

~~~cmd
python main.py
~~~

### 安装ffmpeg

可以去[ffmpeg](https://ffmpeg.org/download.html)下载最新版安装，如果觉得下载速度慢可以用这个[ffmpeg](https://pan.baidu.com/s/1fjNt_ETij787CtEQvXi9PA?pwd=02uw )


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
进入info.ini按照提示填写

### 本机器人目前功能有


1.人工智障梦幻（触发词梦幻）
2.转语音（触发词/）
3.彩虹屁（触发词夸夸xxx）
4.一言（触发词一言）
5.点歌（触发词点歌）
6.随机姓名（触发词给我起个名）
7.天气查询（触发词xxx天气）
8.视频搜索（触发词搜索视频xxx）
9.历史上的今天（触发词历史上的今天）
10.域名状态查询（查询域名状态xxx.com）
11.ping（触发词pingxxx.xxx.xxx）
12.度娘（度娘什么是xxx）
13.翻译（翻译一下）
14.b站热门视频（触发词b站热门视频)
15.摸鱼日历
16.网易云热评

### 联系方式

可以加qq群784469588(有很多隐藏指令,只是因为我不想写那么多菜单，请见谅)
