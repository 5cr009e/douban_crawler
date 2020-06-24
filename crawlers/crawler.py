from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import sqlite3

class Crawler:
    def __init__(self, baseurl, patterns,
                 headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"},
                 max_per_page=1, max_page=1, save_path="./data.xls"):
        self.data_dict= {}
        self.baseurl = baseurl
        self.headers = headers
        self.max_per_page = max_per_page
        self.save_path = save_path
        self.patterns = patterns
        self.max_page = max_page
        self.init_db()

    def get_data(self):
        for page_id in range(0, self.max_page):
            url = self.baseurl + str(page_id * self.max_per_page)
            html = self.ask_url(url)
            # print(html)
            soup = BeautifulSoup(html, "html.parser")
            id_in_page = 0
            for item in soup.find_all('div', class_="item"):
                # print(item)
                item = str(item)
                contens = {
                    key: 
                        self.patterns.post_process(key, 
                                                re.findall(self.patterns.get_pattern(key), item)
                    ) for key in self.patterns.patterns.keys()
                }
                self.data_dict[id_in_page + page_id * self.max_per_page] = contens
                print("id={}:\t{}".format(id_in_page + page_id * self.max_per_page, contens))
                id_in_page += 1
        return self

    def ask_url(self, url):
        request = urllib.request.Request(url, headers=self.headers)
        html = ""
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
            # print(html)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        return html

    def savedata(self):
        conn = sqlite3.connect(self.save_path)
        c = conn.cursor()
        for key in self.data_dict.keys():
            sql = self.patterns.data_to_sql(self.data_dict[key])
            print(sql)
            c.execute(sql)
            conn.commit()
        c.close()
        conn.close()

    def init_db(self):
        conn = sqlite3.connect(self.save_path)
        c = conn.cursor()
        try:
            c.execute(self.patterns.init_db())
        except sqlite3.OperationalError:
            print('DB already exists, skip.')
        conn.commit()
        conn.close()