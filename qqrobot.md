# qqrobot
## 基于go-cqhttp的qq机器人

## 环境安装

安装 python3.8以上版本

安装依赖

~~~python
pip install flask
pip install requests
~~~



## 部署方法

首先打开qq_login 双击go-cqhttp.exe 然后打开go-cqhttp.bat文件。选择0 的http 协议，然后在生成的config.yum里面填写机器人QQ号 然后双击go-cqhttp.bat 运行用机器人qq扫码登录。

然后到项目根目录打开cmd 输入

~~~cmd
python main.py
~~~

### 安装ffmpeg

可以去[ffmpeg](https://ffmpeg.org/download.html)下载最新版安装

#### 安装方法

把压缩包减压放到C:\Program Files下，然后推荐加环境变量

点开属性

<img src="https://github.com/luoguixin/qqrobot/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_20230206_215454.png" alt="屏幕截图_20230206_215454" style="zoom:50%;" />

找到高级系统设置

![image-20230206215801582](https://github.com/luoguixin/qqrobot/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_20230206_215744.png)

点开环境变量

![image-20230206215857225](https://github.com/luoguixin/qqrobot/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_20230206_215842.png)



点开path

![image-20230206215937178](https://github.com/luoguixin/qqrobot/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_20230206_220301.png)

新建添加刚刚ffmpeg的存放地址C:\Program Files\ffmpeg\bin

复制粘贴进去

然后全部确定

最后win + R 输入cmd  在终端里面输入ffmpeg -version

出现

![image-20230206220306780](https://github.com/luoguixin/qqrobot/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE_20230206_220301.png)

就算安装完成了

接下来用管理员身份打开cmd

输入setx /M PATH "C:\Program Files\ffmpeg\bin;%PATH%"

回车出现成功就行

至此安装完成

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
10.域名状态查询（查询域名状态![img](file:///C:\Users\30524\AppData\Roaming\Tencent\QQ\Temp\`7_{~]GF$3{MOQ4V_}PH]YC.png)xxx.com）
11.ping（触发词pingxxx.xxx.xxx）
12.度娘（度娘什么是xxx）
13.翻译（翻译一下）
14.b站热门视频（触发词b站热门视频)
15.摸鱼日历
16.网易云热评

### 联系方式

可以加qq群784469488

