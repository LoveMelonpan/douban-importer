# Douban-Importer

## introduce
将[豆伴](https://chrome.google.com/webstore/detail/%E8%B1%86%E4%BC%B4%EF%BC%9A%E8%B1%86%E7%93%A3%E8%B4%A6%E5%8F%B7%E5%A4%87%E4%BB%BD%E5%B7%A5%E5%85%B7ghppfgfeoafdcaebjoglabppkfmbcjdd)导出工具导出的书影音记录导入新账号.支持图书,电影和音乐的导入。

## run
```
python3 douban_importer.py 
```
## cookie
cookie以json数组形式存储
```
for example
{
    "domain": "book.douban.com",
    "name": "_pk_ses.100001.3ac3",
    "path": "/",
    "value": "*"
}
```

## others
懒得写了，无聊的时候再写