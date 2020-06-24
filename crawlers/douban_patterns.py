import re
from dataclasses import dataclass
import sqlite3

@dataclass
class DoubanPatterns:
    matches_all_list = ['ImgSrc', 'Bd']
    patterns = {
        'Link': r'<a href="(.*?)">',
        'ImgSrc': r'<img.*src="(.*?)"',
        'Title': r'<span class="title">(.*?)</span>',
        'Rating': r'<span class="rating_num" property="v:average">(.*?)</span>',
        'NumVoters': r'<span>(\d*)人评价</span>',
        'Inq': r'<span class="inq">(.*)</span>',
        'Bd': r'<p class="">(.*?)</p>',
    }

    post_process_methods ={
        'Title': lambda titles: list(map(lambda t: t.replace("\\xa0",""), titles)) if len(titles) == 2 else [titles[0], " "],
        'Inq': lambda inq: inq[0].replace(".", "").replace("\\xa0", "") if len(inq) != 0 else ' ',
        'Bd': lambda bd: re.sub('<br(\s+)?/>(\s+)?', " ", bd[0]).strip().replace("\\xa0","") if len(bd) >= 1 else ' '
    }

    entry_to_sql = {
        'Title': lambda titles: "\"{}\",\"{}\"".format(titles[0], titles[1].replace(" / ", "")),
        'Rating': lambda num: num,
        'NumVoters': lambda num: num,
    }

    @staticmethod
    def get_pattern(key):
        return re.compile(DoubanPatterns.patterns[key], re.S) if key in DoubanPatterns.matches_all_list else re.compile(DoubanPatterns.patterns[key])

    @staticmethod
    def post_process(key, contents):
        return DoubanPatterns.post_process_methods[key](contents) if key in DoubanPatterns.post_process_methods.keys() else contents[0].replace("\\xa", "")

    @staticmethod
    def init_db():
        return '''
                create table douban250
                (
                id integer primary key autoincrement,
                info_link text,
                pic_link text,
                cname varchar,
                ename varchar,
                score numeric,
                rated numeric,
                introduction text,
                info text
                )'''
    @staticmethod
    def data_to_sql(data_entry):
        return  '''
                insert into douban250 (
                info_link,pic_link,cname,ename,score,rated,introduction,info)
                values(%s)
                ''' % ",".join(
                        [DoubanPatterns.entry_to_sql[key](data_entry[key]) # call to_sql function
                        if key in DoubanPatterns.entry_to_sql else "\"{}\"".format(data_entry[key]) # expand key, value 
                        for key in data_entry.keys()])
