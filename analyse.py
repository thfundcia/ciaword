import jieba
import json
import pandas as pd
import jieba.analyse
from sqlalchemy import create_engine

# 配置jieba
jieba.load_userdict('txt/new_words.txt')
jieba.enable_parallel(4)

# 连接数据库
config = json.loads(open('config.json').read())


# 连接mysql获取当天的新闻
class Connect(object):
    """数据库连接的接口
    """
    def __init__(self, host, user, password, database):
        self.engine = create_engine('mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8'
                                    % (user, password, host, database), encoding='utf-8')

    def read_sql(self, sql_str):
        """读取sql信息
        """
        return pd.read_sql(sql_str, con=self.engine)

    def get_field(self, table):
        pf = self.read_sql('describe {}'.format(table))
        return pf[['Field']]


def hotWords(start, end, topk=10):
    """提取关键字
    """
    c = Connect(config['hostname'], config['user'], config['password'], config['database'])
    pf = c.read_sql('select title from t_news_zw where publishtime >= "{}" and publishtime <= "{}"'.format(start, end))
    txt = ','.join(pf['title'].values.tolist()).replace('.', '')
    # 获取不要的词汇
    bad_words = open('txt/bad_words.txt').read().split('\n')
    # 分析关键字
    tags = pd.DataFrame(jieba.analyse.textrank(txt, topK=topk), columns=['word'])
    # 打印最高频的词语
    return tags[~tags['word'].isin(bad_words)]


if __name__ == '__main__':
    print(hotWords('20170620', '20170621', 10))