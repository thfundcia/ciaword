# 用于分析热词
# 使用方法
输入参数包括三个
- start: 起始日期
- end: 终止日期
- topk: 排行靠前的几个词汇
```python
>>> from analyse import hotWord
>>> hotWord('20170620', '20170621', 10))
```
# 词库维护
## bad_words.txt
用于记录过滤词，样例如下，每行一个词汇
```
美国
我们
中国
```
## new_words.txt
用于记录新词，样例如下，每行一个词汇
```
美国
我们
中国
```