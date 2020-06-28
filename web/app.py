from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return index()

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/movie')
def movie():
    datalist = []
    con = sqlite3.connect("../database/douban_top250.db")
    cur = con.cursor()
    sql = "select * from douban250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("movie.html", movies=datalist)

@app.route('/score')
def score():
    score = []
    num = []
    con = sqlite3.connect("../database/douban_top250.db")
    cur = con.cursor()
    sql = "select score,count(score) from douban250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    con.close()
    return render_template("score.html", score=score, num=num)

@app.route('/word')
def word():
    return render_template("word.html")

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run()