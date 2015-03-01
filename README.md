# MyDict
>Linux 控制台交互式英语词典，支持Tab键补全

## 词典数据库
[下载地址](http://pan.baidu.com/s/1o6ojxpC)
> 数据库超过百兆所以放在别处下载，下载后放在程序根目录下即可

## 运行环境
- Linux + Python3即可
- DBgenerate文件夹内的不是运行的必要组件，那是我爬单词解释和例句用的，运行需要额外的requests和BeautifulSoup库

## (几乎零)配置
> 最终目标是在shell输入**mydict**命令即可打开字典

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
> 输入单词会自动显示相似的单词，可以上下移动选择

![cn_cp](https://github.com/zhuzhenpeng/MyDict/blob/master/images/cn_cp.png?raw=true)
> Tab键把单词补全成金黄色高亮的备选词

![tab_complete](https://github.com/zhuzhenpeng/MyDict/blob/master/images/tab_complete.png?raw=true)
>显示查询结果


![display](https://github.com/zhuzhenpeng/MyDict/blob/master/images/display.png?raw=true)
