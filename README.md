# MyDict
> Linux 控制台交互式英语词典，支持Tab键补全

## 词典数据库
[下载地址](http://pan.baidu.com/s/1o6ojxpC)
> 数据库超过百兆所以放在别处下载，下载后放在程序根目录下即可

## 运行环境
- Linux + Python3
- DBGenerate文件夹内的不是运行的必要组件，那是我爬单词解释和例句用的，运行需要额外的requests和BeautifulSoup库

## 配置
> 最终目标是在shell输入**mydict**即可打开字典

1. 修改mydict脚本中的内容(/your/path/to/MyDict/main.py), 添加mydict执行权限(chmod u+x mydict)，此时可以执行 **./mydict** 试运行
2. 在 ~/bin 目录中建立相应的软链接到mydict，并把 ~/bin目录放在shell的搜索路径中
3. 根目录下有CONFIG配置文件，主要为了人工控制兼容各种控制台大小，正常情况下不需要配置

## 快捷键
-  ctrl-n 向下选择候选词
-  ctrl-p 向上选择候选词
-  Tab 根据当前选择补全输入单词
-  Enter 确认
-  ctrl-g 后退（可用于取消输入、退出程序）
-  BackSpace 删除一个字母
-  任何时候输入字母打开左侧的输入框

## 截图
> 启动页面

![start](https://raw.githubusercontent.com/zhuzhenpeng/MyDict/master/images/start.png)

> 输入任意字母左侧显示输入栏

![press any key](https://raw.githubusercontent.com/zhuzhenpeng/MyDict/master/images/press%20any%20key.png)

> 随着输入候选词会变化，通过c-n/p上下移动选中想要的单词

![c-n and c-p](https://raw.githubusercontent.com/zhuzhenpeng/MyDict/master/images/c-n%20and%20c-p.png)

> 按Tab补全

![Tab](https://raw.githubusercontent.com/zhuzhenpeng/MyDict/master/images/tab.png)

> 按Enter键查询该词，查看释义

![show explanation](https://raw.githubusercontent.com/zhuzhenpeng/MyDict/master/images/show%20explanation.png)
