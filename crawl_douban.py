# coding = utf-8
from crawlers.douban_patterns import DoubanPatterns
from crawlers.crawler import Crawler

def main():
    Crawler(baseurl="https://movie.douban.com/top250?start=",
            save_path="database/douban_top250.db",
            max_page=10,
            max_per_page=25,
            patterns=DoubanPatterns).get_data().savedata()

if __name__ == '__main__':
    main()    
