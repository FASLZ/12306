# 12306Tickets
[![](https://img.shields.io/github/license/faslz/12306?color=green&style=flat-square)](https://github.com/faslz/12306/blob/master/LICENSE)

get Trains information inquiry from 12306.cn

余票查询
### 版本说明
- [ ] Python2.x
- [x] Python3.x

### 安装依赖包
```bash
pip3 install -r install.txt
```
* requests    获取网页数据 
* docopt      解析命令行参数 
* prettytable 使用表格形式打印数据
* colorama    数据着色

### 参数
<pre>
tickets [-gdtkz] [(from)] [(to)] [(date)]

Options:
    -g     高铁
    -d     动车
    -t     特快
    -k     快速
    -z     直达
    -h   --help     display this help
    -v   --version  show version 

Example:
    tickets 上海 北京 0501
    tickets -gdt beijing shanghai 2018-08-25
</pre>

### run
``` bash
python3 tickets.py [TrainType][FromStation][ToStation][Date]
```

![pic1](./image/2021021701.png)
![pic2](./image/2021021702.png)
